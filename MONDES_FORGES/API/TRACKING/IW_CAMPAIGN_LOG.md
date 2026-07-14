# IW_CAMPAIGN_LOG — MONDE-FORGE API

## [CONSTRUCTION] Phase 0 — Architecture
- Structure PERTURABO : CORE/ + MONDES_FORGES/ (YOUTUBE + API)
- Pattern frégate : --prepare → --iron → --finalize
- ARCHIVUM couche froide (rules, markets) / chaude (targets, ledgers)
- Liber = bus communication inter-frégates + état vivant du siège
- FLEET_STATUS_FLOW : 9 états de pending_reconnaissance à complete

## [CONSTRUCTION] Phase 1 — CONTRACTS
- system_prompt.md : doctrine RapidAPI, stack autorisée, règles absolues
- tyrant_prompt.md : 5 questions (territoire, démon, latence, wrappers, pricing)
- iron_prompt.md : contrat exécuteur Oracle
- anti_bullshit.md : 4 filtres (source, chiffres, patterns, seuils)
- api_scoring_checklist.json : 4 dimensions pondérées + 20 types angles

## [CONSTRUCTION] Phase 2 — Orchestration centrale
- liber_api.json : 9 états fleet_status, tyrant_report 5 dimensions
- IW_CUSTOS.py : 6 modes reset/check-out/check-in/gate/validate/status
- Flux complet : reset → check-out TYRANT → check-in → gate 1 → ...

## [CONSTRUCTION] Phase 3 — ai_gateway.py CORE
- Routing par frégate : TYRANT→Sonnet, F02→DeepSeek, F04→Gemini
- call_oracle(frigate, prompt) → str
- call_oracle_batch(frigate, prompts, max_workers) → list[str]
- Partagé entre tous les Mondes-Forges via CORE/

## [CONSTRUCTION] Phase 4 — TYRANT frégate
- contracts_loader.py : charge couche froide (rules, markets) + chaude (targets, ledgers)
- format_for_prompt() : assemble contexte injectabe dans le prompt
- tyrant.py --prepare : iron_prompt.txt assemblé dans TYRANT/IN/
- tyrant.py --iron : call_oracle("TYRANT", prompt) → tyrant_output.json
- tyrant.py --finalize : valide schema, check-in IW_CUSTOS, affiche Gate 1
- Différence clé vs YOUTUBE : appel Oracle entièrement automatisé

## Prochaine étape : Phase 5 — F01 SENTINEL
3 modules : sentinel_rapid (RapidAPI), sentinel_gh (GitHub API), sentinel_web (Jina)
Output : ARCHIVUM/targets/[siege_id]/raw_intel.json
