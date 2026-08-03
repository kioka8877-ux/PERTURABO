# ARCHIVUM/rules/ — Savoir statique

> *Règles statiques lues par toutes les frégates. Garde-fous fondamentaux.*

---

## Fichiers attendus

| Fichier | Rôle | État |
|---|---|---|
| `whop_rules.md` | Mécanique Content Rewards (CPM, 1h, rejets) | squelette — existe à `CONTRACTS/whop_rules.md` |
| `clipping_rules.md` | Warmup, volume, FTC, transformative — hérésies | squelette — existe à `CONTRACTS/clipping_rules.md` |
| `platform_tiktok.md` | Algo TikTok + format + hook frame + sons trends + SEO commentaires | squelette (à remplir) |
| `platform_shorts.md` | Algo YouTube Shorts + swipe rate + loop + engaged views | squelette (à remplir) |
| `platform_reels.md` | Algo Reels + partages DM + saves + audio trending | squelette (à remplir) |

## Liens vers le core HERESIE

Les règles générales shorts sont dans le core PERTURABO :
- `HERESIE/ARCHIVUM/rules/shorts_rules.md` — règles S1-S16 (MoneyBoyMaxx, Tim Danilov)
- `HERESIE/ARCHIVUM/rules/tim_danilov_rules.md` — niche bending

Ces fichiers ne sont **pas dupliqués** dans ce forge. Les frégates les lisent via path relatif `../../../HERESIE/ARCHIVUM/rules/` ou via URL raw si OMNIS_WATCH les fetch.

## Règle anti-duplication

Le forge CLIPPING ne duplique JAMAIS le contenu du core. Il utilise des liens symboliques (paths relatifs) ou des URLs raw GitHub. Seules les règles spécifiques au clipping Whop sont créées ici (`whop_rules.md`, `clipping_rules.md`).

---

## Template de pattern de rule

Chaque rule suit la structure des rules core (esquisse) :

```
## RÈGLE X1 : <NOM>
**Énoncé :** ...
**Application :** ...
**Validité :** ... (source, exemple observé)
**Sanction si violation :** ...
```

Voir `HERESIE/ARCHIVUM/rules/shorts_rules.md` pour le pattern complet.

---

## À remplir par le Warsmith

- [ ] `platform_tiktok.md` — complet
- [ ] `platform_shorts.md` — complet (peut s'inspirer du core mais doit inclure les spécificités Shorts 2026)
- [ ] `platform_reels.md` — complet
