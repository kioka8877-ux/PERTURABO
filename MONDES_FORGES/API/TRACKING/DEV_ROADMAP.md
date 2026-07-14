# DEV_ROADMAP — Monde-Forge API

## Statut global : Phase 1 complète — Phase 2 à démarrer

---

## Phase 0 — Structure et tracking ✅

- [x] Créer MONDES_FORGES/API/ avec toutes les sous-structures
- [x] Créer les tracking docs (IW_CAMPAIGN_LOG.md, IW_TRANSFER_LOG.md, DEV_ROADMAP.md)
- [x] Créer les logs par frégate (F01 à F06)
- [x] Créer les dossiers TYRANT et ORCHESTRATOR avec IN/OUT/CODEBASE

---

## Phase 1 — CONTRACTS ✅

- [x] `CONTRACTS/system_prompt.md` — doctrine RapidAPI + Iron Warriors
- [x] `CONTRACTS/tyrant_prompt.md` — 5 questions : territoire, démon, latence, wrappers, pricing
- [x] `CONTRACTS/iron_prompt.md` — contrat de l'exécuteur
- [x] `CONTRACTS/anti_bullshit.md` — filtre données prouvées
- [x] `CONTRACTS/api_scoring_checklist.json` — grille de scoring des cibles (4 dimensions × poids)

---

## Phase 2 — liber_api.json + IW_CUSTOS.py ⬜

- [ ] Créer `liber_api.json` avec tous les champs définis (fleet_status, frégates F01-F06, gate_decisions)
- [ ] Adapter `IW_CUSTOS.py` depuis le YOUTUBE pour le Monde-Forge API
  - Paramètre `--monde api`
  - FLEET_STATUS_FLOW API
  - VALID_FRIGATES API
  - Gestion des 4 Gates

---

## Phase 3 — ai_gateway.py ⬜

- [ ] Créer `ai_gateway.py` dans CORE/
- [ ] Routing par frégate (F01 → Haiku, F02 → DeepSeek Flash, F03/F05 → Sonnet, F04/F06 → Gemini Flash)
- [ ] Support AI_GATEWAY_BASE_URL + AI_GATEWAY_API_KEY
- [ ] Fonction commune `call_oracle(frigate_id, prompt)` utilisée par toutes les frégates

---

## Phase 4 — TYRANT ⬜

- [ ] `TYRANT/CODEBASE/tyrant.py` — script Python complet
  - Modules : load_archivum(), assemble_prompt(), call_oracle(), write_liber()
  - Lit ARCHIVUM/targets/ + ARCHIVUM/rules/
  - Produit le JSON TYRANT assessment dans le liber
- [ ] `TYRANT/IN/` — structure des fichiers d'entrée
- [ ] `TYRANT/OUT/` — structure des fichiers de sortie

---

## Phase 5 — F01 SENTINEL ⬜

- [ ] `F01_SENTINEL/CODEBASE/sentinel.py`
  - Module `sentinel_rapid` : scrape listings RapidAPI (score, latence, pricing, reviews)
  - Module `sentinel_gh` : GitHub API — wrappers actifs, issues, étoiles
  - Module `sentinel_web` : Jina Reader pour docs et articles
  - Output : `ARCHIVUM/targets/[siege_id]/raw_intel.json`
- [ ] Test standalone : `python sentinel.py --categorie "linkedin-scraper"`

---

## Phase 6 — F02 BREACHER ⬜

- [ ] `F02_BREACHER/CODEBASE/breacher.py`
  - Lit `raw_intel.json` depuis ARCHIVUM/targets/
  - Croise avec ARCHIVUM/rules/ (couche froide)
  - Calcule le score sur 4 dimensions
  - Génère les 20 angles d'attaque depuis `api_scoring_checklist.json`
  - Output : update liber_api.json (f02 section)

---

## Phase 7 — F03 FORGEWARD ⬜

- [ ] `F03_FORGEWARD/CODEBASE/forgeward.py`
  - Lit les 20 angles depuis le liber
  - Pour chaque angle : génère api.py + openapi.json + requirements.txt + deploy.sh
  - Génération en parallèle (asyncio ou ThreadPoolExecutor)
  - Output : `ARCHIVUM/targets/[siege_id]/ironwarriors/[id]/`
- [ ] Templates de base dans `ARCHIVUM/templates/`

---

## Phase 8 — F04 HERALD + F05 GRAND COMPASS + F06 CAPTEURS ⬜

- [ ] `F04_HERALD/CODEBASE/herald.py` — listing_rapidapi.md + README.md pour chaque Iron Warrior
- [ ] `F05_GRAND_COMPASS/CODEBASE/grand_compass.py` — validation blue ocean, déploiement Railway/Render
- [ ] `F06_CAPTEURS/CODEBASE/capteurs.py` — monitoring post-siège, update ARCHIVUM/ledgers/

---

## Phase 9 — ORCHESTRATOR + test siège complet ⬜

- [ ] `ORCHESTRATOR/CODEBASE/orchestrator.py` — orchestration semi-manuelle des 4 Gates
- [ ] Test siège complet "enclenche" → 20 Iron Warriors déployés
- [ ] Premier ledger : survie/mort après 7 jours

---

## Métriques de succès

| Métrique | Cible |
|---|---|
| Durée d'un siège complet | < 1 heure |
| Iron Warriors par siège | 20 |
| Temps de réponse Iron Warrior | < 500ms |
| Iron Warriors survivants à 30j | ≥ 2/20 (10%) |
| Revenus mois 4-5 | 500$/mois |
