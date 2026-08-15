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
  `MONDES_FORGES/CLIPPING/F00_CAPTEURS/CODEBASE/libs/` :
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

> ⚠️ **MAJ 2026-08-14** : renommage `CAPTEURS` → `F00_CAPTEURS` fait et
> poussé (commit `bd05444`). Nom canonique IW_CUSTOS inchangé = `CAPTEURS`.
> CI-DESSOUS : erreurs constatées lors du test `--scan-subjects --niche NBA`.

> ✅ **MAJ 2026-08-14 (suite)** : `--deliver-subject <index>` implémenté
> (commit à venir). Sujet n°1 du scan `F00-5581179c` (Westbrook tribute
> backlash) livré dans `ARCHIVUM/campaign/` :
> `directive.md` (Campaign ID `NBA_WESTBROOK`) + `article_source.json` +
> `reference_clip.json`. Ledger mis à jour (`campaign_id`, `inputs_warsmith`).
> Prochaine étape : **F01_SCOUT --prepare / --auto** sur cette directive.

> ✅ **MAJ 2026-08-14 (fin de chaîne)** : siège `NBA_WESTBROOK` exécuté de
> bout en bout : F01 (specimen) → F02 (verdict GO) → ANGLESMITH (5 angles)
> → F03 (5 specimens) → F04 (5 text_payloads, premium GLM + 2 forgés Oracle
> A04/A05 en backup suite rate-limit NVIDIA) → F05 (5 production_packs validés).
> Packs exportés dans `EXPORT/production_pack_logo.json` + `packs_index.json`.
> Ledger réinitialisé pour le siège NBA_WESTBROOK (portes vidées).
> ⚠️ Pièges du sandbox : YouTube bloque les transcripts (IP cloud) → F03
> sélectionne sans segments ; NVIDIA rate-limit 429 fréquent → backup Oracle.

### 4.0 ERREURS CONSTATÉES (à traiter en premier dans le nouveau sandbox)

1. **Synthèse GLM timeout** : `premium_client.py:195` hardcode
   `urlopen(..., timeout=120)`. La synthèse 5 sujets dépasse 120s sur
   NVIDIA/GLM-5.2 → `TimeoutError: The read operation timed out`. L'API
   NVIDIA répond pourtant en ~0.2s (test `GET /v1/models` = 200).
   → **CORRIGÉ** : timeout configurable `timeout_seconds` (défaut 240s)
   dans `premium_client._fetch()` + champ ajouté à
   `copywriter_secrets.example.json` et `copywriter_secrets.json`.
2. **pytrends absent** : `ModuleNotFoundError: No module named 'pytrends'`
   (signaux Trends dégradés en `pytrends_absent`). Installer
   `pytrends` + `urllib3==1.26.20` (piège connu, cf. §6).
   → **CORRIGÉ dans le sandbox** (pip install, urllib3 1.26.20 testé OK
   avec requests). À refaire dans chaque nouveau sandbox.
3. **Clé YouTube absente** : `CONTRACTS/youtube_secrets.json` manquant dans
   ce sandbox → signal "vues réelles" YouTube skippé. Ré-injecter la clé.
4. **Clé NVIDIA à re-injecter** : `CLIPPING_PREMIUM_API_KEY` dans `.env.local`
   (gitignored). Présente dans l'historique du chat.
   La config réelle `CONTRACTS/copywriter_secrets.json` (gitignored) :
   `model_id=z-ai/glm-5.2`, `provider=other`,
   `base_url=https://integrate.api.nvidia.com/v1`,
   `max_tokens_per_call=8192`.
5. **JSON GLM tronqué** : à 4096 tokens max, GLM coupe le JSON → erreur
   `Expecting ',' delimiter` dans `f00_premium_synth.synthesize()`.
   → **CORRIGÉ** : `max_tokens_per_call` passé à 8192 (config + example).

### 4.0.1 État du test NBA (2026-08-14)

