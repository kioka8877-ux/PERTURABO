"""
anglesmith.py — ANGLESMITH : La forge des N angles (portee par F02_TYRANT_CAMP)
==============================================================================

Porte 2. Forge N angles d'attaque repartis sur 2 zones (direct + ocean bleu,
MEME source, profondeur 1 couche max), chacun combinant 4 axes :
angle_family, emotion_mode, engagement_type, reframe_dim.

Regles verrouillees :
  - Anti-cannibale : 2 axes differenciants minimum entre chaque angle
  - Ponderation learnings : poids nul si < 50 packs executes
  - Re-ciblage ocean bleu : jamais au-dela de 1 couche (heresie)

Pattern 3 phases :
  Phase 1 (prepare) : genere IN/anglesmith_prompt.json (pour l'IRON)
  Phase 2 (IRON)    : le Warsmith copie le prompt, l'IRON forge/affine les angles
                      -> ecrit OUT/angles.json
  Phase 3 (finalize): validation anti-cannibale + check-in IW_CUSTOS ANGLESMITH

Usage:
  python anglesmith.py --prepare --n-angles 10
  python anglesmith.py --auto --n-angles 10
  python anglesmith.py --finalize
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_F02_DIR = os.path.dirname(_SCRIPT_DIR)
_FORGE_ROOT = os.path.dirname(_F02_DIR)

sys.path.insert(0, os.path.join(_SCRIPT_DIR, "libs"))
from angle_forger import AngleForger
from learnings_weight import LearningsWeight

IN_DIR = os.path.join(_F02_DIR, "IN")
OUT_DIR = os.path.join(_F02_DIR, "OUT")
CAMPAIGN_DIR = os.path.join(_FORGE_ROOT, "ARCHIVUM", "campaign")

ANGLES_PATH = os.path.join(OUT_DIR, "angles.json")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_humour_spin() -> str | None:
    """Récupère le sens humouristique proposé par le Warsmith au --deliver-subject.
    Source de vérité : liber_clipping.json -> inputs_warsmith.spin_humour.
    """
    liber_path = os.path.join(_FORGE_ROOT, "liber_clipping.json")
    if not os.path.exists(liber_path):
        return None
    try:
        liber = load_json(liber_path)
        return liber.get("inputs_warsmith", {}).get("spin_humour") or None
    except Exception:
        return None


def load_verdict() -> dict:
    path = os.path.join(CAMPAIGN_DIR, "verdict.json")
    if not os.path.exists(path):
        print(f"[ANGLESMITH] verdict introuvable: {path}")
        print("[ANGLESMITH] Lancer F02_TYRANT_CAMP --finalize d'abord (Porte 1)")
        sys.exit(1)
    return load_json(path)


def load_meme_virality() -> dict:
    """Mode MEME : charge le scan viralité F00 (OUT/meme_virality_*.json)."""
    f00_out = os.path.join(_FORGE_ROOT, "F00_CAPTEURS", "OUT")
    candidates = sorted(
        f for f in os.listdir(f00_out)
        if f.startswith("meme_virality_") and f.endswith(".json")
    ) if os.path.isdir(f00_out) else []
    if not candidates:
        print("[ANGLESMITH] Aucun scan meme F00 (F00_CAPTEURS/OUT/meme_virality_*.json)")
        print("[ANGLESMITH] Lancer F00_CAPTEURS --scan-meme --keyword <mot-clé> d'abord (Gate 1)")
        sys.exit(1)
    path = os.path.join(f00_out, candidates[-1])
    return load_json(path)


def _apply_weights(angles: list[dict], lw: LearningsWeight):
    for angle in angles:
        angle["weight"] = lw.weight_for_family(angle["angle_family"])
    return angles


def cmd_prepare(args):
    verdict = load_verdict()
    n = int(args.n_angles)
    spin = load_humour_spin()
    prompt = {
        "mission": "ANGLESMITH (Porte 2) — Forge les N angles d'attaque sur "
                   "le verdict de la Porte 1. Zones : direct (territoire du Demon) "
                   "+ ocean bleu (re-ciblage non sature, MEME source, 1 couche max). "
                   "Ecris OUT/angles.json.",
        "n_angles": n,
        "campaign_id": verdict.get("campaign_id"),
        "verdict": verdict,
        "regles": [
            "Chaque angle combine 4 axes : angle_family, emotion_mode, engagement_type, reframe_dim",
            "Anti-cannibale : 2 axes differenciants minimum entre chaque angle",
            "Ocean bleu : depth 1 seulement, jamais 2 couches",
            "Ponderation learnings si eligible (>= 50 packs executes)",
        ],
        "heresies_interdites": [
            "Re-ciblage au-dela de 1 couche",
            "2 angles trop proches (cannibalisme)",
            "Suggere des sources alternatives (assets = forteresse fermee)",
        ],
        "output_attendu": "OUT/angles.json (schema : README.md mecanisme des N angles)",
    }
    if spin:
        prompt["spin_humour_operateur"] = spin
        prompt["regles"] = prompt["regles"] + [
            "SENS HUMOURISTIQUE (Warsmith) : forger les angles AUTOUR de ce sens. "
            "Chaque angle doit decliner la direction humour dans un registre "
            "compatible (parodie, absurde, ironie, jeux de mots) sans quitter "
            "le sujet reel. emotion_mode doit rester credible (joie/tension "
            "humoristique), jamais de moquerie defamatoire."
        ]
    save_json(os.path.join(IN_DIR, "anglesmith_prompt.json"), prompt)
    print(f"[ANGLESMITH] Prompt IRON : {os.path.join(IN_DIR, 'anglesmith_prompt.json')}")
    if spin:
        print(f"[ANGLESMITH] Spin humour operateur injecte dans le prompt: {spin}")
    print("[ANGLESMITH] Copier le prompt dans Claude sandbox -> OUT/angles.json, puis --finalize")


def cmd_auto(args):
    sub_mode = (getattr(args, "sub_mode", None) or "").lower()
    n = int(args.n_angles)
    forger = AngleForger()

    if sub_mode == "meme":
        virality = load_meme_virality()
        angles = forger.forge_meme(n=n, campaign_id=virality.get("keyword"),
                                   keyword=virality.get("keyword"),
                                   virality=virality)
        campaign_id = virality.get("keyword")
    else:
        verdict = load_verdict()
        spin = load_humour_spin()
        angles = forger.forge(n=n, campaign_id=verdict.get("campaign_id"),
                              verdict=verdict, spin_humour=spin)
        campaign_id = verdict.get("campaign_id")

    lw = LearningsWeight(_FORGE_ROOT)
    angles = _apply_weights(angles, lw)

    out = {
        "campaign_id": campaign_id,
        "n_angles": len(angles),
        "anglesmith_status": "done",
        "weighting_eligible": lw.eligible(),
        "sub_mode": sub_mode,
        "angles": angles,
        "check_in_iw_custos": None,
    }
    save_json(ANGLES_PATH, out)
    direct = [a for a in angles if a["zone"] == "direct"]
    blue = [a for a in angles if a["zone"] == "blue_ocean"]
    print(f"[ANGLESMITH] --auto : {len(angles)} angles forges "
          f"({len(direct)} direct / {len(blue)} ocean bleu), weight_eligible={lw.eligible()}")
    if sub_mode == "meme":
        emotions = [a.get("emotion") for a in angles]
        print(f"[ANGLESMITH] mode meme: keyword={campaign_id} — "
              f"emotions={emotions} (anti-spam: 2 max par emotion)")


def cmd_finalize(args):
    if not os.path.exists(ANGLES_PATH):
        print("[ANGLESMITH] OUT/angles.json absent — lancer --prepare puis IRON, ou --auto")
        sys.exit(1)

    out = load_json(ANGLES_PATH)
    angles = out.get("angles", [])
    forger = AngleForger()

    # Heresie guard : profondeur + anti-cannibale
    for angle in angles:
        depth = angle.get("blue_ocean_depth")
        if depth is not None and depth != 1:
            print(f"[ANGLESMITH] HERESIE : depth={depth} != 1 — angle {angle.get('angle_id')} clampe")
            angle["blue_ocean_depth"] = 1

    for i in range(len(angles)):
        for j in range(i + 1, len(angles)):
            if forger._axes_different(angles[i], angles[j]) < 2:
                print(f"[ANGLESMITH] CANNIBALE: {angles[i].get('angle_id')} vs "
                      f"{angles[j].get('angle_id')} trop proches — flags")

    sub_mode = out.get("sub_mode", "")
    if sub_mode == "meme":
        counts = {}
        for angle in angles:
            emo = angle.get("emotion")
            if emo:
                counts[emo] = counts.get(emo, 0) + 1
        spam = {e: c for e, c in counts.items() if c > 2}
        if spam:
            print(f"[ANGLESMITH] HÉRÉSIE ANTI-SPAM: émotion(s) > 2 angles — {spam}")
            print("[ANGLESMITH] Corriger emotions dans OUT/angles.json avant la Porte 3")
        else:
            print("[ANGLESMITH] Anti-spam émotions OK (2 max par émotion)")

    lw = LearningsWeight(_FORGE_ROOT)
    out["angles"] = _apply_weights(angles, lw)
    out["check_in_iw_custos"] = now_iso()
    save_json(ANGLES_PATH, out)

    custos = os.path.join(_FORGE_ROOT, "IW_CUSTOS.py")
    if os.path.exists(custos):
        subprocess.run([sys.executable, custos, "--mode", "check-in",
                        "--frigate", "ANGLESMITH", "--output", ANGLES_PATH],
                       capture_output=True, text=True, timeout=30)
    print(f"[ANGLESMITH] Finalize : {len(angles)} angles valides — check-in ANGLESMITH done")
    print("[ANGLESMITH] OUT/angles.json pret pour la Porte 3 (F03 + F04)")


def main():
    parser = argparse.ArgumentParser(description="ANGLESMITH — Forge des N angles (Porte 2)")
    parser.add_argument("--prepare", action="store_true", help="Phase 1 : prompt IRON")
    parser.add_argument("--auto", action="store_true", help="Forge auto locale (sans IRON)")
    parser.add_argument("--finalize", action="store_true", help="Phase 3 : validation + check-in")
    parser.add_argument("--n-angles", default="10", help="Nombre d'angles (defaut 10)")
    parser.add_argument("--sub-mode", default=None,
                        help="Mode MEME: forger les 5 angles sur le scan F00 "
                             "(keyword + stats), F01/F03 SKIP")
    args = parser.parse_args()

    if args.prepare:
        cmd_prepare(args)
    elif args.auto:
        cmd_auto(args)
    elif args.finalize:
        cmd_finalize(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
