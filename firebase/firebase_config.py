import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account


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


def get_credentials():
    """
    Load Firebase service-account credentials.

    On Vercel:
        FIREBASE_SERVICE_ACCOUNT_B64

    Locally:
        firebase/serviceAccountKey.json
    """

    firebase_json_b64 = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_B64",
        "",
    ).strip()

    if firebase_json_b64:
        try:
            # Remove accidental spaces/new lines
            firebase_json_b64 = "".join(
                firebase_json_b64.split()
            )

            # Add missing Base64 padding if necessary
            firebase_json_b64 += "=" * (
                (-len(firebase_json_b64)) % 4
            )

            service_account_json = base64.b64decode(
                firebase_json_b64
            ).decode("utf-8")

            service_account_info = json.loads(
                service_account_json
            )

            return (
                service_account.Credentials
                .from_service_account_info(
                    service_account_info,
                    scopes=SCOPES,
                )
            )

        except Exception as exc:
            raise ValueError(
                "FIREBASE_SERVICE_ACCOUNT_B64 is invalid. "
                "Make sure Vercel contains the complete Base64 "
                "value generated from serviceAccountKey.json."
            ) from exc

    # Local development fallback
    service_account_file = (
        BASE_DIR
        / "firebase"
        / "serviceAccountKey.json"
    )

    if not service_account_file.exists():
        raise FileNotFoundError(
            "Firebase credentials not found. "
            "Set FIREBASE_SERVICE_ACCOUNT_B64 "
            "in Vercel or place serviceAccountKey.json "
            "inside firebase/."
        )

    return (
        service_account.Credentials
        .from_service_account_file(
            str(service_account_file),
            scopes=SCOPES,
        )
    )


def get_session():
    return AuthorizedSession(
        get_credentials()
    )


BASE_URL = (
    "https://firestore.googleapis.com/v1/"
    f"projects/{PROJECT_ID}"
    f"/databases/{DATABASE_ID}"
    "/documents"
)


def _request(method, path="", **kwargs):
    session = get_session()

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


def _encode_value(value):
    if value is None:
        return {
            "nullValue": None
        }

    if isinstance(value, bool):
        return {
            "booleanValue": value
        }

    if isinstance(value, int):
        return {
            "integerValue": str(value)
        }

    if isinstance(value, float):
        return {
            "doubleValue": value
        }

    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(
                tzinfo=timezone.utc
            )

        return {
            "timestampValue": (
                value.astimezone(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
        }

    if isinstance(value, str):
        return {
            "stringValue": value
        }

    if isinstance(value, list):
        return {
            "arrayValue": {
                "values": [
                    _encode_value(item)
                    for item in value
                ]
            }
        }

    if isinstance(value, dict):
        return {
            "mapValue": {
                "fields": _encode_fields(value)
            }
        }

    raise TypeError(
        f"Unsupported Firestore value: {type(value)}"
    )


def _encode_fields(data):
    return {
        key: _encode_value(value)
        for key, value in data.items()
    }


def list_documents(collection_name):
    documents = []
    page_token = None

    while True:
        params = {
            "pageSize": 300
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
            []
        ):
            name = document.get(
                "name",
                ""
            )

            document_id = name.split("/")[-1]

            documents.append({
                "id": document_id,
                "data": _decode_fields(
                    document.get(
                        "fields",
                        {}
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
                {}
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
            "fields": _encode_fields(data)
        },
    )

    name = response.get(
        "name",
        ""
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
            "fields": _encode_fields(data)
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