# IW_CAMPAIGN_LOG — Monde-Forge API

## Journal de construction — à lire en premier si contexte perdu

Ce fichier permet à tout agent arrivant à froid de reconstituer le contexte en 5 minutes.

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

**Référence cash flow** : ~500$/mois à partir du mois 4-5 avec ~20 Iron Warriors survivants cumulés.

### FLEET_STATUS_FLOW

```
pending_reconnaissance → tyrant_report_ready → intel_captured → target_scored
→ ironwarriors_forged → listings_ready → market_mapped → deployed → complete
```

### Architecture des frégates

| Frégate | Rôle | Moteur |
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
- **Gate 2** : après BREACHER — valider les 20 angles (2 minutes)
- **Gate 3** : après FORGEWARD — review 2-3 Iron Warriors (5 minutes)
- **Gate 4** : après HERALD — valider les listings avant publication (5 minutes)

### ARCHIVUM à deux couches

**Couche froide** (rarement mise à jour — doctrine accumulée) :
- `rules/` — patterns distillés des sieges passés
- `templates/` — specs OpenAPI + code FastAPI réutilisables
- `markets/` — cartographie scorée des catégories RapidAPI
- `docs/` — documentation RapidAPI, FastAPI, OpenAPI

**Couche chaude** (scrapée à chaque siège) :
- `targets/` — fiches cibles : endpoints, pricing, latence, reviews
- `github/` — wrappers actifs, issues, étoiles
- `ledgers/` — survie/mort de chaque Iron Warrior lancé

### IA spécialisées (hors Oracle)

| Outil | Usage | Coût |
|---|---|---|
| Jina Reader | Scrape pages en Markdown | Gratuit |
| Firecrawl | Scrape pages protégées | 500 pages/mois gratuit |
| Tavily | Veille marché structurée | 1000 req/mois gratuit |
| GitHub API | Wrappers actifs, signal agents | Gratuit (5000 req/h) |

---

## [CONSTRUCTION] Phase 0 — Structure créée

Dossiers : ARCHIVUM (targets, docs, github, articles, rules, templates, markets, ledgers),
CONTRACTS, TYRANT (IN/OUT/CODEBASE), ORCHESTRATOR (IN/OUT/CODEBASE),
fregates F01-F06 (IN/OUT/CODEBASE/TRACKING).

---

## [CONSTRUCTION] Phase 1 — CONTRACTS créés

5 fichiers dans CONTRACTS/ :
- `system_prompt.md` : doctrine RapidAPI + Iron Warriors + stack technique
- `tyrant_prompt.md` : 5 questions (territoire, démon, faille, signal agents, cartographie prix) + format JSON
- `iron_prompt.md` : contrat de l'exécuteur (JSON brut, schéma exact, code fonctionnel)
- `anti_bullshit.md` : 4 filtres (source obligatoire, chiffres prouvés, patterns ARCHIVUM, seuils TYRANT)
- `api_scoring_checklist.json` : 4 dimensions pondérées, 20 types d'angles d'attaque, seuils SIEGEZ/ATTENDEZ/REORIENTEZ

---

## Prochaine étape

**Phase 2** : liber_api.json + IW_CUSTOS.py
Voir DEV_ROADMAP.md pour le détail.
