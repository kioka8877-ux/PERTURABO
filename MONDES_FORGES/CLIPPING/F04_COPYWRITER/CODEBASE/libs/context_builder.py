"""
libs/context_builder.py — Phase A de F04_COPYWRITER
===================================================

Rassemble TOUT l'ARCHIVUM pertinent pour le copywriting clipping dans un
contexte structuré consommé par le modèle premium (Phase B) :

  - ARCHIVUM/copywriting/ (les 8 sous-dossiers + reference_clips_titles)
  - ARCHIVUM/rules/ (clipping_rules, whop_rules, platform_*)
  - ARCHIVUM/platform_generator/{p}_profile.md
  - ARCHIVUM/market_generator/{m}.md
  - ARCHIVUM/angles/ (angle_patterns.json, angle_performance.json)
  - ARCHIVUM/demons/ (exemples de titres gagnants)
  - ARCHIVUM/knowledge_base/ (sites, docs, transcripts)
  - ARCHIVUM/learnings/learnings.json
  - CONTRACTS/copywriting_doctrine.md, copywriter_systemprompt.md,
    anti_bullshit.md (si présent)
  - L'angle actif + le specimen source + le verdict campagne

Chaque fichier est tronqué à MAX_FILE_CHARS pour rester dans le contexte
du modèle premium sans diluer. Les fichiers manquants sont tracés
("introuvable") — la frégate n'invente jamais une source absente.
"""

import json
import os

MAX_FILE_CHARS = 30000


class ContextBuilder:
    def __init__(self, forge_root: str):
        self._forge_root = forge_root
        self._archivum = os.path.join(forge_root, "ARCHIVUM")
        self._contracts = os.path.join(forge_root, "CONTRACTS")

    # ------------------------------------------------------------------
    def _read(self, path: str, label: str) -> str:
        if not os.path.exists(path):
            return f"[introuvable: {label}]"
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            return f"[erreur lecture {label}: {e}]"
        if len(content) > MAX_FILE_CHARS:
            return content[:MAX_FILE_CHARS] + "\n[... TRONQUÉ — source > 30k chars]"
        return content

    def _walk(self, root: str, label: str, extensions: tuple = (".md", ".json", ".txt")) -> dict:
        result = {}
        if not os.path.isdir(root):
            return result
        for dirpath, _dirs, files in sorted(os.walk(root)):
            for name in sorted(files):
                if name.startswith(".") or not name.endswith(extensions):
                    continue
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, root).replace("\\", "/")
                result[rel] = self._read(full, f"{label}/{rel}")
        return result

    # ------------------------------------------------------------------
    def collect_archivum(self, platform: str, market: str) -> dict:
        copywriting_root = os.path.join(self._archivum, "copywriting")
        rules_root = os.path.join(self._archivum, "rules")
        platform_profile = os.path.join(
            self._archivum, "platform_generator", f"{platform}_profile.md")
        market_profile = os.path.join(
            self._archivum, "market_generator", f"{market}.md")
        angles_dir = os.path.join(self._archivum, "angles")
        demons_dir = os.path.join(self._archivum, "demons")
        knowledge_root = os.path.join(self._archivum, "knowledge_base")
        learnings_path = os.path.join(self._archivum, "learnings", "learnings.json")

        return {
            "copywriting_8_sous_dossiers": self._walk(copywriting_root, "copywriting"),
            "rules": self._walk(rules_root, "rules"),
            "platform_profile": self._read(platform_profile, f"{platform}_profile.md"),
            "market_profile": self._read(market_profile, f"{market}.md"),
            "angles": {
                "angle_patterns.json": self._read(
                    os.path.join(angles_dir, "angle_patterns.json"), "angle_patterns"),
                "angle_performance.json": self._read(
                    os.path.join(angles_dir, "angle_performance.json"), "angle_performance"),
            },
            "demons": self._walk(demons_dir, "demons"),
            "knowledge_base": self._walk(knowledge_root, "knowledge_base"),
            "learnings": self._read(learnings_path, "learnings.json"),
        }

    def collect_contracts(self) -> dict:
        doctrine = self._read(
            os.path.join(self._contracts, "copywriting_doctrine.md"), "doctrine")
        systemprompt = self._read(
            os.path.join(self._contracts, "copywriter_systemprompt.md"), "systemprompt")
        anti_bullshit = self._read(
            os.path.join(self._contracts, "anti_bullshit.md"), "anti_bullshit")
        return {
            "doctrine": doctrine,
            "systemprompt": systemprompt,
            "anti_bullshit": anti_bullshit,
        }

    # ------------------------------------------------------------------
    def build(self, angle: dict, specimen: dict, verdict: dict,
              platform: str, market: str) -> dict:
        return {
            "campaign_id": verdict.get("campaign_id") or specimen.get("campaign_id"),
            "angle_id": angle.get("angle_id"),
            "angle": {
                "angle_family": angle.get("angle_family"),
                "emotion_mode": angle.get("emotion_mode"),
                "engagement_type": angle.get("engagement_type"),
                "reframe_dim": angle.get("reframe_dim"),
                "zone": angle.get("zone"),
                "blue_ocean_reframe_applied": angle.get("blue_ocean_reframe_applied"),
                "territory": angle.get("territory"),
                "weight": angle.get("weight"),
            },
            "specimen": specimen,
            "verdict": verdict,
            "platform_target": platform,
            "market_target": market,
            "archivum": self.collect_archivum(platform, market),
            "contracts": self.collect_contracts(),
        }