- `--scan-subjects --niche NBA --mode informatif --freshness brulant` :
  **runs 1-2 en cours de debug** (timeout 120s puis JSON tronqué 4096),
  **run 3 RÉUSSI** : scan `F00-e55a8dbf`, 5 sujets générés (scores 7-9),
  export committé `EXPORT/subjects_proposal.json`+`.md`, check-in
  IW_CUSTOS `capteurs: done` (commit `5a258b9`).
- **Verdict** : les fixs (timeout 240s configurable + max_tokens 8192)
  règlent le problème de synthèse. Prochaine étape dans le nouveau
  sandbox : relancer le scan si besoin, puis `--deliver-subject`.

### 4.0.2 Autres refs déjà faites (ne pas refaire)

- Renommage dossier `F00_CAPTEURS/` + `PROFILES/logo/F00_CAPTEURS_IN/`.
- CLI vérifié : `--help`, `premium_client.require_config()` OK.

### 4.0.3 AMÉLIORATIONS "vision globale" implémentées (2026-08-14)

Ajout du "Perturabo lit toutes les cartes" au scan de sujets :

1. **Score mécanique** : chaque sujet porte `score_mecanique` (0-100, calcul
   déterministe dans `f00_virality_scorer.normalize_metrics` + `score_subject`)
   à côté du `score_10` GLM. Le tableau MD montre les DEUX scores.
2. **Baseline historique** : `TRACKING/f00_baseline.json` archive les 20
   derniers scans (par sujet : score, fraîcheur, vues, demande, tendance,
   couverture, diversité). Un résumé statistique (médiane/min/max par métrique)
   est injecté dans le prompt GLM (`=== BASELINE HISTORIQUE ===`) pour calibrer
   les notes — le scoreur a enfin une vision globale.
3. **Diversité de sources** : `source_diversity` = domaines distincts des URLs
   (ex: google.com, youtube.com), affiché dans le tableau.
4. **Traçabilité** : `metric_proof` mappe chaque métrique au capteur qui l'a
   produite (vues -> youtube, demande -> suggest, fraîcheur -> rss…).

Scan de validation : `F00-5581179c` (NBA, 5 sujets, score GLM ET mécanique OK).
⚠️ À noter : les sujets purement YouTube (vidéo existante à fort vues, sans
article RSS) voient leur score mécanique re-pondéré sur vues+demande seuls
(ex: "Trampoline dunk" MECA 98.4) — comportement voulu du re-norm, à surveiller.

## 4. Ce qui reste à faire (travail suivant)

1. **Choisir le sujet** : le Warsmith choisit UN des 5 sujets de
   `EXPORT/subjects_proposal.json` (pas de top-1 automatique — porte dédiée).
   → **FAIT** : sujet n°1 (Westbrook) livré via `--deliver-subject 1`.
2. **Commande de livraison du sujet choisi** : implémenter une nouvelle
   commande (ex. `capteurs.py --deliver-subject <index>`) qui écrit dans
   `ARCHIVUM/campaign/` :
   - `directive.md`
   - `article_source.json`
   - `reference_clip.json`
   (puis push GitHub + mise à jour ledger).
   → **FAIT** : `--deliver-subject <index>` opérationnel (voir §4 MAJ).
3. **Enchaîner sur F01** : lancer `F01_SCOUT --prepare/--auto` puis
   F02→ANGLESMITH→F03→F04→F05→F06 sur la directive `NBA_WESTBROOK`.
   → **FAIT** : chaîne complète F01→F05, packs dans `EXPORT/`.
4. Optionnel : générer une proposition en mode `--hot` (sans niche) et en
   mode `--mode humour` pour valider les 2 sous-modes.
5. Intégration chaîne existante : le sujet choisi doit ensuite alimenter
   F01→F02→ANGLESMITH→F03→F04→F05→F06 (chaîne intacte).
   → **FAIT** (F06_TRACKER reste à faire : posts, vues, payout).

