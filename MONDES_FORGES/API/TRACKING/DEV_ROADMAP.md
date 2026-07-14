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
- [x] `ARCHIVUM/` avec toutes sous-couches (targets/, docs/, github/, articles/, rules/, templates/, markets/, ledgers/)
- [x] `CONTRACTS/` dossier créé
- [x] `fregates/` dossier créé
- [x] `TRACKING/` avec docs de suivi (ce fichier + IW_CAMPAIGN_LOG.md + IW_TRANSFER_LOG.md)
- [x] Structure frégates F01-F06 créée (IN/, OUT/, CODEBASE/, TRACKING/)
- [x] Doctrine et architecture définies (voir IW_CAMPAIGN_LOG.md)
- [x] TYRANT/ structure créée

---

## Phase 1 — CONTRACTS (À FAIRE)

Créer dans `MONDES_FORGES/API/CONTRACTS/` :

- [ ] `system_prompt.md`
  - Doctrine API : marché RapidAPI, rôle Iron Warriors, production en volume
  - Référence : `MONDES_FORGES/YOUTUBE/CONTRACTS/system_prompt.md`
  
- [ ] `tyrant_prompt.md`
  - 5 questions Oracle adaptées API (territoire/démon/latence/wrappers/pricing)
  - Référence : `MONDES_FORGES/YOUTUBE/CONTRACTS/tyrant_prompt.md`
  
- [ ] `iron_prompt.md`
  - Quasi-identique au YOUTUBE — l'IRON produit, ne décide pas
  - Copier et adapter `MONDES_FORGES/YOUTUBE/CONTRACTS/iron_prompt.md`
  
- [ ] `anti_bullshit.md`
  - Identique au YOUTUBE (filtre universel)
  - Copier `MONDES_FORGES/YOUTUBE/CONTRACTS/anti_bullshit.md`
  
- [ ] `api_scoring_checklist.json`
  - Grille scoring : popularité×0.35 + latence×0.25 + wrappers×0.20 + frustration×0.20
  - Équivalent de `skeleton_checklist.json` dans YOUTUBE

---

## Phase 2 — Fichiers Core (À FAIRE)

Créer à la racine de `MONDES_FORGES/API/` :

- [ ] `IW_CUSTOS.py`
  - Adapter depuis `MONDES_FORGES/YOUTUBE/IW_CUSTOS.py`
  - Changer : VALID_FRIGATES, FLEET_STATUS_FLOW, FRIGATE_STATUS_KEY, FRIGATE_TRANSITIONS, PRECONDITIONS
  - CMS_PATH → `liber_api.json`
  - CAMPAIGN_LOG → `TRACKING/IW_CAMPAIGN_LOG.md`
  - TRANSFER_LOG → `TRACKING/IW_TRANSFER_LOG.md`

- [ ] `liber_api.json`
  ```json
  {
    "_comment": "CMS CENTRALISE — LIBER API. Seul IW_CUSTOS.py est autorisé à modifier fleet_status.",
    "fleet_status": "idle",
    "siege_id": null,
    "monde": "api",
    "warsmith_brief": { "mode": "enclenche", "categorie_hint": null, "intent": null },
    "tyrant_report": { "status": "pending" },
    "f01_sentinel": { "status": "pending", "output_path": null },
    "f02_breacher": { "status": "pending", "cible": null, "score": null, "angles_attaque": [] },
    "f03_forgeward": { "status": "pending", "ironwarriors_count": 0, "ironwarriors_paths": [] },
    "f04_herald": { "status": "pending", "listings_count": 0 },
    "f05_grand_compass": { "status": "pending", "blue_ocean_validated": null },
    "f06_capteurs": { "status": "idle" },
    "gate_decisions": { "gate_1": null, "gate_2": null, "gate_3": null, "gate_4": null },
    "iw_custos": { "last_validation": null, "errors": [] },
    "timestamp_start": null,
    "timestamp_end": null
  }
  ```

