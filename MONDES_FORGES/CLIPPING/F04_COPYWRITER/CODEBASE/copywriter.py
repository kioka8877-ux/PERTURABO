"""
copywriter.py — F04_COPYWRITER : La Plume de la Forteresse (forge CLIPPING)
===========================================================================

Frégate lourde de la Porte 3. Forge le text_payload complet pour chaque
angle : 3 titres calibrés + paragraphe reframing + caption + hashtags 3
strates + on-screen text + CTA.

SINGULARITÉ — rupture du pattern 3 phases. F04 parle DIRECT au modèle
premium (clé API dédiée). L'IRON (sandbox Claude) ordonnance seulement.

   Phase A : setup_context        (context_builder rassemble l'ARCHIVUM)
   Phase B : premium_generation   (premium_client — premium direct)
   Phase C : iron_ordonnancing    (iron_ordonnancer — validation + classement)
   Phase D : finalize + ledger    (md_renderer + check-in IW_CUSTOS)

Usage:
  python copywriter.py --init-systemprompt [--force]        # one-time
  python copywriter.py --setup-context --angle A01 [--platform p] [--market m]
  python copywriter.py --generate --angle A01 [--dry-run]
  python copywriter.py --ordonnance --angle A01 [--auto-ord]
  python copywriter.py --finalize --angle A01
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_F04_DIR = os.path.dirname(_SCRIPT_DIR)
_FORGE_ROOT = os.path.dirname(_F04_DIR)

sys.path.insert(0, os.path.join(_SCRIPT_DIR, "libs"))
from context_builder import ContextBuilder
from premium_client import PremiumClient, PremiumClientError
from iron_ordonnancer import IronOrdonnancer
from compliance_checker import ComplianceChecker
from md_renderer import MdRenderer

OUT_DIR = os.path.join(_F04_DIR, "OUT")
IN_DIR = os.path.join(_F04_DIR, "IN")
CONTRACTS_DIR = os.path.join(_FORGE_ROOT, "CONTRACTS")
ARCHIVUM_DIR = os.path.join(_FORGE_ROOT, "ARCHIVUM")
F02_OUT = os.path.join(_FORGE_ROOT, "F02_TYRANT_CAMP", "OUT")
F03_OUT = os.path.join(_FORGE_ROOT, "F03_SOURCE_HUNTER", "OUT")
LIBER_PATH = os.path.join(_FORGE_ROOT, "liber_clipping.json")

SYSTEM_PROMPT_PATH = os.path.join(CONTRACTS_DIR, "copywriter_systemprompt.md")
DOCTRINE_PATH = os.path.join(CONTRACTS_DIR, "copywriting_doctrine.md")
SECRETS_PATH = os.path.join(CONTRACTS_DIR, "copywriter_secrets.json")
SECRETS_EXAMPLE_PATH = os.path.join(CONTRACTS_DIR, "copywriter_secrets.example.json")

PLACEHOLDER_MARKER = "NON GÉNÉRÉ"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------------------------------------------------
# Résolution des entrées
# ----------------------------------------------------------------------
def find_angles_path() -> str:
    candidates = [
        os.path.join(F02_OUT, "angles.json"),
        os.path.join(_FORGE_ROOT, "ANGLESMITH", "OUT", "angles.json"),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    print("[F04] angles.json introuvable (F02_TYRANT_CAMP/OUT ou ANGLESMITH/OUT)")
    print("[F04] Lancer ANGLESMITH --finalize d'abord (Porte 2)")
    sys.exit(1)


def load_angles() -> list[dict]:
    data = load_json(find_angles_path())
    angles = data.get("angles", [])
    if not angles:
        print("[F04] angles.json vide")
        sys.exit(1)
    return angles


def find_angle(angle_id: str) -> dict:
    for angle in load_angles():
        if angle.get("angle_id") == angle_id:
            return angle
    print(f"[F04] Angle inconnu: {angle_id} — angles.json ne contient pas cet id")
    sys.exit(1)


def find_verdict() -> dict:
    for path in (os.path.join(ARCHIVUM_DIR, "campaign", "verdict.json"),
                 os.path.join(F02_OUT, "campaign_verdict.json")):
        if os.path.exists(path):
            return load_json(path)
    print("[F04] campaign_verdict.json introuvable — verdict vide")
    return {}


def find_specimen(angle_id: str) -> dict:
    path = os.path.join(F03_OUT, f"source_specimen_{angle_id}.json")
    if not os.path.exists(path):
        print(f"[F04] Specimen F03 introuvable: {path}")
        print("[F04] Lancer F03_SOURCE_HUNTER d'abord (Porte 3)")
        sys.exit(1)
    return load_json(path)


def warsmith_targets(args) -> tuple[str, str]:
    platform = getattr(args, "platform", None)
    market = getattr(args, "market", None)
    if not platform or not market:
        if os.path.exists(LIBER_PATH):
            inputs = load_json(LIBER_PATH).get("inputs_warsmith", {})
            platform = platform or inputs.get("platform_target")
            market = market or inputs.get("market_target")
    return platform or "youtube", market or "unknown"


# ----------------------------------------------------------------------
# INIT — système prompt (one-time, à ne pas refaire)
# ----------------------------------------------------------------------
def cmd_init_systemprompt(args):
    if not os.path.exists(DOCTRINE_PATH):
        print(f"[F04] Doctrine introuvable: {DOCTRINE_PATH}")
        sys.exit(1)
    if os.path.exists(SYSTEM_PROMPT_PATH) and not getattr(args, "force", False):
        content = read_text(SYSTEM_PROMPT_PATH)
        if PLACEHOLDER_MARKER not in content:
            print("[F04] copywriter_systemprompt.md déjà généré — figé. "
                  "Refaire l'init uniquement avec --force (mise à jour majeure doctrine).")
            sys.exit(1)

    doctrine = read_text(DOCTRINE_PATH)
    builder = ContextBuilder(_FORGE_ROOT)
    archivum = builder.collect_archivum("youtube", "unknown")
    copywriting_dir = os.path.join(ARCHIVUM_DIR, "copywriting")
    sub_dirs = sorted(
        name for name in os.listdir(copywriting_dir)
        if os.path.isdir(os.path.join(copywriting_dir, name))
    )

    meta_prompt = (
        "Tu es le modèle premium de F04_COPYWRITER. Tu dois générer le SYSTEM PROMPT "
        "final de la frégate copywriting, figé ensuite pour toutes les exécutions.\n\n"
        "MATIÈRE SOURCE (ne pas régurgiter, synthétiser) :\n\n"
        "1) DOCTRINE COMPLÈTE :\n"
        + doctrine
        + "\n\n2) SOUS-DOSSIERS ARCHIVUM/copywriting/ (8) :\n- "
        + "\n- ".join(sub_dirs)
        + "\n\n3) CONTEXTE ARCHIVUM (règles, angles, learnings, demons) :\n"
        + json.dumps(archivum, indent=2, ensure_ascii=False)[:60000]
        + "\n\nLe system prompt final DOIT contenir :\n"
        "- Contexte : rôle de la frégate, singularité 4 phases, premium direct\n"
        "- Doctrine : résumé des 10 sections (I-X)\n"
        "- Capacités : 3 titres + paragraphe + caption + hashtags + on-screen + CTA\n"
        "- Contraintes : format JSON strict (schéma text_payload_*.json)\n"
        "- Garde-fous : anti-bullshit, FTC, hérésies (section X)\n"
        "Réponds avec UNIQUEMENT le system prompt final en markdown, "
        "sans en-tête ni explication."
    )

    client = PremiumClient(_FORGE_ROOT)
    client.require_config()
    result = client.chat(
        system_prompt="Tu es l'architecte du system prompt de la frégate copywriting.",
        user_prompt=meta_prompt,
    )
    if not result:
        sys.exit(1)

    header = (
        "# COPYWRITER SYSTEMPROMPT — GÉNÉRÉ PAR LE MODÈLE PREMIUM (init one-time)\n"
        f"\n> * Généré le : {now_iso()} — FIGÉ. Ne pas réécrire sans --force. *\n\n---\n\n"
    )
    with open(SYSTEM_PROMPT_PATH, "w", encoding="utf-8") as f:
        f.write(header + result.strip() + "\n")
    print(f"[F04] System prompt figé : {SYSTEM_PROMPT_PATH}")


# ----------------------------------------------------------------------
# Phase A — setup_context
# ----------------------------------------------------------------------
def cmd_setup_context(args):
    angle = find_angle(args.angle)
    specimen = find_specimen(args.angle)
    verdict = find_verdict()
    platform, market = warsmith_targets(args)

    builder = ContextBuilder(_FORGE_ROOT)
    context = builder.build(angle, specimen, verdict, platform, market)

    out = os.path.join(IN_DIR, f"copywriter_context_{args.angle}.json")
    save_json(out, context)
    size_kb = os.path.getsize(out) // 1024
    print(f"[F04] Phase A : {out} ({size_kb} KB)")
    print(f"[F04] Angle {args.angle} — {angle.get('angle_family')}/{angle.get('emotion_mode')} "
          f"— {platform} / {market}")
    print("[F04] Lancer --generate pour la Phase B (premium direct)")


# ----------------------------------------------------------------------
# Phase B — premium_generation
# ----------------------------------------------------------------------
def _load_context(angle_id: str) -> dict:
    path = os.path.join(IN_DIR, f"copywriter_context_{angle_id}.json")
    if not os.path.exists(path):
        print(f"[F04] Contexte introuvable: {path}")
        print("[F04] Lancer --setup-context d'abord (Phase A)")
        sys.exit(1)
    return load_json(path)


def cmd_generate(args):
    angle = find_angle(args.angle)
    context = _load_context(args.angle)
    platform = context.get("platform_target", "youtube")
    market = context.get("market_target", "unknown")

    system_prompt = ""
    if os.path.exists(SYSTEM_PROMPT_PATH):
        system_prompt = read_text(SYSTEM_PROMPT_PATH)
    if not system_prompt or PLACEHOLDER_MARKER in system_prompt:
        if not getattr(args, "force", False):
            print("[F04] copywriter_systemprompt.md non généré (placeholder).")
            print("[F04] Lancer --init-systemprompt (one-time) ou --generate --force.")
            sys.exit(1)
        system_prompt = (
            "Tu es F04_COPYWRITER, frégate copywriting du forge CLIPPING. "
            "Tu forges des text_payloads gagnants (3 titres + paragraphe + caption "
            "+ hashtags + on-screen + CTA). Réponds en JSON strict conforme au schéma "
            "text_payload_*.json. Interdits : 'abonne-toi', clickbait sans payoff, "
            "paragraphe > 2 lignes, reframing qui ment sur la source."
        )

    user_prompt = {
        "mission": (
            "Forge le text_payload complet pour CET angle : 3 titres calibrés "
            "(scorés platform_fit/market_fit/hook_type), un paragraphe reframing "
            "(2 lignes max), caption, hashtags 3 strates (large + moyen + niche), "
            "on-screen text (1 keyframe max), cta_text subtil. "
            "Respecte le schéma JSON strict ci-dessous."
        ),
        "campaign_id": context.get("campaign_id"),
        "angle_id": args.angle,
        "angle": context.get("angle"),
        "specimen_source": context.get("specimen"),
        "verdict": context.get("verdict"),
        "platform_target": platform,
        "market_target": market,
        "archivum": context.get("archivum"),
        "output_schema": {
            "titles": [
                {"rank": 1, "text": "...", "platform_fit": 0, "market_fit": 0,
                 "hook_type": "stat_choc|question|declaration|mystery|contradiction|cible_naming",
                 "rationale": "..."}
            ],
            "paragraph": {"text": "...", "recommendation": "use|skip",
                          "override_omniswatch": None, "final_operator": None},
            "caption": "...",
            "hashtags": ["#...", "#...", "#..."],
            "on_screen_text": "...|null",
            "cta_text": "...",
            "compliance": {"disclosure": "#ad", "ftc_required": True},
        },
        "heresies_interdites": [
            "Abonne-toi / Like et partage / Swipe up dans CTA, caption ou on-screen",
            "Clickbait sans payoff (le titre doit livrer dans la vidéo)",
            "Reframing qui ment sur le contenu source (anti-cond)",
            "Paragraphe > 2 lignes",
            "Hashtags sans strate niche",
        ],
    }

    client = PremiumClient(_FORGE_ROOT)
    if getattr(args, "dry_run", False):
        call = {
            "mode": "dry-run — aucun appel réseau",
            "model_id": client.config.get("model_id", "<model_premium_id>"),
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }
        out = os.path.join(IN_DIR, f"premium_call_{args.angle}.json")
        save_json(out, call)
        print(f"[F04] Phase B (dry-run) : {out}")
        print("[F04] Aucun appel premium effectué — vérifier le prompt, puis --generate")
        return

    client.require_config()
    user_text = json.dumps(user_prompt, indent=2, ensure_ascii=False)
    result = client.chat(system_prompt=system_prompt, user_prompt=user_text)
    if not result:
        print("[F04] Échec de la génération premium — OUT/text_payload_raw absent")
        sys.exit(1)

    try:
        raw = json.loads(client.extract_json(result))
    except (json.JSONDecodeError, ValueError) as e:
        fallback = os.path.join(OUT_DIR, f"text_payload_raw_{args.angle}.txt")
        with open(fallback, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"[F04] Sortie premium non-JSON: {e}")
        print(f"[F04] Réponse brute conservée : {fallback}")
        print("[F04] L'IRON (Phase C) ne peut pas ordonnancer du non-JSON — relancer ou corriger")
        sys.exit(1)

    raw["campaign_id"] = context.get("campaign_id")
    raw["angle_id"] = args.angle
    out = os.path.join(OUT_DIR, f"text_payload_raw_{args.angle}.json")
    save_json(out, raw)
    print(f"[F04] Phase B : {out}")
    print("[F04] Lancer --ordonnance pour la Phase C (IRON)")


# ----------------------------------------------------------------------
# Phase C — iron_ordonnancing
# ----------------------------------------------------------------------
def _load_raw(angle_id: str) -> dict:
    path = os.path.join(OUT_DIR, f"text_payload_raw_{angle_id}.json")
    if not os.path.exists(path):
        print(f"[F04] Sortie premium introuvable: {path}")
        print("[F04] Lancer --generate d'abord (Phase B)")
        sys.exit(1)
    return load_json(path)


def cmd_ordonnance(args):
    angle = find_angle(args.angle)
    raw = _load_raw(args.angle)
    context = _load_context(args.angle)
    platform = context.get("platform_target", "youtube")
    market = context.get("market_target", "unknown")

    ordonnancer = IronOrdonnancer()
    checker = ComplianceChecker()

    if getattr(args, "auto_ord", False):
        payload, notes = ordonnancer.ordonnance_auto(
            raw, angle, platform, market,
            campaign_id=context.get("campaign_id"))
        issues = checker.check(payload)
        save_json(os.path.join(OUT_DIR, f"text_payload_{args.angle}.json"), payload)
        print(f"[F04] Phase C (auto) : OUT/text_payload_{args.angle}.json")
        for note in notes:
            print(f"  - {note}")
        for issue in issues:
            print(f"  [{issue['severity']}] {issue['code']}: {issue['message']}")
        return

    prompt = ordonnancer.build_iron_prompt(raw, angle, platform, market)
    out = os.path.join(IN_DIR, f"ordonnance_prompt_{args.angle}.json")
    save_json(out, prompt)
    print(f"[F04] Phase C : {out}")
    print("[F04] Copier le prompt dans Claude sandbox -> OUT/text_payload_<angle>.json, "
          "puis --finalize")


# ----------------------------------------------------------------------
# Phase D — finalize + ledger
# ----------------------------------------------------------------------
def cmd_finalize(args):
    angle = find_angle(args.angle)
    path = os.path.join(OUT_DIR, f"text_payload_{args.angle}.json")
    if not os.path.exists(path):
        print(f"[F04] text_payload ordonnancé introuvable: {path}")
        print("[F04] Lancer --ordonnance d'abord (Phase C)")
        sys.exit(1)

    payload = load_json(path)
    checker = ComplianceChecker()
    criticals = [i for i in checker.check(payload) if i["severity"] == "critical"]
    if criticals:
        print(f"[F04] HÉRÉSIES critiques — finalize refusé pour {args.angle} :")
        for issue in criticals:
            print(f"  - {issue['code']}: {issue['message']}")
        sys.exit(1)

    angles = load_angles()
    payload["check_in_iw_custos"] = now_iso()
    save_json(path, payload)

    index = sorted(a.get("angle_id") for a in angles).index(args.angle) + 1
    renderer = MdRenderer()
    md = renderer.render(payload, index=index, total=len(angles))
    md_path = os.path.join(OUT_DIR, f"text_payload_{args.angle}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[F04] Phase D : {md_path} (lisible opérateur)")

    all_done = all(
        os.path.exists(os.path.join(OUT_DIR, f"text_payload_{a.get('angle_id')}.json"))
        for a in angles
    )
    if all_done:
        custos = os.path.join(_FORGE_ROOT, "IW_CUSTOS.py")
        if os.path.exists(custos):
            subprocess.run(
                [sys.executable, custos, "--mode", "check-in",
                 "--frigate", "F04", "--output", md_path],
                capture_output=True, text=True, timeout=30,
            )
        print("[F04] Check-in IW_CUSTOS — fleet_status -> text_payloads_forged")
    else:
        print("[F04] Tous les angles pas encore finalisés — check-in IW_CUSTOS "
              "au finalize du dernier angle")

    print("[F04] OUT prêt pour F05_PACKAGER (production_pack) et l'Oracle OMNIS_WATCH")


def main():
    parser = argparse.ArgumentParser(description="F04_COPYWRITER — La Plume de la Forteresse")
    parser.add_argument("--init-systemprompt", action="store_true",
                        help="Init one-time : premium génère copywriter_systemprompt.md")
    parser.add_argument("--setup-context", action="store_true",
                        help="Phase A : rassemble l'ARCHIVUM dans IN/copywriter_context")
    parser.add_argument("--generate", action="store_true",
                        help="Phase B : génération premium directe")
    parser.add_argument("--ordonnance", action="store_true",
                        help="Phase C : prompt IRON (ou --auto-ord local)")
    parser.add_argument("--finalize", action="store_true",
                        help="Phase D : validation + .md + check-in IW_CUSTOS")
    parser.add_argument("--angle", default=None, help="angle_id (ex: A01)")
    parser.add_argument("--platform", default=None, help="Plateforme cible (override)")
    parser.add_argument("--market", default=None, help="Marché cible (override)")
    parser.add_argument("--auto-ord", action="store_true",
                        help="Phase C locale (sans IRON) : classement + compliance")
    parser.add_argument("--dry-run", action="store_true",
                        help="Phase B sans appel réseau (écrit IN/premium_call)")
    parser.add_argument("--force", action="store_true",
                        help="Init system prompt malgré un fichier déjà figé / placeholder")
    args = parser.parse_args()

    try:
        if args.init_systemprompt:
            cmd_init_systemprompt(args)
        elif args.setup_context:
            if not args.angle:
                print("[F04] --angle requis pour --setup-context"); sys.exit(1)
            cmd_setup_context(args)
        elif args.generate:
            if not args.angle:
                print("[F04] --angle requis pour --generate"); sys.exit(1)
            cmd_generate(args)
        elif args.ordonnance:
            if not args.angle:
                print("[F04] --angle requis pour --ordonnance"); sys.exit(1)
            cmd_ordonnance(args)
        elif args.finalize:
            if not args.angle:
                print("[F04] --angle requis pour --finalize"); sys.exit(1)
            cmd_finalize(args)
        else:
            parser.print_help()
    except PremiumClientError as e:
        print(f"[F04] ERREUR premium : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
