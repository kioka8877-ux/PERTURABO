# DEV_ROADMAP — Monde-Forge API

## Statut global : Phase 3 complète — Phase 4 à démarrer

---

## Phase 0 — Structure et tracking ✅
- [x] Créer MONDES_FORGES/API/ avec toutes les sous-structures
- [x] Tracking docs, logs par frégate, dossiers TYRANT et ORCHESTRATOR

## Phase 1 — CONTRACTS ✅
- [x] system_prompt.md, tyrant_prompt.md, iron_prompt.md, anti_bullshit.md, api_scoring_checklist.json

## Phase 2 — liber_api.json + IW_CUSTOS.py ✅
- [x] liber_api.json : 9 fleet_status, tyrant_report 5 dimensions, f01-f06, 4 gates, siege_timestamps
- [x] IW_CUSTOS.py : 6 modes (reset/check-out/check-in/gate/validate/status)

---

## Phase 3 — ai_gateway.py ✅

- [x] `CORE/ai_gateway.py` créé — routeur Oracle partagé entre tous les Mondes-Forges
  - Routing modèles par frégate : F01→Haiku, F02→DeepSeek Flash, F03/F05→Sonnet, F04→Gemini Flash, F06→Haiku
  - `call_oracle(frigate_id, prompt, ...)` → JSON validé avec retry (max 3)
  - `call_oracle_batch(frigate_id, prompts, max_workers=5)` → 20 Iron Warriors en parallèle
  - `ping()` → test de connectivité
  - Gestion des formats : JSON pur, ```json...```, extraction depuis texte
  - Retry avec contexte d'erreur injecté dans le message suivant
  - CLI : `python ai_gateway.py --ping` / `--frigate F02 --prompt "..."`
- [x] `CORE/requirements.txt` mis à jour (openai, httpx, pydantic, fastapi, uvicorn)
- [x] `CORE/.env.example` créé (AI_GATEWAY_BASE_URL, AI_GATEWAY_API_KEY, GITHUB_TOKEN, RAPIDAPI_KEY, RAILWAY_TOKEN)

---

## Phase 4 — TYRANT ⬜

- [ ] `TYRANT/CODEBASE/tyrant.py`
  - `--prepare` : charge ARCHIVUM couches froide + chaude, assemble le prompt
  - Appelle `call_oracle("TYRANT", prompt)` via ai_gateway
  - `--finalize` : valide JSON tyrant_output, check-in IW_CUSTOS, affiche fiche Gate 1
- [ ] `TYRANT/CODEBASE/contracts_loader.py` — charge CONTRACTS/ + ARCHIVUM/rules/ + ARCHIVUM/markets/
- [ ] `TYRANT/IN/` — structure des fichiers d'entrée (warsmith_brief.json)
- [ ] `TYRANT/OUT/tyrant_output.json` — structure du fichier de sortie

---

## Phase 5 — F01 SENTINEL ⬜

- [ ] `F01_SENTINEL/CODEBASE/sentinel.py`
  - Module `sentinel_rapid` : scrape RapidAPI listings (score, latence, pricing, reviews)
  - Module `sentinel_gh` : GitHub API — wrappers actifs, issues, stars
  - Module `sentinel_web` : Jina Reader (`https://r.jina.ai/[URL]`) pour docs et articles
  - Appelle `call_oracle("F01", ...)` pour structurer les données brutes
  - Output : `ARCHIVUM/targets/[siege_id]/raw_intel.json`

---

## Phase 6 — F02 BREACHER ⬜

- [ ] `F02_BREACHER/CODEBASE/breacher.py`
  - Lit `raw_intel.json` + ARCHIVUM/rules/ (couche froide)
  - Calcule score 4 dimensions (api_scoring_checklist.json)
  - Génère 20 angles d'attaque
  - Appelle `call_oracle("F02", ...)` via DeepSeek Flash

---

## Phase 7 — F03 FORGEWARD ⬜

- [ ] `F03_FORGEWARD/CODEBASE/forgeward.py`
  - Lit les 20 angles depuis le liber
  - Appelle `call_oracle_batch("F03", 20_prompts, max_workers=5)` → 20 × FastAPI code
  - Output : `ARCHIVUM/targets/[siege_id]/ironwarriors/[id]/` × 20

---

## Phase 8 — F04 HERALD + F05 GRAND COMPASS + F06 CAPTEURS ⬜

- [ ] F04 HERALD : listings RapidAPI + README GitHub (call_oracle_batch "F04")
- [ ] F05 GRAND COMPASS : blue ocean + déploiement Railway/Render
- [ ] F06 CAPTEURS : monitoring post-siège, update ARCHIVUM/ledgers/

---

## Phase 9 — ORCHESTRATOR + test siège complet ⬜

- [ ] orchestrator.py — orchestration semi-manuelle des 4 Gates
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
