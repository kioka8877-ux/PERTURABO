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

> ✅ **MAJ 2026-08-15 (mode meme — commit `1e1e0b4`, poussé sur main)** :
> nouveau siège **`student debt`** (sujet S3 "payer sa dette avec des vidéos
> de chats"), marché US -25 ans, YouTube, langue anglais. Les 4 portes
> validées de bout en bout, la campagne est **CLÔTURÉE** :
> - Gate 0 : ancien siège `NBA_WESTBROOK` fermé + archivé dans
>   `ARCHIVUM/campaign/_archive_TS02_NBA_WESTBROOK/`. Nouveaux inputs meme :
>   `ARCHIVUM/campaign/keyword.txt` (`student debt`) + `directive.md`
>   (Campaign `STUDENT_DEBT_MEME`) + `reference_clip.json` placeholder
>   (`source_type: meme_keyword`).
> - Gate 1 : `capteurs.py --scan-meme --keyword "student debt"` → scan
>   `MEME-dee7c660` (youtube+trends+rss+reddit+suggest, **0 clip téléchargé**,
>   demande score 100, news fraîches < 4h). Reddit 403 non bloquant.
>   Sujet choisi par le Warsmith : S3 (cat videos, `youtube.com/watch?v=1st_IbSGI00`).
> - Gate 2 : ANGLESMITH `--sub-mode meme` → 5 angles (poignant/drôle/choc/
>   tendu/émerveillé, anti-spam OK, durée 5-7s) → `F02_TYRANT_CAMP/OUT/angles.json`.
> - Gate 3 : F04 premium **GLM 5.2 via NVIDIA** (clé re-injectée) → 5
>   `text_payload_A0X.json` (titres ≤ 6 mots, tweets ≤ 3 lignes, reactions
>   ≤ 4 mots, garde-fous vérifiés).
> - Gate 4 : F05 `packager.py --assemble --sub-mode meme` → pack
>   `LOGO-SIEGE-siege_20260815_195037` (5 videos, `meme_source.montage_guide_ref
>   = GUIDE_UTILISATION/04_MODE_MEME.md`) exporté
>   `EXPORT/production_pack_meme_student_debt.json` + summary `.md`
>   **→ visible OMNIS_WATCH sur GitHub (il ne lit PAS en local)**.
> - **Patchs meme-aware** (faits et poussés) :
>   `ORCHESTRATOR/CODEBASE/libs/gate_validator.py` (Gate 1 : skip F01/F02 si
>   `ARCHIVUM/campaign/keyword.txt` présent → vérifie scan F00) +
>   `PROFILES/logo/CONTRACTS/production_pack_schema_logo.json`
>   (enum `source_type` + `meme_keyword`, `celebrity_or_subject`/`niche`
>   nullables) — sans ces 2 patchs, le mode meme ne pouvait pas passer les
>   portes 1 et 4.
> - Ledger : `portes_validated: ['1','2','3','4']`, `campaign_status: closed`,
>   `packs_expedies: 1`.
> - **Reste à faire** : F06_TRACKER `tracker.py --post` quand OMNIS_WATCH aura
>   posté les 5 vidéos (vues 1h/24h, payout, learnings).

> ✅ **MAJ 2026-08-16 (format pack meme v2 — commits `b27fc63` + `f4a5197`,
> poussés sur main)** : le pack meme passe au **contrat LACRIMAE v2** (le
> schéma de LACRIMAE fait foi — c'est lui le consommateur final, pas le
> schéma PERTURABO). Restructuration complète :
> - **F04 COPYWRITER** : l'ordonnance meme produit désormais
>   `tweet{text, keywords_style}` + `text_emotion` + `duration_sec`
>   (plage 5-30, défaut 8) au lieu de `tweet_text`/`reaction_text`/
>   `duration_sec_range`. `keywords_style` normalisé : `[{word, color}]`
>   avec `color ∈ vert|rouge` (vert = valeur, rouge = danger), mots absents
>   du tweet retirés silencieusement. Hérésies et render `.md` alignés.
> - **F05 PACKAGER** : la vidéo meme ne porte plus que les champs
>   consommés par OMNIS_WATCH — `meme`, `tweet{text, keywords_style}`,
>   `text_emotion`, `emotion`, `duration_sec`. `cut`/`metadata`/
>   `on_screen_text`/`logo_placement` sont **ignorés par LACRIMAE** (retirés
>   du mode meme, conservés pour informatif/humour). Mapping meme initial :
>   A01+A02+A03 → `meme_1`, A04+A05 → `meme_2` (renommés en `meme_001`/
>   `meme_002` en v2.5 — cf. MAJ suivante). En-tête `meme_source`
>   garde `montage_guide_ref: GUIDE_UTILISATION/04_MODE_MEME.md`, retire
>   `duration_range_sec`. Summary `.md` adapté (colonne Meme/Durée).
> - **Schéma** `production_pack_schema_logo.json` : video item allégé
>   (required `video_index`/`angle_id`/`title`), ajout `meme`
>   (enum initial meme_1/meme_2 → meme_001/002 en v2.5), `tweet{text,
>   keywords_style}`, `text_emotion`, `duration_sec` (5-30). Champs v1 retirés.
> - **Pack `EXPORT/production_pack_meme_student_debt.json`** : les 5 vidéos
>   ont été **converties en v2 sans re-run** (patch direct, pas de relance
>   GLM) — A01-A03 → `meme_1`, A04-A05 → `meme_2` (renommés meme_001/002 en
>   v2.5), `keywords_style` sobre (vert sur les victoires type "wiped $47K",
>   rouge sur les dangers), `duration_sec: 8`. Summary `.md` aligné.
>   **Validation schéma : 0 erreur.**
> - Le `--finalize` de F05 échoue encore sur l'artefact build stale de
>   `F05_PACKAGER/OUT/` (gitignoré, non committé) — sans impact livrable.
> - **Reste à faire** : F06_TRACKER `tracker.py --post` quand OMNIS_WATCH aura
>   posté les 5 vidéos (vues 1h/24h, payout, learnings).

> ✅ **MAJ 2026-08-16 (v2.5 note LACRIMAE — commit `2f73462`, poussé sur main)** :
> LACRIMAE (successeur d'OMNIS_WATCH) a renvoyé la note
> `GUIDE_UTILISATION/05_NOTE_PERTURABO_PACK_MEME.md` avec une **section 4
> dédiée aux couleurs** — corrections v2.5 :
> - **Règle 1 — format** : `tweet.keywords_style` = **DICT** `{"green": [...],
>   "red": [...]}` (clés anglaises). Une liste `[{word, color}]` (v1) →
>   **aucune couleur** (PERTURABO ne produit plus jamais une liste).
> - **Règle 2 — mots** : chaque entrée = **un mot seul** présent mot à mot
>   dans `tweet.text` (ponctuation ignorée). Les phrases multi-mots
>   ("student loans", "owe more") ne matchent jamais → découpées en mots
>   simples (`loans`, `owe`).
> - **2e blocage (levé)** : `meme` doit pointer `meme_001` / `meme_002`
>   (fichiers existants de la méméthèque LACRIMAE), **pas** `meme_1`/`meme_2`.
> - **F04** : `_normalize_keywords_style(kws_style, tweet_text)` réécrit
>   (dict green/red, mots seuls filtrés sur les tokens du tweet), mission +
>   output_schema alignés, `_render_keywords_md` adapté au dict.
> - **F05** : `_meme_for_angle` → `meme_001`/`meme_002` ; garde-fou
>   `_keywords_v2` (liste v1 → dict vide). Schéma : enum `meme_001/002`,
>   `keywords_style` dict green/red.
> - **Pack EXPORT** : les 5 vidéos patchées **sans re-run** (ex. A01 :
>   `{"green": [], "red": ["loans", "interest", "owe"]}` ; A03 :
>   `{"green": ["wiped"], "red": ["debt"]}`). Summary `.md` aligné
>   (meme_001/002). **Validation schéma v2.5 : 0 erreur.**
> - Lien pack et note vérifiés HTTP 200 (raw GitHub).
> - **Reste à faire** : F06_TRACKER `tracker.py --post` quand OMNIS_WATCH aura
>   posté les 5 vidéos (vues 1h/24h, payout, learnings).

## 4bis. Push chaîne actu `cocktail_meme` + description 3 blocs obligatoire

> Création de la chaîne **Daily Shake** (`@memecocktail`, slug `cocktail_meme`)
> dans `MONDES_FORGES/CLIPPING/ARCHIVUM/channels/` (modèle `starflash_us`) :
> meme quotidien sur l'actu US **non-politique** (pop-culture, sport, tech,
> entertainment). Zéro politique. Avertissement **non-monétisation**
> (placements de produit / brand partnerships) dans la description de chaîne.

- **Squelette chaîne** (`ARCHIVUM/channels/cocktail_meme/`) : `identity.json`
  (profile_mode meme, warmup incomplete), `channel_description.md`,
  `channel_tags.md` (15 tags), `description_base_paragraph.md`,
  `performance.json`, `branding/` (banner 2560×1440 + avatar 800×800,
  SVG+PNG). Lien campagne → compte : `ARCHIVUM/campaign/channel.txt`
  (contenu : `cocktail_meme`).
- **Injection F04** (`copywriter.py`) : `_channel_base_paragraph()` lit
  `campaign/channel.txt` → `channels/<slug>/description_base_paragraph.md`
  et concatène le bloc (avertissement + fair use) en fin de
  `metadata.description` de chaque vidéo.
- **Pack vidéo = 4 blocs obligatoires** (contrat Warsmith) dans
  `metadata.description` : 1) résumé du tweet 2-3 lignes (produit par GLM),
  2) note fair use (Section 107), 3) avertissement non-monétisation,
  4) ligne de 15 hashtags `#`. `metadata.tags` = 15 tags préfixés `#`.
- **F04** : `_normalize_tags()` (préfixe `#`, dédoublonnage, max 15, ignore
  tags multi-mots) + ligne hashtags en fin de description. Le prompt ne
  demande plus que le résumé au modèle (fair use + avertissement injectés).
- **F05** (`packager.py`) : `_logo_video_asset` écrit désormais
  `metadata`/description en mode meme (manquant sur le pack précédent) ;
  fallback = résumé + fair use + avertissement + hashtags ; normalisation
  tags idem. `cmd_finalize_logo` bloque si une vidéo est sans description.
- **Schéma** `production_pack_schema_logo.json` : `tags.maxItems` 12 → 15,
  items `pattern: "^#"`. **Validateur** : support du `pattern` regex.
- **Métadonnées pack student debt régénérées** (commit `cc85df8`) : chaque
  vidéo du pack `EXPORT/production_pack_meme_student_debt.json` porte
  désormais `metadata` (title, description 4 blocs, tags 15 `#`). Tags
  complétés depuis `channel_tags.md` du compte actif via `_channel_tags()`
  (accepte les tags multi-mots). Validation schéma : 0 erreur.

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
