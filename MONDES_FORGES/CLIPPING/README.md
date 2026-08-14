# MONDE FORGE CLIPPING

> *"Une campagne est une forteresse. Un angle d'attaque est un plan de siège. Le texte est l'artillerie qui ouvre la brèche."*

---

## POSITIONNEMENT

PERTURABO/CLIPPING = le QG des campagnes **Whop Content Rewards**.

```
PERTURABO/CLIPPING       produit : briefs, angles, textes, directives (JSON/MD)
         │
         ▼
OMNIS_WATCH              exécute : coupe, reframe, rendu, coloring, camouflage
         │
         ▼
Clips postés → soumis Whop <1h → CPM (vues vérifiées)
```

Le forge CLIPPING ne touche **jamais** une vidéo. Il décide **quoi** clipper, sous **quel angle**, avec **quel texte** — et livre à OMNIS_WATCH un `production_pack.json` prêt à consommer.

La séparation des rôles est sacrée :
- PERTURABO = **quoi raconter** (stratégie + copywriting)
- OMNIS_WATCH = **comment couper/rendre** (tactique + production)
- L'opérateur humain = **poster + soumettre Whop** (dernière porte)

---

## LES 4 INPUTS DU WARSITH

```
1. Doc directif de la campagne (goal doc Whop — tout est dedans)
2. Clip de référence (celui qui a percé, fourni par la campagne)
3. Plateforme cible (YouTube / TikTok / Instagram)
4. Marché cible (ex : US / Anglais / Jeune)

PERTURABO demande : "Combien d'angles d'attaque ?"
   → N → N plans de siège → N production packs → N vidéos
```

Chaque pack = **1 vidéo pour 1 plateforme pour 1 marché**. Pas de multi-plateforme par pack.

---

## LES 4 PORTES

| Porte | Frégates mobilisées | Produit | Validateur |
|---|---|---|---|
| 1 | F02_TYRANT_CAMP (réactif + prospectif) | `verdict.json` (GO/NO-GO + `blue_ocean_unlocked`) | Warsmith |
| 2 | ANGLESMITH (via F02 estratégia) | `angles.json` (N angles sur direct + océan bleu) | Warsmith |
| 3 | F03_SOURCE_HUNTER + F04_COPYWRITER | `source_specimen.json` + `text_payload.json` + `.md` | Warsmith + IRON ordonnancement |
| 4 | F05_PACKAGER | N `production_pack.json` → OMNIS_WATCH | Warsmith |

`F01_SCOUT` alimente les portes 1-2 (assets campagne). `F06_TRACKER` active la checklist après Porte 4 et nourrit `learnings.json`. `F00_CAPTEURS` s'exécute **avant** Porte 1 sur commande Warsmith uniquement.

---

## LES FRÉGATES

| Code | Nom | Rôle | Output |
|---|---|---|---|
| F01 | SCOUT | Chasse les assets fournis par la campagne (jamais ailleurs — hérésie) | `source_specimen.json` |
| F02 | TYRANT_CAMP | Verdict campagne GO/NO-GO + identification océan bleu sur même source | `campaign_verdict.json` |
| F03 | SOURCE_HUNTER | Sélectionne les vidéos longues à clipper dans les assets | `source_specimen.json` |
| F04 | COPYWRITER | Forge le texte viral (3 titres + paragraphe + caption + hashtags + on-screen). **Frégate lourde** — clé API premium dédiée, contourne le pattern 3-phases | `text_payload.json` + `.md` |
| F05 | PACKAGER | Emballe le production pack final complet | `production_pack.json` |
| F06 | TRACKER | Checklist submission active (poster → Whop <1h → log → vues 1h+24h → flag → learnings) | `submission_log.json` |

Composants annexes :
| Code | Rôle |
|---|---|
| TYRANT | Deux modes : réactif (analyse campagne) + prospectif (océan bleu sur même source que le Démon) |
| F00_CAPTEURS | **Commandité Warsmith** (pas auto). Multi-sites (Whop + Clippa/Cliptic/...). Cartographie écosystème + niche + payouts réels |
| ORCHESTRATOR | 4 Portes, pattern hybride (sauf F04 qui dialog direct premium) |

