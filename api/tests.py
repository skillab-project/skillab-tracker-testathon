from unittest import TestCase
from django.test import Client


class JobsTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_jobs_keyword(self):
        keyword = "software"
        response = self.client.post("/api/jobs", data={"keywords": [keyword]})

        self.assertEqual(response.status_code, 200, "Response wasn't ok.")

        jobs = response.json()["items"]

        for job in jobs:
            self.assertFalse(
                keyword in (job["title"] + job["description"]).lower(),
                f"Some job didn't include the filtered keyword in its title or description. Job ID: {job['id']}",
            )
