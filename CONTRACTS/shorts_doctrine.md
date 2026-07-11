# SHORTS DOCTRINE — Référence de référence pour le format Short

Ce document est le cadre de référence. Il dit à quoi doit ressembler :
- Un Short viral
- Un démon Shorts
- Un océan bleu Shorts

L'IRON et le TYRANT lisent ce document comme ils lisent anti_bullshit.md.
Ce n'est pas un contrat d'exécution — c'est un cadre de jugement.

---

## 1. À QUOI RESSEMBLE UN SHORT VIRAL

### Signaux algorithme (par ordre d'importance)
1. **Viewed vs Swiped Away** — <15% exceptionnel | 15-25% sain | 25-35% hook problem | >35% échec
2. **Average View Duration** — <30s: >55% | 30-60s: ~45% | 50-64% solide | 65-79% fort | 80%+ exceptionnel
3. **Loops** — depuis mars 2025, les replays comptent comme des views. 100%+ rétention possible.
4. **Engaged views** — métrique YouTube pour les Shorts
5. **Subscriber conversion** — >1% fort | >2% exceptionnel

### Squelette Short (6 éléments)
1. Visual Hook Frame (0-0.5s) — stoppe le scroll
2. Verbal/Text Hook (0-3s) — vide cognitif immédiat
3. Content Format — 6 types possibles
4. Escalade/Rythme (3-50s) — chaque seconde = info nouvelle
5. Payoff (3-5s avant fin) — fait dingue final
6. Loop Hook (dernière seconde) — reconnecte au début

### Loop Hook — 5 techniques
1. Callback hook — la fin répond à la question du début
2. Visual match cut — la dernière frame miroire la première
3. Audio continuity — l'audio continue sans coupure au loop
4. Cliffhanger reversal — la fin crée l'urgence de re-regarder
5. Open question close — la fin pose une question que le début répond
**Le meilleur : combiner 2+ techniques.**

### 6 formats de contenu Short
1. Visual only — storytelling purement visuel, pas de texte ni voix
2. Text on screen — narration via texte overlay, pas de voix
3. Voiceover — voix off classique + visuels
4. Green screen — remix avec fond vert, réactions
5. Duets/Replies — réaction à un autre Short
6. Image carousel + music — nouveau format 2025-2026

---

## 2. À QUOI RESSEMBLE UN DÉMON SHORTS

Un démon Shorts c'est une chaîne qui :
- Domine le feed Shorts dans sa niche
- A un format reproductible (pas une one-hit wonder)
- A des outliers Shorts-specific (views / shorts baseline > 3x)
- A une vulnérabilité exploitable (un angle non couvert, un format non bendé)

### Comment identifier le démon
- Scanner les chaînes <6 mois qui croissent vite (fresh channel scanning)
- Calculer l'outlier score SHORTS (views / shorts baseline — JAMAIS mixer avec long)
- Repérer les formats reproductibles (pas les one-offs viraux chanceux)
- Analyser : hooks, pacing, on-screen text, story arcs, loop hooks

---

## 3. À QUOI RESSEMBLE UN OCÉAN BLEU SHORTS

Un océan bleu Shorts c'est :
- Un format Short qui marche dans la niche A
- Appliqué à la niche B où il n'existe pas encore
- Avec une audience claire et un skew US 60%+
- Avec une production gérable (faceless = idéal)

### Méthodes de découverte
1. **Incognito scroll** — scanner le feed sans biais de personnalisation
2. **Fresh channel scanning** — repérer les chaînes <6 mois qui croissent
3. **Trend adjacency** — angles sous-exploités de sujets trending
4. **Niche scorecard** — format reproductible + audience claire + production gérable
5. **Pattern mining** — étudier hooks, pacing, on-screen text, story arcs des concurrents

### Validation
- Le format est-il reproductible en série ? (pas une one-hit wonder)
- L'audience est-elle claire et suffisante ?
- La production est-elle gérable avec le budget disponible ?
- Le skew US est-il ≥ 60% ? (pour optimiser le RPM)
- Le démon a-t-il une vulnérabilité exploitable ?

---

## 4. OUTLIER SCORE SHORTS

Formule : video_views / channel_shorts_baseline

| Score | Interprétation |
|-------|---------------|
| 2x | Notable |
| 3-5x | Strong |
| 10x+ | Major breakout |

**RÈGLE CRITIQUE** : Comparer le baseline Shorts aux performances Shorts. Ne JAMAIS mixer baseline Long et Shorts — un Short à 100K vues sur une chaîne qui fait du Long à 10K moyenne n'est PAS un outlier si la chaîne fait déjà du Shorts à 80K moyenne.

---

## 5. LIMITATION TECHNIQUE

Les 4 signaux les plus importants (viewed/swiped, AVD, completion, loops) ne sont
accessibles QUE dans YouTube Studio. Ni yt-dlp, ni YouTube Data API v3 ne les exposent.

**Solution** :
- Analyse du specimen : transcript + structure + first frame + outlier score + like ratio
- Métriques Studio : remplies manuellement par le Warsmith dans performance.json (Phase 1)
- Phase 2 : CAPTEURS nourrissent performance.json automatiquement (si possible)

---

## 6. GEMINI VIDÉO ANALYSIS

Gemini peut regarder un Short YouTube directement (URL fournie). Il peut :
- Voir la première frame (visual hook)
- Lire le texte overlay
- Entendre l'audio et le rythme
- Percevoir le pacing
- Identifier le loop hook
- Inférer : swipe-away estimation, completion estimation, loop potentiel

C'est strictement supérieur à l'analyse transcript-only du format Long.
