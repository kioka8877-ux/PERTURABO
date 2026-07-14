"""
tyrant.py — TYRANT : L'Oeil de Perturabo
==========================================

Le TYRANT voit le territoire avant le siège. Il ne produit rien. Il analyse.
Identifie le démon, la faille, le signal agents, la cartographie prix.
Recommande : SIEGEZ / ATTENDEZ / REORIENTEZ.

Différence avec le TYRANT YOUTUBE : pas de IRON manuel.
Le TYRANT API appelle call_oracle() directement — siège en 1 heure.

Flux :
  python tyrant.py           → exécution complète (prepare + oracle + finalize)
  python tyrant.py --status  → état courant
  python tyrant.py --finalize --from-file path → re-valider un output existant

Output :
  TYRANT/OUT/tyrant_output.json — rapport d'assessment pour Gate 1
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
_TYRANT_DIR  = os.path.dirname(_SCRIPT_DIR)
_MONDE_ROOT  = os.path.dirname(_TYRANT_DIR)
_TYRANT_OUT  = os.path.join(_TYRANT_DIR, "OUT")
_TYRANT_IN   = os.path.join(_TYRANT_DIR, "IN")
_LIBER       = os.path.join(_MONDE_ROOT, "liber_api.json")
_CORE        = os.path.abspath(os.path.join(_MONDE_ROOT, "..", "..", "CORE"))

sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(0, _CORE)

from contracts_loader import load_all

try:
    from ai_gateway import call_oracle
except ImportError:
    print("[TYRANT] ERREUR: ai_gateway.py introuvable dans CORE/")
    print(f"  Vérifie que CORE/ est bien à: {_CORE}")
    sys.exit(1)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ─────────────────────────────────────────────
# Assemblage du prompt
# ─────────────────────────────────────────────
def assemble_prompt(data: dict) -> str:
    brief      = data["warsmith_brief"]
    checklist  = json.dumps(data["api_scoring_checklist"], ensure_ascii=False, indent=2)
    cat_hint   = brief.get("categorie_hint") or "Non spécifiée — le TYRANT identifie la meilleure cible"
    target     = brief.get("target_hint") or "Non spécifié"
    notes      = brief.get("notes") or "Aucune"

    return f"""# MISSION DU TYRANT — Monde-Forge API

## CONTRAT DU TYRANT
{data["tyrant_prompt"]}

## DOCTRINE GÉNÉRALE
{data["system_prompt"]}

## RÈGLES ANTI-BULLSHIT
{data["anti_bullshit"]}

## GRILLE DE SCORING (api_scoring_checklist.json)
{checklist}

---

## MÉMOIRE IMPÉRIALE — RÈGLES DISTILLÉES (ARCHIVUM/rules/)
{data["archivum_rules"]}

## MÉMOIRE IMPÉRIALE — CARTOGRAPHIE MARCHÉ (ARCHIVUM/markets/)
{data["archivum_markets"]}

## MÉMOIRE IMPÉRIALE — LEDGERS SIEGES PASSÉS (ARCHIVUM/ledgers/)
{data["archivum_ledgers"]}

---

## BRIEF DU WARSMITH

- **Mode** : {brief.get("mode", "enclenche")}
- **Catégorie suggérée** : {cat_hint}
- **Cible suggérée** : {target}
- **Notes** : {notes}

---

## INSTRUCTIONS

Tu es le TYRANT. Tu vois le territoire RapidAPI avant le siège.
Tu réponds aux 5 questions définies dans ton contrat.
Si les données ARCHIVUM sont vides (premier siège), tu raisonnes sur ce que tu sais
des marchés API et tu appliques la grille de scoring à la catégorie suggérée.
Si aucune catégorie n'est suggérée, tu identifies la meilleure cible selon la grille.

Applique rigoureusement anti_bullshit.md :
- Chaque chiffre doit avoir une source (rapidapi_review, github_search, ledger, raisonnement)
- Si tu n'as pas la donnée réelle, note `null` et explique dans justification
- Ne jamais inventer un score de popularité ou une latence

