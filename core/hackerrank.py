import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

BADGE_SCORE_MAP = {
    5: 100,
    4: 85,
    3: 70,
    2: 55,
    1: 40,
    0: 20,
}

TRACKED_BADGES = [
    "python", "java", "c++", "sql", "algorithms",
    "data structures", "mathematics", "artificial intelligence",
    "problem solving", "linux shell",
]


def get_hackerrank_profile(username: str) -> dict:
    """
    Scrape HackerRank public profile for badges and stars.
    Returns a dict with badge info and computed technical score.
    """
    url = f"https://www.hackerrank.com/{username}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}", "username": username}

    if response.status_code == 404:
        return {"error": "HackerRank username not found.", "username": username}

    if response.status_code != 200:
        return {"error": f"HackerRank returned status {response.status_code}.", "username": username}

    soup = BeautifulSoup(response.text, "html.parser")

    badges = []
    total_stars = 0
    badge_count = 0

    # HackerRank badge containers
    badge_cards = soup.find_all("div", class_="badge-title")

    for card in badge_cards:
        badge_name = card.get_text(strip=True).lower()
        if any(tracked in badge_name for tracked in TRACKED_BADGES):
            # Find star count from sibling elements
            parent = card.find_parent("div")
            star_elements = parent.find_all("svg", class_="badge-star") if parent else []
            filled_stars = len([
                s for s in star_elements
                if "badge-star-full" in s.get("class", [])
            ])
            badges.append({
                "name":  badge_name.title(),
                "stars": filled_stars,
            })
            total_stars += filled_stars
            badge_count += 1

    # Compute technical score from average stars across badges
    if badge_count > 0:
        avg_stars = total_stars / badge_count
        # Normalize: max 5 stars → score 100
        technical_score = min(int((avg_stars / 5) * 100), 100)
    else:
        technical_score = 50  # default if no badges found

    return {
        "username":        username,
        "badges":          badges,
        "total_stars":     total_stars,
        "badge_count":     badge_count,
        "technical_score": technical_score,
        "error":           None,
    }


def stars_to_label(stars: int) -> str:
    labels = {5: "Expert", 4: "Advanced", 3: "Proficient", 2: "Intermediate", 1: "Beginner", 0: "None"}
    return labels.get(stars, "Unknown")