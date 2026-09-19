"""
Media storage backend backed by Google Cloud Storage (the same bucket
Firebase Storage uses). This is required because Vercel's filesystem is
read-only and reset on every request, so files uploaded through Django
admin (resume, certificates, project images) must live somewhere
persistent.

Credentials are loaded the same way firebase/firebase_config.py does:
- On Vercel: FIREBASE_SERVICE_ACCOUNT_B64 (base64-encoded service account JSON)
- Locally: firebase/serviceAccountKey.json
"""

import base64
import json
import os
from pathlib import Path

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from google.cloud import storage as gcs
from google.oauth2 import service_account

BASE_DIR = Path(__file__).resolve().parent.parent

SCOPES = ["https://www.googleapis.com/auth/devstorage.read_write"]


def _load_credentials():
    firebase_json_b64 = os.getenv("FIREBASE_SERVICE_ACCOUNT_B64", "").strip()

    if firebase_json_b64:
        firebase_json_b64 = "".join(firebase_json_b64.split())
        firebase_json_b64 += "=" * ((-len(firebase_json_b64)) % 4)

        service_account_info = json.loads(
            base64.b64decode(firebase_json_b64).decode("utf-8")
        )

        return service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES,
        )

    service_account_file = BASE_DIR / "firebase" / "serviceAccountKey.json"

    if not service_account_file.exists():
        raise FileNotFoundError(
            "Firebase/GCS credentials not found. Set "
            "FIREBASE_SERVICE_ACCOUNT_B64 in Vercel or place "
            "serviceAccountKey.json inside firebase/."
        )

    return service_account.Credentials.from_service_account_file(
        str(service_account_file), scopes=SCOPES,
    )


def _get_bucket():
    credentials = _load_credentials()
    project_id = os.getenv("FIREBASE_PROJECT_ID", credentials.project_id)
    client = gcs.Client(project=project_id, credentials=credentials)
    bucket_name = os.environ["GS_BUCKET_NAME"]
    return client.bucket(bucket_name)


@deconstructible
class MediaGCStorage(Storage):
    """Minimal Storage implementation: enough for FileField/ImageField
    uploads through Django admin and for serving them back publicly."""

    def __init__(self):
        self._bucket = None

    @property
    def bucket(self):
        if self._bucket is None:
            self._bucket = _get_bucket()
        return self._bucket

    def _open(self, name, mode="rb"):
        from django.core.files.base import ContentFile

        blob = self.bucket.blob(name)
        return ContentFile(blob.download_as_bytes(), name=name)

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        content.seek(0)
        blob.upload_from_file(content, content_type=getattr(content, "content_type", None))
        blob.make_public()
        return name

    def exists(self, name):
        return self.bucket.blob(name).exists()

    def url(self, name):
        return self.bucket.blob(name).public_url

    def size(self, name):
        blob = self.bucket.blob(name)
        blob.reload()
        return blob.size

    def delete(self, name):
        blob = self.bucket.blob(name)
        if blob.exists():
            blob.delete()

    def get_available_name(self, name, max_length=None):
        # Let GCS overwrite same-name files rather than renaming, keeping
        # this simple; Django's default de-dup logic still runs first.
        return name
