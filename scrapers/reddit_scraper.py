"""
Reddit & Community Scraper
Finds relevant posts, threads, and resources about European AI/ML/SWE jobs
from Reddit, HackerNews, and other community sources.
"""

import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent


def get_headers():
    try:
        ua = UserAgent()
        return {"User-Agent": ua.random}
    except:
        return {"User-Agent": "CareerScoutEuro/1.0 (Educational Project)"}


# ============================================================
# CURATED REDDIT THREADS & COMMUNITY RESOURCES
# ============================================================

CURATED_SUBREDDITS = [
    {"subreddit": "r/cscareerquestionsEU", "url": "https://www.reddit.com/r/cscareerquestionsEU/", "description": "CS career questions specifically for Europe"},
    {"subreddit": "r/cscareerquestions", "url": "https://www.reddit.com/r/cscareerquestions/", "description": "General CS career questions - filter for Europe posts"},
    {"subreddit": "r/MachineLearning", "url": "https://www.reddit.com/r/MachineLearning/", "description": "ML community - job postings and research opportunities"},
    {"subreddit": "r/PhD", "url": "https://www.reddit.com/r/PhD/", "description": "PhD community - advice on European PhD applications"},
    {"subreddit": "r/GradSchool", "url": "https://www.reddit.com/r/GradSchool/", "description": "Graduate school advice including European programs"},
    {"subreddit": "r/IWantOut", "url": "https://www.reddit.com/r/IWantOut/", "description": "Immigration/relocation advice - visa info for Europe"},
    {"subreddit": "r/europe", "url": "https://www.reddit.com/r/europe/", "description": "European news and discussion"},
    {"subreddit": "r/artificial", "url": "https://www.reddit.com/r/artificial/", "description": "AI discussion and job opportunities"},
    {"subreddit": "r/datascience", "url": "https://www.reddit.com/r/datascience/", "description": "Data science community with European job posts"},
    {"subreddit": "r/india", "url": "https://www.reddit.com/r/india/", "description": "Indian community - visa and relocation experiences"},
    {"subreddit": "r/Indian_Academia", "url": "https://www.reddit.com/r/Indian_Academia/", "description": "Indian academic community - PhD abroad experiences"},
    {"subreddit": "r/developersIndia", "url": "https://www.reddit.com/r/developersIndia/", "description": "Indian developers - international job hunting tips"},
]

SEARCH_QUERIES_REDDIT = [
    "europe AI ML job visa sponsorship",
    "PhD computer science europe english",
    "indian student europe PhD experience",
    "software engineer europe relocation",
    "machine learning jobs europe no french",
    "NLP computer vision jobs europe 2026",
    "research assistant europe AI",
    "europe tech companies hiring international",
    "EU blue card India software",
    "germany netherlands UK AI jobs",
    "PhD europe no recommendation letters",
    "europe startup AI ML hiring",
]

CURATED_POSTS = [
    {
        "title": "Guide: Getting a tech job in Europe as a non-EU citizen",
        "url": "https://www.reddit.com/r/cscareerquestionsEU/search/?q=non+EU+citizen+tech+job",
        "subreddit": "r/cscareerquestionsEU",
        "category": "visa_guide",
    },
    {
        "title": "PhD in Europe - Complete Guide for International Students",
        "url": "https://www.reddit.com/r/PhD/search/?q=europe+international+student",
        "subreddit": "r/PhD",
        "category": "phd_guide",
    },
    {
        "title": "Monthly 'Who is Hiring' threads - Europe",
        "url": "https://www.reddit.com/r/cscareerquestionsEU/search/?q=who+is+hiring&sort=new",
        "subreddit": "r/cscareerquestionsEU",
        "category": "job_listings",
    },
    {
        "title": "Companies with visa sponsorship in Europe",
        "url": "https://www.reddit.com/r/cscareerquestionsEU/search/?q=visa+sponsorship+list",
        "subreddit": "r/cscareerquestionsEU",
        "category": "visa_companies",
    },
    {
        "title": "ML/AI jobs in Europe experience thread",
        "url": "https://www.reddit.com/r/MachineLearning/search/?q=europe+jobs",
        "subreddit": "r/MachineLearning",
        "category": "ai_jobs",
    },
    {
        "title": "Indian students doing PhD in Europe - AMA/Experience",
        "url": "https://www.reddit.com/r/Indian_Academia/search/?q=europe+PhD",
        "subreddit": "r/Indian_Academia",
        "category": "indian_experience",
    },
]


def search_reddit(query, subreddit=None, limit=10):
    """Search Reddit using their JSON API (no auth needed for search)"""
    results = []
    try:
        if subreddit:
            url = f"https://www.reddit.com/r/{subreddit}/search.json"
            params = {"q": query, "restrict_sr": "on", "sort": "relevance", "t": "year", "limit": limit}
        else:
            url = "https://www.reddit.com/search.json"
            params = {"q": query, "sort": "relevance", "t": "year", "limit": limit}

        resp = requests.get(url, params=params, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            posts = data.get("data", {}).get("children", [])
            for post in posts:
                pdata = post.get("data", {})
                results.append({
                    "title": pdata.get("title", ""),
                    "url": f"https://www.reddit.com{pdata.get('permalink', '')}",
                    "subreddit": pdata.get("subreddit_name_prefixed", ""),
                    "score": pdata.get("score", 0),
                    "num_comments": pdata.get("num_comments", 0),
                    "created_utc": pdata.get("created_utc", 0),
                    "selftext_preview": (pdata.get("selftext", ""))[:200],
                    "source": "reddit_search",
                    "query": query,
                })
        time.sleep(2)  # Reddit rate limiting
    except Exception as e:
        print(f"Reddit search error for '{query}': {e}")

    return results


def search_hackernews(query):
    """Search HackerNews using Algolia API"""
    results = []
    try:
        url = "https://hn.algolia.com/api/v1/search"
        params = {"query": query, "tags": "story", "hitsPerPage": 5}
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for hit in data.get("hits", []):
                results.append({
                    "title": hit.get("title", ""),
                    "url": hit.get("url", f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"),
                    "points": hit.get("points", 0),
                    "num_comments": hit.get("num_comments", 0),
                    "source": "hackernews",
                    "query": query,
                })
    except Exception as e:
        print(f"HN search error for '{query}': {e}")

    return results


HN_QUERIES = [
    "Who is Hiring Europe AI",
    "Europe machine learning jobs",
    "PhD Europe computer science",
    "Europe visa sponsorship tech",
]


def scrape_all_community():
    """Scrape all community sources"""
    all_results = {
        "subreddits": CURATED_SUBREDDITS,
        "curated_posts": CURATED_POSTS,
        "reddit_results": [],
        "hackernews_results": [],
    }

    # Search Reddit
    for query in SEARCH_QUERIES_REDDIT[:6]:  # Limit to avoid rate limiting
        results = search_reddit(query, limit=5)
        all_results["reddit_results"].extend(results)
        time.sleep(2)

    # Search HackerNews
    for query in HN_QUERIES:
        results = search_hackernews(query)
        all_results["hackernews_results"].extend(results)
        time.sleep(1)

    return all_results


if __name__ == "__main__":
    import json
    data = scrape_all_community()
    print(json.dumps(data, indent=2, default=str))
