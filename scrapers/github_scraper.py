"""
GitHub Scraper - Finds repos listing European AI/ML/SWE job opportunities,
PhD positions, professor directories, and outreach resources.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from fake_useragent import UserAgent


def get_headers():
    try:
        ua = UserAgent()
        return {"User-Agent": ua.random}
    except:
        return {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


# Curated list of known awesome repos + search queries
KNOWN_REPOS = [
    {
        "name": "academic/awesome-datascience",
        "url": "https://github.com/academic/awesome-datascience",
        "description": "Awesome Data Science repository - comprehensive list of resources",
        "category": "jobs_and_resources",
    },
    {
        "name": "jbhuang0604/awesome-computer-vision",
        "url": "https://github.com/jbhuang0604/awesome-computer-vision",
        "description": "Curated list of awesome computer vision resources",
        "category": "phd_and_research",
    },
    {
        "name": "dair-ai/ML-YouTube-Courses",
        "url": "https://github.com/dair-ai/ML-YouTube-Courses",
        "description": "ML/AI courses and connections to researchers",
        "category": "learning_and_networking",
    },
    {
        "name": "christine-hu/machine-learning-jobs",
        "url": "https://github.com/christine-hu/machine-learning-jobs",
        "description": "Machine Learning job listings tracker",
        "category": "jobs_and_resources",
    },
    {
        "name": "academicpages/academicpages.github.io",
        "url": "https://github.com/academicpages/academicpages.github.io",
        "description": "Academic pages template - find professors' pages and research",
        "category": "phd_and_research",
    },
    {
        "name": "JdeRobot/JdeRobot",
        "url": "https://github.com/JdeRobot",
        "description": "European robotics/AI research org with open positions",
        "category": "european_research",
    },
    {
        "name": "thuiar/awesome-artificial-intelligence",
        "url": "https://github.com/owainlewis/awesome-artificial-intelligence",
        "description": "Curated list of AI courses, books, video lectures, papers",
        "category": "learning_and_networking",
    },
]

SEARCH_QUERIES = [
    "europe AI ML PhD positions 2026",
    "awesome europe tech jobs",
    "european machine learning research positions",
    "europe software engineer visa sponsorship",
    "phd positions europe computer science",
    "AI research internship europe",
    "awesome-europe-jobs",
    "europe-tech-companies hiring",
    "NLP computer vision jobs europe",
    "european universities AI research labs",
]


def search_github_repos(query, max_results=10):
    """Search GitHub for repos matching the query"""
    results = []
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": max_results,
        }
        resp = requests.get(url, params=params, headers=get_headers(), timeout=15)

        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("items", []):
                results.append({
                    "name": item["full_name"],
                    "url": item["html_url"],
                    "description": item.get("description", "No description"),
                    "stars": item["stargazers_count"],
                    "language": item.get("language", "Unknown"),
                    "updated": item["updated_at"][:10],
                    "source": "github_search",
                    "query": query,
                })
        elif resp.status_code == 403:
            print(f"GitHub API rate limited for query: {query}")
        time.sleep(2)  # Rate limiting
    except Exception as e:
        print(f"Error searching GitHub for '{query}': {e}")

    return results


def scrape_all_github():
    """Run all GitHub searches and return combined results"""
    all_results = []

    # Add known repos first
    for repo in KNOWN_REPOS:
        all_results.append({
            **repo,
            "stars": "curated",
            "language": "-",
            "updated": "-",
            "source": "curated_list",
            "query": "curated",
        })

    # Search GitHub
    for query in SEARCH_QUERIES:
        results = search_github_repos(query, max_results=5)
        all_results.extend(results)
        time.sleep(1)

    # Deduplicate by URL
    seen = set()
    unique = []
    for r in all_results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    return unique


# --- University & Professor Outreach ---

ELITE_EUROPEAN_UNIVERSITIES = [
    {"name": "ETH Zurich", "country": "Switzerland", "url": "https://ethz.ch", "cs_dept": "https://inf.ethz.ch/research.html"},
    {"name": "EPFL", "country": "Switzerland", "url": "https://epfl.ch", "cs_dept": "https://www.epfl.ch/schools/ic/"},
    {"name": "University of Oxford", "country": "UK", "url": "https://ox.ac.uk", "cs_dept": "https://www.cs.ox.ac.uk/"},
    {"name": "University of Cambridge", "country": "UK", "url": "https://cam.ac.uk", "cs_dept": "https://www.cst.cam.ac.uk/"},
    {"name": "Imperial College London", "country": "UK", "url": "https://imperial.ac.uk", "cs_dept": "https://www.imperial.ac.uk/computing"},
    {"name": "UCL", "country": "UK", "url": "https://ucl.ac.uk", "cs_dept": "https://www.ucl.ac.uk/computer-science/"},
    {"name": "University of Edinburgh", "country": "UK", "url": "https://ed.ac.uk", "cs_dept": "https://www.ed.ac.uk/informatics"},
    {"name": "TU Munich", "country": "Germany", "url": "https://tum.de", "cs_dept": "https://www.in.tum.de/en/"},
    {"name": "Max Planck Institutes", "country": "Germany", "url": "https://www.mpg.de/en", "cs_dept": "https://www.mpg.de/institutes"},
    {"name": "RWTH Aachen", "country": "Germany", "url": "https://rwth-aachen.de", "cs_dept": "https://www.informatik.rwth-aachen.de/"},
    {"name": "University of Amsterdam", "country": "Netherlands", "url": "https://uva.nl", "cs_dept": "https://www.uva.nl/en/about-the-uva/organisation/faculties/faculty-of-science/"},
    {"name": "TU Delft", "country": "Netherlands", "url": "https://tudelft.nl", "cs_dept": "https://www.tudelft.nl/en/eemcs/"},
    {"name": "KTH Royal Institute", "country": "Sweden", "url": "https://kth.se", "cs_dept": "https://www.kth.se/en/eecs"},
    {"name": "DTU", "country": "Denmark", "url": "https://dtu.dk", "cs_dept": "https://www.dtu.dk/english/research"},
    {"name": "Aalto University", "country": "Finland", "url": "https://aalto.fi", "cs_dept": "https://www.aalto.fi/en/department-of-computer-science"},
    {"name": "INRIA", "country": "France", "url": "https://www.inria.fr/en", "cs_dept": "https://www.inria.fr/en/research"},
    {"name": "Sorbonne University", "country": "France", "url": "https://www.sorbonne-universite.fr/en", "cs_dept": "https://www.sorbonne-universite.fr/en"},
    {"name": "PSL University / ENS Paris", "country": "France", "url": "https://psl.eu/en", "cs_dept": "https://www.di.ens.fr/"},
    {"name": "Trinity College Dublin", "country": "Ireland", "url": "https://tcd.ie", "cs_dept": "https://www.scss.tcd.ie/"},
    {"name": "University of Zurich", "country": "Switzerland", "url": "https://uzh.ch", "cs_dept": "https://www.ifi.uzh.ch/en.html"},
    {"name": "Politecnico di Milano", "country": "Italy", "url": "https://polimi.it", "cs_dept": "https://www.deib.polimi.it/eng/"},
    {"name": "TU Wien", "country": "Austria", "url": "https://www.tuwien.at/en/", "cs_dept": "https://informatics.tuwien.ac.at/"},
    {"name": "KU Leuven", "country": "Belgium", "url": "https://kuleuven.be", "cs_dept": "https://wms.cs.kuleuven.be/"},
    {"name": "University of Helsinki", "country": "Finland", "url": "https://helsinki.fi", "cs_dept": "https://www.helsinki.fi/en/faculty-science/faculty/computer-science"},
    {"name": "CISPA", "country": "Germany", "url": "https://cispa.de", "cs_dept": "https://cispa.de/en/research"},
    {"name": "University of Warsaw", "country": "Poland", "url": "https://uw.edu.pl", "cs_dept": "https://www.mimuw.edu.pl/en"},
]

PROFESSOR_OUTREACH_TIPS = {
    "email_template": """Subject: Prospective PhD/RA Student - [Your Research Interest] - [Your Name], [Your University]

