# CLIPPING RULES â€” RÃ¨gles du clipping Whop Content Rewards

> * STATUT : SQUELETTE â€” Le Warsmith doit enrichir. *

Ce document est le **garde-fous fondamental** du forge CLIPPING. Toutes les frÃ©gates le lisent comme anti_bullshit.md est lu dans le core. Il code les hÃ©rÃ©sies spÃ©cifiques au clipping Whop.

---

## RÃˆGLE C1 â€” STRICT-SOURCE (La Source SacrÃ©e)

**Ã‰noncÃ©** : La source d'un clip ne provient **que** des assets fournis par la campagne Whop. Aucune source externe, aucune adjacence, aucun "scrap complÃ©mentaire".

**Application** : F01_SCOUT inventorie exclusivement les assets de `directive.md`. Toute sortie du pÃ©rimÃ¨tre est hÃ©rÃ©sie.

**Sanction si violation** : rejet Whop + ban possible + perte de crÃ©dibilitÃ© avec la marque.

---

## RÃˆGLE C2 â€” DISCLOSURE FTC OBLIGATOIRE

**Ã‰noncÃ©** : Tout clip porte la mention `#ad` ou `#sponsored` visible dans la caption, AVANT le "voir plus".

**Application** : F04_COPYWRITER inclut dans tous les `caption`. F05_PACKAGER vÃ©rifie dans `COMPLIANCE.disclosure`.

**Sanction si violation** : rejection Whop + shadowban platform (TikTok notamment).

---

## RÃˆGLE C3 â€” SOUMISSION DANS L'HEURE (RÃ¨gle critique Whop)

**Ã‰noncÃ©** : Le premier soumission Whop doit intervenir dans l'heure qui suit la publication du clip.

**Application** : `submission_checklist` activÃ©e par F06_TRACKER avec `deadline_min: 60`. Flag si en retard (`submission_within_1h: false`).

**Sanction si violation** : rejet Whop (rÃ¨gle publique).

---

## RÃˆGLE C4 â€” TRANSFORMATIVE OBLIGATOIRE (Reused Content policy)

**Ã‰noncÃ©** : Le clip doit Ãªtre "transformative" â€” ajouter narrative, commentary, editing. Pas de copie brute de la source.

**Application** : PERTURABO forge des **angles d'attaque** (et non des copies directes) â€” reframing, Ã©motion, engagement. Le rendu (OMNIS_WATCH) applique le reste (cut, captions, sound design).

**Sanction si violation** : rejection Whop + demonetization platform (YouTube notamment).

---

## RÃˆGLE C5 â€” WARMUP COMPTES (Anti-shadowban platform)

**Ã‰noncÃ©** : Les nouveaux comptes platform (TikTok / IG / YT) sont shadowban par dÃ©faut pendant 7-14 jours. Il faut farmer (warmup) avant de poster les clips de campagne.

**Application** :
- `ARCHIVUM/channels/<account_slug>/identity.json` contient `warmup_status` + `account_age_days`.
- F06_TRACKER lit le warmup status avant de valider un post â€” si `warmup` < 7 jours â†’ flag warning `WARMUP_INCOMPLETE`.

**Sanction si violation** : 0 view jail. Le clip ne sort pas du FYP.

---

## RÃˆGLE C6 â€” VOLUME + MULTI-PLATEFORME

**Ã‰noncÃ©** : Volume de production = 10-20 clips/jour en batch. Multi-plateforme (mÃªme clip â†’ TikTok + Reels + Shorts).

**Application** :
- Un angle â†’ un pack par plateforme (pas multi-plateforme dans un mÃªme pack)
- Pour N angles Ã— M plateformes = NÃ—M packs potentiels (le Warsmith dÃ©cide combien de plateformes par angle)

---

## RÃˆGLE C7 â€” TRACKING UTM / BITLY (NÃ©gociation CPM)

**Ã‰noncÃ©** : Utilisation de liens trackÃ©s (UTM, Bitly) pour prouver les perfs et nÃ©gocier meilleurs taux cÃ´tÃ© Whop.

**Application** : F06_TRACKER gÃ©nÃ¨re le lien trackÃ© au moment de la soumission Whop.

---

## HÃ‰RÃ‰SIES SPÃ‰CIFIQUES AU CLIPPING WHOP (RÃ©cap des interdictions absolues)

- âŒ Source non-issue des assets campaign (rÃ¨gle C1)
- âŒ Clip non-transformative (rÃ¨gle C4)
- âŒ Disclosure FTC absent (rÃ¨gle C2)
- âŒ Soumission > 1h aprÃ¨s post (rÃ¨gle C3)
- âŒ Compte non-warmupÃ© qui post (rÃ¨gle C5)
- âŒ Variation directe du clip de rÃ©fÃ©rence (le clip ref = matiÃ¨re premiÃ¨re brute, pas modÃ¨le Ã  cloner â€” dÃ©cision Warsmith)
- âŒ Re-ciblage ocÃ©an bleu au-delÃ  de 1 couche de profondeur
- âŒ Auto-posting / auto-submitting (le Warsmith poster â€” pas le systÃ¨me)
- âŒ Scraper CAPTEURS en automatique (commanditÃ© uniquement)
- âŒ "Abonne-toi" / "Like et partage" / "Swipe up" / fadeouts / silences > 3s

---

## STATUT DE REMPLISSAGE

| Section | Ã‰tat |
|---|---|
| C1 Strict-source | documentÃ© |
| C2 Disclosure FTC | documentÃ© |
| C3 Soumission 1h | documentÃ© |
| C4 Transformative | documentÃ© |
| C5 Warmup comptes | documentÃ© (structure) |
| C6 Volume + multi-plateforme | documentÃ© (chiffres Ã  confirmer) |
| C7 Tracking | documentÃ© |
| HÃ©rÃ©sies spÃ©cifiques | documentÃ© |

**Ã€ enrichir par le Warsmith** : cas particuliers, exemples, sanctions observÃ©es en production.

RÃ©fÃ©rence couplage : `HERESIE/CONTRACTS/anti_bullshit.md` (core).
