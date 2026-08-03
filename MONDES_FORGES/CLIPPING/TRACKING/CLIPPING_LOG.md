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

## [DEV-F01] F01_SCOUT implémentée — Reconnaissance de fer

### Contexte
Deuxième vague de code : la frégate d'acquisition est opérationnelle. Elle inventorie les assets de la campagne (strict-source, règle C1) et produit le `source_specimen.json` consommé par F02_TYRANT_CAMP (Porte 1) et F03_SOURCE_HUNTER (Porte 3).

### Fichiers livrés
```
F01_SCOUT/CODEBASE/
├── scout.py                  ← wrapper 3 phases (--prepare / --auto / --finalize)
├── requirements_c01.txt
└── libs/
    ├── recon.py              ← parse directive.md (section assets, campaign_id, types)
    ├── enrich.py             ← yt-dlp --dump-json + outlier_score (mode dry si absent)
    └── scribe.py             ← transcription (youtube-transcript-api → yt-dlp → dry)
```

### Décisions d'implémentation
- Mode `--prepare` : génère `IN/scout_prompt.json` pour l'IRON + pré-remplit le specimen.
- Mode `--auto` : analyse locale sans IRON (enrichissement + transcription optionnelle) — les assets restent strictement ceux de `directive.md`.
- Mode `--finalize` : valide cohérence (campaign_id, assets non vides, URLs valides), génère `scout_report.md`, check-in IW_CUSTOS (statut F01 = done).
- `outlier_score = view_count / baseline` calculé dans enrich (aucun chiffre inventé).

### Statut des composants

| Composant | Docs Tracking | Code Python | Notes |
|---|---|---|---|
| ORCHESTRATOR | ✅ | ✅ (v1) | |
| F01_SCOUT | ✅ | ✅ (v1) | recon/enrich/scribe + scout.py |
| F02_F06 + TYRANT + CAPTEURS + ANGLESMITH | ✅ | ❌ | Vagues suivantes |

### Prochaines étapes
1. Implémenter F02_TYRANT_CAMP + TYRANT (vague 3)
2. Implémenter ANGLESMITH (vague 4)
3. Implémenter F03_F06 + CAPTEURS

---

## [DEV-F02-TYRANT] F02_TYRANT_CAMP + TYRANT implémentées — Verdict & Oracle

### Contexte
Troisième vague de code : la Porte 1 est couverte côté stratégie. F02_TYRANT_CAMP (mode réactif) rend le verdict GO/NO-GO + océan bleu pour chaque campagne ; TYRANT (mode prospectif) veille les Démons du wild clipping et nourrit `ARCHIVUM/demons/`.

### Fichiers livrés
```
F02_TYRANT_CAMP/CODEBASE/
├── tyrant_camp.py                ← wrapper 3 phases (--prepare / --auto / --finalize)
├── requirements_c02.txt
└── libs/
    ├── skeleton_extractor.py     ← pré-squelette viral du clip ref (l'IRON affine)
    ├── blue_ocean_finder.py      ← océans bleus depuis ARCHIVUM/demons/ + saturation low/medium eligible
    └── fit_scorer.py             ← score fit plateforme x marche x niche (0-10, aucun chiffre invente)

TYRANT/CODEBASE/
├── tyrant.py                     ← wrapper 3 phases (--prepare / --auto / --finalize)
├── requirements_tyrant.txt       ← yt-dlp + youtube-transcript-api (Warsmith/IRON)
└── libs/
    ├── outlier_scorer.py         ← outlier_score = views / baseline, seuil > 3x par defaut
    ├── emotion_classifier.py     ← emotion dominante (drame/joie/outrage/...) depuis titre/transcript
    ├── blue_ocean_mapper.py      ← territoires adjacents 1 couche max (clamp profondeur = heresie guard)
    └── demon_archivist.py        ← ecrit ARCHIVUM/demons/<demon_id>.json
```

### Decisions d'implementation
- Heresie guard au finalize : toute profondeur d'ocean bleu != 1 est clampee (jamais 2 couches).
- Aucun Demon sans preuve quantitative : outlier_score calcule strictement (views / baseline), jamais invente.
- F02 --auto : verdict GO si assets presents dans le specimen, sinon NO-GO (strict-source).
- Les deux frégates font leur check-in IW_CUSTOS (statuts `tyrant_done` / `verdict_ready` via preconditions).
- `TYRANT/IN/tyrant_config.json` : defaults (outlier_threshold_x=3, max_blue_ocean_depth=1) generes par --prepare.

