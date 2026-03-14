"""
CareerScoutEuro - Y2K Pastel Aesthetic European Job Scraper
=============================================================
A web scraper that strategizes job search in European countries
for AI/ML/SWE/PhD opportunities for Indian students in the US.
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import threading

from scrapers.currency import compare_currencies, EUROPEAN_COUNTRIES
from scrapers.github_scraper import scrape_all_github, get_university_data
from scrapers.job_boards import scrape_job_boards, get_all_job_platforms, NO_FRENCH_REQUIRED, NO_RECOMMENDATION_POSITIONS
from scrapers.reddit_scraper import scrape_all_community

app = Flask(__name__)

# Cache for scraped data (so we don't re-scrape on every request)
_cache = {}
_scraping_status = {"status": "idle", "progress": ""}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/currency")
def api_currency():
    """Get European currency comparison data"""
    if "currency" not in _cache:
        _cache["currency"] = compare_currencies()
    return jsonify(_cache["currency"])


@app.route("/api/countries")
def api_countries():
    """Get list of all European countries with metadata"""
    return jsonify(EUROPEAN_COUNTRIES)


@app.route("/api/github")
def api_github():
    """Get GitHub repo search results"""
    if "github" not in _cache:
        _cache["github"] = scrape_all_github()
    return jsonify(_cache["github"])


@app.route("/api/universities")
def api_universities():
    """Get university data and professor outreach tips"""
    return jsonify(get_university_data())


@app.route("/api/jobs")
def api_jobs():
    """Get job board platforms and scraped listings"""
    if "jobs" not in _cache:
        _cache["jobs"] = scrape_job_boards()
    return jsonify(_cache["jobs"])


@app.route("/api/platforms")
def api_platforms():
    """Get curated list of job platforms (no scraping needed)"""
    return jsonify(get_all_job_platforms())


@app.route("/api/community")
def api_community():
    """Get Reddit and HackerNews results"""
    if "community" not in _cache:
        _cache["community"] = scrape_all_community()
    return jsonify(_cache["community"])


@app.route("/api/language-tips")
def api_language_tips():
    """Get language-related tips (no French needed!)"""
    return jsonify({
        "no_french_tips": NO_FRENCH_REQUIRED,
        "no_recommendation_tips": NO_RECOMMENDATION_POSITIONS,
    })


@app.route("/api/scrape-all", methods=["POST"])
def api_scrape_all():
    """Trigger a full scrape of all sources (runs in background)"""
    def _run_scrape():
        _scraping_status["status"] = "running"
        try:
            _scraping_status["progress"] = "Fetching currency data..."
            _cache["currency"] = compare_currencies()

            _scraping_status["progress"] = "Searching GitHub repos..."
            _cache["github"] = scrape_all_github()

            _scraping_status["progress"] = "Scraping job boards..."
            _cache["jobs"] = scrape_job_boards()

            _scraping_status["progress"] = "Searching Reddit & HackerNews..."
            _cache["community"] = scrape_all_community()

            _scraping_status["status"] = "done"
            _scraping_status["progress"] = "All scraping complete!"
        except Exception as e:
            _scraping_status["status"] = "error"
            _scraping_status["progress"] = str(e)

    if _scraping_status["status"] != "running":
        thread = threading.Thread(target=_run_scrape, daemon=True)
        thread.start()
        return jsonify({"message": "Scraping started!", "status": "running"})
    else:
        return jsonify({"message": "Scraping already in progress", "status": "running"})


@app.route("/api/scrape-status")
def api_scrape_status():
    """Check the status of the background scrape"""
    return jsonify(_scraping_status)


@app.route("/api/clear-cache", methods=["POST"])
def api_clear_cache():
    """Clear the cache to force fresh scraping"""
    _cache.clear()
    _scraping_status["status"] = "idle"
    _scraping_status["progress"] = ""
    return jsonify({"message": "Cache cleared!"})


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      ✿ CareerScoutEuro ✿                                ║
    ║      Y2K Pastel Edition                                  ║
    ║                                                          ║
    ║      European AI/ML/SWE Job Scraper                      ║
    ║      For Indian Students in the US                       ║
    ║                                                          ║
    ║      Open: http://127.0.0.1:5000                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, port=5000)
