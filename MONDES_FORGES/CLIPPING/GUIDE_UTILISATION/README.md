# GUIDE_UTILISATION — PERTURABO CLIPPING

> Le mode d'emploi du forge CLIPPING pour les **futurs champions (opérateurs)** et les **oracles**.
> Tout ce qu'il faut savoir pour lancer un siège **sans connaître l'historique du développement**. Le Champion reste l’unique autorité de validation.

---

## 📚 Ce dossier

Ici, **un guide par mode**. Chaque guide explique, étape par étape et avec les **commandes exactes**, comment mener un siège de A à Z : ce que tu fournis, ce que les frégates produisent, ce que tu valides à chaque gate, et ce qui part chez **LACRIMAE**.

## 🗂️ Les guides

| Fichier | Mode | Statut |
|---|---|---|
| `00_COMMENCER_ICI.md` | Tous | ✅ Le strict minimum pour lancer un siège |
| `01_MODE_LOGO_INFORMATIF.md` | **logo / informatif** | ✅ **Complet** (testé en production, siège TS01_SANDOVAL) |
| `02_MODE_LOGO_HUMOUR.md` | logo / humour | ⏳ À compléter (même squelette) |
| `03_MODE_WHOP.md` | whop (clip canon) | ⏳ À compléter (même squelette) |
| `04_MODE_MEME.md` | logo / meme | ✅ **Opérationnel** (10 angles, tweet/motion contextualisés, LACRIMAE) |
| `06_RECHERCHE_SUJETS_US_YOUTUBE_MEME.md` | Recherche | ✅ Profil US / YouTube Shorts / niche meme |
| `07_HORIZONS_RECHERCHE.md` | Recherche | ✅ Fenêtres 2h / 6h / 12h / 24h / 3d / 7d / 30d |
| `08_DISCOVERY_MARKET_DEMONS_RED_BLUE.md` | Discovery | ✅ Marché, Démons, océans rouge/bleu et validation |
| `09_DIRECTEUR_PROSPECTION_PREMIUM.md` | Discovery | ✅ Questions premium, collecte Oracle et anti-invention |
| `_PIEGES_APPRIS.md` | Tous | ✅ Les leçons du siège test — **à lire avant chaque siège** |

## 🧭 Comment naviguer

1. **Premier lancement** → lis `00_COMMENCER_ICI.md`
2. **Avant chaque siège** → relis `_PIEGES_APPRIS.md` (5 minutes, ça évite les erreurs déjà payées)
3. **Recherche de sujet** → lis `06_RECHERCHE_SUJETS_US_YOUTUBE_MEME.md`, `07_HORIZONS_RECHERCHE.md`, `08_DISCOVERY_MARKET_DEMONS_RED_BLUE.md` et `09_DIRECTEUR_PROSPECTION_PREMIUM.md`
4. **Mode utilisé** → ouvre le guide du mode (ex : `01_MODE_LOGO_INFORMATIF.md`)
5. **Doute en cours de siège** → reviens sur la section concernée du guide

## ➕ Comment ajouter un guide (nouveau mode)

Chaque guide suit le **même squelette** — duplique un guide existant et remplis. En mode meme, les champs réels (`tweet.text`, `text_emotion`, métadonnées) priment sur l’ancien schéma généraliste :

1. **Le but en 3 lignes** (ce que fait le mode)
2. **Les inputs** (ce que le champion doit fournir, format, exemple)
3. **Le chemin complet** — les 4 gates avec les commandes EXACTES
4. **La clé premium** (avec clé / backup `--oracle`)
5. **Les règles verrouillées** (garde-fous)
6. **Le livrable final** (pack + EXPORT + liens GitHub)
7. **Checklist rapide avant chaque gate**

Règle de nommage : `NN_MODE_<PROFIL>_<SOUS_MODE>.md` (NN = ordre, 2 chiffres).

## 🏗️ Rappel de l'architecture (en bref)

```
F00_CAPTEURS (recherche contextualisée + scrap écosystème) ── avant Gate 1
F01 SCOUT        → capture le specimen (source)
F02 TYRANT CAMP  → verdict GO/NO-GO (Gate 1)
ANGLESMITH (F02) → forge les angles (Gate 2)
F03 SOURCE HUNTER→ sélectionne asset + segments (skippé en mode logo et meme)
F04 COPYWRITER   → forge les textes : titre, paragraphe, metadata, tags (Gate 3)
F05 PACKAGER     → assemble le pack final (Gate 4)
F06 TRACKER      → suit les posts après publication
ORCHESTRATOR     → le nerf central : gates + ledger + expédition
```

**Mode meme** (logo / meme) : l'opérateur fournit un **sujet ou mot-clé** → F00 scanne les preuves, **0 clip téléchargé** → F02 forge jusqu’à 10 angles distincts → F04 forge pour chaque angle le tweet, le texte motion et les métadonnées → l’opérateur valide → F05 assemble le pack avec la balise mème choisie, par exemple `M1` → l’opérateur valide puis copie dans EXPORT → **LACRIMAE** monte via `04_MODE_MEME.md`. **F01 et F03 sont ignorés en mode meme.**

**Vocabulaire** : on dit **gate** (ou porte) — `gate 1` à `gate 4`. Le champion **valide ou rejette** chaque gate. Rien ne passe sans ta signature.
