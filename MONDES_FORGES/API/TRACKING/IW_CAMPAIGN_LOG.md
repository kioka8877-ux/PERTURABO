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
