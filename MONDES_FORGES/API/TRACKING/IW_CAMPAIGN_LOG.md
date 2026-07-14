# IW_CAMPAIGN_LOG — Journal de Campagne MONDE-FORGE API

> Log chronologique de toutes les activations de frégates, validations, erreurs et événements majeurs.
> Géré automatiquement par `IW_CUSTOS.py`. Ne pas modifier manuellement.
> Exception : les entrées `[CONSTRUCTION]` sont des entrées manuelles documentant la phase de création.

---

## Format d'entrée

```
## [TIMESTAMP ISO 8601] FRÉGATE — ÉVÉNEMENT
- Détail 1
- IW_CUSTOS validation: PASS / FAIL
```

---

## [2026-07-14T00:00:00Z] CONSTRUCTION — DOCTRINE : Architecture Monde-Forge API [MANUEL]

### Contexte
PERTURABO est restructuré en moteur universel de siège à Mondes-Forges autonomes.
Le Monde-Forge API est le deuxième monde après YOUTUBE.
Doctrine établie lors d'une session de brainstorming exhaustive.

### Architecture globale
```
PERTURABO/
├── CORE/                    ← moteur universel (IW_CUSTOS.py, ai_gateway.py)
└── MONDES_FORGES/
    ├── YOUTUBE/             ← monde existant (migré)
    └── API/                 ← ce monde
```

### Input Warsmith
- Mot-clé : **"enclenche"**
- Le Warsmith ne choisit pas la cible. TYRANT identifie seul via les données.
- Gates = seuls moments d'intervention humaine (30 sec à 5 min chacune)

### Objectif de production
- 1h maximum entre "enclenche" et déploiement des Iron Warriors
- 20 variantes simultanées par siège (Iron Warriors)
- Doctrine Shahed : 20 APIs sur UNE seule cible précise — pas de dispersion
- Cash flow pur : APIs simples mais qui vendent — pas d'oeuvre d'art

### Oracle et IA spécialisées
- Oracle = Claude Sonnet via AI Gateway (sandbox) — tout le raisonnement lourd
- IA spécialisées (capteurs uniquement — pas de raisonnement) :
  - Jina Reader (`https://r.jina.ai/[URL]`) : scrape propre, aucune clé requise
  - Firecrawl : 500 pages/mois gratuit, contournement protections avancées
  - Tavily : 1000 recherches/mois gratuit, veille marché structurée
  - GitHub API : 5000 req/heure avec token, mapping wrappers actifs
  - PyPI/npm stats : volume téléchargements wrappers (proxy usage agents)

---

## [2026-07-14T00:01:00Z] CONSTRUCTION — ARCHIVUM : Structure Couche Froide / Chaude [MANUEL]

### Couche FROIDE (rarement mise à jour — doctrine accumulée siège après siège)
- `rules/` — patterns distillés : ce qui vend, ce qui meurt, pourquoi
- `templates/` — 20 specs OpenAPI prêtes + code FastAPI types réutilisables
- `markets/` — cartographie scorée des catégories RapidAPI
- `docs/` — documentation RapidAPI, FastAPI, OpenAPI (scrape stable)

### Couche CHAUDE (scrapée à chaque siège — renseignement frais)
- `targets/` — fiches cibles : endpoints, pricing, latence, reviews
- `github/` — wrappers actifs, issues, étoiles (GitHub API live)
- `ledgers/` — survie/mort de chaque Iron Warrior lancé (F06 CAPTEURS)

### Principe d'injection dans les prompts
`contracts_loader.py` injecte les deux couches dans chaque prompt IRON.
La couche froide donne la doctrine. La chaude donne l'intelligence du siège en cours.
Même pattern que `contracts_loader.py` du Monde-Forge YOUTUBE.

---

## [2026-07-14T00:02:00Z] CONSTRUCTION — FLEET_STATUS_FLOW et FRÉGATES [MANUEL]

### FLEET_STATUS_FLOW
```python
[
    "pending_reconnaissance",
    "tyrant_report_ready",     # TYRANT a éclairé le marché
    "intel_captured",          # F01 SENTINEL a capturé les données brutes
    "target_scored",           # F02 BREACHER a scoré + 20 angles identifiés
    "ironwarriors_forged",     # F03 FORGEWARD a produit les 20 variantes
    "listings_ready",          # F04 HERALD a préparé les 20 listings RapidAPI
    "market_mapped",           # F05 GRAND COMPASS a validé le blue ocean
    "deployed",                # F06 CAPTEURS activés, Iron Warriors en ligne
    "complete",
]
```

### Les 6 frégates + TYRANT

