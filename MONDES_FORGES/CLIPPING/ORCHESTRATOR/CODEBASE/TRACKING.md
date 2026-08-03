# ORCHESTRATOR â€” TRACKING.md (Monde Forge CLIPPING)

> *"L'Orchestrateur ne forge pas. Il conduit les frÃ©gates de porte en porte. Chaque porte validÃ©e = one step closer Ã  la rupture de la forteresse."*
> *Tient le ledger IW_CUSTOS + le liber_clipping.json. Synchronise les 4 portes.*

---

## RÃ”LE

`ORCHESTRATOR/` est la **frÃ©gate-conductrice** du forge CLIPPING. Elle ne produit pas d'artefacts viraux elle-mÃªme â€” elle **synchronise** les C01-C06 + TYRANT + CAPTEURS et tient le **ledger central** (`IW_CUSTOS.py` dans le core PERTURABO + `liber_clipping.json` dans le forge).

Orchestre les **4 Portes**. Le Warsmith valide chaque porte manuellement.

---

## LEDGER CENTRAL â€” IW_CUSTOS

AlignÃ© sur le pattern du core :
- `IW_CUSTOS.py` â€” script registre central (Grand Company Ledger)
- CopiÃ© dans le forge CLIPPING racine (`MONDES_FORGES/CLIPPING/IW_CUSTOS.py`)
- Enregistre l'Ã©tat du siÃ¨ge : campagne active, porte courante, statut de chaque frÃ©gate, soumissions, fermetures

`liber_clipping.json` â€” Ã©tat inter-frÃ©gates (partagÃ© entre les frÃ©gates pour savoir oÃ¹ on en est dans le siÃ¨ge) :

```json
{
  "siege_id": "...",
  "campaign_id": "...",
  "campaign_status": "active|closed",
  "current_porte": "init|p1|p2|p3|p4|closed",
  "inputs_warsmith": {
    "directive_path": "...",
    "reference_clip_path": "...",
    "platform_target": "...",
    "market_target": "...",
    "n_angles": N
  },
  "fregates_status": {
    "F01_SCOUT": "pending|done|blocked",
    "F02_TYRANT_CAMP": "pending|done|blocked",
    "ANGLESMITH": "pending|done|blocked",
    "F03_SOURCE_HUNTER": "pending|done|blocked",
    "F04_COPYWRITER": "pending|done|blocked",
    "F05_PACKAGER": "pending|done|blocked",
    "F06_TRACKER": "pending|done|blocked"
  },
  "portes_validated": ["p1", "p2"],
  "packs_expedies_count": N,
  "packs_posted_count": N,
  "packs_submitted_whop_count": N,
  "last_event": "...",  
  "siege_started_at": "<ISO8601>",
  "siege_closed_at": "<ISO8601 ou null>"
}
```

---

## LES 4 PORTES

### Porte 1 â€” Verdict campagne

FrÃ©gates mobilisÃ©es : F01_SCOUT (alimentation) + F02_TYRANT_CAMP (verdict)

Avant la Porte 1 (optionnel mais recommandÃ©) : CAPTEURS scan Ã©cosystÃ¨me + niche

Le Warsmith valide le verdict GO/NO-GO. Si NO-GO â†’ campaign pas poursuivie. Si GO â†’ Porte 2.

```
orchestrator.py --gate 1 --decision valide|rejette
```

### Porte 2 â€” N angles forgÃ©s

FrÃ©gates mobilisÃ©es : ANGLESMITH (peut Ãªtre portÃ© par C02 ou dÃ©diÃ© â€” voir implÃ©mentation future)

L'Orchestrateur dÃ©clenche la forge des N angles. Le Warsmith voit les N angles (direct + ocÃ©an bleu), valide ou tue 1+ angles (rereforge si kill).

â†’ `OUT/angles.json` validÃ© â†’ Porte 3.

```
orchestrator.py --gate 2 --decision valide
# Si angles rejetÃ©s :
orchestrator.py --gate 2 --decision rejete --angle <angle_id> --reason "..."
# â†’ ANGLESMITH re-forge un angle de remplacement
```

### Porte 3 â€” Source specimens + text payloads

FrÃ©gates mobilisÃ©es : F03_SOURCE_HUNTER (source par angle) + F04_COPYWRITER (texte par angle)

Pour chaque angle, C03 sÃ©lectionne l'asset + segments puis C04 forge le text_payload complet. Le Warsmith + l'IRON ordonnancement valident les N text_payloads.

