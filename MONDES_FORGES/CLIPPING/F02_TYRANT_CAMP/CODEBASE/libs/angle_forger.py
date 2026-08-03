"""
libs/angle_forger.py — Forge combinatoire des N angles (ANGLESMITH)
===================================================================

ANGLESMITH forge N angles repartis sur 2 zones :
  - X angles directs (territoire dominant du Demon, verdict.demon_analysis)
  - Y angles ocean bleu (re-ciblage non sature, MEME source, depth <= 1)

Chaque angle combine 4 axes : angle_family, emotion_mode,
engagement_type, reframe_dim.

Regle anti-cannibale : 2 angles trop proches = fusion ou kill.
2 axes differenciants minimum entre chaque angle.

Usage:
  from angle_forger import AngleForger
  forger = AngleForger()
  angles = forger.forge(n=10, campaign_id=..., verdict=...)
"""

_AXES = {
    "angle_family": ["reframing", "emotion", "engagement", "structural"],
    "emotion_mode": ["tension", "joie", "inspiration", "outrage", "admiration"],
    "engagement_type": ["question", "confirmation", "assertion", "cliffhanger"],
    "reframe_dim": [
        "victime_vers_survivant",
        "anonyme_vers_incroyable",
        "banal_vers_suspect",
        "fait_vers_absurde",
        "echec_vers_lecon",
        "seul_vers_communaute",
        "cache_vers_revele",
        "ordinaire_vers_extraordinaire",
    ],
}

_MIN_DIFFERENT_AXES = 2


class AngleForger:
    def __init__(self):
        self._axis_names = list(_AXES.keys())

    def _axes_different(self, a: dict, b: dict) -> int:
        return sum(1 for ax in self._axis_names if a.get(ax) != b.get(ax))

    def _anti_cannibale(self, angles: list[dict], candidate: dict) -> bool:
        """True si le candidat respecte 2 axes differenciants vs tous les autres."""
        for existing in angles:
            if self._axes_different(existing, candidate) < _MIN_DIFFERENT_AXES:
                return False
        return True

    def forge(self, n: int, campaign_id: str, verdict: dict = None) -> list[dict]:
        """Forge N angles uniques (anti-cannibale) avec zones direct/ocean bleu."""
        verdict = verdict or {}
        demon = verdict.get("demon_analysis", {})
        oceans = demon.get("blue_ocean_unlocked", [])
        oceans = [o for o in oceans if str(o.get("blue_ocean_depth", 1)) == "1"]

        n_blue = min(len(oceans), max(0, n // 3)) if oceans else 0
        n_direct = n - n_blue

        angles = []
        idx = 1

        # Zone direct : territoire dominant du Demon
        for family in _AXES["angle_family"]:
            for emotion in _AXES["emotion_mode"]:
                for engagement in _AXES["engagement_type"]:
                    for reframe in _AXES["reframe_dim"]:
                        if idx > n_direct:
                            break
                        candidate = {
                            "angle_id": f"A{idx:02d}",
                            "angle_family": family,
                            "emotion_mode": emotion,
                            "engagement_type": engagement,
                            "reframe_dim": reframe,
                            "zone": "direct",
                            "blue_ocean_reframe_applied": False,
                            "blue_ocean_depth": None,
                            "territory": demon.get("dominant_emotion"),
                            "weight": 1.0,
                        }
                        if self._anti_cannibale(angles, candidate):
                            angles.append(candidate)
                            idx += 1
                        if idx > n_direct:
                            break
                    if idx > n_direct:
                        break
                if idx > n_direct:
                    break
            if idx > n_direct:
                break

        # Zone ocean bleu : re-ciblage 1 couche sur MEME source
        for territory in oceans:
            if idx > n:
                break
            if idx > n_blue + n_direct:
                break
            for family in ["reframing", "emotion"]:
                if idx > n:
                    break
                for engagement in ["question", "assertion"]:
                    if idx > n:
                        break
                    candidate = {
                        "angle_id": f"A{idx:02d}",
                        "angle_family": family,
                        "emotion_mode": demon.get("dominant_emotion") or "tension",
                        "engagement_type": engagement,
                        "reframe_dim": "banal_vers_suspect",
                        "zone": "blue_ocean",
                        "blue_ocean_reframe_applied": True,
                        "blue_ocean_depth": 1,
                        "territory": territory.get("territory"),
                        "territory_rationale": territory.get("rationale"),
                        "weight": 1.0,
                    }
                    if self._anti_cannibale(angles, candidate):
                        angles.append(candidate)
                        idx += 1

        return angles[:n]