| Composant | Rôle | Input | Output |
|-----------|------|-------|--------|
| TYRANT | Oracle pré-siège | brief.json | eclairissement_api.json |
| F01 SENTINEL | Renseignement multi-source | catégorie RapidAPI | raw_intel.json |
| F02 BREACHER | Scoring + 20 angles | raw_intel.json + ARCHIVUM | scored_target.json |
| F03 FORGEWARD | Production 20 Iron Warriors | scored_target.json + templates | 20× api.py + openapi.json |
| F04 HERALD | Listings RapidAPI + README | ironwarriors/ | 20× listing_rapidapi.md + README.md |
| F05 GRAND COMPASS | Validation blue ocean | scored_target.json + web | blue_ocean_report.json |
| F06 CAPTEURS | Surveillance post-déploiement | deployed_urls.json | alerts + ledgers update |

### Scoring F02 BREACHER
```
Score = popularité_RapidAPI × 0.35
      + latence_élevée (faille exploitable) × 0.25
      + wrappers_GitHub_actifs × 0.20
      + frustration_pricing_dans_reviews × 0.20
```

---

## [2026-07-14T00:03:00Z] CONSTRUCTION — CONTRACTS : Contenu défini [MANUEL]

### Fichiers CONTRACTS/

| Fichier | Rôle | Source |
|---------|------|--------|
| `system_prompt.md` | Doctrine API — marché RapidAPI, Iron Warriors, production volume | À écrire |
| `tyrant_prompt.md` | 5 questions Oracle : territoire/démon/latence/wrappers/pricing | À écrire |
| `iron_prompt.md` | Contrat Exécuteur — produit, ne décide pas | Adapter YOUTUBE |
| `anti_bullshit.md` | Filtre patterns non prouvés | Copier YOUTUBE (identique) |
| `api_scoring_checklist.json` | Grille scoring : popularité/latence/wrappers/frustration | À écrire |

### TYRANT — 5 questions de vision adaptées API
1. **Le Territoire** : quelle catégorie RapidAPI, taille, volume d'agents utilisateurs
2. **Le Démon** : API leader, pricing actuel, latence mesurée, vulnérabilités visibles
3. **La Faille** : latence élevée ? pricing frustrant dans reviews ? support absent ? doc inexistante ?
4. **Les 20 angles** : variantes de prix, endpoint, niche, format output, audience cible
5. **Le Chemin** : attaque directe (mêmes clients que le leader) ou ocean bleu (nouveau segment)

---

## [2026-07-14T00:04:00Z] CONSTRUCTION — LES 4 PORTES DE SIÈGE API [MANUEL]

| Porte | Moment | Le Warsmith valide | Durée cible |
|-------|--------|--------------------|-------------|
| Porte 1 | Après TYRANT | La cible identifiée : catégorie + API leader + faille principale | 30 secondes |
| Porte 2 | Après F02 BREACHER | Les 20 angles d'attaque — cohérence et couverture | 2 minutes |
| Porte 3 | Après F03+F04 | Review rapide 2-3 Iron Warriors : code + listing RapidAPI | 5 minutes |
| Porte 4 | Après déploiement | Confirmation 20 Iron Warriors live sur RapidAPI + GitHub | 30 secondes |

---

## [2026-07-14T00:05:00Z] CONSTRUCTION — liber_api.json : Structure définie [MANUEL]

Structure complète définie (voir DEV_ROADMAP.md Phase 2 pour le JSON).
Fleet_status initial : "idle"
Chemin : `MONDES_FORGES/API/liber_api.json`

---

## [2026-07-14T00:06:00Z] CONSTRUCTION — ROUTING IA par frégate [MANUEL]

| Frégate | Modèle | Raison |
|---------|--------|--------|
| TYRANT | `anthropic/claude-sonnet-4.6` | Raisonnement stratégique profond |
| F01 SENTINEL | Aucun | Collecte brute — pas d'IA |
| F02 BREACHER | `deepseek/deepseek-v4-flash` | Scoring + patterns — rapide et économique |
| F03 FORGEWARD | `anthropic/claude-sonnet-4.6` | Génération code FastAPI × 20 |
| F04 HERALD | `google/gemini-3.5-flash` | Rédaction listings + README |
| F05 GRAND COMPASS | `anthropic/claude-sonnet-4.6` | Analyse blue ocean |
| F06 CAPTEURS | `anthropic/claude-haiku-4.5` | Surveillance légère |

Variables : `AI_GATEWAY_BASE_URL`, `AI_GATEWAY_API_KEY`
Tous les appels passent par `ai_gateway.py` — jamais directs dans les frégates.

---

## Historique des opérations de production

*(Généré automatiquement par IW_CUSTOS.py lors des sièges)*
