"""
capteurs.py — CAPTEURS : Les Yeux du Siège (forge CLIPPING)
===========================================================

Réseau de senseurs de l'écosystème clipping. COMMANDITÉ par le
Warsmith — jamais de cron, jamais d'auto. Produit une cartographie
complète (Whop + sites clipping + perception niche) pour que
F02_TYRANT_CAMP rende son verdict GO/NO-GO + blue_ocean en connaissance
de cause.

Commandes:
  python capteurs.py --scan --campaign IN/campaign_to_observe.json
  python capteurs.py --scan-demons --scan-list IN/scan_list.json
  python capteurs.py --scrap-youtube --channel <url> [--max-videos 20]

Hérésies gardées :
  - Scrap automatique (pas de cron, pas d'auto-loop)
  - Scrap de sites non listés dans clipping_sites_to_scrap.json
    (Whop est TOUJOURS scanné — défaut système)
  - Scraper après la fermeture de campagne (campaign_status closed)
"""

import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_CAPTEURS_DIR = os.path.dirname(_SCRIPT_DIR)
_FORGE_ROOT = os.path.dirname(_CAPTEURS_DIR)

sys.path.insert(0, os.path.join(_SCRIPT_DIR, "libs"))
from whop_scanner import WhopScanner
from clipping_ecosystem_scanner import ClippingEcosystemScanner
from campaign_context_scanner import CampaignContextScanner
from demon_scanner import DemonScanner
from youtube_channel_scraper import YoutubeChannelScraper
from f00_rss_ingestor import scan as rss_scan
from f00_trends_ingestor import scan as trends_scan
from f00_youtube_ingestor import scan as youtube_scan
from f00_suggestions_ingestor import scan as suggestions_scan
from f00_virality_scorer import score_subject
from f00_premium_synth import synthesize as premium_synthesize

OUT_DIR = os.path.join(_CAPTEURS_DIR, "OUT")
IN_DIR = os.path.join(_CAPTEURS_DIR, "IN")
ARCHIVUM_DIR = os.path.join(_FORGE_ROOT, "ARCHIVUM")
LIBER_PATH = os.path.join(_FORGE_ROOT, "liber_clipping.json")
DEMONS_DIR = os.path.join(ARCHIVUM_DIR, "demons")

WHOP_DISCOVER_DEFAULT = "https://whop.com/discover/"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: str, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ----------------------------------------------------------------------
# Gardes (hérésies)
# ----------------------------------------------------------------------
def guard_campaign_open():
    liber = load_json(LIBER_PATH)
    if liber and liber.get("campaign_status") == "closed":
        print("[CAPTEURS] HÉRÉSIE: campagne fermée — CAPTEURS est éteint "
              "(F06 --close-campaign a scellé le siège). Réarme via un nouveau siège.")
        sys.exit(1)


def guard_sites_list(sites: list[dict], config: dict) -> list[dict]:
    allowed = {s.get("name") for s in config.get("sites", []) or []}
    scannable = [s for s in sites if s.get("name") in allowed]
    rejected = [s.get("name") for s in sites if s.get("name") not in allowed]
    for name in rejected:
        print(f"[CAPTEURS] Site '{name}' non listé dans clipping_sites_to_scrap.json "
              f"— HÉRÉSIE, ignoré")
    return scannable