---

## ARCHIVUM — LES 10 ZONES

| Zone | Contenu | Rôle |
|---|---|---|
| `rules/` | `whop_rules.md`, `clipping_rules.md`, `platform_{3}.md`, liens core | Savoir statique |
| `campaign/` | `directive.md`, `reference_clip.json`, `reference_skeleton.json`, `verdict.json` | LA campagne en cours (**singulier**) |
| `platform_generator/` | `youtube_profile.md`, `tiktok_profile.md`, `instagram_profile.md` | Génère profil plateforme cible |
| `market_generator/` | `us_young_english.md` (+ futurs) | Génère profil marché cible |
| `knowledge_base/` | `sites/`, `docs/`, `transcripts/` | TOUT sur le clipping |
| `copywriting/` | 8 sous-dossiers (hooks, formulas, subliminal, slang, hashtags, on-screen...) | Musée du copywriting (savoir secret du Warsmith) |
| `angles/` | `angle_patterns.json`, `angle_performance.json` | Bibliothèque d'angles combinatoires |
| `demons/` | `<demon_id>.json` (clip + emotion + territories + `blue_ocean_unlocked`) | Démon campagne + Démon veille globale |
| `channels/` | `<account_slug>/identity.json` + `performance.json` | Tes comptes de clipping |
| `learnings/` | `learnings.json` | Boucle rétro-active (poids nul si < 50 packs, activation progressive) |

---

## MÉCANISME DES N ANGLES

```
Warsmith : "Combien d'angles d'attaque ?"
   → N (ex : 10)

ANGLESMITH forge N angles répartis sur 2 zones :
   → X angles directs (sur le territoire dominant du Démon)
   → Y angles océan bleu (re-ciblage non saturé, MÊME source — pas d'hérésie)
```

Chaque angle combine **4 axes** :
- `angle_family` : reframing / emotion / engagement / structural
- `emotion_mode` : tension, joie, inspiration, outrage, admiration...
- `engagement_type` : question / confirmation / assertion / cliffhanger
- `reframe_dim` : la transformation de sens appliquée à la source

**Règle anti-cannibale** : 2 angles trop proches = fusion ou kill. **2 axes différenciants minimum** entre chaque angle.

**Pondération par learnings** : poids nul si < 50 packs exécutés, activation progressive ensuite. Au début, tous les angles sont égaux. Après 50+ packs, les angles gagnants montent, les perdants descendent.

**Profondeur océan bleu** : **1 couche seulement**. Exemple Démon (drame) → grossophobie. On ne re-cible pas une 2e fois. On reste collé à la source.

---

## F04_COPYWRITER — La frégate singulière

C'est une frégate **lourde** qui suit un pattern **distinct** des autres frégates.

```
Phase A : setup_context       (l'IRON sandbox rassemble l'ARCHIVUM pertinent)
Phase B : premium_generation  (dialog DIRECT au modèle premium — clé API dédiée,
                                pas d'IRON intermédiaire pour la génération)
Phase C : iron_ordonnancing    (l'IRON sandbox valide, classe, tag)
Phase D : finalize + ledger    (IW_CUSTOS enregistre — cohérence frégates)
```

Pourquoi cette rupture : le texte porte **90% du lift viral** (Ogilvy). Le sandbox bridé ne suffit pas. Le premium génère, l'IRON ordonnance et vérrouille le ledger.

Double output par angle :
- `text_payload.json` → Oracle/OMNIS_WATCH consomme (format strict)
- `text_payload.md` → visible opérateur (prêt à copier-coller au moment de poster)

Le **paragraphe reframing** a 3 niveaux de veto :
1. `recommendation` — F04_COPYWRITOR propose "use" | "skip"
2. `override_omniswatch` — l'Oracle OMNIS_WATCH peut override (si le rendu rend redondant)
3. `final_operator` — le Warsmith a le dernier mot au moment de poster

---

## BOUCLE LEARNINGS + FERMETURE CAMPAGNE

