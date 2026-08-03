# MONDE FORGE CLIPPING

> *"Une campagne est une forteresse. Un angle d'attaque est un plan de siÃ¨ge. Le texte est l'artillerie qui ouvre la brÃ¨che."*

---

## POSITIONNEMENT

PERTURABO/CLIPPING = le QG des campagnes **Whop Content Rewards**.

```
PERTURABO/CLIPPING       produit : briefs, angles, textes, directives (JSON/MD)
         â”‚
         â–¼
OMNIS_WATCH              exÃ©cute : coupe, reframe, rendu, coloring, camouflage
         â”‚
         â–¼
Clips postÃ©s â†’ soumis Whop <1h â†’ CPM (vues vÃ©rifiÃ©es)
```

Le forge CLIPPING ne touche **jamais** une vidÃ©o. Il dÃ©cide **quoi** clipper, sous **quel angle**, avec **quel texte** â€” et livre Ã  OMNIS_WATCH un `production_pack.json` prÃªt Ã  consommer.

La sÃ©paration des rÃ´les est sacrÃ©e :
- PERTURABO = **quoi raconter** (stratÃ©gie + copywriting)
- OMNIS_WATCH = **comment couper/rendre** (tactique + production)
- L'opÃ©rateur humain = **poster + soumettre Whop** (derniÃ¨re porte)

---

## LES 4 INPUTS DU WARSITH

```
1. Doc directif de la campagne (goal doc Whop â€” tout est dedans)
2. Clip de rÃ©fÃ©rence (celui qui a percÃ©, fourni par la campagne)
3. Plateforme cible (YouTube / TikTok / Instagram)
4. MarchÃ© cible (ex : US / Anglais / Jeune)

PERTURABO demande : "Combien d'angles d'attaque ?"
   â†’ N â†’ N plans de siÃ¨ge â†’ N production packs â†’ N vidÃ©os
```

Chaque pack = **1 vidÃ©o pour 1 plateforme pour 1 marchÃ©**. Pas de multi-plateforme par pack.

---

## LES 4 PORTES

| Porte | FrÃ©gates mobilisÃ©es | Produit | Validateur |
|---|---|---|---|
| 1 | F02_TYRANT_CAMP (rÃ©actif + prospectif) | `verdict.json` (GO/NO-GO + `blue_ocean_unlocked`) | Warsmith |
| 2 | ANGLESMITH (via C02 estratÃ©gia) | `angles.json` (N angles sur direct + ocÃ©an bleu) | Warsmith |
| 3 | F03_SOURCE_HUNTER + F04_COPYWRITER | `source_specimen.json` + `text_payload.json` + `.md` | Warsmith + IRON ordonnancement |
| 4 | F05_PACKAGER | N `production_pack.json` â†’ OMNIS_WATCH | Warsmith |

`F01_SCOUT` alimente les portes 1-2 (assets campagne). `F06_TRACKER` active la checklist aprÃ¨s Porte 4 et nourrit `learnings.json`. `CAPTEURS` s'exÃ©cute **avant** Porte 1 sur commande Warsmith uniquement.

---

## LES FRÃ‰GATES

| Code | Nom | RÃ´le | Output |
|---|---|---|---|
| C01 | SCOUT | Chasse les assets fournis par la campagne (jamais ailleurs â€” hÃ©rÃ©sie) | `source_specimen.json` |
| C02 | TYRANT_CAMP | Verdict campagne GO/NO-GO + identification ocÃ©an bleu sur mÃªme source | `campaign_verdict.json` |
| C03 | SOURCE_HUNTER | SÃ©lectionne les vidÃ©os longues Ã  clipper dans les assets | `source_specimen.json` |
| C04 | COPYWRITER | Forge le texte viral (3 titres + paragraphe + caption + hashtags + on-screen). **FrÃ©gate lourde** â€” clÃ© API premium dÃ©diÃ©e, contourne le pattern 3-phases | `text_payload.json` + `.md` |
| C05 | PACKAGER | Emballe le production pack final complet | `production_pack.json` |
| C06 | TRACKER | Checklist submission active (poster â†’ Whop <1h â†’ log â†’ vues 1h+24h â†’ flag â†’ learnings) | `submission_log.json` |

Composants annexes :
| Code | RÃ´le |
|---|---|
| TYRANT | Deux modes : rÃ©actif (analyse campagne) + prospectif (ocÃ©an bleu sur mÃªme source que le DÃ©mon) |
| CAPTEURS | **CommanditÃ© Warsmith** (pas auto). Multi-sites (Whop + Clippa/Cliptic/...). Cartographie Ã©cosystÃ¨me + niche + payouts rÃ©els |
| ORCHESTRATOR | 4 Portes, pattern hybride (sauf C04 qui dialog direct premium) |

