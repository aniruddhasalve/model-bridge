import os
import sys
import unittest

sys.path.insert(0, os.path.abspath("backend"))
os.environ.setdefault("MODEL_BRIDGE_API_KEY", "test-key")

from fastapi.testclient import TestClient
from app.main import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_is_public(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_ml_endpoint_requires_api_key(self):
        response = self.client.post("/v1/summarize", json={"text": "hello"})
        self.assertEqual(response.status_code, 401)

    def test_mock_summarize(self):
        response = self.client.post("/v1/summarize", headers={"Authorization": "Bearer test-key"}, json={"text": "one two three"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"]["summary"], "one two three")

    def test_classify_accepts_labels(self):
        response = self.client.post("/v1/classify", headers={"Authorization": "Bearer test-key"}, json={"text": "This is a bug", "labels": ["bug", "question"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"]["label"], "bug")

    def test_input_limit(self):
        response = self.client.post("/v1/summarize", headers={"Authorization": "Bearer test-key"}, json={"text": "x" * 12001})
        self.assertEqual(response.status_code, 413)


if __name__ == "__main__":
    unittest.main()
