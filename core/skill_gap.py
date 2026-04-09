# Industry benchmarks for placement readiness
BENCHMARKS = {
    "CGPA":                    7.0,
    "Internships":             2,
    "Projects":                3,
    "Technical_Skills_Score":  70,
    "HackerRank_Score":        70,
}

RECOMMENDATIONS = {
    "CGPA": [
        "Focus on core subject fundamentals",
        "Attend extra tutoring or study groups",
        "Aim for consistent performance in upcoming semesters",
    ],
    "Internships": [
        "Apply to internships on LinkedIn, Internshala, or AngelList",
        "Contribute to open-source projects as practical experience",
        "Look for part-time freelance projects",
    ],
    "Projects": [
        "Build 2–3 end-to-end projects with GitHub documentation",
        "Create a portfolio website showcasing your work",
        "Participate in hackathons to build projects fast",
    ],
    "Technical_Skills_Score": [
        "Complete DSA course on LeetCode or GeeksForGeeks",
        "Practice 50+ problems across arrays, trees, and graphs",
        "Take mock technical interviews on Pramp or InterviewBit",
    ],
    "HackerRank_Score": [
        "Earn at least 3 stars in Python, Java, or C++ on HackerRank",
        "Complete the HackerRank '30 Days of Code' challenge",
        "Practice SQL and algorithms badges on HackerRank",
    ],
}


def compute_skill_gap(student_data: dict) -> dict:
    """
    Compare student scores against benchmarks.
    Returns gaps, recommendations, and radar chart data.
    """
    gaps = {}
    recommendations = []
    radar_student = []
    radar_benchmark = []
    radar_labels = []

    field_map = {
        "CGPA":                    ("cgpa",                    10.0),
        "Internships":             ("internships",             10),
        "Projects":                ("projects",                20),
        "Technical_Skills_Score":  ("technical_skills_score",  100),
        "HackerRank_Score":        ("hackerrank_score",        100),
    }

    for field, (key, max_val) in field_map.items():
        student_val = student_data.get(key, 0)
        benchmark   = BENCHMARKS[field]

        gap = benchmark - student_val
        gaps[field] = {
            "student":   student_val,
            "benchmark": benchmark,
            "gap":       round(gap, 2),
            "met":       student_val >= benchmark,
        }

        if gap > 0:
            recommendations.extend(RECOMMENDATIONS[field])

        # Normalize to 0–100 for radar chart
        radar_labels.append(field.replace("_", " "))
        radar_student.append(round((student_val / max_val) * 100, 1))
        radar_benchmark.append(round((benchmark / max_val) * 100, 1))

    # Deduplicate recommendations
    seen = set()
    unique_recs = []
    for r in recommendations:
        if r not in seen:
            seen.add(r)
            unique_recs.append(r)

    gaps_met     = sum(1 for g in gaps.values() if g["met"])
    total_fields = len(gaps)
    readiness    = round((gaps_met / total_fields) * 100)

    return {
        "gaps":            gaps,
        "recommendations": unique_recs,
        "radar_labels":    radar_labels,
        "radar_student":   radar_student,
        "radar_benchmark": radar_benchmark,
        "readiness_score": readiness,
        "gaps_met":        gaps_met,
        "total_fields":    total_fields,
    }