---

## ARCHIVUM â€” LES 10 ZONES

| Zone | Contenu | RÃ´le |
|---|---|---|
| `rules/` | `whop_rules.md`, `clipping_rules.md`, `platform_{3}.md`, liens core | Savoir statique |
| `campaign/` | `directive.md`, `reference_clip.json`, `reference_skeleton.json`, `verdict.json` | LA campagne en cours (**singulier**) |
| `platform_generator/` | `youtube_profile.md`, `tiktok_profile.md`, `instagram_profile.md` | GÃ©nÃ¨re profil plateforme cible |
| `market_generator/` | `us_young_english.md` (+ futurs) | GÃ©nÃ¨re profil marchÃ© cible |
| `knowledge_base/` | `sites/`, `docs/`, `transcripts/` | TOUT sur le clipping |
| `copywriting/` | 8 sous-dossiers (hooks, formulas, subliminal, slang, hashtags, on-screen...) | MusÃ©e du copywriting (savoir secret du Warsmith) |
| `angles/` | `angle_patterns.json`, `angle_performance.json` | BibliothÃ¨que d'angles combinatoires |
| `demons/` | `<demon_id>.json` (clip + emotion + territories + `blue_ocean_unlocked`) | DÃ©mon campagne + DÃ©mon veille globale |
| `channels/` | `<account_slug>/identity.json` + `performance.json` | Tes comptes de clipping |
| `learnings/` | `learnings.json` | Boucle rÃ©tro-active (poids nul si < 50 packs, activation progressive) |

---

## MÃ‰CANISME DES N ANGLES

```
Warsmith : "Combien d'angles d'attaque ?"
   â†’ N (ex : 10)

ANGLESMITH forge N angles rÃ©partis sur 2 zones :
   â†’ X angles directs (sur le territoire dominant du DÃ©mon)
   â†’ Y angles ocÃ©an bleu (re-ciblage non saturÃ©, MÃŠME source â€” pas d'hÃ©rÃ©sie)
```

Chaque angle combine **4 axes** :
- `angle_family` : reframing / emotion / engagement / structural
- `emotion_mode` : tension, joie, inspiration, outrage, admiration...
- `engagement_type` : question / confirmation / assertion / cliffhanger
- `reframe_dim` : la transformation de sens appliquÃ©e Ã  la source

**RÃ¨gle anti-cannibale** : 2 angles trop proches = fusion ou kill. **2 axes diffÃ©renciants minimum** entre chaque angle.

**PondÃ©ration par learnings** : poids nul si < 50 packs exÃ©cutÃ©s, activation progressive ensuite. Au dÃ©but, tous les angles sont Ã©gaux. AprÃ¨s 50+ packs, les angles gagnants montent, les perdants descendent.

**Profondeur ocÃ©an bleu** : **1 couche seulement**. Exemple DÃ©mon (drame) â†’ grossophobie. On ne re-cible pas une 2e fois. On reste collÃ© Ã  la source.

---

## F04_COPYWRITER â€” La frÃ©gate singuliÃ¨re

C'est une frÃ©gate **lourde** qui suit un pattern **distinct** des autres frÃ©gates.

```
Phase A : setup_context       (l'IRON sandbox rassemble l'ARCHIVUM pertinent)
Phase B : premium_generation  (dialog DIRECT au modÃ¨le premium â€” clÃ© API dÃ©diÃ©e,
                                pas d'IRON intermÃ©diaire pour la gÃ©nÃ©ration)
Phase C : iron_ordonnancing    (l'IRON sandbox valide, classe, tag)
Phase D : finalize + ledger    (IW_CUSTOS enregistre â€” cohÃ©rence frÃ©gates)
```

Pourquoi cette rupture : le texte porte **90% du lift viral** (Ogilvy). Le sandbox bridÃ© ne suffit pas. Le premium gÃ©nÃ¨re, l'IRON ordonnance et vÃ©rrouille le ledger.

Double output par angle :
- `text_payload.json` â†’ Oracle/OMNIS_WATCH consomme (format strict)
- `text_payload.md` â†’ visible opÃ©rateur (prÃªt Ã  copier-coller au moment de poster)

Le **paragraphe reframing** a 3 niveaux de veto :
1. `recommendation` â€” F04_COPYWRITOR propose "use" | "skip"
2. `override_omniswatch` â€” l'Oracle OMNIS_WATCH peut override (si le rendu rend redondant)
3. `final_operator` â€” le Warsmith a le dernier mot au moment de poster

---

## BOUCLE LEARNINGS + FERMETURE CAMPAGNE

