import json
import mimetypes
import time
import uuid
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured


class VercelBlobStorage(Storage):
    api_url = "https://vercel.com/api/blob"
    api_version = "13"

    def __init__(self):
        token = settings.BLOB_READ_WRITE_TOKEN
        token_parts = token.split("_")
        if len(token_parts) < 4 or not token_parts[3]:
            raise ImproperlyConfigured("BLOB_READ_WRITE_TOKEN is not a valid Vercel Blob token.")

        self.token = token
        self.store_id = token_parts[3]

    def _api_request(self, path, method, data=None, headers=None):
        request_headers = {
            "authorization": f"Bearer {self.token}",
            "x-api-version": self.api_version,
            "x-vercel-blob-store-id": self.store_id,
            "x-api-blob-request-id": f"{self.store_id}:{int(time.time() * 1000)}:{uuid.uuid4().hex}",
            "x-api-blob-request-attempt": "0",
        }
        if headers:
            request_headers.update(headers)

        request = Request(
            f"{self.api_url}{path}",
            data=data,
            headers=request_headers,
            method=method,
        )
        return urlopen(request, timeout=30)

    def _blob_url(self, name):
        encoded_path = quote(name.lstrip("/"), safe="/")
        return f"https://{self.store_id}.public.blob.vercel-storage.com/{encoded_path}"

    def _blob_info(self, name):
        query = urlencode({"url": self._blob_url(name)})
        with self._api_request(f"?{query}", "GET") as response:
            return json.loads(response.read())

    def _open(self, name, mode="rb"):
        response = urlopen(self._blob_url(name), timeout=30)
        return File(response, name=name)

    def _save(self, name, content):
        if hasattr(content, "seek"):
            content.seek(0)
        body = content.read()
        content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
        query = urlencode({"pathname": name})

        with self._api_request(
            f"/?{query}",
            "PUT",
            data=body,
            headers={
                "x-vercel-blob-access": "public",
                "x-add-random-suffix": "1",
                "x-content-type": content_type,
            },
        ) as response:
            blob = json.loads(response.read())

        return blob["pathname"]

    def delete(self, name):
        data = json.dumps({"urls": [self._blob_url(name)]}).encode("utf-8")
        with self._api_request(
            "/delete",
            "POST",
            data=data,
            headers={"content-type": "application/json"},
        ):
            pass

    def exists(self, name):
        try:
            self._blob_info(name)
        except HTTPError as error:
            if error.code == 404:
                return False
            raise
        return True

    def size(self, name):
        return self._blob_info(name)["size"]

    def url(self, name):
        return self._blob_url(name)