- [ ] `contracts_loader.py`
  - Adapter depuis `MONDES_FORGES/YOUTUBE/SHARED/` ou équivalent
  - Charge : system_prompt, tyrant_prompt, iron_prompt, anti_bullshit, api_scoring_checklist
  - Charge : `ARCHIVUM/rules/*.md` (couche froide)
  - Charge : `ARCHIVUM/targets/*.json` (couche chaude — si disponible)
  - Charge : signaux F06 CAPTEURS si disponibles

- [ ] `ai_gateway.py`
  - Routing modèles par frégate (voir IW_CAMPAIGN_LOG.md entrée [2026-07-14T00:06:00Z])
  - Variables : `AI_GATEWAY_BASE_URL`, `AI_GATEWAY_API_KEY`

---

## Phase 3 — TYRANT (À FAIRE)

Créer dans `MONDES_FORGES/API/TYRANT/CODEBASE/` :

- [ ] `tyrant.py`
  - Pattern : `--prepare` → iron_prompt.txt → IRON → eclairissement_api.json → `--finalize`
  - Référence : `MONDES_FORGES/YOUTUBE/TYRANT/CODEBASE/tyrant.py` (même structure exacte)
  - Adapter les 5 questions de vision pour le marché API (voir IW_CAMPAIGN_LOG.md)
  - Output validé : `eclairissement_api.json`

---

## Phase 4 — Frégates (À FAIRE)

### F01_SENTINEL

- [ ] `fregates/F01_SENTINEL/CODEBASE/sentinel.py`
  - **Pas d'appel IA** — collecte brute uniquement
  - Module `sentinel_rapid` : scrape RapidAPI listing (endpoint, pricing, latence, reviews, popularité)
  - Module `sentinel_gh` : GitHub API `search/code?q=[rapidapi_host]` — wrappers actifs, étoiles, issues
  - Module `sentinel_web` : Jina Reader `https://r.jina.ai/[URL]` pour docs et articles
  - Output : `raw_intel.json` dans `F01_SENTINEL/OUT/`

### F02_BREACHER

- [ ] `fregates/F02_BREACHER/CODEBASE/breacher.py`
  - Pattern : `--prepare` → iron_prompt.txt → IRON → scored_target.json → `--finalize`
  - Input : raw_intel.json + ARCHIVUM/rules/ (couche froide)
  - IRON calcule le score et génère les 20 angles d'attaque
  - Scoring : popularité×0.35 + latence×0.25 + wrappers×0.20 + frustration×0.20
  - Output : `scored_target.json` (cible, score, 20 angles avec variantes)

### F03_FORGEWARD

- [ ] `fregates/F03_FORGEWARD/CODEBASE/forgeward.py`
  - Pattern : `--prepare` → iron_prompt.txt × 20 → IRON (parallèle) → 20× dirs → `--finalize`
  - Input : scored_target.json + ARCHIVUM/templates/ (specs OpenAPI type, code FastAPI type)
  - Pour chaque Iron Warrior : `api.py` + `openapi.json` + `requirements.txt` + `deploy.sh`
  - Stack constante dans les IW : FastAPI + httpx — zéro dépendance payante
  - Output : `ironwarriors/[id]/` × 20 dans `F03_FORGEWARD/OUT/`

### F04_HERALD

- [ ] `fregates/F04_HERALD/CODEBASE/herald.py`
  - Pattern : `--prepare` → iron_prompt.txt → IRON → listings → `--finalize`
  - Input : ironwarriors/ (20 dirs depuis F03)
  - IRON génère pour chaque IW : `listing_rapidapi.md` + `README.md` (LLM-optimized avec openapi.json)
  - Validation : syntaxe Python valide + openapi.json bien formé
  - Output : `listings/[id]/` × 20 dans `F04_HERALD/OUT/`

### F05_GRAND_COMPASS