```
Pendant la campagne :
   F06_TRACKER logge chaque pack postÃ© + soumis + vues + payout
   
Fermeture campagne :
   Warsmith dÃ©clare "fin de campagne" â†’ notÃ© dans IW_CUSTOS.py (ledger)
   â†’ C06 agrÃ¨ge les rÃ©sultats â†’ intÃ¨gre learnings.json
   â†’ campaign/ marquÃ© "closed"
   â†’ learnings.json enrichi (cumul)
   â†’ si learnings > 50 packs cumulÃ©s â†’ ANGLESMITH commence
     Ã  pondÃ©rer les angles selon leur perf rÃ©elle
   â†’ CAPTEURS arrÃªte de scraper (campagne close = plus de veille)
   â†’ le Warsmith peut lancer la campagne suivante
     (archive/efface campaign/ et repart vierge)
```

---

## LE PRODUCTION PACK â€” Format final verrouillÃ©

Voir `CONTRACTS/production_pack_schema.json` pour le schÃ©ma JSON complet, contrat d'interface entre PERTURABO et OMNIS_WATCH.

Structure en 9 blocs :
1. `IDENTITÃ‰` : campaign_id, angle_id, pack_index/total
2. `CIBLES` : target_platform, target_market
3. `SOURCE` : video_url, suggested_segments, source_segment_sec
4. `ANGLE` : family, emotion, engagement, reframe, hook, loop, anti_cannibal, blue_ocean
5. `CUT` : max/min duration, moments_to_chase, moments_to_avoid, forbidden
6. `STYLE` : pacing, energy_level, cut_density, color_palette, text_treatment
7. `TEXT_PAYLOAD` : 3 titres calibrÃ©s + paragraphe (3 vetos) + caption + hashtags + on-screen + cta
8. `COMPLIANCE` : disclosure "#ad", submit_deadline_min=60, source_permission
9. `METADATA` + `SUBMISSION_CHECKLIST` (active)

---

## HÃ‰RÃ‰SIES INTERDITES

Le forge CLIPPING **ne fait jamais** :
- âŒ Coupe vidÃ©o (boulot de D-F01/D-F02 d'OMNIS_WATCH)
- âŒ Rendu (D-F03â†’D-F06 d'OMNIS_WATCH)
- âŒ Auto-posting (l'opÃ©rateur poste â€” risque ban)
- âŒ Duplication des rÃ¨gles core (liens, pas copies)
- âŒ Chasse externe aux sources (assets campagne seulement â€” hÃ©rÃ©sie sinon)
- âŒ Variation directe du clip de rÃ©fÃ©rence (il sert de matiÃ¨re premiÃ¨re brute, pas de modÃ¨le Ã  cloner)
- âŒ Re-ciblage ocÃ©an bleu au-delÃ  de 1 couche (rester collÃ© Ã  la source)
- âŒ Scrap auto CAPTEURS (commanditÃ© Warsmith seulement)
- âŒ DÃ©cider du style visuel final (OMNIS_WATCH applique ses presets coloring â€” PERTURABO transmet l'ADN observÃ© seulement)
- âŒ "Abonne-toi" / "Like et partage" / sons fadeouts / silences > 3s

---

## STACK D'INTÃ‰GRATION OMNIS_WATCH

```
OMNIS_WATCH (dev1, delta) :
  - PERTURABO_BASE = "https://raw.githubusercontent.com/kioka8877-ux/PERTURABO
                      /main/MONDES_FORGES/CLIPPING/ARCHIVUM"
  - Nouveau mode dans OMNIS_EXECUTEUR_DELTA.py :
       --pack production_pack.json
    remplit auto les inputs G3 (clip_count, duration)
    + fetch les rÃ¨gles depuis MONDES_FORGES/CLIPPING/
      (au lieu de YOUTUBE/)
  - Oracle OMNIS_WATCH lit text_payload.json â†’
    peut override paragraph.reco si rendu rend redondant
  - L'opÃ©rateur lit text_payload.md au moment de poster â†’
    hard veto final
```

---

## TRACKING

- `TRACKING/CLIPPING_LOG.md` â€” journal gÃ©nÃ©ral du forge (statut, portes, ledger)
- `<FREGATE>/TRACKING/<XX>_LOG.md` â€” journal de dÃ©ploiement par frÃ©gate
- `MANIFEST.md` â€” manifeste de livraison (tous les fichiers crÃ©Ã©s + leur statut)

Voir `TRACKING/INDEX.md` pour la cartographie complÃ¨te.

*Fer au-dedans, Fer au-dehors. Aucune hÃ©rÃ©sie ne survivra au siÃ¨ge.*
