# F04_COPYWRITER â€” TRACKING.md

> *"Le titre est 90% du travail. Le reste suit. Une forteresse tombe par ses mots, pas par sa pierre."*
> *FrÃ©gate lourde. FrÃ©gate singuliÃ¨re. Elle ne suit pas le pattern 3-phases â€” elle parle direct au modÃ¨le premium, et l'IRON ordonnance seulement.*

---

## RÃ”LE

F04_COPYWRITER est la **frÃ©gate lourde** de la Porte 3. Elle forge le **text_payload** complet pour chaque angle :
- **3 titres calibrÃ©s** (pas 1, pas 5) â€” chacun scorÃ© sur `platform_fit`, `market_fit`, `hook_type`
- **Un paragraphe reframing** (2 lignes max) â€” la transformation de sens optionnelle
- **Caption** (sous-titre d'ouverture / description courte)
- **Hashtags** â€” 3 strates (large + moyen + niche)
- **On-screen text** (phrase affichÃ©e Ã  une keyframe prÃ©cise dans le clip)
- **CTA text** â€” jamais "abonne-toi", toujours subtil ("commente X", "suis pour la suite")

La frÃ©gate produit **deux outputs** par angle :
1. `text_payload.json` â€” format strict, consommÃ© par l'Oracle OMNIS_WATCH
2. `text_payload.md` â€” format lisible opÃ©rateur, prÃªt Ã  copier-coller au moment de poster

---

## SINGULARITÃ‰ â€” RUPTURE DU PATTERN 3-PHASES

Contrairement aux autres frÃ©gates qui dialoguent avec l'IRON (Claude sandbox) en 3 phases (prepare â†’ IRON â†’ finalize), C04 **contourne** ce pattern :

```
Phase A : setup_context       (l'IRON sandbox rassemble l'ARCHIVUM pertinent)
Phase B : premium_generation  (la frÃ©gate parle DIRECT au modÃ¨le premium
                                via clÃ© API dÃ©diÃ©e â€” aucun IRON 
                                intermÃ©diaire pour la gÃ©nÃ©ration)
Phase C : iron_ordonnancing    (l'IRON sandbox rÃ©cupÃ¨re la sortie premium,
                                valide cohÃ©rence, classe, tag, vÃ©rrouille)
Phase D : finalize + ledger    (IW_CUSTOS enregistre â€” cohÃ©rence frÃ©gates)
```

**Justification** : le texte porte 90% du lift viral (Ogilvy : "The reader isn't going to read your body copy unless your headline wins"). Le sandbox bridÃ© ne suffit pas. Le modÃ¨le premium gÃ©nÃ¨re, l'IRON sandbox ordonnance et enregistre dans le ledger pour garder la cohÃ©rence du systÃ¨me.

---

## INPUTS

| Input | Source | Format | Obligatoire |
|---|---|---|---|
| `angles.json` | ANGLESMITH | JSON | âœ… |
| `campaign_verdict.json` | F02_TYRANT_CAMP | JSON | âœ… |
| `source_specimen_<angle>.json` | F03_SOURCE_HUNTER (un par angle) | JSON | âœ… (N specimens) |
| `platform_target` | Warsmith | string | âœ… |
| `market_target` | Warsmith | string | âœ… |
| ClÃ© API premium | `CONTRACTS/copywriter_secrets.json` (gitignored) â€” nom env var `CLIPPING_PREMIUM_API_KEY` | env | âœ… |

ARCHIVUM injectÃ© dans le prompt (Phase A) :
- `ARCHIVUM/copywriting/hooks_library.md`
- `ARCHIVUM/copywriting/title_formulas.md`
- `ARCHIVUM/copywriting/caption_frameworks.md`
- `ARCHIVUM/copywriting/subliminal_language.md`
- `ARCHIVUM/copywriting/slang_by_market.md`
- `ARCHIVUM/copywriting/hashtags_research.md`
- `ARCHIVUM/copywriting/on_screen_text_patterns.md`
- `ARCHIVUM/copywriting/reference_clips_titles/` (exemples annotÃ©s)
- `ARCHIVUM/rules/clipping_rules.md`
- `ARCHIVUM/rules/whop_rules.md`
- `ARCHIVUM/rules/platform_{plateforme}.md`
- `ARCHIVUM/platform_generator/{plateforme}_profile.md`
- `ARCHIVUM/market_generator/{marchÃ©}.md`
- `ARCHIVUM/angles/angle_patterns.json`
- `ARCHIVUM/angles/angle_performance.json` (poids nul si < 50 packs)
- `ARCHIVUM/demons/<demon_id>.json` (exemples de titres qui ont marchÃ©)
- `ARCHIVUM/knowledge_base/` (sites, docs, transcripts â€” tout ce qui marche en clipping)
- `ARCHIVUM/learnings/learnings.json` (perf passÃ©e)
- `CONTRACTS/copywriting_doctrine.md` â€” socle doctrinal
- `CONTRACTS/copywriter_systemprompt.md` â€” system prompt figÃ© (gÃ©nÃ©rÃ© par premium Ã  l'init)
- `CONTRACTS/anti_bullshit.md` (liens core)

---

## OUTPUTS

### `OUT/text_payload_<angle_id>.json` (1 par angle)

```json
{
  "campaign_id": "...",
  "angle_id": "...",
  "angle_family": "...",
  "emotion_mode": "...",
  "platform_target": "youtube|tiktok|instagram",
  "market_target": "...",
  
  "titles": [
    {
      "rank": 1,
      "text": "...",
      "platform_fit": <0-10>,
      "market_fit": <0-10>,
      "hook_type": "stat_choc|question|declaration|mystery|contradiction|cible_naming",
      "rationale": "Pourquoi ce titre"
    },
    { "rank": 2, ... },
    { "rank": 3, ... }
  ],
  
  "paragraph": {
    "text": "...",                  // 2 lignes max
    "recommendation": "use|skip",    // F04_COPYWRITER propose
    "override_omniswatch": null,     // Oracle OMNIS_WATCH peut override
    "final_operator": null          // Warsmith a le dernier mot au moment de poster
    // 3 niveaux de veto, dans cet ordre
  },
  
  "caption": "...",
  "hashtags": ["#...", "#...", "#..."],
  "on_screen_text": "..." | null,
  "cta_text": "...",
  
  "compliance": {
    "disclosure": "#ad",
    "ftc_required": true
  },
  
  "check_in_iw_custos": "<ISO8601>"
}
```

### `OUT/text_payload_<angle_id>.md` (1 par angle â€” lisible opÃ©rateur)

```
â•â•â• ANGLE X/N â•â•â•
ANGLE : <angle_family>
Ã‰MOTION : <emotion_mode>
ENGAGEMENT : <engagement_type>
PLATEFORME : <platform_target>
MARCHÃ‰ : <market_target>

â”€â”€ TITRES (3 calibrÃ©s) â”€â”€
1. <titre 1>
   [platform_fit: X/10, market_fit: Y/10, hook: Z]
2. <titre 2>
   [...]
3. <titre 3>
   [...]

â”€â”€ PARAGRAPHE (optionnel, 2 lignes) â”€â”€
<texte du paragraphe>
 reco: <use|skip>  |  oracle: <null|skip>  |  operateur: <null|use|skip>

â”€â”€ CAPTION â”€â”€
<caption>

â”€â”€ HASHTAGS â”€â”€
#... #... #ad

â”€â”€ ON-SCREEN TEXT (keyframe optionnelle) â”€â”€
<texte>

â”€â”€ CTA â”€â”€
<cta_text>
```

Ce `.md` est ce que le Warsmith lise au moment de poster. Pas le JSON.

---

## SYSTEM PROMPT â€” INIT Ã€ NE PAS REFAIRE

Le `CONTRACTS/copywriter_systemprompt.md` est **gÃ©nÃ©rÃ© par le modÃ¨le premium lui-mÃªme** Ã  la premiÃ¨re initialisation de la frÃ©gate. ProcÃ©dure (one-time) :

1. Le Warsmith alimente le prompt d'init avec :
   - La doctrine copywriting (10 sections, Ã  remplir par le Warsmith â€” voir `CONTRACTS/copywriting_doctrine.md`)
   - Un exemple de bon text_payload JSON cible
   - La liste des 8 sous-dossiers de `ARCHIVUM/copywriting/`
2. Le modÃ¨le premium produit le system prompt final, qui sera figÃ© dans `copywriter_systemprompt.md`.
3. Pour toutes les exÃ©cutions suivantes (Phase B), ce system prompt est utilisÃ© tel quel.

**Ne pas rÃ©gÃ©nÃ©rer le system prompt Ã  chaque campagne â€” il est figÃ© aprÃ¨s l'init.**

---

## CLÃ‰ API PRÃ‰MIUM

La clÃ© API de F04_COPYWRITER est la **plus puissante** que le Warsmith possÃ¨de. Elle est stockÃ©e dans :
- `CONTRACTS/copywriter_secrets.json` â€” fichier **gitignored**, ne contient que la rÃ©fÃ©rence Ã  la variable d'env, jamais la clÃ© en clair
- Variable d'env : `CLIPPING_PREMIUM_API_KEY` (sur la machine du Warsmith)

Le fichier public (commitÃ©) est `CONTRACTS/copywriter_secrets.example.json` qui documente la structure attendue sans exposer aucune clÃ©.

---

## PATTERN D'EXÃ‰CUTION â€” 4 PHASES

### Phase A â€” setup_context

```
python copywriter.py --setup-context --angle <angle_id> --platform <p> --market <m>
```

L'IRON (sandbox Claude) rassemble :
- Le contenu de `ARCHIVUM/copywriting/*` (les 8 sous-dossiers)
- `ARCHIVUM/rules/*`
- `ARCHIVUM/platform_generator/{p}_profile.md`
- `ARCHIVUM/market_generator/{m}.md`
- `ARCHIVUM/angles/angle_patterns.json` + `angle_performance.json`
- `ARCHIVUM/demons/*` (exemples de titres gagnants)
- `ARCHIVUM/knowledge_base/*` (sites, docs, transcripts)
- `ARCHIVUM/learnings/learnings.json`
- `CONTRACTS/copywriting_doctrine.md`
- `CONTRACTS/copywriter_systemprompt.md`
- `CONTRACTS/anti_bullshit.md` (liens core)
- L'angle actif (depuis ANGLESMITH)
- Le specimen source (depuis F03_SOURCE_HUNTER)

â†’ Output : `IN/copywriter_context_<angle_id>.json` (contexte strukturÃ© pour le premium)

### Phase B â€” premium_generation

```
python copywriter.py --generate --angle <angle_id>
# Lit CLIPPING_PREMIUM_API_KEY depuis l'env
# Dialog DIRECT avec le modÃ¨le premium (pas d'IRON intermÃ©diaire)
```

La frÃ©gate parle directement au modÃ¨le premium (via son SDK dÃ©diÃ©). Le system prompt est `copywriter_systemprompt.md`. Le user prompt est le contexte Phase A + la mission "forge 3 titres + paragraphe + caption + hashtags + on-screen pour cet angle".

â†’ Output : `OUT/text_payload_raw_<angle_id>.json` (sortie brute du premium)

### Phase C â€” iron_ordonnancing

```
python copywriter.py --ordonnance --angle <angle_id>
# L'IRON (sandbox Claude) rÃ©cupÃ¨re le raw premium
```

L'IRON :
- Valide la cohÃ©rence (pas de contradiction, pas d'hallucination de hook_type)
- Classe les 3 titres par `rank` (1, 2, 3) selon `platform_fit + market_fit + hook_strength`
- Tag le `paragraph.recommendation` ("use" ou "skip" selon pertinence vs angle)
- VÃ©rifie FTC compliance (disclosure "#ad" prÃ©sent dans caption)
- VÃ©rifie anti-bullshit (pas de "abonne-toi", pas de clickbait pur)

â†’ Output : `OUT/text_payload_<angle_id>.json` (ordonnancÃ©)

### Phase D â€” finalize + ledger

```
python copywriter.py --finalize --angle <angle_id>
```

- Check-in `IW_CUSTOS.py` (statut C04 = done pour cet angle)
- Copie le `.json` + gÃ©nÃ¨re le `.md` lisible opÃ©rateur
- Met Ã  jour `liber_clipping.json`

Pour N angles â†’ rÃ©pÃ©ter Phase A â†’ B â†’ C â†’ D pour chaque. Peut se batcher en // (Phase A en sÃ©rie, B en //, etc.).

---

## CONTRATS RÃ‰FÃ‰RENCÃ‰S

Voir la liste exhaustive ci-dessus dans "ARCHIVUM injectÃ© dans le prompt". La frÃ©gate lit TOUT l'ARCHIVUM pertinent pour le copywriting clipping â€” c'est sa singularitÃ©. Elle ne invente pas depuis zÃ©ro ; elle synthÃ©tise depuis tout ce que PERTURABO sait.

---

## DÃ‰PENDANCES

- **Amont** :
  - F02_TYRANT_CAMP (verdict, squelette rÃ©fÃ©rence)
  - F03_SOURCE_HUNTER (source specimen + segments)
  - ANGLESMITH (angle actif)
  - ARCHIVUM complet (la matiÃ¨re Ã  synthÃ©tiser)
- **Downstream** :
  - F05_PACKAGER (intÃ¨gre `text_payload.json` dans `production_pack.json`)
  - Oracle OMNIS_WATCH (lit `text_payload.json` â†’ peut `override_omniswatch` du paragraphe)
  - Warsmith (lit `text_payload.md` au moment de poster â†’ `final_operator`)

---

## 3 NIVEAUX DE VETO DU PARAGRAPHE

Le `paragraph` a une chaÃ®ne de dÃ©cision stricte :

1. **`recommendation`** (F04_COPYWIRITER) â€” en Phase C, l'IRON tag le paragraphe `"use"` ou `"skip"`. Une reco "skip" ne signifie pas suppression â€” signifie "Ã  utiliser uniquement Ã  des fins de rÃ©vision possible".
2. **`override_omniswatch`** (Oracle OMNIS_WATCH, plus tard dans la prod) â€” initialement `null`. Si l'Oracle estime que le rendu rend le paragraphe redondant ou que le clip n'a pas besoin de paragraphe, il met `"skip"`.
3. **`final_operator`** (Warsmith, au moment de poster) â€” initialement `null`. Le Warsmith a le dernier mot : `"use"` ou `"skip"` Ã©crase les 2 dÃ©cisions prÃ©cÃ©dentes.

RÃ¨gle de rÃ©solution : si `final_operator` est non-null, il gagne. Sinon, si `override_omniswatch` est non-null, il gagne. Sinon, `recommendation` s'applique.

---

## HÃ‰RÃ‰SIES

- âŒ "Abonne-toi" / "Like et partage" / "Swipe up" dans CTA / caption / on-screen
- âŒ Clickbait sans payoff : le titre doit livrer dans la vidÃ©o, pas seulement teaser
- âŒ Anti-re ÐºÐ¾Ð½Ð´ition : transformer une interview calme en "BEEF EXPLOSIF" = mensonge sur le contenu source (cf. `CONTRACTS/anti_bullshit.md`)
- âŒ Paragraphe > 2 lignes (la longueur-courte-longue est morte)
- âŒ Hashtags sans strate niche (les hashtags "large + moyen" ne suffisent pas â€” faut la strate niche spÃ©cifique)
- âŒ RÃ©utiliser le system prompt sans initialisationä¸€å®š (le system prompt est figÃ© aprÃ¨s init, mais doit Ãªtre initialisÃ© une fois)
- âŒ Passer par l'IRON pour la gÃ©nÃ©ration (Phase B = premium direct, l'IRON intervient seulement en Phase C pour ordonnancer)

---

## STATUT

| Phase | Ã‰tat | Notes |
|---|---|---|
| Arborescence crÃ©Ã©e | âœ… | |
| TRACKING.md rÃ©digÃ© | âœ… | Ce fichier |
| Code Python implÃ©mentÃ© | âŒ | Ã€ implÃ©menter |
| `copywriter.py` | âŒ | Orchestrator (4 phases distinguÃ©es â€” pas le mÃªme script que les autres frÃ©gates) |
| `libs/context_builder.py` | âŒ | Phase A â€” assemble l'ARCHIVUM dans l'IN/context.json |
| `libs/premium_client.py` | âŒ | Phase B â€” client SDK modÃ¨le premium (clÃ© via env var) |
| `libs/iron_ordonnancer.py` | âŒ | Phase C â€” appel IRON sandbox pour validation + classement |
| `libs/md_renderer.py` | âŒ | Phase D â€” gÃ©nÃ¨re le `.md` lisible opÃ©rateur depuis le `.json` |
| `libs/compliance_checker.py` | âŒ | VÃ©rifie FTC + anti-bullshit |
| `requirements_c04.txt` | âŒ | SDK modÃ¨le premium + sdk IRON + PyYAML si besoin |
| `CONTRACTS/copywriting_doctrine.md` | squelette âœ…, contenu âŒ | Ã€ remplir par le Warsmith (10 sections) |
| `CONTRACTS/copywriter_systemprompt.md` | placeholder âœ…, contenu âŒ | Ã€ gÃ©nÃ©rer par premium Ã  l'init (one-time) |

*Fer au-dedans, Fer au-dehors. Le titre ouvre la brÃ¨che, le paragraphe la tient, le loop verrouille la victoire.*
