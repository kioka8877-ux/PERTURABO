# DEV_ROADMAP — Monde-Forge API

> Feuille de route de développement. Statut mis à jour manuellement par le Warsmith ou l'agent de développement.
> **Si le chat meurt** : lire ce fichier + IW_CAMPAIGN_LOG.md pour reconstituer le contexte complet.

---

## Contexte de reprise rapide

- **Projet** : PERTURABO / Monde-Forge API
- **Objectif** : moteur de siège RapidAPI — identifier une catégorie faible, déployer 20 APIs en 1h
- **Doctrine** : input "enclenche" → TYRANT trouve la cible seul → 20 Iron Warriors déployés simultanément
- **Repo** : `github.com/kioka8877-ux/PERTURABO`
- **Chemin de ce monde** : `MONDES_FORGES/API/`
- **Référence architecture** : `MONDES_FORGES/YOUTUBE/` — même pattern exact (frégates/IW_CUSTOS/orchestrateur)
- **Pattern de chaque frégate** : `--prepare` → iron_prompt.txt → IRON écrit output.json → `--finalize` → check-in IW_CUSTOS

---

## Légende statut

- `[ ]` À faire
- `[x]` Terminé
- `[~]` En cours

---

## Phase 0 — Infrastructure (TERMINÉE)

- [x] Structure `MONDES_FORGES/API/` créée sur le repo
- [x] `ARCHIVUM/` avec toutes sous-couches
- [x] `CONTRACTS/` dossier créé
- [x] `fregates/` dossier créé
- [x] `TRACKING/` avec docs de suivi
- [x] Structure frégates F01-F06 créée (IN/, OUT/, CODEBASE/, TRACKING/)
- [x] TYRANT/ et ORCHESTRATOR/ structures créées
- [x] Doctrine et architecture définies (voir IW_CAMPAIGN_LOG.md)

---

## Phase 1 — CONTRACTS (TERMINÉE)

- [x] `CONTRACTS/system_prompt.md` — doctrine API, flux siège, contraintes absolues
- [x] `CONTRACTS/tyrant_prompt.md` — 5 questions Oracle API (territoire/démon/faille/20 angles/chemin)
- [x] `CONTRACTS/iron_prompt.md` — contrat Exécuteur adapté API (règles par frégate)
- [x] `CONTRACTS/anti_bullshit.md` — filtre patterns non prouvés (adapté API)
- [x] `CONTRACTS/api_scoring_checklist.json` — grille scoring complète avec poids et critères

---

## Phase 2 — Fichiers Core (À FAIRE)

Créer à la racine de `MONDES_FORGES/API/` :

- [ ] `IW_CUSTOS.py`
  - Adapter depuis `MONDES_FORGES/YOUTUBE/IW_CUSTOS.py`
  - Changer : VALID_FRIGATES, FLEET_STATUS_FLOW, FRIGATE_STATUS_KEY, FRIGATE_TRANSITIONS, PRECONDITIONS
  - CMS_PATH → `liber_api.json`

- [ ] `liber_api.json`
  - fleet_status initial : "idle"
  - Structure définie dans IW_CAMPAIGN_LOG.md + DEV_ROADMAP Phase 2

- [ ] `contracts_loader.py`
  - Charge : system_prompt, tyrant_prompt, iron_prompt, anti_bullshit, api_scoring_checklist
  - Charge : ARCHIVUM/rules/*.md + ARCHIVUM/targets/*.json + ARCHIVUM/markets/*.json

- [ ] `ai_gateway.py`
  - Routing modèles par frégate
  - Variables : AI_GATEWAY_BASE_URL, AI_GATEWAY_API_KEY

---

## Phase 3 — TYRANT (À FAIRE)

- [ ] `TYRANT/CODEBASE/tyrant.py`
  - Pattern --prepare / --finalize
  - 5 questions Oracle API
  - Output : eclairissement_api.json

---

## Phase 4 — Frégates (À FAIRE)

- [ ] `fregates/F01_SENTINEL/CODEBASE/sentinel.py` — collecte brute, pas d'IA
- [ ] `fregates/F02_BREACHER/CODEBASE/breacher.py` — scoring + 20 angles
- [ ] `fregates/F03_FORGEWARD/CODEBASE/forgeward.py` — 20 Iron Warriors parallèle
- [ ] `fregates/F04_HERALD/CODEBASE/herald.py` — listings + README
- [ ] `fregates/F05_GRAND_COMPASS/CODEBASE/grand_compass.py` — blue ocean
- [ ] `fregates/F06_CAPTEURS/CODEBASE/capteurs.py` — surveillance quotidienne

---

## Phase 5 — Orchestrateur (À FAIRE)

- [ ] `ORCHESTRATOR/CODEBASE/orchestrator.py`
- [ ] `ORCHESTRATOR/CODEBASE/gates.py`

---

## Phase 6 — GitHub Actions CAPTEURS (À FAIRE)

- [ ] `.github/workflows/api_capteurs.yml`

---

## Phase 7 — ARCHIVUM amorçage (À FAIRE)

- [ ] `ARCHIVUM/docs/rapidapi_guide.md`
- [ ] `ARCHIVUM/docs/fastapi_template.md`
- [ ] `ARCHIVUM/docs/openapi_template.md`
- [ ] `ARCHIVUM/templates/api_base.py`
- [ ] `ARCHIVUM/templates/openapi_base.json`
- [ ] `ARCHIVUM/rules/market_rules.md`

---

## Phase 8 — Validation premier siège (OBJECTIF FINAL)

- [ ] Lancer `python orchestrator.py start --mode enclenche`
- [ ] Valider les 4 portes
- [ ] 20 Iron Warriors déployés en moins d'1h
- [ ] F06 CAPTEURS actifs
- [ ] `ARCHIVUM/ledgers/` mis à jour

---

## Règles pour l'agent de développement

1. Toujours partir du code YOUTUBE comme base — les patterns sont prouvés
2. `IW_CUSTOS.py` est le seul autorisé à modifier `liber_api.json` — règle absolue
3. F01 SENTINEL : aucun appel IA — collecte brute uniquement
4. Tous les appels IA passent par `ai_gateway.py` — jamais directs dans les frégates
5. F03 FORGEWARD produit les 20 Iron Warriors en parallèle (threads ou async)
6. `ARCHIVUM/templates/` doit exister avant le premier siège
7. Stack Iron Warriors : Python + FastAPI + httpx — zéro dépendance payante

---

*Dernière mise à jour : 2026-07-14 — Phase 1 terminée*
*Statut global : Phase 1 terminée — Phase 2 à démarrer*