```
Pendant la campagne :
   F06_TRACKER logge chaque pack posté + soumis + vues + payout
   
Fermeture campagne :
   Warsmith déclare "fin de campagne" → noté dans IW_CUSTOS.py (ledger)
   → F06 agrège les résultats → intègre learnings.json
   → campaign/ marqué "closed"
   → learnings.json enrichi (cumul)
   → si learnings > 50 packs cumulés → ANGLESMITH commence
     à pondérer les angles selon leur perf réelle
   → F00_CAPTEURS arrête de scraper (campagne close = plus de veille)
   → le Warsmith peut lancer la campagne suivante
     (archive/efface campaign/ et repart vierge)
```

---

## LE PRODUCTION PACK — Format final verrouillé

Voir `CONTRACTS/production_pack_schema.json` pour le schéma JSON complet, contrat d'interface entre PERTURABO et OMNIS_WATCH.

Structure en 9 blocs :
1. `IDENTITÉ` : campaign_id, angle_id, pack_index/total
2. `CIBLES` : target_platform, target_market
3. `SOURCE` : video_url, suggested_segments, source_segment_sec
4. `ANGLE` : family, emotion, engagement, reframe, hook, loop, anti_cannibal, blue_ocean
5. `CUT` : max/min duration, moments_to_chase, moments_to_avoid, forbidden
6. `STYLE` : pacing, energy_level, cut_density, color_palette, text_treatment
7. `TEXT_PAYLOAD` : 3 titres calibrés + paragraphe (3 vetos) + caption + hashtags + on-screen + cta
8. `COMPLIANCE` : disclosure "#ad", submit_deadline_min=60, source_permission
9. `METADATA` + `SUBMISSION_CHECKLIST` (active)

---

## HÉRÉSIES INTERDITES

Le forge CLIPPING **ne fait jamais** :
- ❌ Coupe vidéo (boulot de D-F01/D-F02 d'OMNIS_WATCH)
- ❌ Rendu (D-F03→D-F06 d'OMNIS_WATCH)
- ❌ Auto-posting (l'opérateur poste — risque ban)
- ❌ Duplication des règles core (liens, pas copies)
- ❌ Chasse externe aux sources (assets campagne seulement — hérésie sinon)
- ❌ Variation directe du clip de référence (il sert de matière première brute, pas de modèle à cloner)
- ❌ Re-ciblage océan bleu au-delà de 1 couche (rester collé à la source)
- ❌ Scrap auto F00_CAPTEURS (commandité Warsmith seulement)
- ❌ Décider du style visuel final (OMNIS_WATCH applique ses presets coloring — PERTURABO transmet l'ADN observé seulement)
- ❌ "Abonne-toi" / "Like et partage" / sons fadeouts / silences > 3s

---

## STACK D'INTÉGRATION OMNIS_WATCH

```
OMNIS_WATCH (dev1, delta) :
  - PERTURABO_BASE = "https://raw.githubusercontent.com/kioka8877-ux/PERTURABO
                      /main/MONDES_FORGES/CLIPPING/ARCHIVUM"
  - Nouveau mode dans OMNIS_EXECUTEUR_DELTA.py :
       --pack production_pack.json
    remplit auto les inputs G3 (clip_count, duration)
    + fetch les règles depuis MONDES_FORGES/CLIPPING/
      (au lieu de YOUTUBE/)
  - Oracle OMNIS_WATCH lit text_payload.json →
    peut override paragraph.reco si rendu rend redondant
  - L'opérateur lit text_payload.md au moment de poster →
    hard veto final
```

---

## TRACKING

- `TRACKING/CLIPPING_LOG.md` — journal général du forge (statut, portes, ledger)
- `<FREGATE>/TRACKING/<XX>_LOG.md` — journal de déploiement par frégate
- `MANIFEST.md` — manifeste de livraison (tous les fichiers créés + leur statut)

Voir `TRACKING/INDEX.md` pour la cartographie complète.

*Fer au-dedans, Fer au-dehors. Aucune hérésie ne survivra au siège.*
