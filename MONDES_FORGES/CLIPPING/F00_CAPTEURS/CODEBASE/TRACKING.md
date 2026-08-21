# F00_CAPTEURS — TRACKING.md

> *"Les capteurs sont les yeux du siège. Ils voient avant que le fer ne frappe."*
> *Scrap commandité par le Warsmith. Multi-sites. Pas d'auto-cron. Vision globale clipping = aucune info ne doit manquer pendant une campagne.*

---

## RÔLE

`F00_CAPTEURS/` est le **réseau de senseurs du forge CLIPPING**. Contrairement aux frégates d'exécution (F01-F06), F00_CAPTEURS ne s'exécoute pas automatiquement. Elle s'active **sur commande explicite du Warsmith**.

Objectif : produire une **cartographie complète de l'écosystème clipping** autour d'une campagne Whop spécifique ou d'une niche visée — de sorte que F02_TYRANT_CAMP ait toutes les infos nécessaires pour rendre son verdict GO/NO-GO + blue_ocean.

**Principe PERTURABO** : aucune information ne doit échapper au Warsmith pendant une campagne. F00_CAPTEURS couvre :
1. **Whop Discover** + la page de la campagne fournie
2. **Tous les sites clipping que le Warsmith indique** (Clippa, Cliptic, ...) — pas limité à Whop
3. **La perception de la niche / campagne dans l'écosystème clipping** (comment elle est perçue par les clippers, qui l'a déjà clipée, quel angle marché chez les concurrents, quel payout réel observé)

---

## RECHERCHE CONTEXTUALISÉE — V2 ADDITIVE

F00 conserve le comportement historique et ajoute un profil de recherche optionnel pour les sujets. Le profil initial cible `youtube_shorts` / `us_young_english` / `meme` et accepte les horizons `6h`, `24h`, `7d`, `30d`.

Exemple :

```bash
python3 capteurs.py --scan-subjects \
  --niche "student debt" \
  --horizon 24h \
  --platform youtube_shorts \
  --market us_young_english \
  --niche-mode meme \
  --mode informatif
```

Le score historique reste dans `score_mecanique_legacy`. Le nouveau résultat est exposé dans `score_contextualise`, `contextual_scores`, `safety_gate`, `saturation_penalty` et `contextual_profile`. Le Champion reste le seul décideur (`warsmith_review`). Aucun top 1 automatique n’est autorisé.

Les quatre horizons changent la pondération : `6h` privilégie la fraîcheur et l’accélération ; `24h` équilibre fraîcheur et stabilité ; `7d` privilégie tendance et répétabilité ; `30d` privilégie demande régulière et confirmation communautaire. YouTube est le signal de preuve principal ; Trends, Suggest, RSS et Reddit confirment ou contextualisent.

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
- `OUT/subjects_proposal.json` — proposition de sujets avec scores legacy et contextualisés
- `OUT/subjects_proposal.md` — tableau lisible pour le Champion

### Champs contextualisés d’un sujet

| Champ | Rôle |
|---|---|
| `score_mecanique_legacy` | Référence du score historique |
| `score_contextualise` | Classement du profil actif |
| `contextual_scores.us_native` | Ancrage marché US |
| `contextual_scores.youtube_shorts` | Preuve vidéo et adéquation Shorts |
| `contextual_scores.horizon` | Adéquation à la fenêtre demandée |
| `contextual_scores.meme_fit` | Faisabilité dans la niche meme |
| `contextual_scores.repeatability` | Déclinaison en angles |
| `contextual_scores.confidence` | Confiance dans les preuves |
| `safety_gate` | `pass` ou `block`, revue Champion obligatoire |

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

