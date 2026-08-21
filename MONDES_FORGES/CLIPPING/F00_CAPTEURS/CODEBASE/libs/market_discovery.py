"""Moteur de découverte de marché F00.

Principes : les candidats sont extraits uniquement de signaux observés. Les
requêtes générées servent à sonder les capteurs, mais ne deviennent jamais des
candidats sans preuve. Le module est déterministe et n'exige pas de clé premium.
"""
from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Callable

HORIZONS = {
    "2h": {"hours": 2, "timeframe": "day", "freshness": "brulant"},
    "6h": {"hours": 6, "timeframe": "day", "freshness": "brulant"},
    "12h": {"hours": 12, "timeframe": "day", "freshness": "frais"},
    "24h": {"hours": 24, "timeframe": "day", "freshness": "frais"},
    "3d": {"hours": 72, "timeframe": "week", "freshness": "frais"},
    "7d": {"hours": 168, "timeframe": "week", "freshness": "frais"},
    "30d": {"hours": 720, "timeframe": "month", "freshness": "frais"},
}

STOPWORDS = {"people", "living", "in", "the", "us", "usa", "united", "states",
             "interested", "who", "like", "likes", "playing", "play", "game",
             "fans", "audience", "and", "for", "with", "from", "youtube", "shorts"}
BLOCKED = {"election", "president", "politics", "political", "abortion", "war",
           "terrorism", "terrorist", "shooting", "racial", "religion"}


def _tokens(text: str) -> list[str]:
    return [x.lower() for x in re.findall(r"[A-Za-z0-9][A-Za-z0-9'_-]{2,}", text or "")]


def build_probe_queries(market: str) -> list[str]:
    """Construit des sondes ; aucune sonde ne devient candidat sans evidence."""
    words = [w for w in _tokens(market) if w not in STOPWORDS]
    if not words:
        return [market.strip()]
    queries = [market.strip(), " ".join(words)]
    if len(words) > 1:
        queries += [" ".join(words[:i]) for i in range(1, min(4, len(words)) + 1)]
    return list(dict.fromkeys(q for q in queries if q))[:6]


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", (text or "").lower()).strip()


def _candidate_key(text: str) -> str:
    words = [w for w in _norm(text).split() if w not in STOPWORDS]
    return " ".join(words[:8])


def _evidence_url(item: dict) -> str | None:
    return item.get("url") or item.get("permalink") or item.get("source_url")


def _youtube_items(yt: dict) -> list[dict]:
    out = []
    for group in ((yt.get("search") or {}).get("videos") or [],
                  (yt.get("trending") or {}).get("videos") or []):
        out.extend(group)
    return out


def _extract_observed_candidates(probe_queries: list[str], yt: dict, sugg: dict,
                                 reddit: dict, trends: dict) -> list[dict]:
    raw = []
    for video in _youtube_items(yt):
        title = (video.get("title") or "").strip()
        if title:
            raw.append({"text": title, "kind": "youtube", "item": video})
    for group in (sugg.get("keywords") or []):
        for value in group.get("suggestions") or []:
            raw.append({"text": value, "kind": "suggest", "item": group})
    for post in reddit.get("posts") or []:
        title = (post.get("title") or "").strip()
        if title:
            raw.append({"text": title, "kind": "reddit", "item": post})
    for trend in ((trends.get("global_trending_rss") or {}).get("trending") or []):
        value = (trend.get("query") or "").strip()
        if value:
            raw.append({"text": value, "kind": "trends", "item": trend})

    grouped = defaultdict(list)
    for entry in raw:
        key = _candidate_key(entry["text"])
        if key and len(key.split()) >= 1:
            grouped[key].append(entry)
    candidates = []
    for key, entries in grouped.items():
        youtube = [e for e in entries if e["kind"] == "youtube"]
        reddit_items = [e for e in entries if e["kind"] == "reddit"]
        suggestions = [e for e in entries if e["kind"] == "suggest"]
        urls = list(dict.fromkeys(u for u in (_evidence_url(e["item"]) for e in entries) if u))
        views = [int(e["item"].get("view_count", 0) or 0) for e in youtube]
        comments = [int(e["item"].get("num_comments", 0) or 0) for e in reddit_items]
        channels = {e["item"].get("channel", "") for e in youtube if e["item"].get("channel")}
        title = max(entries, key=lambda e: len(e["text"]))["text"]
        candidates.append({
            "candidate_id": "CAND-" + hashlib.sha1(key.encode()).hexdigest()[:8],
            "keyword": title[:120],
            "normalized_key": key,
            "evidence_urls": urls[:12],
            "evidence_types": sorted(set(e["kind"] for e in entries)),
            "youtube_video_count": len(youtube),
            "youtube_top_views": max(views or [0]),
            "youtube_total_views": sum(views),
            "reddit_post_count": len(reddit_items),
            "reddit_comments": sum(comments),
            "suggestion_count": len(suggestions),
            "channel_count": len(channels),
            "observed": True,
        })
    return candidates


