import re
from collections import defaultdict

GROUP_COLORS = {
    "commerce": "🟦",
    "activism_legal": "🟥",
    "support": "🟨",
    "food_drink": "🟧",
    "education_resources": "🟩",
    "culture": "🟪",
    "music_nightlife": "🟫",
    "community_work": "⬛️",
    "children": "⬜️",
    "unknown": "🔲",
}

KEYWORDS = {
    "commerce": 
        [
            "shop", "market", "store", "sale", "swap", "bazaar", "free shop", "giveaway", "donation", "exchange", "flea market", "second hand", "secondhand", "thrift", "fair", "stall", "kiosk", "solidarity shop"
        ],
    "activism_legal": 
        [
            "action", "protest", "demo", "demonstration", "camp", "strike", "court", "legal", "case", "trial", "rally", "march", "blockade", "occupation", "sit in", "sit-in", "picket", "boycott", "campaign", "mobilization", "mobilisation", "resistance", "direct action", "civil disobedience", "solidarity action", "eviction", "anti eviction", "hearing", "lawsuit", "law", "rights", "legal aid", "legal support", "arrest", "prison", "detention", "police", "repression", "appeal", "sentence", "verdict", "tribunal"
        ],
    "support": 
        [
            "advice", "help", "support", "office hour", "office hours", "consultation", "counseling", "counselling", "clinic", "drop in", "drop-in", "assistance", "guidance", "peer support", "hotline", "open office", "sprechstunde", "beratung", "care", "mutual aid", "aid", "service", "questions", "faq", "orientation", "onboarding", "information session", "info session", "helpdesk", "help desk"
        ],
    "food_drink": 
        [
            "bar", "cafe", "coffee", "tea", "food", "dinner", "lunch", "breakfast", "kitchen", "meal", "brunch", "supper", "snack", "snacks", "drink", "drinks", "beverage", "beverages", "cocktail", "mocktail", "pub", "kneipe", "canteen", "küfa", "kuefa", "volxküche", "volxkueche", "people's kitchen", "peoples kitchen", "community kitchen", "soup", "soup kitchen", "bbq", "barbecue", "grill", "picnic", "potluck", "buffet", "cooking", "cookout", "baking", "cake", "cakes", "cookies", "pizza", "vegan", "vegetarian"
        ],
    "education_resources": 
        [
            "course", "workshop", "class", "training", "seminar", "discussion", "presentation", "lecture", "talk", "panel", "guided tour", "tour", "lesson", "teach in", "teach-in", "webinar", "skillshare", "skill share", "study group", "reading group", "working group", "roundtable", "round table", "debate", "conversation", "q and a", "qa", "q&a", "symposium", "conference", "forum", "colloquium", "introduction", "intro", "basics", "advanced", "practice session", "lab", "tutorial", "walkthrough", "training session", "learning", "education", "library", "book", "books", "bookshop", "book shop", "info", "infoshop", "info shop", "archive", "zine", "zines", "publication", "publications", "pamphlet", "pamphlets", "brochure", "brochures", "materials", "resources", "documentation"
        ],
    "culture": 
        [
            "exhibition", "gallery", "film", "movie", "cinema", "screening", "theater", "theatre", "performance", "reading", "poetry", "art", "arts", "installation", "vernissage", "finissage", "show", "showcase", "play", "drama", "stage", "staging", "actor", "acting", "dance performance", "opera", "cabaret", "comedy", "stand up", "stand-up", "spoken word", "storytelling", "literature", "book reading", "author reading", "screenplay", "documentary", "docu", "short film", "animation", "video art", "visual art", "photography", "photo", "painting", "drawing", "sculpture", "museum", "artist talk"
        ],
    "music_nightlife": 
        [
            "music", "concert", "gig", "dj", "party", "club", "dance", "karaoke", "live music", "band", "bands", "jam", "jam session", "open mic", "open stage", "choir", "orchestra", "sound", "sound system", "rave", "disco", "nightlife", "night", "festival", "set", "dj set", "acoustic", "electronic", "techno", "punk", "rock", "hip hop", "rap", "jazz", "folk", "singing", "song", "songs", "session", "afterparty", "after party", "dancefloor", "dance floor"
        ],
    "community_work": 
        [
            "meeting", "assembly", "plenum", "workspace", "work space", "coworking", "diy", "repair", "hacklab", "maker", "makerspace", "hackspace", "workday", "working day", "build day", "clean up", "cleanup", "maintenance", "fixing", "fix", "bike repair", "bicycle repair", "sewing", "printing", "screen printing", "woodwork", "woodworking", "metalwork", "craft", "crafting", "open space", "community space", "social center", "social centre", "collective", "collective meeting", "orga", "organizing", "organising", "planning", "coordination", "volunteer", "volunteering", "garden", "gardening", "urban garden", "repair cafe", "repair café"
        ],
    "children": 
        [
            "child", "children", "kids", "family", "parents", "families", "parent", "baby", "babies", "toddler", "toddlers", "youth", "young people", "teen", "teens", "teenager", "teenagers", "play", "playgroup", "play group", "games", "crafts for kids", "kids workshop", "children workshop", "children's activity", "childrens activity", "family friendly", "family-friendly", "parenting", "caregivers", "caregiver", "school children"
        ],
}


def normalize(text):
    text = text.lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9äöüß]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def classify_category(category, min_score=1):
    text = normalize(category)
    scores = defaultdict(int)
    matched_keywords = defaultdict(list)

    for group, keywords in KEYWORDS.items():
        for keyword in keywords:
            keyword_norm = normalize(keyword)
            if re.search(rf"\b{re.escape(keyword_norm)}\b", text):
                scores[group] += len(keyword_norm.split())
                matched_keywords[group].append(keyword)

    if not scores:
        return {
            "category": category,
            "group": "unknown",
            "color": GROUP_COLORS["unknown"],
            "confidence": 0.0,
            "matched_keywords": [],
            "needs_review": True,
        }

    best_group = max(scores, key=scores.get)
    best_score = scores[best_group]
    total_score = sum(scores.values())
    confidence = best_score / total_score

    return {
        "category": category,
        "group": best_group,
        "color": GROUP_COLORS[best_group],
        "confidence": round(confidence, 2),
        "matched_keywords": matched_keywords[best_group],
        "needs_review": best_score < min_score or confidence < 0.6,
    }


def category_color(category):
    category = (category or "").strip()
    if not category:
        return ""
    return classify_category(category)["color"]
