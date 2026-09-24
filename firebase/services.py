from datetime import datetime, timezone

from .firebase_config import (
    create_document,
    delete_document,
    get_document,
    list_documents,
    update_document,
)


# =========================================================
# PROJECTS
# =========================================================

def get_projects():
    try:
        documents = list_documents("projects")
    except Exception:
        return []

    projects = []

    for document in documents:
        data = document.get("data", {})

        projects.append({
            "id": document.get("id", ""),
            "slug": document.get("id", ""),
            "title": data.get("title", ""),
            "short_description": data.get(
                "short_description",
                "",
            ),
            "description": data.get(
                "description",
                "",
            ),
            "technologies": data.get(
                "technologies",
                "",
            ),
            "github_url": data.get(
                "github_url",
                "",
            ),
            "live_url": data.get(
                "live_url",
                "",
            ),
            "featured": data.get(
                "featured",
                False,
            ),
            "published": data.get(
                "published",
                False,
            ),
        })

    return projects


# =========================================================
# SKILLS
# =========================================================

def get_skills():
    try:
        documents = list_documents("skills")
    except Exception:
        return []

    skills = []

    for document in documents:
        data = document.get("data", {})

        skills.append({
            "id": document.get("id", ""),
            "name": data.get(
                "name",
                "",
            ),
            "category": data.get(
                "category",
                "",
            ),
            "level": data.get(
                "level",
                0,
            ),
            "description": data.get(
                "description",
                "",
            ),
            "published": data.get(
                "published",
                False,
            ),
        })

    return skills


# =========================================================
# PROFILE
# =========================================================

def get_profile():
    try:
        document = get_document(
            "profile",
            "main",
        )

        data = document.get(
            "data",
            {},
        )

    except Exception:
        data = {}

    return {
        "id": "main",

        "name": data.get(
            "name",
            "Ankur Yadav",
        ),

        "professional_title": data.get(
            "professional_title",
            data.get(
                "title",
                "Data Analytics & Python Developer",
            ),
        ),

        "short_intro": data.get(
            "short_intro",
            (
                "I build data-driven solutions, dashboards, "
                "automation tools and practical web applications "
                "using Python, Django and modern technologies."
            ),
        ),

        "bio": data.get(
            "bio",
            (
                "I am developing my career around data analytics, "
                "Python development, automation, dashboards and "
                "real-world digital solutions."
            ),
        ),

        "about_data_analytics": data.get(
            "about_data_analytics",
            (
                "Data cleaning, analysis, Excel, SQL, dashboards, "
                "reporting and visualization."
            ),
        ),

        "about_python": data.get(
            "about_python",
            (
                "Python, Django, automation, database-driven "
                "applications and practical software solutions."
            ),
        ),

        "about_problem_solving": data.get(
            "about_problem_solving",
            (
                "I focus on creating practical, useful solutions "
                "for real business and data problems."
            ),
        ),

        "email": data.get(
            "email",
            "",
        ),

        "phone": data.get(
            "phone",
            "",
        ),

        "location": data.get(
            "location",
            "Jaipur, Rajasthan",
        ),

        "linkedin_url": data.get(
            "linkedin_url",
            "",
        ),

        "github_url": data.get(
            "github_url",
            "",
        ),

        "instagram_url": data.get(
            "instagram_url",
            "",
        ),

        "website_status": data.get(
            "website_status",
            False,
        ),
    }


# =========================================================
# CONTACT MESSAGES
# =========================================================

def save_message(
    name,
    email,
    subject,
    message,
):
    document_id = create_document(
        "messages",
        {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "read": False,
            "created_at": datetime.now(
                timezone.utc
            ),
        },
    )

    print(
        f"FIREBASE MESSAGE SAVED: {document_id}"
    )

    return document_id


def get_firebase_messages():
    try:
        documents = list_documents("messages")
    except Exception:
        return []

    messages = []

    for document in documents:
        data = document.get(
            "data",
            {},
        )

        messages.append({
            "id": document.get(
                "id",
                "",
            ),
            "name": data.get(
                "name",
                "",
            ),
            "email": data.get(
                "email",
                "",
            ),
            "subject": data.get(
                "subject",
                "",
            ),
            "message": data.get(
                "message",
                "",
            ),
            "read": data.get(
                "read",
                False,
            ),
            "created_at": data.get(
                "created_at"
            ),
        })

    def message_date(item):
        created_at = item.get(
            "created_at"
        )

        if created_at is None:
            return datetime.min.replace(
                tzinfo=timezone.utc
            )

        # Make naive datetimes timezone-aware
        if created_at.tzinfo is None:
            return created_at.replace(
                tzinfo=timezone.utc
            )

        return created_at

    messages.sort(
        key=message_date,
        reverse=True,
    )

    return messages


# =========================================================
# DELETE MESSAGE
# =========================================================

def delete_firebase_message(
    message_id,
):
    delete_document(
        "messages",
        message_id,
    )

    print(
        f"FIREBASE MESSAGE DELETED: {message_id}"
    )


# =========================================================
# MARK MESSAGE AS READ
# =========================================================

def mark_firebase_message_read(
    message_id,
):
    update_document(
        "messages",
        message_id,
        {
            "read": True,
        },
    )

    print(
        f"FIREBASE MESSAGE MARKED AS READ: {message_id}"
    )