# IW_CAMPAIGN_LOG — Monde-Forge API

## Journal de construction — à lire en premier si contexte perdu

---

## [CONSTRUCTION] Session fondatrice — Doctrine complète

### Contexte projet

PERTURABO = système de siège automatisé. CORE/ + MONDES_FORGES/ (YOUTUBE + API).
Chaque Monde-Forge autonome : liber, ARCHIVUM, frégates, CONTRACTS.

### Doctrine API résumée

- Input : "enclenche" → système trouve la cible seul
- Output : 20 Iron Warriors (APIs FastAPI) en < 1 heure
- Stack 100% gratuit : FastAPI + Railway/Render
- Cash flow cible : 500$/mois à partir du mois 4-5

### FLEET_STATUS_FLOW
```
pending_reconnaissance → tyrant_report_ready → intel_captured → target_scored
→ ironwarriors_forged → listings_ready → market_mapped → deployed → complete
```

### Frégates et modèles

TYRANT → claude-sonnet-4.6 | F01 → haiku-4.5 | F02 → deepseek-v4-flash
F03/F05 → sonnet-4.6 | F04 → gemini-3.5-flash | F06 → haiku-4.5

### Gates

Gate 1 : après TYRANT (valider cible)
Gate 2 : après F01/F02 (valider 20 angles)
Gate 3 : après F03 (review code Iron Warriors)
Gate 4 : après F04 (valider listings RapidAPI)

---

## [CONSTRUCTION] Phases 0-3 — Structure + CONTRACTS + liber + IW_CUSTOS + ai_gateway.py

Voir commits précédents.

---

## [CONSTRUCTION] Phase 4 — TYRANT créé

**Différence clé avec YOUTUBE** : pas de IRON manuel. `call_oracle("TYRANT", prompt)` direct.

**contracts_loader.py** — charge :
- CONTRACTS/ (system_prompt, tyrant_prompt, anti_bullshit, api_scoring_checklist)
- ARCHIVUM/rules/ (patterns distillés — vide au premier siège)
- ARCHIVUM/markets/ (cartographie RapidAPI — vide au premier siège)
- ARCHIVUM/ledgers/ (résultats sieges passés — vide au premier siège)
- warsmith_brief depuis liber_api.json

**tyrant.py** — flux complet en une commande :
1. `load_all()` — charge tout
2. `assemble_prompt()` — prompt 5 questions + checklist + ARCHIVUM + brief
3. `call_oracle("TYRANT", prompt)` — Oracle répond avec tyrant_assessment JSON
4. `validate_output()` — vérifie champs obligatoires, recommandation, score
5. `update_liber()` — écrit tyrant_report dans liber_api.json
6. `check_in()` — IW_CUSTOS check-in → fleet_status: tyrant_report_ready
7. `print_gate1_fiche()` — tableau de bord complet pour le Warsmith

**Comportement premier siège** (ARCHIVUM vide) :
- Si `categorie_hint` fourni → Oracle raisonne sur cette catégorie
- Si aucun hint → Oracle identifie la meilleure cible selon la grille
- Champs sans données réelles → `null` (anti_bullshit strictement respecté)

**Fichier IN** : `warsmith_brief.example.json` — template pour le brief Warsmith

---

## Prochaine étape

**Phase 5** : F01 SENTINEL — scraping multi-source (RapidAPI + GitHub + web).
Alimentera ARCHIVUM/targets/ avec les données réelles pour F02 BREACHER.