> ⚠️ **MAJ 2026-08-15 (cuts 7s — commit `77cb715`)** : les 5 clips des packs
> humour ET informatif sont désormais à **7s chacun** (windows séquentielles
> dans la vidéo `5XJUyMct2eQ`) :
> A01 0-7s / A02 7-14s / A03 14-21s / A04 21-28s / A05 28-35s.
> Fournis dans `ARCHIVUM/campaign/cuts.json` (`cut_source: operator`) et
> injectés dans `EXPORT/westbrook_pack_logo.json` (informatif) +
> `EXPORT/westbrook_pack_logo_humour.json` (humour).
> ⚠️ Durée réelle de la vidéo non vérifiable (pas de clé YouTube/yt-dlp) —
> les windows sont arbitraires, à ajuster si la vidéo fait <35s.

> ⚠️ **MAJ 2026-08-15 (mode humour)** : la chaîne F01→F05 est REFAIte en
> humour (pack `LOGO-NBA_WESTBROOK` humour, 5 videos). Reste à faire :
>
> 1. **F06_TRACKER** : `tracker.py --post` pour expédier le pack humour vers
>    OMNIS_WATCH (le checkpoint F06 a été signalé par l'orchestrateur après
>    la Porte 4).
> 2. **Cuts vidéo** : FAIT — `ARCHIVUM/campaign/cuts.json` fourni (7s par
>    clip, A01 0-7s → A05 28-35s), injecté dans les packs humour + informatif
>    (commit `77cb715`).
> 3. **`joke_source` à compléter** : dans ce run humour, `joke_source` est
>    null (pas de fichier blague fourni) — l'humour est porté par le spin
>    Warsmith + les payloads F04. Si l'on veut une blague dédiée par angle,
>    fournir `ARCHIVUM/campaign/joke_source.json`.
> 4. **Clé premium NVIDIA** (`CLIPPING_PREMIUM_API_KEY` via `.env.local`,
>    gitignoré) à ré-injecter dans tout nouveau sandbox, sinon F04 repasse
>    en mode Oracle.
> 5. Prochaine itération possible : générer un pack `--mode humour` sur un
>    autre sujet du scan, ou valider le pack humour existant auprès du
>    Warsmith avant diffusion.

> ✅ **MAJ 2026-08-15 (mode humour — commit `be44729`, poussé sur main)** :
> le siège NBA_WESTBROOK a été régénéré en **mode humour** de bout en bout
> (les 4 portes validées) :
> - Porte 1 : F01 specimen + F02 verdict GO.
> - Porte 2 : ANGLESMITH 5 angles forgés avec le **spin humour** du Warsmith
>   ("la dette étudiante et la calvitie qui s'unissent pour augmenter mon
>   stress"), enregistré dans `liber_clipping.json -> inputs_warsmith.spin_humour`.
> - Porte 3 : F04 humour A01-A05 — clé premium ABSENTE dans ce sandbox →
>   **mode Oracle** (raws forgés à la main dans `OUT/text_payload_raw_A0*.json`,
>   puis ordonnance/finalize). Contextes reconfigurés `--sub-mode humour`.
> - Porte 4 : pack `LOGO-NBA_WESTBROOK-siege_20260810_205150` (5 videos,
>   `cut_source: operator`).
> - Code F04 étendu : `_load_spin_humour()` dans `context_builder.py` (source
>   de vérité = ledger) + injection `humour_spin` dans le prompt de
>   `copywriter.py` quand `sub_mode == humour`.
> - Export : `EXPORT/westbrook_pack_logo_humour.json` +
>   `EXPORT/packs_index_humour.json` + `EXPORT/westbrook_pack_humour_apercu.md`.

## 5. Commandes de vérification rapide

```bash
# Depuis la racine du repo clone (ex: /tmp/opencode/perturabo)
cd MONDES_FORGES/CLIPPING/F00_CAPTEURS/CODEBASE
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
