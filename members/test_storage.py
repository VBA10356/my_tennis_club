import json
from unittest.mock import patch

from django.core.files.base import ContentFile
from django.test import SimpleTestCase, override_settings

from .storage import VercelBlobStorage


@override_settings(BLOB_READ_WRITE_TOKEN="vercel_blob_rw_test-store_secret")
class VercelBlobStorageTests(SimpleTestCase):
    def test_upload_saves_blob_path_and_uses_public_upload_api(self):
        urlopen = patch("members.storage.urlopen")
        response = urlopen.start()
        self.addCleanup(urlopen.stop)
        response.return_value.__enter__.return_value.read.return_value = json.dumps(
            {"pathname": "member_images/hero-abc.jpg"}
        ).encode()

        storage = VercelBlobStorage()
        result = storage._save("member_images/hero.jpg", ContentFile(b"image-bytes"))

        request = response.call_args.args[0]
        self.assertEqual(result, "member_images/hero-abc.jpg")
        self.assertEqual(request.method, "PUT")
        self.assertEqual(
            request.full_url,
            "https://vercel.com/api/blob/?pathname=member_images%2Fhero.jpg",
        )
        self.assertEqual(request.get_header("X-vercel-blob-access"), "public")
        self.assertEqual(request.data, b"image-bytes")

    def test_url_builds_public_blob_url_from_saved_path(self):
        storage = VercelBlobStorage()

        self.assertEqual(
            storage.url("member_images/hero-abc.jpg"),
            "https://test-store.public.blob.vercel-storage.com/member_images/hero-abc.jpg",
        )
