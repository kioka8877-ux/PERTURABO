# CAPTEURS — TRACKING.md

> *"Les capteurs sont les yeux du siège. Ils voient avant que le fer ne frappe."*
> *Scrap commandité par le Warsmith. Multi-sites. Pas d'auto-cron. Vision globale clipping = aucune info ne doit manquer pendant une campagne.*

---

## RÔLE

`CAPTEURS/` est le **réseau de senseurs du forge CLIPPING**. Contrairement aux frégates d'exécution (F01-F06), CAPTEURS ne s'exécoute pas automatiquement. Elle s'active **sur commande explicite du Warsmith**.

Objectif : produire une **cartographie complète de l'écosystème clipping** autour d'une campagne Whop spécifique ou d'une niche visée — de sorte que F02_TYRANT_CAMP ait toutes les infos nécessaires pour rendre son verdict GO/NO-GO + blue_ocean.

**Principe PERTURABO** : aucune information ne doit échapper au Warsmith pendant une campagne. CAPTEURS couvre :
1. **Whop Discover** + la page de la campagne fournie
2. **Tous les sites clipping que le Warsmith indique** (Clippa, Cliptic, ...) — pas limité à Whop
3. **La perception de la niche / campagne dans l'écosystème clipping** (comment elle est perçue par les clippers, qui l'a déjà clipée, quel angle marché chez les concurrents, quel payout réel observé)

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `IN/clipping_sites_to_scrap.json` | Warsmith | JSON | ✅ |
| `IN/campaign_to_observe.json` | Warsmith (URL campagne + niche + questions spécifiques) | JSON | ✅ |

`clipping_sites_to_scrap.json` est laissé **vide** par défaut dans l'arborescence — c'est le Warsmith qui le peuple avec les sites qu'il veut scraper. Voir `CONTRACTS/clipping_sites_to_scrap.example.json` pour le schéma.

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
- `OUT/cartographie.md` — synthèse lisible pour le Warsmith (ce que l'écosystème dit de la campaigne, qui a clip quel angle, où sont les angles libres)

---

## MÉCANIQUE DE SCRAP

4 modules distincts :

### `libs/whop_scanner.py`
Scrape Whop Discover + page de la campagne donnée. Extraction : statut, budget restant, CPM attendu, guidelines, assets publiés.

### `libs/clipping_ecosystem_scanner.py`
Scrap tous les sites du `clipping_sites_to_scrap.json`. Extraction : quelle campagnes Whop sont listées, hormis la campaigne ciblée — pour identifier des opportunités futures. Aussi : outils IA mentionnés, payouts moyens observés.

### `libs/campaign_context_scanner.py`
Pour la campaigne observée : recherche sur les sites clipping + Twitter/X + Reddit + YouTube des discussions / contenu publié par des clippers. Extraction : qui l'a déjà clipé, avec quel angle, quel résultat.

### `libs/demon_scanner.py`
Si demandé : scanne le wild clipping (TikTok / Shorts / Reels) pour identifier des Démon dominants hors campagne. Output qui nourrit aussi `TYRANT prospectif` → via `ARCHIVUM/demons/`.

---

## PATTERN D'EXÉCUTION — COMMANDE WARSMITH UNIQUEMENT

```
# Pas de cron. Pas d'auto. Warsmith appelle explicitement :
python capteurs.py --scan --campaign IN/campaign_to_observe.json
# → Lance whop_scanner + ecosystem_scanner + campaign_context_scanner (en série)
# → Écrit OUT/cartographie.json + .md
# → Check-in IW_CUSTOS.py

# Si demandé :
python capteurs.py --scan-demons --scan-list IN/scan_list.json
# → Lance demon_scanner (renvoie vers TYRANT/ si analyse pélométrique nécessaire)
```

---

## CONTRATS RÉFÉRENCÉS

- `CONTRACTS/clipping_sites_to_scrap.example.json` — schéma des sites
- `ARCHIVUM/knowledge_base/sites/` — sites connus, ressources
- `ARCHIVUM/rules/whop_rules.md` — contexte Whop
- `CONTRACTS/anti_bullshit.md` (liens core)

---

## DÉPENDANCES

- **Amont** : Warsmith (site list + campaign_to_observe)
- **Downstream** :
  - F02_TYRANT_CAMP (consomme `cartographie.json` à la Porte 1 — optionnel mais fortement recommandé)
  - `ARCHIVUM/demons/` (si demon_scanner active)
  - TYRANT prospectif (peut utiliser demon_scanner)

---

## HÉRÉSIES

- ❌ Scrap automatique (CAPTEURS est commandité — pas de cron, pas d'auto-loop)
- ❌ Lancer CAPTEURS sans Warsmith explicit call
- ❌ Scrap des sites non-listés dans `clipping_sites_to_scrap.json` (sauf Whop, qui est toujours)
- ❌ Continuer à scraper après fermeture de campaigne (le tracker ferme CAPTEURS à `--close-campaign` de F06)

---

## STATUT

| Phase | État | Notes |
|---|---|---|
| Arborescence créée | ✅ | |
| TRACKING.md rédigé | ✅ | Ce fichier |
| Code Python implémenté | ❌ | À implémenter |
| `capteurs.py` | ❌ | CLI commandité |
| `libs/whop_scanner.py` | ❌ | Scrap Whop Discover + pages campagne |
| `libs/clipping_ecosystem_scanner.py` | ❌ | Scrap sites clipping du Warsmith |
| `libs/campaign_context_scanner.py` | ❌ | Perception campaigne dans l'écosystème |
| `libs/demon_scanner.py` | ❌ | Démon wild clipping |
| `requirements_capteurs.txt` | ❌ | requests + BeautifulSoup4 + (selon sites, playwright ou selenium) |

*Fer au-dedans, Fer au-dehors. Rien n'échappe au siège.*
