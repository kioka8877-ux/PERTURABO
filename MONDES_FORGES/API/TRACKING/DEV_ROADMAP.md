# DEV_ROADMAP — Monde-Forge API

## Statut global : Phase 2 complète — Phase 3 à démarrer

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

## Phase 2 — liber_api.json + IW_CUSTOS.py ✅

- [x] `liber_api.json` — bus d'état complet du siège
  - fleet_status, siege_id, monde, warsmith_brief
  - tyrant_report avec territoire/démon/faille/signal_agents/cartographie_prix
  - f01 à f06 avec tous les champs spécifiques (hashes, counts, urls)
  - gate_decisions × 4 avec label/validated/timestamp/notes
  - siege_timestamps pour mesurer la durée de chaque phase
- [x] `IW_CUSTOS.py` — orchestrateur complet
  - `--mode reset` : initialise un nouveau siège avec ID auto ou custom
  - `--mode check-out` : autorise une frégate + vérifie gate requise
  - `--mode check-in` : valide output + avance fleet_status + affiche next action
  - `--mode gate` : valide/rejette une gate + affiche ce qui est débloqué
  - `--mode validate` : vérifie le schéma du liber
  - `--mode status` : tableau de bord complet avec icônes

---

## Phase 3 — ai_gateway.py ⬜

- [ ] Créer `ai_gateway.py` dans CORE/ (partagé entre tous les Mondes-Forges)
- [ ] Routing par frégate : F01 → Haiku, F02 → DeepSeek Flash, F03/F05 → Sonnet, F04/F06 → Gemini Flash
- [ ] Support `AI_GATEWAY_BASE_URL` + `AI_GATEWAY_API_KEY` (variables d'env)
- [ ] Fonction centrale `call_oracle(frigate_id, prompt, schema=None)` → JSON validé
- [ ] Retry automatique (max 3) si réponse non-JSON ou JSON invalide
- [ ] Log de chaque appel Oracle dans TRACKING/IW_CAMPAIGN_LOG.md

---

## Phase 4 — TYRANT ⬜

- [ ] `TYRANT/CODEBASE/tyrant.py` — script Python complet
  - `--prepare` : charge ARCHIVUM couches froide + chaude, assemble iron_prompt.txt
  - IRON lit iron_prompt.txt → produit tyrant_output.json
  - `--finalize` : valide JSON, check-in IW_CUSTOS, affiche fiche Gate 1
- [ ] `TYRANT/IN/` — structure des fichiers d'entrée
- [ ] `TYRANT/OUT/` — structure des fichiers de sortie

---

## Phase 5 — F01 SENTINEL ⬜

- [ ] `F01_SENTINEL/CODEBASE/sentinel.py`
  - Module `sentinel_rapid` : scrape listings RapidAPI (score, latence, pricing, reviews)
  - Module `sentinel_gh` : GitHub API — wrappers actifs, issues, étoiles
  - Module `sentinel_web` : Jina Reader pour docs et articles
  - Output : `ARCHIVUM/targets/[siege_id]/raw_intel.json`
  - Check-in IW_CUSTOS automatique en fin d'exécution

---

## Phase 6 — F02 BREACHER ⬜

- [ ] `F02_BREACHER/CODEBASE/breacher.py`
  - Lit `raw_intel.json` depuis ARCHIVUM/targets/
  - Croise avec ARCHIVUM/rules/ (couche froide)
  - Calcule score sur 4 dimensions (formula api_scoring_checklist.json)
  - Génère les 20 angles d'attaque depuis les types définis
  - Output : update liber_api.json (f02 section) + angles_attaque.json

---

## Phase 7 — F03 FORGEWARD ⬜

- [ ] `F03_FORGEWARD/CODEBASE/forgeward.py`
  - Lit les 20 angles depuis le liber
  - Pour chaque angle : génère api.py + openapi.json + requirements.txt + deploy.sh
  - Génération en parallèle (asyncio / ThreadPoolExecutor)
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
