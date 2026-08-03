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


def load_verdict() -> dict:
    path = os.path.join(CAMPAIGN_DIR, "verdict.json")
    if not os.path.exists(path):
        print(f"[ANGLESMITH] verdict introuvable: {path}")
        print("[ANGLESMITH] Lancer F02_TYRANT_CAMP --finalize d'abord (Porte 1)")
        sys.exit(1)
    return load_json(path)


def _apply_weights(angles: list[dict], lw: LearningsWeight):
    for angle in angles:
        angle["weight"] = lw.weight_for_family(angle["angle_family"])
    return angles


def cmd_prepare(args):
    verdict = load_verdict()
    n = int(args.n_angles)
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
    save_json(os.path.join(IN_DIR, "anglesmith_prompt.json"), prompt)
    print(f"[ANGLESMITH] Prompt IRON : {os.path.join(IN_DIR, 'anglesmith_prompt.json')}")
    print("[ANGLESMITH] Copier le prompt dans Claude sandbox -> OUT/angles.json, puis --finalize")


def cmd_auto(args):
    verdict = load_verdict()
    n = int(args.n_angles)
    forger = AngleForger()
    angles = forger.forge(n=n, campaign_id=verdict.get("campaign_id"), verdict=verdict)
    lw = LearningsWeight(_FORGE_ROOT)
    angles = _apply_weights(angles, lw)

    out = {
        "campaign_id": verdict.get("campaign_id"),
        "n_angles": len(angles),
        "anglesmith_status": "done",
        "weighting_eligible": lw.eligible(),
        "angles": angles,
        "check_in_iw_custos": None,
    }
    save_json(ANGLES_PATH, out)
    direct = [a for a in angles if a["zone"] == "direct"]
    blue = [a for a in angles if a["zone"] == "blue_ocean"]
    print(f"[ANGLESMITH] --auto : {len(angles)} angles forges "
          f"({len(direct)} direct / {len(blue)} ocean bleu), weight_eligible={lw.eligible()}")


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
