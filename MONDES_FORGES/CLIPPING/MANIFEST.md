# MANIFEST.md â€” Manifeste de livraison du Monde Forge CLIPPING

> *Liste exhaustive des fichiers crÃ©Ã©s. L'implÃ©menteur Python lira ce manifest + chaque TRACKING.md pour savoir exactement quoi coder.*

---

## Scope de la livraison

- âœ… **Arborescence complÃ¨te** : 82 dossiers crÃ©Ã©s
- âœ… **README.md racine** : vue d'ensemble du forge (positionnement, inputs, portes, frÃ©gates, ARCHIVUM, hÃ©rÃ©sies)
- âœ… **TRACKING.md par frÃ©gate** : doc dÃ©diÃ©e Ã  chaque frÃ©gate (rÃ´le, inputs, outputs, pattern d'exÃ©cution, contrats, dÃ©pendances, hÃ©rÃ©sies, statut)
- âœ… **CONTRACTS** : copywriting_doctrine.md, copywriter_systemprompt.md (placeholder), copywriter_secrets.example.json, whop_rules.md, clipping_rules.md, production_pack_schema.json, clipping_sites_to_scrap.example.json
- âœ… **ARCHIVUM** : 10 zones + README pour chaque zone importante + squelettes JSON initiaux (learnings, angle_patterns, angle_performance)
- âœ… **.gitignore** : protÃ¨ge les secrets et le runtime
- âœ… **TRACKING/INDEX.md** : cartographie des journaux

Cette livraison est **la trame stratÃ©gique**. Aucun code Python n'est Ã©crit. La production du code est dÃ©lÃ©guÃ©e Ã  un autre model qui suivra religieusement les TRACKING.md.

---

## Inventaire par catÃ©gorie

### ðŸ“„ Fichiers de pilotage (racine + tracking)

| Fichier | Statut | RÃ´le |
|---|---|---|
| `README.md` | âœ… finalisÃ© | Vue d'ensemble du forge |
| `TRACKING/CLIPPING_LOG.md` | âœ… finalisÃ© | Journal gÃ©nÃ©ral (init, portes, statuts) |
| `TRACKING/INDEX.md` | âœ… finalisÃ© | Cartographie des journaux |
| `MANIFEST.md` | âœ… finalisÃ© | Ce fichier |
| `.gitignore` | âœ… finalisÃ© | Secrets + runtime + caches |

### âš”ï¸ TRACKING.md des 9 composants

| Composant | Fichier TRACKING.md | Statut |
|---|---|---|
| F01_SCOUT | `F01_SCOUT/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© |
| F02_TYRANT_CAMP | `F02_TYRANT_CAMP/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© |
| F03_SOURCE_HUNTER | `F03_SOURCE_HUNTER/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© |
| F04_COPYWRITER | `F04_COPYWRITER/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© (le plus dÃ©taillÃ© â€” frÃ©gate lourde 4 phases) |
| F05_PACKAGER | `F05_PACKAGER/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© |
| F06_TRACKER | `F06_TRACKER/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© |
| TYRANT (prospectif) | `TYRANT/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© |
| CAPTEURS | `CAPTEURS/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© |
| ORCHESTRATOR | `ORCHESTRATOR/CODEBASE/TRACKING.md` | âœ… rÃ©digÃ© |

### ðŸ“œ CONTRACTS/

| Fichier | Statut | Rempli par |
|---|---|---|
| `copywriting_doctrine.md` | squelette (10 sections structurÃ©es) | Le Warsmith doit remplir chaque section â€” surtout VI (subliminal, savoir secret) |
| `copywriter_systemprompt.md` | placeholder | GÃ©nÃ©ration par premium Ã  l'init (one-time) |
| `copywriter_secrets.example.json` | âœ… schÃ©ma public | Le Warsmith crÃ©e `copywriter_secrets.json` (gitignored) avec clÃ© + model_id |
| `whop_rules.md` | squelette (sections documentÃ©es) | Warsmith confirme chiffres + cas particuliers |
| `clipping_rules.md` | âœ… 8 rÃ¨gles documentÃ©es (C1-C7) | Warsmith peut enrichir cas particuliers |
| `production_pack_schema.json` | âœ… schÃ©ma canonique | Contrat figÃ© PERTURABO â†” OMNIS_WATCH |
| `clipping_sites_to_scrap.example.json` | âœ… schÃ©ma public | Warsmith crÃ©e le .json rÃ©el avec les sites qu'il veut scraper |

### ðŸ“š ARCHIVUM/

| Zone | README | Squelettes JSON | Statut |
|---|---|---|---|
| `rules/` | âœ… | n/a (squelettes dans `CONTRACTS/`) | squelettes â€” Warsmith Ã  remplir pour platform_tiktok/shorts/reels_md |
| `campaign/` | âœ… | n/a | runtime (Warsmith y dÃ©pose directive.md avant chaque siÃ¨ge) |
| `platform_generator/` | âœ… | n/a | squelettes â€” Warsmith remplit youtube/tiktok/instagram_profile.md |
| `market_generator/` | âœ… | n/a | squelettes â€” Warsmith remplit us_young_english.md |
| `knowledge_base/` | âœ… | n/a | squelettes â€” Warsmith peuple sites/, docs/, transcripts/ |
| `copywriting/` | âœ… | n/a | squelettes â€” 8 sous-dossiers, savoir secret Warsmith |
| `angles/` | âœ… | âœ… `angle_patterns.json` + `angle_performance.json` | squelettes â€” Warsmith catalogue les patterns |
| `demons/` | âœ… | n/a | runtime (TYRANT prospectif y Ã©crit) |
| `channels/` | âœ… | n/a | runtime (Warsmith y crÃ©e un sous-dossier par compte) |
| `learnings/` | âœ… | âœ… `learnings.json` (squelette initial) | runtime (C06 nourrit) |
| `ledgers/` | n/a (core tient IW_CUSTOS.py Ã  racine) | n/a | runtime |
| `templates/` | n/a | n/a | rÃ©servÃ© â€” usage futur |

### ðŸ§± Sous-dossiers CODEBASE/ (vides â€” contenu `.gitkeep`)

Chaque frÃ©gate a :
- `CODEBASE/` â€” destinÃ© Ã  recevoir le code Python (Ã  implÃ©menter par autre model)
- `CODEBASE/libs/` â€” bibliothÃ¨ques auxiliaires (Ã  implÃ©menter)
- `IN/` â€” inputs runtime
- `OUT/` â€” artefacts produits runtime
- `TRACKING/` â€” extendable si besoin (par dÃ©faut seulement `.gitkeep`)

`SHARED/` dispose de `IN/` + `OUT/` pour les ressources communes.

`ORCHESTRATOR/CODEBASE/TRACKING.md` documente aussi la gestion de `IW_CUSTOS.py` Ã  la racine du forge (Ã  copier du core â€” script registre).

---

## âš ï¸ Note sÃ©curitÃ©

Un token GitHub a Ã©tÃ© partagÃ© en clair dans le chat pendant la session (token redacted par sÃ©curitÃ©). Il a Ã©tÃ© utilisÃ© **temporairement** pour cloner PERTURABO et pousser le forge.

**Le Warsmith doit** :
1. RÃ©voquer ce token immÃ©diatement sur https://github.com/settings/tokens (il est publiquement compromis)
2. Ne jamais le rÃ©utiliser
3. Ne plus partager de token en clair dans le chat
4. CrÃ©er un nouveau token pour les sessions futures, Ã  stocker dans une var d'env locale

---

## ðŸŽ¯ Prochaines Ã©tapes pour le Warsmith

### Phase 1 â€” Remplir la doctrine et l'ARCHIVUM (savoir secret)

1. Remplir `CONTRACTS/copywriting_doctrine.md` (sections I Ã  X) â€” surtout VI (subliminal, savoir secret)
2. Remplir `ARCHIVUM/copywriting/` (8 sous-dossiers) â€” c'est le musÃ©e du copywriting:
   - `hooks_library/` â€” types de hooks + exemples
   - `title_formulas/` â€” formules de titres
   - `caption_frameworks/` â€” structures caption
   - `subliminal_language/` â€” le savoir secret
   - `slang_by_market/` â€” codex slang US jeune + bannis TikTok
   - `hashtags_research/` â€” stratÃ©gies 3-strates + bannis
   - `on_screen_text_patterns/` â€” patterns de keyframe
   - `reference_clips_titles/` â€” titres gagnants indexÃ©s
3. Remplir les platform_generator (youtube/tiktok/instagram)
4. Remplir market_generator (us_young_english par dÃ©faut)
5. Peupler knowledge_base/ (sites, docs, transcripts clipping)
6. PrÃ©-peupler `ARCHIVUM/angles/angle_patterns.json` avec les patterns initiaux
7. CrÃ©er des sous-dossiers pour ses comptes de clipping dans `ARCHIVUM/channels/`

### Phase 2 â€” Configurer les secrets

8. Ã€ la racine du forge, crÃ©er `CONTRACTS/copywriter_secrets.json` (gitignored) :
   ```json
   {
     "env_var_name": "CLIPPING_PREMIUM_API_KEY",
     "model_id": "<vrai model premium>",
     "provider": "...",
     "base_url": "...",
     "max_tokens_per_call": 4096,
     "temperature_default": 0.7
   }
   ```
9. Sur sa machine : `export CLIPPING_PREMIUM_API_KEY=...` (jamais committÃ©)

### Phase 3 â€” Initialiser le system prompt (one-time)

10. Une fois le copywriting doctrine rempli + musÃ©e copywriting peuplÃ©, exÃ©cuter le script d'init (Ã  implÃ©menter) :
    ```
    python copywriter.py --init-systemprompt
    ```
    Le modÃ¨le premium lit la doctrine + le musÃ©e â†’ gÃ©nÃ¨re `CONTRACTS/copywriter_systemprompt.md` (figÃ© ensuite).

### Phase 4 â€” DÃ©lÃ©guer le code Python

11. Lancer un autre model (Claude, GPT, etc.) sur ce dÃ©pÃ´t avec comme instruction :
    "Lis tous les TRACKING.md du forge CLIPPING + README.md + MANIFEST.md + CONTRACTS/. ImplÃ©mente tous les scripts Python des frÃ©gates en suivant religieusement chaque TRACKING.md. Le schÃ©ma du production pack doit Ãªtre respectÃ© strictement (CONTRACTS/production_pack_schema.json)."
12. Le model implÃ©mente `*.py` according aux TRACKING.md

### Phase 5 â€” Premier siÃ¨ge

13. First siege :
    - DÃ©poser `directive.md` + `reference_clip.json` dans `ARCHIVUM/campaign/`
    - PrÃ©parer `clipping_sites_to_scrap.json` (si tu veux scanner plus large)
    - Lancer `python orchestrator.py --start-siege ...` (Ã  implÃ©menter)
    - Suivre les 4 Portes avec validation Warsmith Ã  chaque.

---

*Fer au-dedans, Fer au-dehors. La structure est en place. La doctrine reste Ã  Ã©crire. Le code suit.*
