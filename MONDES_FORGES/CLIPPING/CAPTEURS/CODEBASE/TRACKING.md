# CAPTEURS â€” TRACKING.md

> *"Les capteurs sont les yeux du siÃ¨ge. Ils voient avant que le fer ne frappe."*
> *Scrap commanditÃ© par le Warsmith. Multi-sites. Pas d'auto-cron. Vision globale clipping = aucune info ne doit manquer pendant une campagne.*

---

## RÃ”LE

`CAPTEURS/` est le **rÃ©seau de senseurs du forge CLIPPING**. Contrairement aux frÃ©gates d'exÃ©cution (C01-C06), CAPTEURS ne s'exÃ©coute pas automatiquement. Elle s'active **sur commande explicite du Warsmith**.

Objectif : produire une **cartographie complÃ¨te de l'Ã©cosystÃ¨me clipping** autour d'une campagne Whop spÃ©cifique ou d'une niche visÃ©e â€” de sorte que F02_TYRANT_CAMP ait toutes les infos nÃ©cessaires pour rendre son verdict GO/NO-GO + blue_ocean.

**Principe PERTURABO** : aucune information ne doit Ã©chapper au Warsmith pendant une campagne. CAPTEURS couvre :
1. **Whop Discover** + la page de la campagne fournie
2. **Tous les sites clipping que le Warsmith indique** (Clippa, Cliptic, ...) â€” pas limitÃ© Ã  Whop
3. **La perception de la niche / campagne dans l'Ã©cosystÃ¨me clipping** (comment elle est perÃ§ue par les clippers, qui l'a dÃ©jÃ  clipÃ©e, quel angle marchÃ© chez les concurrents, quel payout rÃ©el observÃ©)

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `IN/clipping_sites_to_scrap.json` | Warsmith | JSON | âœ… |
| `IN/campaign_to_observe.json` | Warsmith (URL campagne + niche + questions spÃ©cifiques) | JSON | âœ… |

`clipping_sites_to_scrap.json` est laissÃ© **vide** par dÃ©faut dans l'arborescence â€” c'est le Warsmith qui le peuple avec les sites qu'il veut scraper. Voir `CONTRACTS/clipping_sites_to_scrap.example.json` pour le schÃ©ma.

---

## OUTPUTS

### `OUT/cartographie.json`

```json
{
  "scan_id": "...",
  "scanned_at": "<ISO8601>",
  
  "whop_scan": {
    "campaign_url": "...",
    "campaign_status": "active|ending|closed",
    "campaign_budget_remaining_estimate": "...",
    "cpm_expected": "...",
    "campaign_guidelines": "...",
    "campaign_assets_published": [...]
  },
  
  "ecosystem_scan": {
    "scanned_sites": [
      {"site": "clippa.com", "url_scraped": "...", "data_extracted": {...}}
    ],
    "competitors_observed": [
      {"clipper_name": "...", "angle_used": "...", "platform": "...", "views": N, "payout_reported": "..."}
    ],
    "angles_already_used_on_this_campaign": [
      {"angle": "...", "competitor": "...", "result": "low|medium|high views"}
    ]
  },
  
  "niche_perception": {
    "dominant_emotion_in_niche": "...",
    "saturated_angles": [...],
    "undersaturated_angles": [...]
  },
  
  "check_in_iw_custos": "<ISO8601>"
}
```

### Autres
- `OUT/cartographie.md` â€” synthÃ¨se lisible pour le Warsmith (ce que l'Ã©cosystÃ¨me dit de la campaigne, qui a clip quel angle, oÃ¹ sont les angles libres)

---

## MÃ‰CANIQUE DE SCRAP

4 modules distincts :

### `libs/whop_scanner.py`
Scrape Whop Discover + page de la campagne donnÃ©e. Extraction : statut, budget restant, CPM attendu, guidelines, assets publiÃ©s.

### `libs/clipping_ecosystem_scanner.py`
Scrap tous les sites du `clipping_sites_to_scrap.json`. Extraction : quelle campagnes Whop sont listÃ©es, hormis la campaigne ciblÃ©e â€” pour identifier des opportunitÃ©s futures. Aussi : outils IA mentionnÃ©s, payouts moyens observÃ©s.

### `libs/campaign_context_scanner.py`
Pour la campaigne observÃ©e : recherche sur les sites clipping + Twitter/X + Reddit + YouTube des discussions / contenu publiÃ© par des clippers. Extraction : qui l'a dÃ©jÃ  clipÃ©, avec quel angle, quel rÃ©sultat.

### `libs/demon_scanner.py`
Si demandÃ© : scanne le wild clipping (TikTok / Shorts / Reels) pour identifier des DÃ©mon dominants hors campagne. Output qui nourrit aussi `TYRANT prospectif` â†’ via `ARCHIVUM/demons/`.

---

## PATTERN D'EXÃ‰CUTION â€” COMMANDE WARSMITH UNIQUEMENT

```
# Pas de cron. Pas d'auto. Warsmith appelle explicitement :
python capteurs.py --scan --campaign IN/campaign_to_observe.json
# â†’ Lance whop_scanner + ecosystem_scanner + campaign_context_scanner (en sÃ©rie)
# â†’ Ã‰crit OUT/cartographie.json + .md
# â†’ Check-in IW_CUSTOS.py

# Si demandÃ© :
python capteurs.py --scan-demons --scan-list IN/scan_list.json
# â†’ Lance demon_scanner (renvoie vers TYRANT/ si analyse pÃ©lomÃ©trique nÃ©cessaire)
```

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S

- `CONTRACTS/clipping_sites_to_scrap.example.json` â€” schÃ©ma des sites
- `ARCHIVUM/knowledge_base/sites/` â€” sites connus, ressources
- `ARCHIVUM/rules/whop_rules.md` â€” contexte Whop
- `CONTRACTS/anti_bullshit.md` (liens core)

---

## DÃ‰PENDANCES

- **Amont** : Warsmith (site list + campaign_to_observe)
- **Downstream** :
  - F02_TYRANT_CAMP (consomme `cartographie.json` Ã  la Porte 1 â€” optionnel mais fortement recommandÃ©)
  - `ARCHIVUM/demons/` (si demon_scanner active)
  - TYRANT prospectif (peut utiliser demon_scanner)

---

## HÃ‰RÃ‰SIES

- âŒ Scrap automatique (CAPTEURS est commanditÃ© â€” pas de cron, pas d'auto-loop)
- âŒ Lancer CAPTEURS sans Warsmith explicit call
- âŒ Scrap des sites non-listÃ©s dans `clipping_sites_to_scrap.json` (sauf Whop, qui est toujours)
- âŒ Continuer Ã  scraper aprÃ¨s fermeture de campaigne (le tracker ferme CAPTEURS Ã  `--close-campaign` de C06)

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python implÃ©mentÃ© | âŒ | Ã€ implÃ©menter |
| `capteurs.py` | âŒ | CLI commanditÃ© |
| `libs/whop_scanner.py` | âŒ | Scrap Whop Discover + pages campagne |
| `libs/clipping_ecosystem_scanner.py` | âŒ | Scrap sites clipping du Warsmith |
| `libs/campaign_context_scanner.py` | âŒ | Perception campaigne dans l'Ã©cosystÃ¨me |
| `libs/demon_scanner.py` | âŒ | DÃ©mon wild clipping |
| `requirements_capteurs.txt` | âŒ | requests + BeautifulSoup4 + (selon sites, playwright ou selenium) |

*Fer au-dedans, Fer au-dehors. Rien n'Ã©chappe au siÃ¨ge.*
