"""
contracts_loader.py — Charge les contrats et l'ARCHIVUM pour le TYRANT API
Récupère : tyrant_prompt.md, anti_bullshit.md, system_prompt.md,
           ARCHIVUM/rules/, ARCHIVUM/markets/, ARCHIVUM/targets/,
           api_scoring_checklist.json, liber_api.json (warsmith_brief)
"""

import json
import os
from pathlib import Path

_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_TYRANT_DIR   = os.path.dirname(_SCRIPT_DIR)           # TYRANT/
_MONDE_ROOT   = os.path.dirname(_TYRANT_DIR)           # MONDES_FORGES/API/
_CONTRACTS    = os.path.join(_MONDE_ROOT, "CONTRACTS")
_ARCHIVUM     = os.path.join(_MONDE_ROOT, "ARCHIVUM")
_LIBER        = os.path.join(_MONDE_ROOT, "liber_api.json")


def _read(path: str, default: str = "") -> str:
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _read_json(path: str, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default


def load_contracts() -> dict:
    """Charge les 4 fichiers CONTRACTS/."""
    return {
        "system_prompt":         _read(os.path.join(_CONTRACTS, "system_prompt.md")),
        "tyrant_prompt":         _read(os.path.join(_CONTRACTS, "tyrant_prompt.md")),
        "anti_bullshit":         _read(os.path.join(_CONTRACTS, "anti_bullshit.md")),
        "api_scoring_checklist": _read_json(
            os.path.join(_CONTRACTS, "api_scoring_checklist.json"), {}
        ),
    }


def load_archivum_rules() -> str:
    """Charge ARCHIVUM/rules/ — patterns distillés des sieges passés (couche froide)."""
    rules_dir = os.path.join(_ARCHIVUM, "rules")
    if not os.path.exists(rules_dir):
        return "[ARCHIVUM/rules] Vide — premier siège, aucun pattern enregistré."
    files = sorted(Path(rules_dir).glob("*.md"))
    if not files:
        return "[ARCHIVUM/rules] Vide — premier siège, aucun pattern enregistré."
    parts = []
    for f in files:
        content = f.read_text(encoding="utf-8").strip()
        if content:
            parts.append(f"--- {f.name} ---
{content}")
    return "

".join(parts) if parts else "[ARCHIVUM/rules] Aucun fichier .md trouvé."


def load_archivum_markets() -> str:
    """Charge ARCHIVUM/markets/ — cartographie scorée des catégories RapidAPI (couche froide)."""
    markets_dir = os.path.join(_ARCHIVUM, "markets")
    if not os.path.exists(markets_dir):
        return "[ARCHIVUM/markets] Vide — cartographie non encore construite."
    files = list(Path(markets_dir).glob("*.json")) + list(Path(markets_dir).glob("*.md"))
    if not files:
        return "[ARCHIVUM/markets] Vide — cartographie non encore construite."
    parts = []
    for f in sorted(files)[:10]:  # max 10 fichiers
        try:
            if f.suffix == ".json":
                data = json.loads(f.read_text(encoding="utf-8"))
                parts.append(f"--- {f.name} ---
{json.dumps(data, ensure_ascii=False, indent=2)[:2000]}")
            else:
                parts.append(f"--- {f.name} ---
{f.read_text(encoding='utf-8')[:2000]}")
        except Exception:
            continue
    return "

".join(parts) if parts else "[ARCHIVUM/markets] Fichiers illisibles."


def load_archivum_ledgers() -> str:
    """Charge ARCHIVUM/ledgers/ — résultats des sieges passés (Iron Warriors survivants/morts)."""
    ledgers_dir = os.path.join(_ARCHIVUM, "ledgers")
    if not os.path.exists(ledgers_dir):
        return "[ARCHIVUM/ledgers] Vide — aucun siège précédent."
    files = sorted(Path(ledgers_dir).glob("*.json"), reverse=True)[:5]  # 5 derniers
    if not files:
        return "[ARCHIVUM/ledgers] Vide — aucun siège précédent."
    parts = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            parts.append(f"--- {f.name} ---
{json.dumps(data, ensure_ascii=False, indent=2)[:1500]}")
        except Exception:
            continue
    return "

".join(parts) if parts else "[ARCHIVUM/ledgers] Fichiers illisibles."


def load_warsmith_brief() -> dict:
    """Charge le warsmith_brief depuis liber_api.json."""
    liber = _read_json(_LIBER, {})
    return liber.get("warsmith_brief", {
        "mode": "enclenche",
        "categorie_hint": None,
        "target_hint": None,
        "notes": None,
    })


def load_all() -> dict:
    """Charge tout ce dont le TYRANT a besoin pour assembler son prompt."""
    contracts = load_contracts()
    warsmith_brief = load_warsmith_brief()

    rules_count    = len(list(Path(os.path.join(_ARCHIVUM, "rules")).glob("*.md"))) if os.path.exists(os.path.join(_ARCHIVUM, "rules")) else 0
    markets_count  = len(list(Path(os.path.join(_ARCHIVUM, "markets")).glob("*")))  if os.path.exists(os.path.join(_ARCHIVUM, "markets")) else 0
    ledgers_count  = len(list(Path(os.path.join(_ARCHIVUM, "ledgers")).glob("*.json"))) if os.path.exists(os.path.join(_ARCHIVUM, "ledgers")) else 0

    return {
        **contracts,
        "archivum_rules":   load_archivum_rules(),
        "archivum_markets": load_archivum_markets(),
        "archivum_ledgers": load_archivum_ledgers(),
        "warsmith_brief":   warsmith_brief,
        "meta": {
            "monde_root":    _MONDE_ROOT,
            "rules_count":   rules_count,
            "markets_count": markets_count,
            "ledgers_count": ledgers_count,
        }
    }


if __name__ == "__main__":
    data = load_all()
    print(f"[CONTRACTS] system_prompt : {len(data['system_prompt'])} chars")
    print(f"[CONTRACTS] tyrant_prompt : {len(data['tyrant_prompt'])} chars")
    print(f"[ARCHIVUM]  rules         : {data['meta']['rules_count']} fichiers")
    print(f"[ARCHIVUM]  markets       : {data['meta']['markets_count']} fichiers")
    print(f"[ARCHIVUM]  ledgers       : {data['meta']['ledgers_count']} fichiers")
    print(f"[LIBER]     warsmith_brief: {data['warsmith_brief']}")