def _demon_map(yt: dict) -> list[dict]:
    videos = _youtube_items(yt)
    channels = Counter(v.get("channel") for v in videos if v.get("channel"))
    demons = []
    for channel, count in channels.most_common(10):
        related = [v for v in videos if v.get("channel") == channel]
        views = sum(int(v.get("view_count", 0) or 0) for v in related)
        demons.append({
            "demon_id": "DEMON-" + hashlib.sha1(channel.encode()).hexdigest()[:8],
            "type": "creator_or_channel",
            "identity": channel,
            "territory": [v.get("title", "") for v in related[:5]],
            "evidence_urls": [f"https://youtube.com/watch?v={v.get('video_id')}" for v in related if v.get("video_id")],
            "observed_video_count": count,
            "observed_views": views,
            "pressure_score": min(100, count * 12 + (views // 100000)),
            "status": "observed",
        })
    return demons


def _score_candidate(c: dict, horizon: str, demons: list[dict], market: str) -> dict:
    views_score = min(100, c["youtube_top_views"] / 10000)
    demand_score = min(100, c["suggestion_count"] * 15 + c["reddit_post_count"] * 10 + c["reddit_comments"] / 50)
    evidence_score = min(100, len(c["evidence_types"]) * 25)
    demon_pressure = min(100, c["channel_count"] * 15 + c["youtube_video_count"] * 8)
    saturation = min(100, demon_pressure * 0.7 + c["youtube_video_count"] * 5)
    us_score = 70 if any(x in market.lower() for x in ("us", "usa", "united states", "american")) else 50
    blue_score = max(0, min(100, demand_score * .45 + evidence_score * .25 + (100 - saturation) * .30))
    red_score = min(100, demand_score * .45 + views_score * .35 + demon_pressure * .20)
    fit = min(100, 35 + len(c["evidence_types"]) * 15 + (15 if len(c["keyword"].split()) <= 8 else 0))
    confidence = min(100, evidence_score * .5 + (25 if c["evidence_urls"] else 0) + (25 if c["youtube_video_count"] else 0))
    camp = "red" if red_score >= blue_score and demand_score >= 35 else ("blue" if blue_score >= 35 else "desert")
    c.update({
        "scores": {"demand": round(demand_score, 1), "youtube": round(views_score, 1),
                   "us_native": us_score, "demon_pressure": round(demon_pressure, 1),
                   "saturation": round(saturation, 1), "blue_ocean": round(blue_score, 1),
                   "red_ocean": round(red_score, 1), "meme_fit": round(fit, 1),
                   "confidence": round(confidence, 1)},
        "ocean": camp,
        "horizon": horizon,
        "source_status": "observed_only",
        "safety_gate": "block" if set(_tokens(c["keyword"])) & BLOCKED else "pass",
        "decision": "warsmith_review",
    })
    return c


def _deduplicate(candidates: list[dict]) -> tuple[list[dict], list[dict]]:
    kept, removed = [], []
    seen = {}
    for c in sorted(candidates, key=lambda x: (x["youtube_total_views"], len(x["evidence_types"])), reverse=True):
        key = c["normalized_key"]
        if key in seen:
            c["status"] = "duplicate"
            c["duplicate_of"] = seen[key]
            removed.append(c)
        else:
            c["status"] = "unique"
            seen[key] = c["candidate_id"]
            kept.append(c)
    return kept, removed


def discover_market(market: str, platform: str, horizon: str, *,
                    rss_scan: Callable, trends_scan: Callable,
                    youtube_scan: Callable, suggestions_scan: Callable,
                    reddit_scan: Callable, max_items: int = 10,
                    probe_queries: list[str] | None = None,
                    question_plan: list[dict] | None = None) -> dict:
    if not market.strip():
        raise ValueError("market requis")
    if platform != "youtube_shorts":
        raise ValueError("plateforme non supportée: youtube_shorts uniquement")
    if horizon not in HORIZONS:
        raise ValueError("horizon requis: 2h|6h|12h|24h|3d|7d|30d")
    spec = HORIZONS[horizon]
    probes = list(dict.fromkeys(probe_queries or build_probe_queries(market)))[:20]
    if not probes:
        raise ValueError("aucune requête de prospection valide")
    rss = rss_scan(probes, freshness=spec["freshness"], max_items=max_items)
    trends = trends_scan(probes)
    yt = youtube_scan(probes, max_results=20)
    sugg = suggestions_scan(probes)
    reddit = reddit_scan(probes, max_items=max_items, timeframe=spec["timeframe"])
    demons = _demon_map(yt)
    raw = _extract_observed_candidates(probes, yt, sugg, reddit, trends)
    scored = [_score_candidate(c, horizon, demons, market) for c in raw]
    unique, removed = _deduplicate(scored)
    eligible = [c for c in unique if c["safety_gate"] == "pass" and c["ocean"] != "desert"]
    eligible.sort(key=lambda c: max(c["scores"]["red_ocean"], c["scores"]["blue_ocean"]), reverse=True)
    for index, c in enumerate(eligible[:30], 1):
        c["rank"] = index
    red = [c for c in eligible[:30] if c["ocean"] == "red"]
    blue = [c for c in eligible[:30] if c["ocean"] == "blue"]
    return {
        "discovery_id": "DISC-" + hashlib.sha1(f"{market}|{platform}|{horizon}".encode()).hexdigest()[:10],
        "discovered_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "market_input": {"market": market, "platform": platform, "horizon": horizon, "language": "en-US", "production_niche": "meme"},
        "research_profile": {"horizon_hours": spec["hours"], "probe_queries": probes, "candidate_limit": 30},
        "demon_map": demons,
        "candidate_clusters": {"unique_count": len(unique), "removed_duplicates": removed},
        "candidates": eligible[:30],
        "red_candidates": red,
        "blue_candidates": blue,
        "availability": {"requested": 30, "observed_eligible": len(eligible), "invented": 0, "quota_filled": len(eligible) >= 30},
        "signal_payload": {"rss": rss, "trends": trends, "youtube": yt, "suggestions": sugg, "reddit": reddit},
        "validation": {"state": "warsmith_review", "premium_used": bool(question_plan), "anti_invention": "pass"},
        "question_plan": question_plan or [],
    }


def build_packs(candidates: list[dict], max_packs: int = 5) -> list[dict]:
    """Propose des paires ancre/contraste uniquement entre candidats distincts."""
    packs = []
    for anchor in candidates:
        for contrast in candidates:
            if anchor["candidate_id"] >= contrast["candidate_id"]:
                continue
            if anchor.get("normalized_key") == contrast.get("normalized_key"):
                continue
            shared = set(anchor.get("normalized_key", "").split()) & set(contrast.get("normalized_key", "").split())
            if not shared:
                continue
            if anchor.get("ocean") == contrast.get("ocean") and anchor.get("ocean") == "desert":
                continue
            packs.append({
                "pack_id": "PACK-" + hashlib.sha1((anchor["candidate_id"] + contrast["candidate_id"]).encode()).hexdigest()[:8],
                "words": [anchor["keyword"], contrast["keyword"]],
                "anchor_candidate_id": anchor["candidate_id"],
                "contrast_candidate_id": contrast["candidate_id"],
                "ocean_mix": [anchor.get("ocean"), contrast.get("ocean")],
                "anti_cannibalization": "pass",
                "decision": "warsmith_review",
            })
            if len(packs) >= max_packs:
                return packs
    return packs


def allocate_angles(candidates: list[dict], total: int, blue: int | None = None,
                    red: int | None = None) -> dict:
    if total < 1:
        raise ValueError("total angles doit être positif")
    blue_available = sum(1 for c in candidates if c.get("ocean") == "blue")
    red_available = sum(1 for c in candidates if c.get("ocean") == "red")
    if blue is None and red is None:
        blue = total // 2
        red = total - blue
    elif blue is None:
        red = red or 0
        blue = total - red
    elif red is None:
        blue = blue or 0
        red = total - blue
    if blue + red != total:
        raise ValueError("allocation angles incohérente")
    return {
        "requested_total": total,
        "requested_blue": blue,
        "requested_red": red,
        "available_blue_candidates": blue_available,
        "available_red_candidates": red_available,
        "status": "pass" if blue <= blue_available and red <= red_available else "insufficient_candidates",
        "decision": "warsmith_review",
    }