### Statut des composants

| Composant | Docs Tracking | Code Python | Notes |
|---|---|---|---|
| ORCHESTRATOR | ✅ | ✅ (v1) | |
| F01_SCOUT | ✅ | ✅ (v1) | |
| F02_TYRANT_CAMP | ✅ | ✅ (v1) | Verdict GO/NO-GO + ocean bleu (Porte 1) |
| TYRANT (prospectif) | ✅ | ✅ (v1) | Veille Demon -> ARCHIVUM/demons/ |
| F03_F06 + CAPTEURS + ANGLESMITH | ✅ | ❌ | Vagues suivantes |

### Prochaines etapes
1. Implementer ANGLESMITH (vague 4 — forge les N angles sur verdict.json)
2. Implementer F03_SOURCE_HUNTER + F04_COPYWRITER (vague 5)
3. Implementer F05_PACKAGER + F06_TRACKER + CAPTEURS
4. Premier siege reel avec les inputs du Warsmith

---

## [DEV-ANGLESMITH] ANGLESMITH implémentée — La forge des N angles (Porte 2)

### Contexte
Quatrième vague de code. ANGLESMITH est portée par F02_TYRANT_CAMP (décision README/ORCHESTRATOR : "ANGLESMITH via F02 stratégie"). Elle forge les N angles d'attaque sur le verdict de la Porte 1 : X directs (territoire du Démon) + Y océan bleu (re-ciblage non saturé, MÊME source, 1 couche max).

### Fichiers livrés
```
F02_TYRANT_CAMP/CODEBASE/
├── anglesmith.py                  ← wrapper 3 phases (--prepare / --auto / --finalize)
│                                    (--n-angles, sortie OUT/angles.json pour F03 + F04)
└── libs/
    ├── angle_forger.py            ← combinatoire 4 axes (family/emotion/engagement/reframe_dim)
    │                                 + anti-cannibale (2 axes différenciants minimum)
    └── learnings_weight.py        ← pondération (poids nul si < 50 packs exécutés)
```

### Décisions d'implémentation
- Zones : `n_blue = min(len(blue_ocean_unlocked), n/3)` — le reste en direct. Chaque angle porte `zone`, `territory`, `blue_ocean_depth=1` (blue) et `blue_ocean_reframe_applied`.
- Anti-cannibale vérifié au forge ET re-vérifié au finalize (2 axes différenciants min, sinon flag CANNIBALE).
- Poids : `learnings.json.cumulative_packs_executed < 50` → tous les poids = 1.0 (neutre) ; éligible ensuite → poids par `angle_performance[*].weight`.
- Hérésie guard au finalize : toute profondeur != 1 est clampée.
- Check-in IW_CUSTOS `--frigate ANGLESMITH` (fleet_status → `angles_forged` quand la précondition verdict_ready est remplie).

### Statut des composants

| Composant | Docs Tracking | Code Python | Notes |
|---|---|---|---|
| ORCHESTRATOR | ✅ | ✅ (v1) | |
| F01_SCOUT | ✅ | ✅ (v1) | |
| F02_TYRANT_CAMP | ✅ | ✅ (v1) | Verdict + océan bleu (Porte 1) |
| ANGLESMITH (via F02) | ✅ (README/F02) | ✅ (v1) | N angles direct + blue ocean (Porte 2) |
| TYRANT (prospectif) | ✅ | ✅ (v1) | Veille Démon -> ARCHIVUM/demons/ |
| F03_F06 + CAPTEURS | ✅ | ❌ | Vagues suivantes |

### Prochaines étapes
1. Implémenter F03_SOURCE_HUNTER (vague 5)
2. Implémenter F04_COPYWRITER (vague 6 — frégate lourde premium)
3. Implémenter F05_PACKAGER + F06_TRACKER + CAPTEURS
4. Premier siège réel avec les inputs du Warsmith

---

## Portes — mapping des jalons futurs

| Porte | Jalon attendu | Statut |
|---|---|---|
| Avant Porte 1 | CAPTEURS scrap ecosysteme + niche | Non demarre |
| Porte 1 | F02_TYRANT_CAMP verdict campagne | Code pret (attente siege reel) |
| Porte 2 | ANGLESMITH N angles forges | Code pret (attente siege reel) |
| Porte 3 | F03 + F04 text_payloads prets | Non demarre |
| Porte 4 | F05 production packs expedies -> OMNIS_WATCH | Non demarre |

*Fer au-dedans, Fer au-dehors.*