Retourne UNIQUEMENT le JSON défini dans ton contrat (format tyrant_assessment).
Pas de texte avant, pas de texte après. JSON brut.
"""


# ─────────────────────────────────────────────
# Validation du tyrant_output.json
# ─────────────────────────────────────────────
def validate_output(output: dict) -> dict:
    """Valide la structure du JSON produit par l'Oracle."""
    root = output.get("tyrant_assessment", output)  # accepte les deux formes

    required_top = ["territoire", "demon", "faille", "signal_agents",
                    "cartographie_prix", "score_global", "recommandation", "justification"]
    missing = [k for k in required_top if k not in root]
    if missing:
        return {"valid": False, "error": f"Champs manquants dans tyrant_assessment: {missing}"}

    # Vérifier recommandation
    reco = root.get("recommandation", "")
    if reco not in ["SIEGEZ", "ATTENDEZ", "REORIENTEZ"]:
        return {"valid": False, "error": f"recommandation invalide: '{reco}' (SIEGEZ|ATTENDEZ|REORIENTEZ)"}

    # Score entre 0 et 100
    score = root.get("score_global")
    if score is not None and not (0 <= score <= 100):
        return {"valid": False, "error": f"score_global hors plage: {score} (0-100)"}

    return {"valid": True, "error": None, "assessment": root}


# ─────────────────────────────────────────────
# Écriture dans le liber_api.json
# ─────────────────────────────────────────────
def update_liber(assessment: dict):
    """Met à jour la section tyrant_report dans liber_api.json."""
    if not os.path.exists(_LIBER):
        print("[TYRANT] ⚠️ liber_api.json introuvable — mise à jour ignorée")
        return
    with open(_LIBER, "r", encoding="utf-8") as f:
        liber = json.load(f)

    tr = liber.setdefault("tyrant_report", {})
    tr["status"]          = "done"
    tr["territoire"]      = assessment.get("territoire", {})
    tr["demon"]           = assessment.get("demon", {})
    tr["faille"]          = assessment.get("faille", {})
    tr["signal_agents"]   = assessment.get("signal_agents", {})
    tr["cartographie_prix"] = assessment.get("cartographie_prix", {})
    tr["score_global"]    = assessment.get("score_global")
    tr["recommandation"]  = assessment.get("recommandation")
    tr["justification"]   = assessment.get("justification")
    tr["output_path"]     = os.path.join(_TYRANT_OUT, "tyrant_output.json")

    with open(_LIBER, "w", encoding="utf-8") as f:
        json.dump(liber, f, indent=2, ensure_ascii=False)
    print("[TYRANT] liber_api.json → tyrant_report mis à jour")


# ─────────────────────────────────────────────
# Check-in IW_CUSTOS
# ─────────────────────────────────────────────
def check_in(output_path: str):
    custos = os.path.join(_MONDE_ROOT, "IW_CUSTOS.py")
    if not os.path.exists(custos):
        print("[TYRANT] ⚠️ IW_CUSTOS.py introuvable — check-in ignoré")
        return
    import subprocess
    r = subprocess.run(
        [sys.executable, custos, "--mode", "check-in",
         "--frigate", "TYRANT", "--output", output_path],
        capture_output=True, text=True, timeout=30
    )
    print(f"[TYRANT] IW_CUSTOS: {r.stdout.strip()}")
    if r.stderr:
        print(f"[TYRANT] IW_CUSTOS stderr: {r.stderr.strip()}")


