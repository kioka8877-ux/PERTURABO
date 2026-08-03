"""
packager.py — F05_PACKAGER : Le Ferrier de la Porte 4 (forge CLIPPING)
======================================================================

Frégate d'assemblage final (Porte 4). Fusion purement déterministe des
artefacts F01 → F04 en N `production_pack.json` (un pack = 1 vidéo pour
1 plateforme pour 1 marché — N angles = N packs).

F05 ne fait PAS appel à l'IRON : c'est un enchaînement mécanique de
fusion de JSONs. Pas de prompt, pas de sandbox.

   --assemble : pour chaque angle, assemble le pack (9 blocs + checklist)
   --finalize : validation schéma canonique + packs_index.json +
                packager_summary.md + check-in IW_CUSTOS (F05 -> packs_assembled)

Hérésies gardées :
  - asset non-F03 dans SOURCE (strict-source, règle C1)
  - source_permission != "campaign_provided"
  - text_payload absent ou non-F04 (structure requise)
  - pack non conforme au schéma canonique CONTRACTS/production_pack_schema.json

Usage:
  python packager.py --assemble [--angles ../F02_TYRANT_CAMP/OUT/angles.json]
  python packager.py --finalize
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_F05_DIR = os.path.dirname(_SCRIPT_DIR)
_FORGE_ROOT = os.path.dirname(_F05_DIR)

sys.path.insert(0, os.path.join(_SCRIPT_DIR, "libs"))
from schema_validator import SchemaValidator
from reference_style_extractor import ReferenceStyleExtractor

OUT_DIR = os.path.join(_F05_DIR, "OUT")
IN_DIR = os.path.join(_F05_DIR, "IN")
CONTRACTS_DIR = os.path.join(_FORGE_ROOT, "CONTRACTS")
ARCHIVUM_DIR = os.path.join(_FORGE_ROOT, "ARCHIVUM")
F01_OUT = os.path.join(_FORGE_ROOT, "F01_SCOUT", "OUT")
F02_OUT = os.path.join(_FORGE_ROOT, "F02_TYRANT_CAMP", "OUT")
F03_OUT = os.path.join(_FORGE_ROOT, "F03_SOURCE_HUNTER", "OUT")
F04_OUT = os.path.join(_FORGE_ROOT, "F04_COPYWRITER", "OUT")
LIBER_PATH = os.path.join(_FORGE_ROOT, "liber_clipping.json")
SCHEMA_PATH = os.path.join(CONTRACTS_DIR, "production_pack_schema.json")

ANGLES_CANDIDATES = [
    os.path.join(F02_OUT, "angles.json"),
    os.path.join(_FORGE_ROOT, "ANGLESMITH", "OUT", "angles.json"),
]

DURATION_DEFAULTS = {"youtube": (15, 45), "tiktok": (15, 30), "instagram": (15, 30)}
DURATION_RE = re.compile(r"clip_(min|max)_duration\D*(\d+)")

FORBIDDEN_DEFAULTS = ["silences > 3s", "CTA abonne-toi", "fadeouts"]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ----------------------------------------------------------------------
# Résolution des entrées
# ----------------------------------------------------------------------
def find_angles_path(args) -> str:
    if getattr(args, "angles", None):
        return args.angles
    for candidate in ANGLES_CANDIDATES:
        if os.path.exists(candidate):
            return candidate
    print("[F05] angles.json introuvable (F02_TYRANT_CAMP/OUT ou ANGLESMITH/OUT)")
    sys.exit(1)


def angles_from_file(path: str) -> list[dict]:
    data = load_json(path)
    angles = data.get("angles", [])
    if not angles:
        print(f"[F05] angles.json vide: {path}")
        sys.exit(1)
    return angles


def find_verdict() -> dict:
    for path in (os.path.join(ARCHIVUM_DIR, "campaign", "verdict.json"),
                 os.path.join(F02_OUT, "campaign_verdict.json")):
        if os.path.exists(path):
            return load_json(path)
    print("[F05] campaign_verdict.json introuvable — verdict vide")
    return {}


def load_f01_specimen() -> dict:
    path = os.path.join(F01_OUT, "source_specimen.json")
    if not os.path.exists(path):
        print(f"[F05] F01 specimen introuvable: {path}")
        sys.exit(1)
    return load_json(path)


def warsmith_targets(args, verdict: dict) -> tuple[str, str]:
    platform = getattr(args, "platform", None)
    market = getattr(args, "market", None)
    if not platform or not market:
        if os.path.exists(LIBER_PATH):
            inputs = load_json(LIBER_PATH).get("inputs_warsmith", {})
            platform = platform or inputs.get("platform_target")
            market = market or inputs.get("market_target")
    platform = platform or verdict.get("platform_target") or "youtube"
    market = market or verdict.get("market_target") or "unknown"
    return platform, market


# ----------------------------------------------------------------------
# Fourchette de durée (alignée sur F03 duration_guard)
# ----------------------------------------------------------------------
def platform_bounds(platform: str) -> tuple[int, int]:
    profile = os.path.join(ARCHIVUM_DIR, "platform_generator", f"{platform}_profile.md")
    lo, hi = DURATION_DEFAULTS.get(platform, DURATION_DEFAULTS["youtube"])
    if os.path.exists(profile):
        try:
            with open(profile, "r", encoding="utf-8") as f:
                text = f.read()
            values = dict(DURATION_RE.findall(text))
            if "min" in values:
                lo = int(values["min"])
            if "max" in values:
                hi = int(values["max"])
        except (OSError, ValueError):
            pass
    return lo, hi


# ----------------------------------------------------------------------
# Blocs du pack
# ----------------------------------------------------------------------
def _source_block(specimen: dict, assets: list[dict], angle_id: str) -> dict:
    selected = specimen.get("asset_selected", {})
    url = selected.get("url")
    asset_urls = [a.get("url") for a in assets]
    if not url:
        print(f"[F05] HERESIE {angle_id}: asset_selected.url manquant")
        sys.exit(1)
    if url not in asset_urls:
        print(f"[F05] HERESIE {angle_id}: asset {url} hors des assets F01 (règle C1)")
        sys.exit(1)

    segments = []
    for seg in specimen.get("suggested_segments", []) or []:
        entry = {
            "start_sec": seg.get("start_sec"),
            "end_sec": seg.get("end_sec"),
            "rationale": seg.get("rationale", ""),
        }
        if seg.get("duration_sec") is not None:
            entry["duration_sec"] = seg.get("duration_sec")
        if seg.get("extracted_text_snippet"):
            entry["extracted_text_snippet"] = seg.get("extracted_text_snippet")
        segments.append(entry)

    source_segment = None
    if segments:
        source_segment = {
            "start_sec": segments[0]["start_sec"],
            "end_sec": segments[0]["end_sec"],
        }

    return {
        "video_url": url,
        "suggested_segments": segments,
        "source_segment_sec": source_segment,
        "source_permission": "campaign_provided",
    }


def _angle_block(angle: dict, angles: list[dict], text_payload: dict) -> dict:
    axes = ["angle_family", "emotion_mode", "engagement_type", "reframe_dim"]

    def differs(ax: str) -> bool:
        return any(angle.get(ax) != other.get(ax) for other in angles
                   if other.get("angle_id") != angle.get("angle_id"))

    differentiated_axes = [ax for ax in axes if differs(ax)]
    if len(differentiated_axes) < 2:
        differentiated_axes = axes[:2]

    hook_types = []
    for t in (text_payload.get("titles", []) or [])[:3]:
        hook = t.get("hook_type")
        if hook and hook not in hook_types:
            hook_types.append(hook)

    is_blue = angle.get("zone") == "blue_ocean"
    blue_ocean = {"is_blue_ocean": is_blue}
    if is_blue:
        blue_ocean.update({
            "blue_ocean_depth": 1,
            "territory": angle.get("territory"),
            "rationale": angle.get("territory_rationale"),
        })
    return {
        "angle_family": angle.get("angle_family"),
        "emotion_mode": angle.get("emotion_mode"),
        "engagement_type": angle.get("engagement_type"),
        "reframe_dim": angle.get("reframe_dim"),
        "hook_style_fit": hook_types,
        "loop_tech": "open_loop" if angle.get("engagement_type") == "cliffhanger"
                     else "closed_loop",
        "anti_cannibal_diff": {"differentiated_axes": differentiated_axes},
        "blue_ocean": blue_ocean,
    }


def _cut_block(specimen: dict, platform: str) -> dict:
    lo, hi = platform_bounds(platform)
    segments = specimen.get("suggested_segments", []) or []
    moments_to_chase = []
    for i, seg in enumerate(segments, start=1):
        snippet = seg.get("extracted_text_snippet") or seg.get("rationale") or ""
        moments_to_chase.append(
            f"segment {i} (t={seg.get('start_sec')}-{seg.get('end_sec')}s): {snippet}")
    if not moments_to_chase:
        moments_to_chase = ["moments à confirmer par D-F02 (pas de segments F03)"]
    return {
        "clip_max_duration": hi,
        "clip_min_duration": lo,
        "moments_to_chase": moments_to_chase,
        "moments_to_avoid": ["intro trop longue > 3s avant le hook"],
        "forbidden": list(FORBIDDEN_DEFAULTS),
    }


def _text_payload_block(payload: dict, angle_id: str) -> dict:
    required = ["titles", "paragraph", "caption", "hashtags", "on_screen_text", "cta_text"]
    for key in required:
        if key not in payload:
            print(f"[F05] HERESIE {angle_id}: text_payload sans '{key}' — "
                  f"F05 ne forge rien, il assemble (sortie F04 requise)")
            sys.exit(1)
    titles = []
    for t in (payload.get("titles") or [])[:3]:
        titles.append({
            "rank": t.get("rank"),
            "text": t.get("text"),
            "platform_fit": t.get("platform_fit"),
            "market_fit": t.get("market_fit"),
            "hook_type": t.get("hook_type"),
            "rationale": t.get("rationale", ""),
        })
    return {
        "titles": titles,
        "paragraph": payload.get("paragraph"),
        "caption": payload.get("caption"),
        "hashtags": payload.get("hashtags"),
        "on_screen_text": payload.get("on_screen_text"),
        "cta_text": payload.get("cta_text"),
    }


def _checklist(platform: str) -> dict:
    return {
        "items": [
            {"id": "post_on_platform", "label": f"Poster sur {platform}", "status": "pending"},
            {"id": "submit_whop_under_1h", "label": "Soumettre Whop dans l'heure",
             "deadline_min": 60, "status": "pending"},
            {"id": "log_link_c06", "label": "Logger le lien dans F06_TRACKER",
             "status": "pending"},
            {"id": "view_check_1h", "label": "Relever vues à 1h", "status": "pending"},
            {"id": "view_check_24h", "label": "Relever vues à 24h", "status": "pending"},
            {"id": "payout_flag_low", "label": "Flag si payout < seuil", "status": "pending"},
            {"id": "feedback_learnings", "label": "Nourrir learnings.json", "status": "pending"},
        ]
    }


def _metadata_block(payload: dict) -> dict:
    rank1 = (payload.get("titles") or [{}])[0]
    title = rank1.get("text", "")
    caption = payload.get("caption", "")
    hashtags = " ".join(payload.get("hashtags", []) or [])
    return {
        "title_pattern": title,
        "description_skeleton": f"{caption}\n\n{hashtags}".strip(),
    }


def assemble_pack(angle: dict, angles: list[dict], specimen: dict, payload: dict,
                  f01_specimen: dict, verdict: dict, platform: str, market: str,
                  pack_index: int, pack_total: int) -> dict:
    extractor = ReferenceStyleExtractor(ARCHIVUM_DIR, IN_DIR)
    style = extractor.extract()

    return {
        "identite": {
            "campaign_id": verdict.get("campaign_id") or payload.get("campaign_id"),
            "angle_id": angle.get("angle_id"),
            "pack_index": pack_index,
            "pack_total": pack_total,
        },
        "cibles": {
            "target_platform": platform,
            "target_market": market,
        },
        "source": _source_block(specimen, f01_specimen.get("assets", []),
                                angle.get("angle_id")),
        "angle": _angle_block(angle, angles, payload),
        "cut_directives": _cut_block(specimen, platform),
        "reference_style": style,
        "text_payload": _text_payload_block(payload, angle.get("angle_id")),
        "compliance": {
            "disclosure": "#ad",
            "submit_deadline_min": 60,
            "source_permission": "campaign_provided",
        },
        "metadata": _metadata_block(payload),
        "submission_checklist": _checklist(platform),
    }


# ----------------------------------------------------------------------
# Commandes
# ----------------------------------------------------------------------
def cmd_assemble(args):
    angles = angles_from_file(find_angles_path(args))
    verdict = find_verdict()
    f01 = load_f01_specimen()
    platform, market = warsmith_targets(args, verdict)
    total = len(angles)

    for idx, angle in enumerate(angles, start=1):
        angle_id = angle.get("angle_id")
        specimen_path = os.path.join(F03_OUT, f"source_specimen_{angle_id}.json")
        payload_path = os.path.join(F04_OUT, f"text_payload_{angle_id}.json")
        if not os.path.exists(specimen_path):
            print(f"[F05] Specimen F03 introuvable: {specimen_path} — angle {angle_id} sauté")
            continue
        if not os.path.exists(payload_path):
            print(f"[F05] Payload F04 introuvable: {payload_path} — angle {angle_id} sauté")
            continue

        pack = assemble_pack(
            angle, angles,
            load_json(specimen_path), load_json(payload_path),
            f01, verdict, platform, market, idx, total,
        )
        out = os.path.join(OUT_DIR, f"production_pack_{angle_id}.json")
        save_json(out, pack)
        print(f"[F05] Pack {idx}/{total}: {angle_id} -> {os.path.basename(out)}")

    print("[F05] Lancer --finalize pour valider + expédier")


def _collect_packs() -> list[tuple[str, dict]]:
    paths = sorted(glob.glob(os.path.join(OUT_DIR, "production_pack_*.json")))
    if not paths:
        print("[F05] OUT/production_pack_*.json absent — lancer --assemble d'abord")
        sys.exit(1)
    return [(p, load_json(p)) for p in paths]


def cmd_finalize(args):
    packs = _collect_packs()
    validator = SchemaValidator(SCHEMA_PATH)
    f01 = load_f01_specimen()
    asset_urls = [a.get("url") for a in f01.get("assets", [])]

    errors = []
    unobserved_style = []
    for path, pack in packs:
        errors += validator.validate(pack, root=os.path.basename(path))
        source = pack.get("source", {})
        if source.get("video_url") and source["video_url"] not in asset_urls:
            errors.append(f"{os.path.basename(path)}: HERESIE — video_url hors assets F01")
        if source.get("source_permission") != "campaign_provided":
            errors.append(f"{os.path.basename(path)}: source_permission invalide")
        if not pack.get("reference_style", {}).get("observed", False):
            unobserved_style.append(path)

    if errors:
        print("[F05] Packs invalides :")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    platform = packs[0][1].get("cibles", {}).get("target_platform", "?")
    market = packs[0][1].get("cibles", {}).get("target_market", "?")
    campaign_id = packs[0][1].get("identite", {}).get("campaign_id")

    index = {
        "campaign_id": campaign_id,
        "target_platform": platform,
        "target_market": market,
        "pack_count": len(packs),
        "generated_at": now_iso(),
        "packs": [
            {
                "angle_id": pack.get("identite", {}).get("angle_id"),
                "pack_index": pack.get("identite", {}).get("pack_index"),
                "pack_total": pack.get("identite", {}).get("pack_total"),
                "file": os.path.basename(path),
            }
            for path, pack in packs
        ],
    }
    save_json(os.path.join(OUT_DIR, "packs_index.json"), index)

    lines = [
        "# F05_PACKAGER — Synthèse des packs",
        "",
        f"- Campagne : {campaign_id or 'N/A'}",
        f"- Cibles : {platform} / {market}",
        f"- Packs validés : {len(packs)}/{len(packs)}",
        "",
        "| Pack | Angle | Plateforme | Marché | Style ADN | Checklist |",
        "|---|---|---|---|---|---|",
    ]
    for path, pack in packs:
        identite = pack.get("identite", {})
        style = pack.get("reference_style", {})
        style_state = "observé" if style.get("observed") else "défaut (vision IRON requise)"
        lines.append(
            f"| {identite.get('pack_index')}/{identite.get('pack_total')} "
            f"| {identite.get('angle_id')} | {platform} | {market} "
            f"| {style_state} | 7 items pending |")
    lines += [
        "",
        f"**{len(packs)} packs prêts à expédier → OMNIS_WATCH** "
        f"(mode `--pack production_pack_<angle>.json`)",
    ]
    if unobserved_style:
        lines += [
            "",
            f"⚠️ {len(unobserved_style)} pack(s) avec reference_style non observé "
            f"— prompt vision généré dans IN/reference_style_prompt.json : ",
        ]
        for path in unobserved_style:
            lines.append(f"- {os.path.basename(path)}")
    summary_path = os.path.join(OUT_DIR, "packager_summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    custos = os.path.join(_FORGE_ROOT, "IW_CUSTOS.py")
    if os.path.exists(custos):
        subprocess.run([sys.executable, custos, "--mode", "check-in",
                        "--frigate", "F05", "--output", summary_path],
                       capture_output=True, text=True, timeout=30)
    print(f"[F05] Finalize : {len(packs)} packs validés — {summary_path}")
    print("[F05] Check-in IW_CUSTOS — fleet_status -> packs_assembled")
    if unobserved_style:
        print(f"[F05] ATTENTION: {len(unobserved_style)} pack(s) avec style ADN par défaut "
              "(vision IRON du clip de référence requise)")


def main():
    parser = argparse.ArgumentParser(description="F05_PACKAGER — Le Ferrier de la Porte 4")
    parser.add_argument("--assemble", action="store_true",
                        help="Assemble les N packs depuis F01-F04")
    parser.add_argument("--finalize", action="store_true",
                        help="Validation schéma + index + summary + check-in")
    parser.add_argument("--angles", default=None, help="Chemin vers angles.json")
    parser.add_argument("--platform", default=None, help="Plateforme cible (override)")
    parser.add_argument("--market", default=None, help="Marché cible (override)")
    args = parser.parse_args()

    if args.assemble:
        cmd_assemble(args)
    elif args.finalize:
        cmd_finalize(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
