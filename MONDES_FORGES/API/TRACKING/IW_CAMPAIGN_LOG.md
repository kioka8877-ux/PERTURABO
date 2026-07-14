# IW_CAMPAIGN_LOG — MONDE-FORGE API

## [CONSTRUCTION] Phases 0-6
- Architecture, CONTRACTS, liber, IW_CUSTOS, ai_gateway, TYRANT, F01 SENTINEL, F02 BREACHER

## [CONSTRUCTION] Phase 7 — F03 FORGEWARD + F04 HERALD
- forgeward.py : 20 prompts indépendants → call_oracle_batch(max_workers=5)
- Chaque prompt = angle d'attaque + cible + contracts → JSON warrior complet
- Matérialisation : api.py + requirements.txt + openapi.json + deploy.sh + meta.json
- herald.py : prompts listing → call_oracle_batch → listing RapidAPI + README
- Listing : titre SEO (avec nom concurrent), description 200-400 chars, 5 tags
- README : optimisé LLM (mention 'AI agent', 'LLM', 'automation', openapi.json)
- Gate 4 : récap final affiché au Warsmith

## Prochaine étape : Phase 8 — F05 GRAND COMPASS + F06 CAPTEURS
- grand_compass.py : deploy Railway/GitHub en parallèle + capture URLs
- capteurs.py : monitoring quotidien RapidAPI + GitHub + ledgers ARCHIVUM


## [CONSTRUCTION] Phase 8 — F05 GRAND COMPASS + F06 CAPTEURS
- grand_compass.py : --prepare / --iron (GitHub repos + push parallèle) / --finalize (URLs + F06 init)
- Deploy automatique : crée repo GitHub via API, push api.py + openapi.json + README
- GITHUB_TOKEN requis dans .env — URLs Railway/Render toujours générées même sans token
- capteurs.py : --init (ledger siège) / --scan (métriques quotidiennes) / --report (survie + rules)
- Seuils : vivant=3 abonnés, gagnant=10, mort=0 après 30j
- Patterns gagnants alimentent ARCHIVUM/rules/patterns_gagnants.md (couche froide)
- Métriques RapidAPI via --manual-update (Provider Dashboard non exposé publiquement)
- Prochaine étape : Phase 9 — ORCHESTRATOR + test end-to-end