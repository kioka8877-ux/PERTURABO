# IW_CAMPAIGN_LOG — MONDE-FORGE API

## [CONSTRUCTION] Phase 0-4
- Architecture PERTURABO, CONTRACTS, liber_api.json, IW_CUSTOS.py, ai_gateway.py, TYRANT

## [CONSTRUCTION] Phase 5 — F01 SENTINEL frégate
- sentinel_rapid.py : scrape RapidAPI via Jina Reader + regex parsing
- sentinel_gh.py : GitHub code search par host RapidAPI
- sentinel_web.py : Jina Reader générique
- sentinel.py : orchestrateur 3 modes → ARCHIVUM/targets/[siege_id]/raw_intel.json

## [CONSTRUCTION] Phase 6 — F02 BREACHER frégate
- breacher.py : scoring 4 dimensions pondérées
- 20 angles d'attaque (prix, endpoint, niche, format, vitesse)
- Gate 2 interactive : fiche cible → validation Warsmith
- _extract_json : extraction JSON robuste depuis réponse Oracle

## Prochaine étape : Phase 7 — F03 FORGEWARD + F04 HERALD
- forgeward.py : 20 codes FastAPI en parallèle
- herald.py : listings RapidAPI + README GitHub LLM-ready
