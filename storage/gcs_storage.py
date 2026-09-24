"""
Google Cloud Storage backend for Django media files.

Vercel's filesystem is temporary/read-only, so uploaded files
should be stored in Google Cloud Storage.

Credentials:
    Vercel:
        FIREBASE_SERVICE_ACCOUNT_B64

    Local:
        firebase/serviceAccountKey.json
"""

import base64
import json
import os
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from google.cloud import storage as gcs
from google.oauth2 import service_account


BASE_DIR = Path(__file__).resolve().parent.parent

SCOPES = [
    "https://www.googleapis.com/auth/devstorage.read_write",
]


def _load_credentials():
    """Load Google service-account credentials."""

    firebase_json_b64 = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_B64",
        "",
    ).strip()

    # ---------------------------------------------------------
    # VERCEL
    # ---------------------------------------------------------

    if firebase_json_b64:
        try:
            firebase_json_b64 = "".join(
                firebase_json_b64.split()
            )

            firebase_json_b64 += "=" * (
                (-len(firebase_json_b64)) % 4
            )

            service_account_info = json.loads(
                base64.b64decode(
                    firebase_json_b64
                ).decode("utf-8")
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
                "Invalid FIREBASE_SERVICE_ACCOUNT_B64."
            ) from exc

    # ---------------------------------------------------------
    # LOCAL DEVELOPMENT
    # ---------------------------------------------------------

    service_account_file = (
        BASE_DIR
        / "firebase"
        / "serviceAccountKey.json"
    )

    if not service_account_file.exists():
        raise FileNotFoundError(
            "Firebase/GCS credentials not found. "
            "Set FIREBASE_SERVICE_ACCOUNT_B64 in Vercel "
            "or place serviceAccountKey.json inside firebase/."
        )

    return (
        service_account.Credentials
        .from_service_account_file(
            str(service_account_file),
            scopes=SCOPES,
        )
    )


def _get_bucket():
    """Create and return the configured GCS bucket."""

    credentials = _load_credentials()

    project_id = os.getenv(
        "FIREBASE_PROJECT_ID",
        credentials.project_id,
    )

    bucket_name = os.getenv(
        "GS_BUCKET_NAME",
        "",
    ).strip()

    if not bucket_name:
        raise ValueError(
            "GS_BUCKET_NAME is not configured."
        )

    client = gcs.Client(
        project=project_id,
        credentials=credentials,
    )

    return client.bucket(bucket_name)


@deconstructible
class MediaGCStorage(Storage):
    """
    Django storage backend using Google Cloud Storage.
    """

    def __init__(self):
        self._bucket = None

    @property
    def bucket(self):
        if self._bucket is None:
            self._bucket = _get_bucket()

        return self._bucket

    def _open(self, name, mode="rb"):
        blob = self.bucket.blob(name)

        return ContentFile(
            blob.download_as_bytes(),
            name=name,
        )

    def _save(self, name, content):
        blob = self.bucket.blob(name)

        content.seek(0)

        content_type = getattr(
            content,
            "content_type",
            None,
        )

        blob.upload_from_file(
            content,
            content_type=content_type,
        )

        return name

    def exists(self, name):
        return self.bucket.blob(name).exists()

    def url(self, name):
        """
        Return the public URL.

        The bucket/object must be publicly readable for this
        URL to work. If your bucket uses Firebase download
        tokens or signed URLs, this method should be changed
        accordingly.
        """

        return self.bucket.blob(name).public_url

    def size(self, name):
        blob = self.bucket.blob(name)

        blob.reload()

        return blob.size

    def delete(self, name):
        blob = self.bucket.blob(name)

        if blob.exists():
            blob.delete()

    def get_available_name(
        self,
        name,
        max_length=None,
    ):
        return name