# ----------------------------------------------------------------------
# Scan principal
# ----------------------------------------------------------------------
def cmd_scan(args):
    guard_campaign_open()

    campaign = load_json(args.campaign)
    if not campaign:
        print(f"[CAPTEURS] campaign_to_observe introuvable: {args.campaign}")
        sys.exit(1)

    sites_config = load_json(
        os.path.join(IN_DIR, "clipping_sites_to_scrap.json"), {"sites": []})
    sites = guard_sites_list(sites_config.get("sites", []) or [], sites_config)
    campaign_url = campaign.get("campaign_url") or ""
    niche = campaign.get("niche") or "unknown"
    if not campaign_url:
        print("[CAPTEURS] campaign_url manquant dans campaign_to_observe.json")
        sys.exit(1)

    scan_id = f"SCAN-{uuid.uuid4().hex[:8]}"
    carto = {
        "scan_id": scan_id,
        "scanned_at": now_iso(),
        "campaign": {
            "campaign_id": campaign.get("campaign_id"),
            "campaign_url": campaign_url,
            "niche": niche,
            "questions": campaign.get("questions", []),
        },
        "whop_scan": None,
        "ecosystem_scan": None,
        "niche_perception": None,
        "demon_scan": None,
        "check_in_iw_custos": None,
    }

    whop = WhopScanner(campaign_url,
                       campaign.get("whop_discover_url") or WHOP_DISCOVER_DEFAULT)
    carto["whop_scan"] = whop.scan()

    ecosystem = ClippingEcosystemScanner(sites)
    carto["ecosystem_scan"] = ecosystem.scan()

    context = CampaignContextScanner(
        campaign_url,
        niche=niche,
        sources=campaign.get("context_sources", []) or [])
    context_result = context.scan()
    carto["ecosystem_scan"]["competitors_observed"] = context_result["competitors_observed"]
    carto["ecosystem_scan"]["angles_already_used_on_this_campaign"] = \
        context_result["angles_already_used"]

    carto["niche_perception"] = _niche_perception(
        niche, carto["ecosystem_scan"], context_result)

    out = os.path.join(OUT_DIR, "cartographie.json")
    save_json(out, carto)

    md_path = _write_cartographie_md(carto, scan_id)

    custos = os.path.join(_FORGE_ROOT, "IW_CUSTOS.py")
    if os.path.exists(custos):
        subprocess.run([sys.executable, custos, "--mode", "check-in",
                        "--frigate", "CAPTEURS", "--output", md_path],
                       capture_output=True, text=True, timeout=30)
    print(f"[CAPTEURS] Scan {scan_id} terminé — {out}")
    print(f"[CAPTEURS] {md_path} — check-in IW_CUSTOS (fleet_status -> capteurs_done)")


def _niche_perception(niche: str, ecosystem: dict, context_result: dict) -> dict:
    emotions = ["tension", "joie", "inspiration", "outrage", "admiration"]
    corpus = " ".join(
        str((s.get("data_extracted") or {}).get("title", ""))
        for s in ecosystem.get("scanned_sites", []) or [])
    corpus += " " + " ".join(
        str(c.get("angle_used", "")) for c in context_result["competitors_observed"])
    hits = {e: corpus.lower().count(e) for e in emotions}
    dominant = max(hits, key=hits.get) if any(hits.values()) else None

    saturated = []
    for angle in context_result["angles_already_used"]:
        result = angle.get("result", "medium")
        if result in ("medium", "high"):
            saturated.append(angle.get("angle", ""))
    saturated = sorted(set(a for a in saturated if a))

    return {
        "dominant_emotion_in_niche": dominant or "non_estime",
        "saturated_angles": saturated,
        "undersaturated_angles": [],
        "requires_vision": [
            f"perception niche '{niche}' non quantifiable mécaniquement — "
            f"lecture IRON de l'écosystème requise"
        ],
    }