â†’ N `source_specimen_<angle>.json` + N `text_payload_<angle>.json` (et `.md` pour le Warsmith).

```
orchestrator.py --gate 3 --decision valide
```

### Porte 4 â€” N production packs expÃ©diÃ©s â†’ OMNIS_WATCH

FrÃ©gate mobilisÃ©e : F05_PACKAGER

Ces N `production_pack_<angle>.json` sont livrÃ©s Ã  OMNIS_WATCH (par raw.githubusercontent.com URL â€” point d'intÃ©gration existant).

F06_TRACKER prend le relais post-publication.

```
orchestrator.py --gate 4 --decision valide
# â†’ distribue packs_index.json vers OMNIS_WATCH (via git push ou raw URL)
# â†’ F06_TRACKER dÃ©marre
```

---

## PATTERN D'EXÃ‰CUTION â€” COMMANDES PRINCIPALES

```
# DÃ©marrage d'un siÃ¨ge (campagne active)
orchestrator.py --start-siege --directive ARCHIVUM/campaign/directive.md \
   --reference-clip ARCHIVUM/campaign/reference_clip.json \
   --platform youtube --market us_young_english \
   --n-angles 10
# â†’ Initialise liber_clipping.json
# â†’ Statut = "init", en attente de CAPTEURS warpping et Porte 1

# AprÃ¨s chaque porte :
orchestrator.py --gate N --decision valide
# â†’ Avance current_porte Ã  la suivante
# â†’ Active les frÃ©gates de la prochaine porte

# Reprise aprÃ¨s une pause :
orchestrator.py --resume
# â†’ Lit liber_clipping.json, identifie la porte courante, indique 
#   au Warsmith comment reprendre

# Fermeture campaigne :
orchestrator.py --close-siege --final-payout-summary ...
# â†’ Marque siehe comme closed, dÃ©clenche C06 agrÃ©gation learnings
# â†’ LibÃ¨re la campaign/ pour la suivante (archivage optionnel)
```

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S

- `HERESIE/CONTRACTS/iron_prompt.md` (core, lien) â€” pattern prepare/IRON/finalize
- `HERESIE/CONTRACTS/system_prompt.md` (core, lien) â€” boussole systÃ¨me
- `CONTRACTS/anti_bullshit.md` (core, lien)
- Tous les `ARCHIVUM/rules/`

---

## DÃ‰PENDANCES

- **Amont** : Le Warsmith (4 inputs initiaux)
- **RÃ©seau interne** : toutes les frÃ©gates C01-C06, TYRANT, CAPTEURS
- **Downstream** : OMNIS_WATCH (recoit les packs via Porte 4), `ARCHIVUM/learnings/learnings.json` (Ã  la fermeture)

---

## HÃ‰RÃ‰SIES

- âŒ Passer une porte sans validation Warsmith explicite
- âŒ Sauter une porte (sÃ©quence Porte 1 â†’ 2 â†’ 3 â†’ 4 obligatoire)
- âŒ Auto-fermer une siÃ¨ge (seul le Warsmith dÃ©clare la fin)
- âŒ DÃ©marrer un nouveau siÃ¨ge sans fermer le prÃ©cÃ©dent (campaign/ est singulier)
- âŒ N'importe quelle frÃ©gate modifie directement `IW_CUSTOS.py` sans passer par l'Orchestrateur (chaque frÃ©gate appelle check-in mais c'est l'Orchestrateur qui tient la cohÃ©rence)

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python implÃ©mentÃ© | âŒ | Ã€ implÃ©menter |
| `orchestrator.py` | âŒ | CLI multi-commandes (start/resume/gate/close) |
| `libs/ledger_manager.py` | âŒ | GÃ¨re liber_clipping.json + IW_CUSTOS.py |
| `libs/gate_validator.py` | âŒ | VÃ©rifie que les outputs attendus sont prÃ©sents avant validation de porte |
| `libs/siege_initializer.py` | âŒ | Init liber_clipping.json |
| `libs/omnis_watch_distributor.py` | âŒ | Push les packs vers raw URL / git tag pour OMNIS_WATCH |
| `requirements_orchestrator.txt` | âŒ | |

RÃ©fÃ©rence d'implÃ©mentation : `HERESIE/ORCHESTRATOR/CODEBASE/orchestrator.py` dans le core (probable rÃ©utilisation Ã  60-70%, adaptation pour les 4 Portes du forge clipping et la spÃ©cificitÃ© de C04).

*Fer au-dedans, Fer au-dehors. L'Orchestrateur ne ment pas â€” il conduit.*
