from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Dummy Data for Speakers and Talks
# Topic: Google Cloud Technologies

SPEAKERS = [
    {"id": 1, "first_name": "Alice", "last_name": "Johnson", "linkedin": "https://linkedin.com/in/alicejohnson"},
    {"id": 2, "first_name": "Bob", "last_name": "Smith", "linkedin": "https://linkedin.com/in/bobsmith"},
    {"id": 3, "first_name": "Charlie", "last_name": "Davis", "linkedin": "https://linkedin.com/in/charliedavis"},
    {"id": 4, "first_name": "Dana", "last_name": "Lee", "linkedin": "https://linkedin.com/in/danalee"},
    {"id": 5, "first_name": "Evan", "last_name": "Wright", "linkedin": "https://linkedin.com/in/evanwright"},
    {"id": 6, "first_name": "Fiona", "last_name": "Chen", "linkedin": "https://linkedin.com/in/fionachen"},
    {"id": 7, "first_name": "George", "last_name": "Miller", "linkedin": "https://linkedin.com/in/georgemiller"},
    {"id": 8, "first_name": "Hannah", "last_name": "Wilson", "linkedin": "https://linkedin.com/in/hannahwilson"},
]

TALKS = [
    {
        "id": 101,
        "title": "Keynote: The Future of Cloud Computing",
        "speaker_ids": [1],
        "categories": ["Keynote", "Strategy"],
        "description": "An overview of where Google Cloud is heading in the next 5 years.",
        "time_start": "09:00",
        "time_end": "10:00"
    },
    {
        "id": 102,
        "title": "Mastering Kubernetes on GKE",
        "speaker_ids": [2, 3],
        "categories": ["DevOps", "Infrastructure"],
        "description": "Deep dive into GKE networking, security, and scaling patterns.",
        "time_start": "10:15",
        "time_end": "11:15"
    },
    {
        "id": 103,
        "title": "Serverless with Cloud Run",
        "speaker_ids": [4],
        "categories": ["Serverless", "App Dev"],
        "description": "How to build and deploy scalable containerized applications without managing servers.",
        "time_start": "11:30",
        "time_end": "12:30"
    },
    # LUNCH BREAK 12:30 - 13:30 (Handled in template or explicit entry?)
    # Let's add it as a special event type for easier rendering, or just time gap.
    # Requirement says "Give a lunch break of 60 minutes". We will render it visually.
    {
        "id": 104,
        "title": "BigQuery for Data Warehousing",
        "speaker_ids": [5],
        "categories": ["Data", "Analytics"],
        "description": "Best practices for querying petabytes of data in seconds.",
        "time_start": "13:30",
        "time_end": "14:15"
    },
    {
        "id": 105,
        "title": "Machine Learning with Vertex AI",
        "speaker_ids": [6, 1],
        "categories": ["AI/ML", "Data"],
        "description": "End-to-end ML ops using Google's unified AI platform.",
        "time_start": "14:30",
        "time_end": "15:15"
    },
    {
        "id": 106,
        "title": "Securing Your Cloud Environment",
        "speaker_ids": [7],
        "categories": ["Security"],
        "description": "IAM, VPC Service Controls, and other security essentials.",
        "time_start": "15:30",
        "time_end": "16:15"
    },
    {
        "id": 107,
        "title": "Modernizing Legacy Apps with Anthos",
        "speaker_ids": [8],
        "categories": ["Hybrid Cloud", "Modernization"],
        "description": "Strategies for moving monolithic apps to microservices.",
        "time_start": "16:30",
        "time_end": "17:15"
    },
    {
        "id": 109,
        "title": "SRE Best Practices for Scalable Systems",
        "speaker_ids": [3],
        "categories": ["devops", "sre"],
        "description": "Learn how Google keeps its systems reliable and scalable.",
        "time_start": "17:30",
        "time_end": "18:15"
    },
    {
        "id": 110,
        "title": "Cost Management Strategies on GCP",
        "speaker_ids": [4, 5],
        "categories": ["FinOps", "Management"],
        "description": "Optimizing your cloud spend without compromising performance.",
        "time_start": "18:30",
        "time_end": "19:15"
    },
    {
        "id": 108,
        "title": "Closing Remarks & Networking",
        "speaker_ids": [2],
        "categories": ["Community"],
        "description": "Wrap up of the day and networking session details.",
        "time_start": "19:30",
        "time_end": "20:00"
    },
    {
        "id": 111,
        "title": "Github actualizado",
        "speaker_ids": [1],
        "categories": ["Updates", "Tools"],
        "description": "Una charla sobre las últimas novedades de Github.",
        "time_start": "20:00",
        "time_end": "20:30"
    },
]

def get_speaker_by_id(speaker_id):
    return next((s for s in SPEAKERS if s["id"] == speaker_id), None)

def enrich_talks(talks_list):
    """Adds full speaker objects to talks."""
    enriched = []
    for talk in talks_list:
        new_talk = talk.copy()
        new_talk["speakers_obj"] = [get_speaker_by_id(sid) for sid in talk["speaker_ids"]]
        enriched.append(new_talk)
    return enriched

@app.route("/")
def index():
    # Conference details
    conference_date = datetime.now().strftime("%B %d, %Y")
    location = "Moscone Center, San Francisco, CA"
    
    # Enrich talks with speaker data
    schedule = enrich_talks(TALKS)
    
    return render_template("index.html", 
                           date=conference_date, 
                           location=location, 
                           schedule=schedule,
                           all_categories=sorted(list(set(cat for talk in TALKS for cat in talk["categories"]))))

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    
    if not query:
        return index()

    filtered_talks = []
    for talk in TALKS:
        # Check title
        if query in talk["title"].lower():
            filtered_talks.append(talk)
            continue
        
        # Check category
        if any(query in cat.lower() for cat in talk["categories"]):
            filtered_talks.append(talk)
            continue
            
        # Check speakers
        speakers = [get_speaker_by_id(sid) for sid in talk["speaker_ids"]]
        if any(query in s["first_name"].lower() or query in s["last_name"].lower() for s in speakers):
            filtered_talks.append(talk)
            continue

    conference_date = datetime.now().strftime("%B %d, %Y")
    location = "Moscone Center, San Francisco, CA"
    schedule = enrich_talks(filtered_talks)
    
    return render_template("index.html", 
                           date=conference_date, 
                           location=location, 
                           schedule=schedule,
                           search_query=query,
                           all_categories=sorted(list(set(cat for talk in TALKS for cat in talk["categories"]))))

if __name__ == "__main__":
    app.run(debug=True)
