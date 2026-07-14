# DEV_ROADMAP — Monde-Forge API

## Statut global : Phase 4 complète — Phase 5 à démarrer

---

## Phase 0 — Structure et tracking ✅
## Phase 1 — CONTRACTS ✅
## Phase 2 — liber_api.json + IW_CUSTOS.py ✅
## Phase 3 — ai_gateway.py ✅

---

## Phase 4 — TYRANT ✅

- [x] `TYRANT/CODEBASE/contracts_loader.py`
  - Charge CONTRACTS/ (system_prompt, tyrant_prompt, anti_bullshit, api_scoring_checklist)
  - Charge ARCHIVUM/rules/ (couche froide — patterns distillés)
  - Charge ARCHIVUM/markets/ (cartographie RapidAPI — vide au premier siège)
  - Charge ARCHIVUM/ledgers/ (résultats des sieges passés — vide au premier siège)
  - Charge warsmith_brief depuis liber_api.json
- [x] `TYRANT/CODEBASE/tyrant.py`
  - `python tyrant.py` : exécution complète (load → oracle → validate → liber → check-in → Gate 1 fiche)
  - `python tyrant.py --finalize --from-file path` : re-valider un output existant
  - `python tyrant.py --status` : état courant
  - Appelle `call_oracle("TYRANT", prompt)` via ai_gateway.py — pas de IRON manuel
  - Sauvegarde `iron_prompt.txt` pour audit
  - Valide le JSON (champs obligatoires, recommandation SIEGEZ/ATTENDEZ/REORIENTEZ, score 0-100)
  - Met à jour `liber_api.json → tyrant_report` après validation
  - Affiche la fiche Gate 1 avec tableau de bord complet
- [x] `TYRANT/IN/warsmith_brief.example.json` — template du brief Warsmith

---

## Phase 5 — F01 SENTINEL ⬜

- [ ] `F01_SENTINEL/CODEBASE/sentinel.py`
  - `--mode scrape --categorie "..."` : scrape la catégorie cible
  - Module `sentinel_rapid` : scrape RapidAPI listings (score, latence, pricing, reviews)
    - Source : Jina Reader (`https://r.jina.ai/https://rapidapi.com/category/[cat]`)
    - Output : liste d'APIs avec endpoints, pricing, latence, reviews
  - Module `sentinel_gh` : GitHub API — `search/code?q=[rapidapi_host]`
    - Compte repos qui importent l'API → signal adoption agents
    - Lit les issues ouvertes → signal frustration
  - Module `sentinel_web` : Jina Reader pour docs et articles (dev.to, medium)
  - Appelle `call_oracle("F01", ...)` pour structurer les données brutes en JSON propre
  - Output : `ARCHIVUM/targets/[siege_id]/raw_intel.json`
  - Check-in IW_CUSTOS automatique

---

## Phase 6 — F02 BREACHER ⬜

- [ ] `F02_BREACHER/CODEBASE/breacher.py`
  - Lit `raw_intel.json` + ARCHIVUM/rules/ (couche froide)
  - Applique `api_scoring_checklist.json` : calcule score 4 dimensions
  - Génère 20 angles d'attaque depuis les types définis dans la checklist
  - Appelle `call_oracle("F02", ...)` via DeepSeek Flash
  - Output : mise à jour liber f02 + `angles_attaque.json`

---

## Phase 7 — F03 FORGEWARD ⬜

- [ ] `F03_FORGEWARD/CODEBASE/forgeward.py`
  - Lit les 20 angles depuis le liber
  - Pour chaque angle : génère api.py + openapi.json + requirements.txt + deploy.sh
  - `call_oracle_batch("F03", 20_prompts, max_workers=5)` → 20 × FastAPI code en parallèle
  - Output : `ARCHIVUM/targets/[siege_id]/ironwarriors/[id]/` × 20

---

## Phase 8 — F04 HERALD + F05 GRAND COMPASS + F06 CAPTEURS ⬜

- [ ] F04 HERALD : listings RapidAPI + README GitHub
- [ ] F05 GRAND COMPASS : validation blue ocean + déploiement Railway/Render
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
