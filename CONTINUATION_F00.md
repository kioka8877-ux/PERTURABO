# CONTINUATION — Reprise du siège (F00_CAPTEURS)

> LIRE CE FICHIER EN PREMIER si vous arrivez dans ce repo "à froid".
> Il dit EXACTEMENT où le travail s'est arrêté et quoi faire ensuite.

## 1. État au dernier push (commit `19ed5ca`, branche `main`)

- F00_CAPTEURS est **opérationnel de bout en bout** : les 4 signaux sont
  captés (RSS, Trends, YouTube, Suggest), GLM 5.2 synthétise 5 sujets
  bilingues, le tout est exporté dans `EXPORT/` et enregistré dans le ledger.
- Une proposition réelle a été générée pour la niche **"Lakers basketball"**
  (scan `F00-a6fa824c`, 5 sujets notés 8→10/10, métriques réelles croisées).
  Voir `MONDES_FORGES/CLIPPING/EXPORT/subjects_proposal.json` et `.md`.

## 2. Ce qui est déjà fait (à ne PAS refaire)

- Modules F00 (nommage canonique `f00_*`) dans
  `MONDES_FORGES/CLIPPING/CAPTEURS/CODEBASE/libs/` :
  `f00_rss_ingestor.py` (fraîcheur 5h/24h + couverture médias)
  `f00_trends_ingestor.py` (pytrends courbe 7j + RSS trending global)
  `f00_youtube_ingestor.py` (YouTube Data API v3 : stats, search par vues, trending)
  `f00_suggestions_ingestor.py` (Google Suggest ds=yt, demand_score)
  `f00_virality_scorer.py` (score 4 signaux pondérés + 2 checklists)
  `f00_premium_synth.py` (synthèse GLM 5.2, réutilise `premium_client.py` de F04)
- Commande CLI : `capteurs.py --scan-subjects` (`--niche` OU `--hot`,
  `--mode informatif|humour`, `--freshness brulant|frais`).
- Check-in IW_CUSTOS : le ledger `liber_clipping.json` a `capteurs: done`,
  `fleet_status: capteurs_done`. Utiliser le nom canonique `CAPTEURS` pour
  IW_CUSTOS (PAS `F00_CAPTEURS` — frégate inconnue).
- Export automatique dans `MONDES_FORGES/CLIPPING/EXPORT/` (committé) à
  chaque run de `--scan-subjects`.

## 3. La clé premium (IMPORTANT — à reconfigurer dans un nouveau sandbox)

- Le modèle premium est GLM 5.2 via NVIDIA (`z-ai/glm-5.2`,
  `https://integrate.api.nvidia.com/v1`, config dans
  `CONTRACTS/copywriter_secrets.json` qui référence la var d'env).
- La clé N'EST PAS committée (bonne pratique — ne jamais pousser la clé).
- Localement elle était dans le `.env.local` à la racine du repo
  (gitignoré). `premium_client.py` le charge automatiquement.
- **Dans un nouveau sandbox** : le Warsmith doit re-injecter la clé
  NVIDIA (`CLIPPING_PREMIUM_API_KEY`) via API Keys / `.env.local`
  avant de relancer `--scan-subjects`, sinon la synthèse échoue avec
  "Clé premium absente". (La clé figure dans l'historique du chat.)

## 4. Ce qui reste à faire (travail suivant)

1. **Choisir le sujet** : le Warsmith choisit UN des 5 sujets de
   `EXPORT/subjects_proposal.json` (pas de top-1 automatique — porte dédiée).
2. **Commande de livraison du sujet choisi** : implémenter une nouvelle
   commande (ex. `capteurs.py --deliver-subject <index>`) qui écrit dans
   `ARCHIVUM/campaign/` :
   - `directive.md`
   - `article_source.json`
   - `reference_clip.json`
   (puis push GitHub + mise à jour ledger).
3. Optionnel : générer une proposition en mode `--hot` (sans niche) et en
   mode `--mode humour` pour valider les 2 sous-modes.
4. Intégration chaîne existante : le sujet choisi doit ensuite alimenter
   F01→F02→ANGLESMITH→F03→F04→F05→F06 (chaîne intacte).

## 5. Commandes de vérification rapide

```bash
# Depuis la racine du repo clone (ex: /tmp/opencode/perturabo)
cd MONDES_FORGES/CLIPPING/CAPTEURS/CODEBASE
python3 capteurs.py --scan-subjects --niche "Lakers basketball" --mode informatif --freshness brulant
# -> capture les signaux, appelle GLM 5.2, écrit OUT/ + EXPORT/, check-in ledger
```

- Le repo remote est `https://github.com/kioka8877-ux/PERTURABO` (main).
- En cas de divergence locale : `git pull --rebase origin main && git push`.

## 6. Rappels / pièges connus

- `.env.local` et `CONTRACTS/youtube_secrets.json` sont gitignorés —
  jamais committer une clé.
- pytrends nécessite urllib3 == 1.26.20 (sinon `TypeError:
  Retry.__init__() got an unexpected keyword argument 'method_whitelist'`).
- La clé YouTube (CONTRACTS/youtube_secrets.json) est valide et testée.
- IW_CUSTOS : nom canonique `CAPTEURS`, PAS `F00_CAPTEURS`.
