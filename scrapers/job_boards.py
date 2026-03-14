"""
Job Board Scraper - Scrapes European job boards and aggregators
for AI/ML/SWE/PhD positions with visa sponsorship and English-friendly roles.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from fake_useragent import UserAgent
from urllib.parse import quote_plus


def get_headers():
    try:
        ua = UserAgent()
        return {"User-Agent": ua.random}
    except:
        return {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


# ============================================================
# CURATED JOB BOARDS & PLATFORMS (guaranteed useful links)
# ============================================================

JOB_PLATFORMS = [
    # --- PhD & Research Positions ---
    {
        "name": "EURAXESS - EU Researcher Jobs",
        "url": "https://euraxess.ec.europa.eu/jobs/search",
        "search_url": "https://euraxess.ec.europa.eu/jobs/search/field_research_field/computer-science-702",
        "type": "phd_research",
        "description": "Official EU portal for researcher mobility. PhD, postdoc, and research positions across all EU countries.",
        "english_friendly": True,
        "recommendations_required": "varies",
        "visa_sponsorship": True,
    },
    {
        "name": "FindAPhD - Europe",
        "url": "https://www.findaphd.com/phds/?Keywords=artificial+intelligence&Location=europe",
        "search_url": "https://www.findaphd.com/phds/?Keywords=machine+learning&Location=europe",
        "type": "phd_research",
        "description": "Largest database of PhD opportunities. Filter by country, funding, and field.",
        "english_friendly": True,
        "recommendations_required": "usually",
        "visa_sponsorship": True,
    },
    {
        "name": "AcademicPositions.com",
        "url": "https://academicpositions.com/jobs?q=computer+science&location=europe",
        "search_url": "https://academicpositions.com/jobs?q=artificial+intelligence&location=europe",
        "type": "phd_research",
        "description": "Academic jobs across Europe - PhD, postdoc, professor, and research positions.",
        "english_friendly": True,
        "recommendations_required": "varies",
        "visa_sponsorship": True,
    },
    {
        "name": "Academic Transfer (Netherlands)",
        "url": "https://www.academictransfer.com/en/jobs/?q=computer+science",
        "search_url": "https://www.academictransfer.com/en/jobs/?q=machine+learning",
        "type": "phd_research",
        "description": "Dutch university jobs portal. Netherlands is very English-friendly!",
        "english_friendly": True,
        "recommendations_required": "sometimes",
        "visa_sponsorship": True,
    },
    {
        "name": "jobs.ac.uk (UK Academic Jobs)",
        "url": "https://www.jobs.ac.uk/search/?keywords=artificial+intelligence",
        "search_url": "https://www.jobs.ac.uk/search/?keywords=machine+learning+PhD",
        "type": "phd_research",
        "description": "UK's primary academic job board. PhD studentships, research associate roles.",
        "english_friendly": True,
        "recommendations_required": "usually",
        "visa_sponsorship": True,
    },
    {
        "name": "DAAD Scholarship Database",
        "url": "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/",
        "search_url": "https://www.daad.de/en/studying-in-germany/scholarships/",
        "type": "phd_research",
        "description": "German Academic Exchange Service - funded positions in Germany, many in English.",
        "english_friendly": True,
        "recommendations_required": "sometimes",
        "visa_sponsorship": True,
    },

    # --- Tech/SWE Job Boards ---
    {
        "name": "Landing.jobs (Europe Tech)",
        "url": "https://landing.jobs/jobs?keywords=artificial+intelligence&location=europe",
        "search_url": "https://landing.jobs/jobs?keywords=software+engineer&location=europe",
        "type": "tech_jobs",
        "description": "European tech job platform. Strong focus on visa sponsorship and relocation support.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": True,
    },
    {
        "name": "SwissDevJobs",
        "url": "https://swissdevjobs.ch",
        "search_url": "https://swissdevjobs.ch/jobs/machine-learning",
        "type": "tech_jobs",
        "description": "Swiss tech jobs. High salaries, English-friendly environment.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": "varies",
    },
    {
        "name": "relocate.me",
        "url": "https://relocate.me/search?q=ai+machine+learning",
        "search_url": "https://relocate.me/search?q=software+engineer",
        "type": "tech_jobs",
        "description": "Jobs that explicitly offer relocation packages. Perfect for international candidates!",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": True,
    },
    {
        "name": "EuroTechJobs",
        "url": "https://www.eurotechjobs.com/search/artificial+intelligence",
        "search_url": "https://www.eurotechjobs.com/search/software+engineer",
        "type": "tech_jobs",
        "description": "European tech job aggregator. Filter by country and English language requirement.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": "varies",
    },
    {
        "name": "Berlin Startup Jobs",
        "url": "https://berlinstartupjobs.com/engineering/",
        "search_url": "https://berlinstartupjobs.com/skill-areas/machine-learning/",
        "type": "tech_jobs",
        "description": "Berlin startup scene - very English-friendly, lots of AI/ML roles.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": True,
    },
    {
        "name": "Welcome to the Jungle (France/Europe)",
        "url": "https://www.welcometothejungle.com/en/jobs?query=artificial+intelligence&refinementList%5Blanguage%5D%5B0%5D=en",
        "search_url": "https://www.welcometothejungle.com/en/jobs?query=machine+learning",
        "type": "tech_jobs",
        "description": "Popular in France but expanding Europe-wide. Filter by English-speaking roles.",
        "english_friendly": "filter_available",
        "recommendations_required": False,
        "visa_sponsorship": "varies",
    },
    {
        "name": "Glassdoor Europe",
        "url": "https://www.glassdoor.com/Job/europe-artificial-intelligence-jobs-SRCH_IL.0,6_IN2_KO7,30.htm",
        "search_url": "https://www.glassdoor.com/Job/europe-machine-learning-jobs-SRCH_IL.0,6_IN2_KO7,23.htm",
        "type": "tech_jobs",
        "description": "Glassdoor's European job listings with company reviews and salary data.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": "varies",
    },
    {
        "name": "LinkedIn Jobs Europe",
        "url": "https://www.linkedin.com/jobs/search/?keywords=artificial%20intelligence&location=Europe",
        "search_url": "https://www.linkedin.com/jobs/search/?keywords=machine%20learning%20engineer&location=Europe",
        "type": "tech_jobs",
        "description": "LinkedIn's European job search. Use 'visa sponsorship' filter.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": "varies",
    },

    # --- AI/ML Specific ---
    {
        "name": "AI Jobs Europe",
        "url": "https://aijobs.net/jobs/?location=europe",
        "search_url": "https://aijobs.net",
        "type": "ai_specific",
        "description": "AI-focused job board with European listings.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": "varies",
    },
    {
        "name": "Hugging Face Jobs",
        "url": "https://apply.workable.com/huggingface/",
        "search_url": "https://huggingface.co/jobs",
        "type": "ai_specific",
        "description": "Hugging Face (HQ in Paris) - top NLP/ML company, English-speaking.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": True,
    },
    {
        "name": "DeepMind Careers",
        "url": "https://deepmind.google/about/careers/",
        "search_url": "https://deepmind.google/about/careers/",
        "type": "ai_specific",
        "description": "Google DeepMind - London-based AI research lab.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": True,
    },
    {
        "name": "ML Jobs List",
        "url": "https://mljobslist.com",
        "search_url": "https://mljobslist.com/jobs/?location=europe",
        "type": "ai_specific",
        "description": "Curated machine learning job listings.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": "varies",
    },

    # --- Visa-Friendly Resources ---
    {
        "name": "Visa Sponsorship Jobs (GitHub)",
        "url": "https://github.com/shubhampathak/visa-sponsorship-companies",
        "search_url": "https://github.com/topics/visa-sponsorship",
        "type": "visa_resource",
        "description": "Curated list of companies that sponsor work visas in Europe.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": True,
    },
    {
        "name": "EU Blue Card Guide",
        "url": "https://www.eu-bluecard.com/",
        "search_url": "https://www.eu-bluecard.com/",
        "type": "visa_resource",
        "description": "EU Blue Card info - the primary work visa for skilled workers in EU countries.",
        "english_friendly": True,
        "recommendations_required": False,
        "visa_sponsorship": True,
    },
]


def scrape_euraxess(keywords=None):
    """
    Scrape EURAXESS for research/PhD positions.
    Returns job listings with details.
    """
    if keywords is None:
        keywords = ["artificial intelligence", "machine learning", "computer science", "NLP", "computer vision"]

    results = []
    for kw in keywords:
        try:
            url = f"https://euraxess.ec.europa.eu/jobs/search/field_research_field/computer-science-702?keywords={quote_plus(kw)}"
            resp = requests.get(url, headers=get_headers(), timeout=15)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                listings = soup.select(".views-row")
                for listing in listings[:5]:
                    title_el = listing.select_one("h2 a, .views-field-title a")
                    if title_el:
                        results.append({
                            "title": title_el.get_text(strip=True),
                            "url": "https://euraxess.ec.europa.eu" + title_el.get("href", ""),
                            "source": "EURAXESS",
                            "keyword": kw,
                            "type": "research",
                        })
            time.sleep(2)
        except Exception as e:
            print(f"EURAXESS scrape error for '{kw}': {e}")

    return results


def scrape_findaphd(keywords=None):
    """Scrape FindAPhD for European PhD positions"""
    if keywords is None:
        keywords = ["artificial intelligence", "machine learning", "deep learning", "NLP", "computer vision"]

    results = []
    for kw in keywords:
        try:
            url = f"https://www.findaphd.com/phds/?Keywords={quote_plus(kw)}&Location=europe&PG=1"
            resp = requests.get(url, headers=get_headers(), timeout=15)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                listings = soup.select(".phd-result, .resultsRow")
                for listing in listings[:5]:
                    title_el = listing.select_one("h4 a, .d-none a, a.courseLink")
                    if title_el:
                        href = title_el.get("href", "")
                        if not href.startswith("http"):
                            href = "https://www.findaphd.com" + href
                        results.append({
                            "title": title_el.get_text(strip=True),
                            "url": href,
                            "source": "FindAPhD",
                            "keyword": kw,
                            "type": "phd",
                        })
            time.sleep(2)
        except Exception as e:
            print(f"FindAPhD scrape error for '{kw}': {e}")

    return results


def get_all_job_platforms():
    """Return the curated list of all job platforms with metadata"""
    return JOB_PLATFORMS


def scrape_job_boards():
    """Run all job board scrapers"""
    all_results = {
        "platforms": JOB_PLATFORMS,
        "scraped_euraxess": scrape_euraxess(),
        "scraped_findaphd": scrape_findaphd(),
    }
    return all_results


# --- Language Filter ---
NO_FRENCH_REQUIRED = [
    "English-only positions are common in: UK, Ireland, Netherlands, Scandinavia, Germany (many), Switzerland (partial)",
    "EU Blue Card does NOT require local language for most tech positions",
    "Startups across Europe typically operate in English",
    "Research positions at universities almost always accept English-only candidates",
    "EURAXESS listings often specify language requirements - filter for 'English'",
    "Germany: Many tech companies in Berlin, Munich work entirely in English",
    "Netherlands: Nearly everyone speaks English, very international work culture",
    "Nordics (Sweden, Denmark, Norway, Finland): Extremely English-friendly",
    "Switzerland: English common in tech, especially in Zurich/Geneva",
]

# --- No Recommendation Resources ---
NO_RECOMMENDATION_POSITIONS = [
    "Many funded PhD positions in Europe (especially Germany, Netherlands, Nordics) only require CV + motivation letter",
    "Industry positions NEVER require recommendation letters",
    "Research engineer/scientific programmer positions typically don't need recommendations",
    "Some Marie Curie positions have streamlined applications without letters",
    "RA positions at Max Planck, Fraunhofer often just need CV + cover letter",
    "Look for 'direct application' or 'apply now' positions on EURAXESS",
    "Many structured PhD programs (like IMPRS in Germany) have their own process without separate letters",
]


if __name__ == "__main__":
    import json
    data = scrape_job_boards()
    print(json.dumps(data, indent=2, default=str))
