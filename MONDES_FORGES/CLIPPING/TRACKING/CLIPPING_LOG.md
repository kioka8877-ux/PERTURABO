# TRACKING/CLIPPING_LOG — Monde Forge CLIPPING

> *Journal général de déploiement du forge. Une entrée par jalon.*
> *Pour le détail par frégate, voir `<FREGATE>/TRACKING/<XX>_LOG.md`.*

---

## [INIT] Monde Forge CLIPPING déployé — Arborescence + docs tracking

### Contexte
Le forge CLIPPING est le 3e Monde Forge de PERTURABO, après `API/` (générique) et `YOUTUBE/` (spécialisé shorts YouTube). Il se concentre sur le **clipping Whop Content Rewards** : produire les **stratégies + textes** (pas les vidéos) consommées par OMNIS_WATCH (projet externe, branche `dev1`).

### Arborescence créée
```
MONDES_FORGES/CLIPPING/
├── README.md                  ← vue d'ensemble du forge
├── CONTRACTS/                 ← see CONTRACTS/INDEX.md
├── ARCHIVUM/                  ← 10 zones (rules, campaign, platform_gen,
│                                 market_gen, knowledge_base, copywriting,
│                                 angles, demons, channels, learnings,
│                                 ledgers, templates)
├── SHARED/                    ← IN/ + OUT/ partagés
├── F01_SCOUT/                 ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── F02_TYRANT_CAMP/           ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── F03_SOURCE_HUNTER/         ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── F04_COPYWRITER/            ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── F05_PACKAGER/              ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── F06_TRACKER/               ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── TYRANT/                    ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── CAPTEURS/                  ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── ORCHESTRATOR/              ← CODEBASE/ + IN/ + OUT/ + TRACKING/
├── TRACKING/                  ← ce dossier
└── MANIFEST.md                ← manifeste de livraison (fichiers + statuts)
```

### Conventions alignées sur YOUTUBE/
Chaque frégate suit la structure `CODEBASE/` (code Python — pas rempli pour l'instant), `IN/` (inputs), `OUT/` (artefacts produits), `TRACKING/` (journal de déploiement). Voir `MONDES_FORGES/YOUTUBE/` pour la référence.

### Statut des composants

| Composant | Arborescence | Docs Tracking | Code Python | Notes |
|---|---|---|---|---|
| F01_SCOUT | ✅ | ✅ | ❌ | À implémenter par autre model |
| F02_TYRANT_CAMP | ✅ | ✅ | ❌ | À implémenter |
| F03_SOURCE_HUNTER | ✅ | ✅ | ❌ | À implémenter |
| F04_COPYWRITER | ✅ | ✅ | ❌ | Frégate lourde — pattern 4 phases distinct |
| F05_PACKAGER | ✅ | ✅ | ❌ | À implémenter |
| F06_TRACKER | ✅ | ✅ | ❌ | À implémenter |
| TYRANT | ✅ | ✅ | ❌ | 2 modes (réactif + prospectif) |
| CAPTEURS | ✅ | ✅ | ❌ | Commandité Warsmith, pas auto |
| ORCHESTRATOR | ✅ | ✅ | ❌ | 4 Portes, pattern hybride |
| CONTRACTS | ✅ | ✅ (squelettes) | n/a | copywriting_doctrine à remplir par le Warsmith |
| ARCHIVUM (10 zones) | ✅ | ✅ (squelettes) | n/a | Contenu secret à remplir par le Warsmith |

### Prochaines étapes
1. Le Warsmith remplit `CONTRACTS/copywriting_doctrine.md` (son savoir secret — slang, subliminal, formulas)
2. Le Warsmith peuple `ARCHIVUM/copywriting/` (8 sous-dossiers) avec son musée
3. Un autre model implémente le code Python des frégates en suivant religieusement chaque `TRACKING.md`
4. Le Warsmith révoque le token GitHub exposé (cf. note sécurité)

### Note sécurité
⚠️ Un token GitHub a été partagé en clair pendant la session. **Il doit être révoqué** immédiatement après cette session — il est publiquement compromis. Ce token a été utilisé **temporairement** pour cloner/pusher le forge. Ne pas réutiliser.

---

## [DEV-ORCHESTRATOR] Nerf central implémenté — ORCHESTRATOR + IW_CUSTOS

### Contexte
Première vague de code Python du forge CLIPPING. Le nerf central est en place : le ledger (`liber_clipping.json`), le gardien (`IW_CUSTOS.py`) et l'Orchestrateur (4 Portes).

### Fichiers livrés
```
CLIPPING/
├── IW_CUSTOS.py                    ← gardien du ledger (check-out/check-in/validate/status)
├── liber_clipping.json             ← état inter-frégates (singulier, 1 siège actif max)
└── ORCHESTRATOR/CODEBASE/
    ├── orchestrator.py             ← CLI : --start-siege / --gate N / --resume / --status / --close-siege
    ├── gates.py                    ← les 4 Portes (verdict, angles, textes, packs)
    ├── requirements_orchestrator.txt
    └── libs/
        ├── ledger_manager.py       ← CRUD liber_clipping.json + délégation IW_CUSTOS
        ├── siege_initializer.py    ← validation des 4 inputs Warsmith (campaign/ singulier)
        ├── gate_validator.py       ← vérifie les artefacts attendus avant validation de porte
        └── omnis_watch_distributor.py ← génère packs_index.json + raw URLs OMNIS_WATCH
```

### Décisions d'implémentation
- `gate_validator` refuse la validation d'une porte si les artefacts attendus sont absents (hérésie « passer une porte sans validation » impossible).
- Le `--close-siege` est la seule voie de fermeture (seul le Warsmith déclare la fin).
- F04 reste autonome : l'Orchestrateur ne pilote pas le dialogue premium direct (statut F04 = done via son propre check-in).
- `gates.py` est calqué sur le pattern `YOUTUBE/ORCHESTRATOR/CODEBASE/gates.py` (réutilisation ~70%).

### Statut des composants

| Composant | Docs Tracking | Code Python | Notes |
|---|---|---|---|
| ORCHESTRATOR | ✅ | ✅ (v1) | 4 Portes, pattern hybride, ledger |
| IW_CUSTOS | ✅ (racine) | ✅ (v1) | Gardien liber_clipping.json |
| F01_F06 + TYRANT + CAPTEURS + ANGLESMITH | ✅ | ❌ | Prochaines vagues |

### Prochaines étapes
1. Implémenter F01_SCOUT (vague 2)
2. Implémenter F02_TYRANT_CAMP + TYRANT (vague 3)
3. Implémenter ANGLESMITH + F03_SOURCE_HUNTER + F04_COPYWRITER + F05_PACKAGER + F06_TRACKER + CAPTEURS
4. Premier siège réel avec les inputs du Warsmith

---

## Portes — mapping des jalons futurs

| Porte | Jalon attendu | Statut |
|---|---|---|
| Avant Porte 1 | CAPTEURS scrap écosystème + niche | Non démarré |
| Porte 1 | F02_TYRANT_CAMP verdict campagne | Non démarré |
| Porte 2 | ANGLESMITH N angles forgés | Non démarré |
| Porte 3 | F03 + F04 text_payloads prêts | Non démarré |
| Porte 4 | F05 production packs expédiés → OMNIS_WATCH | Non démarré |

*Fer au-dedans, Fer au-dehors.*
