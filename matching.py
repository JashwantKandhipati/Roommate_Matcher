
SLEEP_ORDER = {
    'early bird': 1,
    'flexible': 2,
    'night owl': 3
}


def year_similarity(year1, year2):
    if not year1 or not year2:
        return 0
    diff = abs(year1 - year2)
    return max(0, 1 - (diff / 4))  # max diff of 4 (freshman vs senior)


def calculate_compatibility(user, other):
    score = 0
    max_score = 0

    # Budget (25%)
    if user.budget is not None and other.budget is not None:
        budget_diff = abs(user.budget - other.budget)
        budget_score = max(0, 100 - (budget_diff / 10))  # Scales $1000 diff down by 100 points
        score += budget_score * 0.25
        max_score += 100 * 0.25

    # Noise level (20%) - Assumes 1 to 10 scale
    if user.noise_level is not None and other.noise_level is not None:
        diff = abs(user.noise_level - other.noise_level)
        noise_score = max(0, 100 - (diff * 10))
        score += noise_score * 0.20
        max_score += 100 * 0.20

    # Cleanliness (15%) - Assumes 1 to 10 scale
    if user.cleanliness is not None and other.cleanliness is not None:
        diff = abs(user.cleanliness - other.cleanliness)
        cleanliness_score = max(0, 100 - (diff * 10))
        score += cleanliness_score * 0.15
        max_score += 100 * 0.15

    # Sleep schedule (15%)
    if user.sleep_schedule and other.sleep_schedule:
        # Case-insensitive lookup with default fallback to 'flexible' (2)
        s1 = SLEEP_ORDER.get(str(user.sleep_schedule).strip().lower(), 2)
        s2 = SLEEP_ORDER.get(str(other.sleep_schedule).strip().lower(), 2)
        diff = abs(s1 - s2)
        sleep_score = max(0, 100 - (diff * 50))
        score += sleep_score * 0.15
        max_score += 100 * 0.15

    # Class year (10%)
    if user.year and other.year:
        score += year_similarity(user.year, other.year) * 100 * 0.10
        max_score += 100 * 0.10

    # Smoking (10%)
    if user.smoking is not None and other.smoking is not None:
        score += 100 * 0.10 if user.smoking == other.smoking else 0
        max_score += 100 * 0.10

    # Drinking (5%)
    if user.drinking is not None and other.drinking is not None:
        score += 100 * 0.05 if user.drinking == other.drinking else 0
        max_score += 100 * 0.05

    if max_score == 0:
        return 0

    return round((score / max_score) * 100, 1)