Dear Professor [Last Name],

I am [Your Name], a [Master's/graduating] student in Computer Science at [University] in the United States, originally from India. I am writing to express my strong interest in your research on [SPECIFIC PAPER/PROJECT NAME].

I was particularly drawn to your work on [SPECIFIC DETAIL] because [WHY IT MATTERS TO YOU/YOUR EXPERIENCE]. In my recent work, I have [BRIEF RELEVANT EXPERIENCE - 1-2 sentences].

I am seeking [PhD/Research Assistant] opportunities starting June 2026. I would be grateful for the opportunity to discuss potential positions in your group.

I have attached my CV and am happy to provide any additional materials.

Thank you for your time and consideration.

Best regards,
[Your Name]
[LinkedIn URL]
[GitHub URL]""",

    "strategies": [
        "Read 2-3 of the professor's recent papers BEFORE emailing - reference specific findings",
        "Follow them on Twitter/X and engage with their research posts",
        "Check if their PhD students have personal websites - reach out to them for insider info",
        "Look for professors who have supervised international students before (check lab pages)",
        "Attend virtual seminars/talks by the professor's research group",
        "Check if the professor has upcoming conference presentations - attend and introduce yourself",
        "Look for professors who list 'open positions' on their website - these are warm leads",
        "Use Google Scholar to find professors whose h-index and recent activity suggest active labs",
        "Check DBLP for recent co-authors who might be postdocs/senior PhDs willing to chat",
        "Apply to summer schools/workshops run by the research group as a foot in the door",
    ],

    "ta_ra_strategies": [
        "Many European universities post RA/TA positions on their department websites",
        "Check euraxess.ec.europa.eu - EU's official researcher mobility portal",
        "Look for funded PhD positions (no recommendation letters needed for many EU positions)",
        "Some positions only require a motivation letter + CV (no recommendations)",
        "Check if universities have 'scientific programmer' or 'research engineer' roles",
        "DAAD (daad.de) for Germany-specific funded positions",
        "Marie Curie fellowships - EU-funded, often English-only requirement",
    ],
}


def get_university_data():
    """Return university data with outreach tips"""
    return {
        "universities": ELITE_EUROPEAN_UNIVERSITIES,
        "outreach": PROFESSOR_OUTREACH_TIPS,
    }


if __name__ == "__main__":
    import json
    results = scrape_all_github()
    print(json.dumps(results, indent=2))