- [ ] `fregates/F05_GRAND_COMPASS/CODEBASE/grand_compass.py`
  - Pattern : `--prepare` → iron_prompt.txt → IRON → blue_ocean_report.json → `--finalize`
  - Input : scored_target.json + Tavily (recherche web marché adjacent)
  - IRON cartographie les marchés adjacents, valide le blue ocean
  - Output : `blue_ocean_report.json` → archivé dans `ARCHIVUM/markets/`

### F06_CAPTEURS

- [ ] `fregates/F06_CAPTEURS/CODEBASE/capteurs.py`
  - Surveillance quotidienne des Iron Warriors déployés
  - Surveille : abonnés RapidAPI, stars GitHub, nouveaux entrants catégorie
  - Alerte si variante >= 5 abonnés → pattern gagnant → `ARCHIVUM/rules/`
  - Mise à jour `ARCHIVUM/ledgers/` après chaque cycle de surveillance

---

## Phase 5 — Orchestrateur (À FAIRE)

- [ ] `ORCHESTRATOR/CODEBASE/orchestrator.py`
  - Adapter depuis `MONDES_FORGES/YOUTUBE/ORCHESTRATOR/CODEBASE/orchestrator.py`
  - Flux : [Gate 1] → TYRANT → F01 → F02 → [Gate 2] → F03+F05 (parallèle) → F04 → [Gate 3] → deploy → F06 → [Gate 4]
  - Commands : `start --mode enclenche`, `resume`, `gate --gate N --decision valide/rejete`, `status`

- [ ] `ORCHESTRATOR/CODEBASE/gates.py`
  - Adapter depuis `MONDES_FORGES/YOUTUBE/ORCHESTRATOR/CODEBASE/gates.py`

---

## Phase 6 — GitHub Actions CAPTEURS (À FAIRE)

- [ ] `.github/workflows/api_capteurs.yml`
  - Surveillance quotidienne : cron `0 7 * * *`
  - Lance `capteurs.py --daily-scan`
  - Commit automatique `ARCHIVUM/ledgers/` mis à jour

---

## Phase 7 — ARCHIVUM amorçage (À FAIRE)

Alimenter la couche froide avant le premier siège :

- [ ] `ARCHIVUM/docs/rapidapi_guide.md` — endpoints RapidAPI, méthodes scoring
- [ ] `ARCHIVUM/docs/fastapi_template.md` — patterns FastAPI micro-API
- [ ] `ARCHIVUM/docs/openapi_template.md` — structure openapi.json minimal valide
- [ ] `ARCHIVUM/templates/api_base.py` — template FastAPI 1 endpoint (copier-adapter)
- [ ] `ARCHIVUM/templates/openapi_base.json` — template OpenAPI minimal
- [ ] `ARCHIVUM/rules/market_rules.md` — règles initiales marché RapidAPI

---

## Phase 8 — Validation premier siège (OBJECTIF FINAL)

- [ ] `python orchestrator.py start --mode enclenche`
- [ ] Valider les 4 portes
- [ ] 20 Iron Warriors déployés en moins d'1h
- [ ] F06 CAPTEURS actifs
- [ ] `ARCHIVUM/ledgers/` mis à jour avec résultats du siège

---

## Règles pour l'agent de développement

1. Toujours partir du code YOUTUBE comme base — les patterns sont prouvés
2. `IW_CUSTOS.py` est le seul autorisé à modifier `liber_api.json` — règle absolue
3. F01 SENTINEL : aucun appel IA — collecte brute uniquement
4. Tous les appels IA passent par `ai_gateway.py` — jamais directs dans les frégates
5. F03 FORGEWARD produit les 20 Iron Warriors en parallèle (threads ou async)
6. `ARCHIVUM/templates/` doit exister avant le premier siège — pré-requis de FORGEWARD
7. Stack Iron Warriors : Python + FastAPI + httpx — zéro dépendance payante

---

*Dernière mise à jour : 2026-07-14*
*Statut global : Phase 0 terminée — Phase 1 à démarrer*
