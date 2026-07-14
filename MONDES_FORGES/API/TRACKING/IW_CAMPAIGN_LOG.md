# IW_CAMPAIGN_LOG — Monde-Forge API

## Journal de construction — à lire en premier si contexte perdu

---

## [CONSTRUCTION] Session fondatrice — Doctrine complète

### Contexte projet

PERTURABO est un système de production automatisé organisé en flotte de frégates.
Structure : CORE/ + MONDES_FORGES/ (YOUTUBE existant + API en construction).
Chaque Monde-Forge est autonome : son liber, son ARCHIVUM, ses frégates, ses CONTRACTS.

### Doctrine du Monde-Forge API

**Objectif** : identifier une catégorie d'API RapidAPI faible, produire 20 variantes concurrentes (Iron Warriors) en moins d'1 heure, les déployer simultanément.

**Input Warsmith** : "enclenche" → le système trouve la cible seul.

**Règles absolues** :
- 1 catégorie ciblée, 20 Iron Warriors simultanés (pas 20 catégories, 1 API)
- Stack 100% gratuit : FastAPI + httpx + Railway/Render tier gratuit
- Latence Iron Warrior < 500ms (arme principale contre les leaders lents)
- Marge nette : 75% après commission RapidAPI (25%)

**Référence cash flow** : ~500$/mois à partir du mois 4-5.

### FLEET_STATUS_FLOW

```
pending_reconnaissance → tyrant_report_ready → intel_captured → target_scored
→ ironwarriors_forged → listings_ready → market_mapped → deployed → complete
```

### Architecture des frégates

| Frégate | Rôle | Modèle |
|---|---|---|
| TYRANT | Analyse territoire, identifie démon et faille | claude-sonnet-4.6 |
| F01 SENTINEL | Scraping multi-source (RapidAPI + GitHub + web) | claude-haiku-4.5 |
| F02 BREACHER | Scoring cible + génération 20 angles d'attaque | deepseek-v4-flash |
| F03 FORGEWARD | Production 20 × (api.py + openapi.json + deploy.sh) | claude-sonnet-4.6 |
| F04 HERALD | Production 20 × (listing RapidAPI + README GitHub) | gemini-3.5-flash |
| F05 GRAND COMPASS | Validation blue ocean + déploiement Railway/Render | claude-sonnet-4.6 |
| F06 CAPTEURS | Monitoring post-siège, update ARCHIVUM/ledgers/ | claude-haiku-4.5 |

### Les 4 Gates (validation Warsmith)

- **Gate 1** : après TYRANT — valider la cible (30 secondes)
- **Gate 2** : après F01 SENTINEL — valider les 20 angles BREACHER (2 minutes)
- **Gate 3** : après F03 FORGEWARD — review code Iron Warriors (5 minutes)
- **Gate 4** : après F04 HERALD — valider listings avant publication (5 minutes)

### ARCHIVUM deux couches

Froide : rules/, templates/, markets/, docs/
Chaude : targets/, github/, ledgers/

### IA spécialisées

Jina Reader, Firecrawl, Tavily, GitHub API — tous gratuits

---

## [CONSTRUCTION] Phase 0 — Structure créée

Dossiers ARCHIVUM, CONTRACTS, TYRANT, ORCHESTRATOR, frégates F01-F06.

---

## [CONSTRUCTION] Phase 1 — CONTRACTS créés

system_prompt.md, tyrant_prompt.md, iron_prompt.md, anti_bullshit.md, api_scoring_checklist.json

---

## [CONSTRUCTION] Phase 2 — liber_api.json + IW_CUSTOS.py

liber_api.json : 9 fleet_status, 5 dimensions TYRANT, f01-f06 complets, 4 gates, timestamps.
IW_CUSTOS.py : 6 modes (reset/check-out/check-in/gate/validate/status).

---

## [CONSTRUCTION] Phase 3 — ai_gateway.py

**Fichier** : `CORE/ai_gateway.py` — partagé entre tous les Mondes-Forges.

**Différence clé avec YOUTUBE** : le YOUTUBE Monde-Forge utilise un IRON manuel (iron_prompt.txt 
lu par Claude en conversation). Le API Monde-Forge est **automatisé** — chaque frégate appelle 
`call_oracle()` directement, pas d'étape manuelle.

**Fonctions** :
- `call_oracle(frigate_id, prompt, ...)` — appel unique avec retry (max 3)
  - Retry avec contexte d'erreur injecté si JSON invalide
  - Extraction JSON robuste : pur / markdown / extraction heuristique
- `call_oracle_batch(frigate_id, prompts, max_workers=5)` — parallèle
  - Conçu pour F03 : 20 prompts → 20 api.py en simultané
  - max_workers=5 par défaut (évite rate limiting)
- `ping()` — test connectivité
- CLI direct : `python ai_gateway.py --ping`

**Routing modèles** :
- F02 → deepseek-v4-flash (analytique + économique pour le scoring)
- F03/F05/TYRANT → claude-sonnet-4.6 (raisonnement + code)
- F04/F06 → gemini-3.5-flash / haiku (volume + vitesse)

**Fichiers ajoutés dans CORE/** :
- `requirements.txt` : openai, httpx, pydantic, fastapi, uvicorn
- `.env.example` : AI_GATEWAY_BASE_URL, AI_GATEWAY_API_KEY, GITHUB_TOKEN, RAPIDAPI_KEY, RAILWAY_TOKEN

---

## Prochaine étape

**Phase 4** : TYRANT — premier vrai cerveau du système.
Lit l'ARCHIVUM, appelle call_oracle("TYRANT"), produit le JSON d'assessment pour Gate 1.