def _write_cartographie_md(carto: dict, scan_id: str) -> str:
    whop = carto.get("whop_scan") or {}
    eco = carto.get("ecosystem_scan") or {}
    niche = carto.get("niche_perception") or {}

    lines = [
        "# CAPTEURS — Cartographie du siège",
        "",
        f"- Scan : {scan_id}",
        f"- Date : {carto.get('scanned_at')}",
        f"- Campagne : {carto.get('campaign', {}).get('campaign_url')}",
        f"- Niche : {carto.get('campaign', {}).get('niche')}",
        "",
        "## Whop",
        f"- Statut page : {whop.get('campaign_status', '?')}",
        f"- Budget restant (est.) : {whop.get('campaign_budget_remaining_estimate', '?')}",
        f"- CPM attendu : {whop.get('cpm_expected', '?')}",
        f"- Guidelines : {whop.get('campaign_guidelines', '?')}",
        f"- Assets publiés : {len(whop.get('campaign_assets_published', []) or [])}",
        "",
        "## Sites scannés",
    ]
    for site in eco.get("scanned_sites", []) or []:
        data = site.get("data_extracted", {}) or {}
        lines.append(f"- {site.get('site')}: {site.get('status', '?')} — "
                     f"{data.get('title', '—')} (payouts: {data.get('payouts_observed', [])})")
    lines += [
        "",
        "## Compétiteurs observés",
    ]
    for comp in eco.get("competitors_observed", []) or []:
        lines.append(f"- {comp.get('clipper_name', '?')} | {comp.get('platform', '?')} "
                     f"| vues {comp.get('views', '?')} | angle: {comp.get('angle_used', '?')}")
    lines += [
        "",
        "## Angles déjà utilisés sur cette campagne",
    ]
    for angle in eco.get("angles_already_used_on_this_campaign", []) or []:
        lines.append(f"- {angle.get('angle')} ({angle.get('competitor')}) -> "
                     f"{angle.get('result')}")
    lines += [
        "",
        "## Perception niche",
        f"- Émotion dominante : {niche.get('dominant_emotion_in_niche', '?')}",
        f"- Angles saturés : {', '.join(niche.get('saturated_angles', [])) or 'aucun détecté'}",
    ]
    vision = niche.get("requires_vision", []) or []
    if vision:
        lines += ["", "## À faire lire par l'IRON"]
        for v in vision:
            lines.append(f"- {v}")
    lines.append("")
    lines.append("*Fer au-dedans, Fer au-dehors. Rien n'échappe au siège.*")

    path = os.path.join(OUT_DIR, "cartographie.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


# ----------------------------------------------------------------------
# Scan demons (wild clipping)
# ----------------------------------------------------------------------
def cmd_scan_demons(args):
    guard_campaign_open()
    scan_list = load_json(args.scan_list)
    if not scan_list or not scan_list.get("queries"):
        print(f"[CAPTEURS] scan_list.json introuvable ou vide: {args.scan_list}")
        sys.exit(1)

    scanner = DemonScanner(scan_list.get("queries", []) or [])
    result = scanner.scan()

    scan_id = f"DEMON-{uuid.uuid4().hex[:8]}"
    out = os.path.join(DEMONS_DIR, f"demon_wild_scan_{scan_id}.json")
    save_json(out, result)
    print(f"[CAPTEURS] Scan demons {scan_id} — {out}")
    print(f"[CAPTEURS] {len(result.get('demons_observed', []))} démon(s) observé(s), "
          f"{len(result.get('requires_vision', []))} sonde(s) à lire par l'IRON")
    print("[CAPTEURS] TYRANT prospectif peut poursuivre l'analyse (ARCHIVUM/demons/)")


# ----------------------------------------------------------------------
# Scrap de chaînes YouTube (base de savoir copywriting)
# ----------------------------------------------------------------------
def cmd_scrap_youtube(args):
    guard_campaign_open()

    channel_url = args.channel
    if not channel_url and args.scan_list:
        scan_list = load_json(args.scan_list)
        channels = scan_list.get("channels", []) if scan_list else []
        channel_url = channels[0] if channels else None
    if not channel_url:
        print("[CAPTEURS] --channel requis pour --scrap-youtube "
              "(ou IN/scan_list.json -> {\"channels\": [...]})")
        sys.exit(1)

    kb_transcripts = os.path.join(ARCHIVUM_DIR, "knowledge_base", "transcripts")
    out_dir = args.out or kb_transcripts
    scraper = YoutubeChannelScraper(channel_url, out_dir,
                                    max_videos=args.max_videos,
                                    languages=(args.languages or
                                               ["fr", "en", "en-US"]),
                                    rate_limit_sec=args.rate_limit)
    try:
        result = scraper.scrape()
    except RuntimeError as e:
        print(f"[CAPTEURS] Scrap échoué: {e}")
        sys.exit(1)

    print(f"[CAPTEURS] Chaîne: {result.get('channel_name')} ({result.get('channel_slug')})")
    print(f"[CAPTEURS] {len(result['captured'])} capturée(s), "
          f"{len(result['skipped'])} déjà archivée(s), "
          f"{len(result['failed'])} échec(s)")
    print(f"[CAPTEURS] Archivé: {result['out_dir']}")


# ----------------------------------------------------------------------
# Scan de sujets viraux (F00_CAPTEURS)
# ----------------------------------------------------------------------
FRESHNESS_WINDOWS = {"brulant": 5, "frais": 24}


def _derive_keywords(niche: str) -> list[str]:
    """Dérive jusqu'à 6 mots-clés de la niche (phrase + bigrammes)."""
    words = [w.strip() for w in niche.split() if w.strip()]
    kws = [niche] if niche else []
    for w in words:
        if len(kws) >= 6:
            break
        if w not in kws:
            kws.append(w)
    if len(kws) < 6 and len(words) > 1:
        bigrams = [" ".join(words[i:i + 2]) for i in range(len(words) - 1)]
        for bg in bigrams:
            if len(kws) >= 6:
                break
            if bg not in kws:
                kws.append(bg)
    return kws[:6]


def _hot_keywords() -> list[str]:
    """En mode --hot, prend les requêtes montantes du RSS Trends comme mots-clés."""
    from f00_trends_ingestor import scan_global_trending
    top = scan_global_trending(max_items=6)
    queries = [t["query"] for t in top.get("trending", []) or []]
    return queries[:6] or ["trending"]


def _capteur_snapshot(module: str, kw: str, result: dict) -> dict:
    """Normalise le résultat d'un capteur pour le payload de synthèse."""
    return {"module": module, "keyword": kw, "result": result}


def cmd_scan_subjects(args):
    guard_campaign_open()

    niche = args.niche
    hot = args.hot
    if not niche and not hot:
        print("[F00_CAPTEURS] --niche <nom> OU --hot requis")
        sys.exit(1)

    mode = args.mode or "informatif"
    freshness = args.freshness or "brulant"
    if freshness not in FRESHNESS_WINDOWS:
        print(f"[F00_CAPTEURS] freshness inconnue: {freshness} "
              f"(brulant|frais)"); sys.exit(1)

    keywords = _hot_keywords() if hot else _derive_keywords(niche)
    print(f"[F00_CAPTEURS] niche={niche or 'hot'} | mode={mode} | "
          f"fraîcheur={freshness} ({FRESHNESS_WINDOWS[freshness]}h) | "
          f"keywords={keywords}")

    # ---- Capture des 4 signaux (toujours en direct, jamais inventé) ----
    rss = rss_scan(keywords, freshness=freshness, max_items=args.max_items)
    trends = trends_scan(keywords)
    yt = youtube_scan(keywords, max_results=8)
    sugg = suggestions_scan(keywords)

    payload = {
        "config": {"niche": niche, "hot": hot, "mode": mode,
                   "freshness": freshness,
                   "window_hours": FRESHNESS_WINDOWS[freshness],
                   "keywords": keywords},
        "signal_rss_fraicheur": _capteur_snapshot("rss", keywords[0], rss),
        "signal_tendance": trends,
        "signal_vues_youtube": yt,
        "signal_demande": sugg,
        "scoring_method": {
            "weights": {"vues_youtube": 0.30, "tendance": 0.25,
                        "fraicheur": 0.20, "demande": 0.15,
                        "couverture": 0.10},
            "note": "GLM 5.2 synthétise à partir de ces seules observations",
        },
    }

    scan_id = f"F00-{uuid.uuid4().hex[:8]}"
    print(f"[F00_CAPTEURS] Capture signaux ok ({scan_id}) — synthèse GLM 5.2…")

    synth = premium_synthesize(niche, hot, mode, freshness, payload)
    if synth.get("status") != "ok":
        print(f"[F00_CAPTEURS] SYNTHÈSE ÉCHOUÉE: {synth.get('error')}")
        sys.exit(1)

    subjects = synth["subjects"]
    for s in subjects:
        s["scan_id"] = scan_id

    proposal = {
        "scan_id": scan_id,
        "scanned_at": now_iso(),
        "config": payload["config"],
        "signal_payload": payload,
        "subjects": subjects,
        "premium_model": "z-ai/glm-5.2",
        "gate": "warsmith_chooses",
        "note": "Le Warsmith choisit le sujet après lecture du tableau — "
                "aucun top-1 automatique.",
    }
    out_json = os.path.join(OUT_DIR, "subjects_proposal.json")
    save_json(out_json, proposal)

    md_path = _write_subjects_proposal_md(proposal, out_json)
    print(f"[F00_CAPTEURS] Proposition écrite: {out_json}")
    print(f"[F00_CAPTEURS] Tableau bilingue: {md_path}")

    export_dir = os.path.join(_FORGE_ROOT, "EXPORT")
    os.makedirs(export_dir, exist_ok=True)
    for fname, fpath in (("subjects_proposal.json", out_json),
                         ("subjects_proposal.md", md_path)):
        export_path = os.path.join(export_dir, fname)
        with open(fpath, "r", encoding="utf-8") as fsrc, \
                open(export_path, "w", encoding="utf-8") as fdst:
            fdst.write(fsrc.read())
    print(f"[F00_CAPTEURS] Exporté dans {export_dir} (checkable sur GitHub)")

    custos = os.path.join(_FORGE_ROOT, "IW_CUSTOS.py")
    if os.path.exists(custos):
        subprocess.run([sys.executable, custos, "--mode", "check-in",
                        "--frigate", "CAPTEURS", "--output", md_path],
                       capture_output=True, text=True, timeout=30)
    print("[F00_CAPTEURS] check-in IW_CUSTOS — le Warsmith choisit le sujet.")


def _write_subjects_proposal_md(proposal: dict, json_path: str) -> str:
    cfg = proposal["config"]
    lines = [
        "# F00_CAPTEURS — Proposition de sujets viraux",
        "",
        f"- Scan : {proposal['scan_id']}",
        f"- Date : {proposal['scanned_at']}",
        f"- Niche : {cfg.get('niche') or 'HOT (actu montante)'}",
        f"- Mode : {cfg.get('mode')} | Fraîcheur : {cfg.get('freshness')} "
        f"({cfg.get('window_hours')}h)",
        f"- Modèle : {proposal['premium_model']} (synthèse — stats observées)",
        "",
        "## Tableau des 5 sujets (score /10, métriques réelles)",
        "",
        "| # | Sujet (EN) | Score | Vues YT top | Recherche | Tendance 7j | "
        "Demande | Fraîcheur | Couverture | Sous-mode |",
        "|---|------------|-------|-------------|-----------|-------------|"
        "---------|-----------|------------|-----------|",
    ]
    for i, s in enumerate(proposal["subjects"], 1):
        m = s.get("metrics") or {}
        def fmt(key):
            v = m.get(key)
            return "—" if v is None else str(v)
        lines.append(
            f"| {i} | {s.get('subject_en','')} | **{s.get('score_10')}** | "
            f"{fmt('top_video_views')} | {fmt('yt_search_views')} | "
            f"{fmt('trend_growth_7d')} | {fmt('demand_score')} | "
            f"{fmt('freshness_hours')}h | {fmt('coverage_media_count')} | "
            f"{s.get('sous_mode','')} |")
    lines += ["", "## Détail par sujet", ""]
    for i, s in enumerate(proposal["subjects"], 1):
        m = s.get("metrics") or {}
        missing = m.get("signal_missing") or []
        lines += [
            f"### {i}. {s.get('subject_en','')} — score {s.get('score_10')}/10",
            "",
            f"**Notes (FR)** : {s.get('notes_fr','')}",
            "",
            f"**Angle 90s (FR)** : {s.get('angle_propose_fr','')}",
            "",
            f"**Métriques** : vues YT {m.get('top_video_views')} | "
            f"recherche {m.get('yt_search_views')} | tendance "
            f"{m.get('trend_growth_7d')} | demande {m.get('demand_score')} | "
            f"fraîcheur {m.get('freshness_hours')}h | couverture "
            f"{m.get('coverage_media_count')} médias",
            "",
            f"**Signaux manquants** : {', '.join(missing) or 'aucun'}",
            "",
            f"**Sources** : {' ; '.join(s.get('sources', []) or [])}",
            "",
            "**Clips background candidats** :",
        ]
        for c in s.get("clip_background_candidates", []) or []:
            lines.append(f"- {c.get('desc_fr','')} "
                         f"({c.get('source_hint','')})")
        lines += [
            "",
            f"**Checklists** : viabilité {'✅' if s.get('checklist_viabilite_ok') else '❌'} "
            f"| viralité {'✅' if s.get('checklist_viralite_ok') else '❌'} "
            f"({sum(1 for v in (s.get('viral_checks') or {}).values() if v)}/10)",
            "",
            "---",
            "",
        ]
    lines += ["", f"JSON complet : `{json_path}`", "",
              "*Le Warsmith choisit — aucun top-1 automatique.*"]

    path = os.path.join(OUT_DIR, "subjects_proposal.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def main():
    parser = argparse.ArgumentParser(description="CAPTEURS — Les Yeux du Siège")
    parser.add_argument("--scan", action="store_true",
                        help="Cartographie complète (Whop + sites + contexte)")
    parser.add_argument("--campaign", default=None,
                        help="Chemin vers IN/campaign_to_observe.json")
    parser.add_argument("--scan-demons", action="store_true",
                        help="Scan des Démon wild clipping (TikTok/Shorts/Reels)")
    parser.add_argument("--scan-list", default=None,
                        help="Chemin vers IN/scan_list.json (queries demons ou chaînes)")
    parser.add_argument("--scrap-youtube", action="store_true",
                        help="Scrap d'une chaîne YouTube commanditée (transcripts + méta)")
    parser.add_argument("--channel", default=None,
                        help="URL de la chaîne YouTube à scraper")
    parser.add_argument("--max-videos", type=int, default=20,
                        help="Nombre max de vidéos par chaîne (défaut 20)")
    parser.add_argument("--out", default=None,
                        help="Dossier d'archivage (défaut ARCHIVUM/knowledge_base/transcripts)")
    parser.add_argument("--languages", nargs="*", default=None,
                        help="Langues de transcript préférées")
    parser.add_argument("--rate-limit", type=float, default=1.0,
                        help="Secondes entre deux captures (défaut 1.0)")
    parser.add_argument("--scan-subjects", action="store_true",
                        help="F00: proposer 5 sujets viraux (niche OU hot)")
    parser.add_argument("--niche", default=None,
                        help="Nom de la niche (ex: 'Lakers basketball')")
    parser.add_argument("--hot", action="store_true",
                        help="Mode HOT: les requêtes montantes du RSS Trends")
    parser.add_argument("--mode", choices=["informatif", "humour"], default=None,
                        help="Sous-mode dominant (défaut informatif)")
    parser.add_argument("--freshness", choices=["brulant", "frais"],
                        default="brulant",
                        help="Fenêtre de fraîcheur (défaut brulant=5h)")
    parser.add_argument("--max-items", type=int, default=10,
                        help="Articles RSS max par scan (défaut 10)")
    args = parser.parse_args()

    if args.scan:
        if not args.campaign:
            print("[CAPTEURS] --campaign requis pour --scan"); sys.exit(1)
        cmd_scan(args)
    elif args.scan_demons:
        if not args.scan_list:
            print("[CAPTEURS] --scan-list requis pour --scan-demons"); sys.exit(1)
        cmd_scan_demons(args)
    elif args.scrap_youtube:
        cmd_scrap_youtube(args)
    elif args.scan_subjects:
        cmd_scan_subjects(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