- ❌ Scrap automatique (F00_CAPTEURS est commandité — pas de cron, pas d'auto-loop)
- ❌ Lancer F00_CAPTEURS sans Warsmith explicit call
- ❌ Scrap des sites non-listés dans `clipping_sites_to_scrap.json` (sauf Whop, qui est toujours)
- ❌ Continuer à scraper après fermeture de campaigne (le tracker ferme F00_CAPTEURS à `--close-campaign` de F06)

---

## STATUT

| Phase | État | Notes |
|---|---|---|
| Arborescence créée | ✅ | |
| TRACKING.md rédigé | ✅ | Ce fichier |
| Code Python implémenté | ✅ | v1 (commit F00_CAPTEURS) |
| `capteurs.py` | ✅ | CLI commandité : `--scan`, `--scan-demons`, `--scan-subjects` legacy et profil contextualisé |
| `research_profile.py` | ✅ | Profils horizon / plateforme / marché / niche et pondérations |
| `libs/whop_scanner.py` | ✅ | Scrap Whop Discover + pages campagne (statut, budget, CPM, guidelines, assets) |
| `libs/clipping_ecosystem_scanner.py` | ✅ | Scrap sites clipping du Warsmith (payouts, outils AI, campagnes référencées) |
| `libs/campaign_context_scanner.py` | ✅ | Perception de la campagne dans l'écosystème (compétiteurs, angles déjà utilisés) |
| `libs/demon_scanner.py` | ✅ | Démon wild clipping (sondes TikTok/Shorts/Reels, archivées ARCHIVUM/demons/) |
| `libs/youtube_channel_scraper.py` | ✅ | Scrap de chaînes YouTube commandité (`--scrap-youtube`) — transcripts + méta dans knowledge_base/transcripts/ |
| `requirements_capteurs.txt` | ✅ | Stdlib urllib requis + yt-dlp/youtube-transcript-api (--scrap-youtube) ; requests/bs4/playwright/selenium optionnels selon sites |

### Décisions v1

- **Jamais de cron, jamais d'auto** : F00_CAPTEURS ne tourne que commandité par le
  Warsmith (précondition hérésie). Scrap post-fermeture de campagne refusé
  (liber `campaign_status == closed` → exit 1).
- **Périmètre strict** : seuls les sites listés dans
  `IN/clipping_sites_to_scrap.json` sont touchés ; Whop est TOUJOURS scanné
  (défaut système, non listable). Un site hors liste n'est jamais scanné.
- **Best-effort mécanique + lecture IRON** : fetch stdlib (urllib, aucun binaire
  requis). Ce qui n'est pas quantifiable mécaniquement (page JS, 403/404,
  perception niche, budget non extrait) est flaggé `requires_vision` et remonté
  au Warsmith pour lecture IRON (fichier cartographie.md).
- **`requires_vision`** : liste explicite dans la cartographie de tout ce que
  l'IRON doit confirmer avant que F02 rende le verdict GO/NO-GO.
- **Démon wild** : sondes fournies explicitement par le Warsmith
  (IN/scan_list.json, URLs de recherche par plateforme) ; résultat archivé dans
  `ARCHIVUM/demons/demon_wild_scan_<id>.json`.
- **Check-in IW_CUSTOS** : fin de scan → `CAPTEURS` done, `fleet_status`
  → `capteurs_done`.
- **Compatibilité legacy** : les anciennes options `--freshness brulant|frais`
  et leurs pondérations sont conservées ; le profil contextualisé s’ajoute en
  parallèle et n’efface jamais `score_mecanique_legacy`.
- **YouTube Shorts prioritaire** : YouTube porte la preuve vidéo ; les autres
  capteurs servent de confirmation, de fraîcheur, de demande ou de conversation.
- **Sécurité** : `safety_gate=block` interdit le classement opérationnel, même si
  les vues sont élevées ; le Champion garde la revue finale.
- **`--scrap-youtube`** (ajout v1.1, [DEV-F00_CAPTEURS-SCRAP]) : scrape une chaîne
  YouTube commanditée par le Warsmith (URL chaîne via `--channel` ou liste dans
  IN/scan_list.json `{"channels": [...]}`). Listing `yt-dlp --flat-playlist`
  (rapide), transcript `youtube-transcript-api` (fallback yt-dlp --write-subs),
  méta `yt-dlp --dump-single-json` (vues, subs, outlier = vues/subs). Archivage
  `ARCHIVUM/knowledge_base/transcripts/<slug>/<video_id>.json` — même schéma
  que le core YOUTUBE. Reprise native : vidéo déjà archivée → sautée. Limite
  par défaut 20 vidéos (`--max-videos`), rate-limit 1s (`--rate-limit`).
  Doctrine inchangée : commandité (jamais de cron), éteint si campagne fermée.

*Fer au-dedans, Fer au-dehors. Rien n'échappe au siège.*
