# F00B_LOG — Journal de la sous-frégate VOX

## 2026-09-05

- **Création initiale** de F00B_VOX
- Spécification complète dans ARCHIVUM/capture/README_F00B_VOX.md
- Code : `f00b_vox.py` — pipeline ingest → detect → score → gate → trail
- Scoring multicritère (6 critères pondérés + bonus/malus)
- Gate Warsmith (approval manuelle requise)
- Trail pour F03_SOURCE_HUNTER
- Workflow PUR : F00B_VOX → F01 → F02 → F03 → F04 → F05 → F06

### Structure
```
F00B_VOX/
├── CODEBASE/
│   ├── f00b_vox.py          ← Script principal (CLI)
│   └── requirements_f00b.txt
├── IN/                      ← Inputs (vox_input.json, signals.json)
│   ├── vox_input.example.json
│   └── signals.example.json
├── OUT/                     ← Outputs (vox_manifest, candidats, scoring, gate, trail)
└── TRACKING/
    └── F00B_LOG.md          ← Ce fichier
```
