import base64
import os
from pathlib import Path
from datetime import datetime

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account


# ==========================================================
# PROJECT SETTINGS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ID = os.getenv(
    "FIREBASE_PROJECT_ID",
    "ankur-portfolio-f8fb2",
)

DATABASE_ID = os.getenv(
    "FIREBASE_DATABASE_ID",
    "(default)",
)

SCOPES = [
    "https://www.googleapis.com/auth/datastore",
]


# ==========================================================
# FIREBASE CREDENTIALS
# ==========================================================

def get_credentials():
    firebase_json_b64 = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_B64"
    )

    # Production:
    # Railway will provide the service-account JSON
    # as a Base64 environment variable.
    if firebase_json_b64:
        service_account_json = base64.b64decode(
            firebase_json_b64
        ).decode("utf-8")

        import json

        service_account_info = json.loads(
            service_account_json
        )

        return service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES,
        )

    # Local development:
    # Use the local JSON file when the environment variable
    # is not available.
    service_account_file = (
        BASE_DIR
        / "firebase"
        / "serviceAccountKey.json"
    )

    if not service_account_file.exists():
        raise FileNotFoundError(
            "Firebase credentials not found. "
            "Set FIREBASE_SERVICE_ACCOUNT_B64 "
            "or place serviceAccountKey.json in "
            "firebase/."
        )

    return service_account.Credentials.from_service_account_file(
        str(service_account_file),
        scopes=SCOPES,
    )


credentials = get_credentials()

session = AuthorizedSession(credentials)


# ==========================================================
# FIRESTORE REST API
# ==========================================================

BASE_URL = (
    "https://firestore.googleapis.com/v1/"
    f"projects/{PROJECT_ID}"
    f"/databases/{DATABASE_ID}"
    "/documents"
)


def _request(
    method,
    path="",
    **kwargs,
):
    url = f"{BASE_URL}{path}"

    response = session.request(
        method,
        url,
        timeout=30,
        **kwargs,
    )

    response.raise_for_status()

    if response.text:
        return response.json()

    return {}


# ==========================================================
# FIRESTORE DECODING
# ==========================================================

def _decode_value(value):
    if "nullValue" in value:
        return None

    if "stringValue" in value:
        return value["stringValue"]

    if "booleanValue" in value:
        return value["booleanValue"]

    if "integerValue" in value:
        return int(value["integerValue"])

    if "doubleValue" in value:
        return float(value["doubleValue"])

    if "timestampValue" in value:
        return datetime.fromisoformat(
            value["timestampValue"].replace(
                "Z",
                "+00:00",
            )
        )

    if "arrayValue" in value:
        return [
            _decode_value(item)
            for item in value["arrayValue"].get(
                "values",
                [],
            )
        ]

    if "mapValue" in value:
        return _decode_fields(
            value["mapValue"].get(
                "fields",
                {},
            )
        )

    return None


def _decode_fields(fields):
    return {
        key: _decode_value(value)
        for key, value in fields.items()
    }


# ==========================================================
# FIRESTORE ENCODING
# ==========================================================

def _encode_value(value):
    if value is None:
        return {
            "nullValue": None,
        }

    if isinstance(value, bool):
        return {
            "booleanValue": value,
        }

    if isinstance(value, int):
        return {
            "integerValue": str(value),
        }

    if isinstance(value, float):
        return {
            "doubleValue": value,
        }

    if isinstance(value, datetime):
        return {
            "timestampValue": (
                value.astimezone().isoformat()
            ),
        }

    if isinstance(value, str):
        return {
            "stringValue": value,
        }

    if isinstance(value, list):
        return {
            "arrayValue": {
                "values": [
                    _encode_value(item)
                    for item in value
                ],
            },
        }

    if isinstance(value, dict):
        return {
            "mapValue": {
                "fields": _encode_fields(value),
            },
        }

    raise TypeError(
        f"Unsupported Firestore value: {type(value)}"
    )


def _encode_fields(data):
    return {
        key: _encode_value(value)
        for key, value in data.items()
    }


# ==========================================================
# FIRESTORE DOCUMENT FUNCTIONS
# ==========================================================

def list_documents(collection_name):
    documents = []
    page_token = None

    while True:
        params = {
            "pageSize": 300,
        }

        if page_token:
            params["pageToken"] = page_token

        response = _request(
            "GET",
            f"/{collection_name}",
            params=params,
        )

        for document in response.get(
            "documents",
            [],
        ):
            name = document.get(
                "name",
                "",
            )

            document_id = name.split("/")[-1]

            documents.append({
                "id": document_id,
                "data": _decode_fields(
                    document.get(
                        "fields",
                        {},
                    )
                ),
            })

        page_token = response.get(
            "nextPageToken"
        )

        if not page_token:
            break

    return documents


def get_document(
    collection_name,
    document_id,
):
    response = _request(
        "GET",
        f"/{collection_name}/{document_id}",
    )

    return {
        "id": document_id,
        "data": _decode_fields(
            response.get(
                "fields",
                {},
            )
        ),
    }


def create_document(
    collection_name,
    data,
):
    response = _request(
        "POST",
        f"/{collection_name}",
        json={
            "fields": _encode_fields(data),
        },
    )

    name = response.get(
        "name",
        "",
    )

    return name.split("/")[-1]


def update_document(
    collection_name,
    document_id,
    data,
):
    _request(
        "PATCH",
        f"/{collection_name}/{document_id}",
        json={
            "fields": _encode_fields(data),
        },
    )


def delete_document(
    collection_name,
    document_id,
):
    _request(
        "DELETE",
        f"/{collection_name}/{document_id}",
    )