# ─────────────────────────────────────────────
# Affichage Gate 1
# ─────────────────────────────────────────────
def print_gate1_fiche(assessment: dict):
    t  = assessment.get("territoire", {})
    d  = assessment.get("demon", {})
    f  = assessment.get("faille", {})
    sa = assessment.get("signal_agents", {})
    cp = assessment.get("cartographie_prix", {})

    reco  = assessment.get("recommandation", "?")
    score = assessment.get("score_global", "?")
    just  = assessment.get("justification", "")

    reco_icon = {"SIEGEZ": "⚔️", "ATTENDEZ": "⏳", "REORIENTEZ": "🔄"}.get(reco, "?")

    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  TYRANT — FICHE GATE 1                                      ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Catégorie      : {str(t.get('categorie') or '—'):<42}║")
    print(f"║  Leader         : {str(t.get('leader') or '—'):<42}║")
    print(f"║  Popularité     : {str(t.get('score_popularite') or '—'):<42}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Démon          : {str(d.get('nom') or '—'):<42}║")
    print(f"║  Latence        : {str(d.get('latence_ms') or '—') + 'ms':<42}║")
    print(f"║  Prix dominant  : ${str(d.get('tier_dominant_prix') or '—'):<41}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Faille         : {str(f.get('type') or '—'):<42}║")
    print(f"║  Preuve         : {str(f.get('preuve') or '—')[:42]:<42}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Signal agents  : {str(sa.get('verdict') or '—'):<42}║")
    print(f"║  Repos GitHub   : {str(sa.get('repos_github') or '—'):<42}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Zone d'attaque : {str(cp.get('zone_attaque') or '—')[:42]:<42}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  SCORE GLOBAL   : {str(score):<42}║")
    print(f"║  RECOMMANDATION : {reco_icon + '  ' + reco:<42}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    # Justification tronquée sur 2 lignes
    just_lines = [just[i:i+42] for i in range(0, min(len(just), 84), 42)]
    for line in just_lines:
        print(f"║  {line:<60}║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("  → Valider : python IW_CUSTOS.py --mode gate --gate 1 --decision yes")
    print("  → Rejeter : python IW_CUSTOS.py --mode gate --gate 1 --decision no --notes 'raison'")
    print()


# ─────────────────────────────────────────────
# Commandes
# ─────────────────────────────────────────────
def cmd_run(args):
    """Exécution complète : prepare → oracle → finalize."""
    print("=" * 60)
    print("👁️  TYRANT — L'Oeil de Perturabo")
    print("=" * 60)

    # 1. Charger tous les contrats + ARCHIVUM
    print("
[TYRANT] Chargement ARCHIVUM + CONTRACTS...")
    data = load_all()
    print(f"[TYRANT] rules: {data['meta']['rules_count']} | "
          f"markets: {data['meta']['markets_count']} | "
          f"ledgers: {data['meta']['ledgers_count']}")
    print(f"[TYRANT] Brief: {data['warsmith_brief']}")

    # 2. Assembler le prompt
    print("
[TYRANT] Assemblage du prompt...")
    prompt = assemble_prompt(data)
    prompt_size = len(prompt.encode("utf-8")) / 1024
    print(f"[TYRANT] Prompt: {prompt_size:.1f} KB")

    # Sauvegarder le prompt pour audit
    os.makedirs(_TYRANT_OUT, exist_ok=True)
    prompt_path = os.path.join(_TYRANT_OUT, "iron_prompt.txt")
    with open(prompt_path, "w", encoding="utf-8") as pf:
        pf.write(prompt)

    # 3. Appeler l'Oracle
    print(f"
[TYRANT] Appel Oracle (TYRANT → claude-sonnet-4.6)...")
    result = call_oracle("TYRANT", prompt, expect_json=True)

    if result["status"] == "error":
        print(f"[TYRANT] ❌ Oracle error: {result['error']}")
        sys.exit(1)

    print(f"[TYRANT] ✅ Oracle répondu en {result['attempts']} tentative(s) — modèle: {result['model']}")

    # 4. Sauvegarder le output brut
    output = result["content"]
    # Normaliser : accepte {"tyrant_assessment": {...}} ou directement l'objet
    if "tyrant_assessment" not in output:
        output = {"tyrant_assessment": output}

    output_path = os.path.join(_TYRANT_OUT, "tyrant_output.json")
    with open(output_path, "w", encoding="utf-8") as of:
        json.dump(output, of, indent=2, ensure_ascii=False)
    print(f"[TYRANT] Output sauvegardé: {output_path}")

    # 5. Valider
    val = validate_output(output)
    if not val["valid"]:
        print(f"[TYRANT] ❌ Validation échouée: {val['error']}")
        print(f"[TYRANT] Output brut sauvegardé dans {output_path} pour inspection")
        sys.exit(1)

    assessment = val["assessment"]
    print("[TYRANT] ✅ JSON valide")

    # 6. Mettre à jour le liber
    update_liber(assessment)

    # 7. Check-in IW_CUSTOS
    if not args.no_checkin:
        check_in(output_path)

    # 8. Afficher la fiche Gate 1
    print_gate1_fiche(assessment)

    print(f"{'=' * 60}")
    print("👁️  TYRANT — ÉCLAIRAGE TERMINÉ")
    print(f"{'=' * 60}")
    print(f"Output: {output_path}")


def cmd_finalize(args):
    """Re-valider un output existant sans appeler l'Oracle."""
    output_path = args.from_file or os.path.join(_TYRANT_OUT, "tyrant_output.json")

    if not os.path.exists(output_path):
        print(f"[TYRANT] ❌ Fichier introuvable: {output_path}")
        sys.exit(1)

    with open(output_path, "r", encoding="utf-8") as f:
        output = json.load(f)

    val = validate_output(output)
    if not val["valid"]:
        print(f"[TYRANT] ❌ Validation échouée: {val['error']}")
        sys.exit(1)

    assessment = val["assessment"]
    print("[TYRANT] ✅ JSON valide")
    update_liber(assessment)

    if not args.no_checkin:
        check_in(output_path)

    print_gate1_fiche(assessment)


def cmd_status(args):
    prompt_path = os.path.join(_TYRANT_OUT, "iron_prompt.txt")
    output_path = os.path.join(_TYRANT_OUT, "tyrant_output.json")

    print()
    print("╔═══════════════════════════════════════╗")
    print("║  TYRANT — ÉTAT                        ║")
    print("╠═══════════════════════════════════════╣")
    print(f"║  iron_prompt.txt  : {'✅' if os.path.exists(prompt_path) else '❌'}{'  prêt' if os.path.exists(prompt_path) else '  absent'}                     ║")
    print(f"║  tyrant_output.json: {'✅' if os.path.exists(output_path) else '❌'}{'  prêt' if os.path.exists(output_path) else '  absent'}                    ║")

    if os.path.exists(_LIBER):
        with open(_LIBER) as f:
            liber = json.load(f)
        tr_status = liber.get("tyrant_report", {}).get("status", "?")
        reco = liber.get("tyrant_report", {}).get("recommandation") or "—"
        score = liber.get("tyrant_report", {}).get("score_global") or "—"
        print(f"║  liber status     : {tr_status:<19}║")
        print(f"║  score / reco     : {str(score)}/{reco:<16}║")

    print("╚═══════════════════════════════════════╝")

    if not os.path.exists(output_path):
        print("
→ Lancer: python tyrant.py")
    else:
        print("
→ Gate 1: python IW_CUSTOS.py --mode gate --gate 1 --decision yes")
    print()


def main():
    parser = argparse.ArgumentParser(description="TYRANT — L'Oeil de Perturabo")
    parser.add_argument("--status",      action="store_true", help="Afficher l'état courant")
    parser.add_argument("--finalize",    action="store_true", help="Re-valider un output existant")
    parser.add_argument("--from-file",   default=None,        help="Chemin vers tyrant_output.json existant")
    parser.add_argument("--no-checkin",  action="store_true", help="Ne pas appeler IW_CUSTOS check-in")
    args = parser.parse_args()

    if args.status:
        cmd_status(args)
    elif args.finalize:
        cmd_finalize(args)
    else:
        cmd_run(args)


if __name__ == "__main__":
    main()
