# ARCHIVUM/channels/ â€” Mes comptes de clipping

> *Un sous-dossier par compte. Tracke l'identitÃ© + la perf rÃ©el.*
> *Lu par F06_TRACKER (warmup check, perf update) et F04_COPYWRITER (contexte).*

---

## Structure attendue

```
channels/
â”œâ”€â”€ <account_slug>/
â”‚   â”œâ”€â”€ identity.json
â”‚   â””â”€â”€ performance.json
â””â”€â”€ README.md  (ce fichier)
```

### `identity.json`

```json
{
  "account_slug": "monclipper_01",
  "platform": "tiktok|youtube|instagram",
  "market": "us_young_english",
  "niche": "...",
  "account_age_days": N,
  "warmup_status": "complete|incomplete",
  "warmup_started_at": "<ISO8601>",
  "warmup_completed_at": "<ISO8601 ou null>",
  "notes": "..."
}
```

RÃ¨gle warmup : `warmup_status: "complete"` require `account_age_days >= 7` (voire 14 selon platform). Voir `CONTRACTS/clipping_rules.md` C5.

### `performance.json`

```json
{
  "account_slug": "monclipper_01",
  "packs_posted_count": N,
  "aggregate_views_24h": N,
  "aggregate_payout": N,
  "rejections_count": N,
  "last_post_at": "<ISO8601>",
  "by_campaign": [
    {
      "campaign_id": "...",
      "packs_count": N,
      "total_views": N,
      "total_payout": N
    }
  ]
}
```

Mis Ã  jour par F06_TRACKER Ã  chaque pack postÃ© + Ã  la fermeture de campagne.

## Ã€ remplit par le Warsmith

- [ ] CrÃ©er un sous-dossier par compte de clipping
- [ ] Remplir `identity.json` pour chaque
- [ ] Laisser `performance.json` vide initialement â€” C06 le remplira au runtime
