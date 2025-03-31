from unittest import TestCase
from django.test import Client


class JobsTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_jobs_keyword(self):
        #This test checks whether the job search API correctly filters jobs based on a given keyword, in this case "software".

        keyword = "software"
        print(keyword)
        response = self.client.post("/api/jobs", data={"keywords": [keyword]})

        self.assertEqual(response.status_code, 200, "Response wasn't ok.")

        jobs = response.json()["items"]

        for job in jobs:
            self.assertTrue(
                keyword in (job["title"] + job["description"]).lower(),
                f"Some job didn't include the filtered keyword in its title or description. Job ID: {job['id']}",
            )

    def test_courses_unique_ids(self):
        # This test verifies that the `/api/courses` endpoint returns a list of courses 
        # where each course has a unique ID (i.e., no duplicate courses are present).

        course_ids = set()
        page = 1

        while True:
            response = self.client.post(f"/api/courses?page={page}")
            self.assertEqual(response.status_code, 200, f"Response wasn't ok for page {page}.")

            data = response.json()
            courses = data["items"]

            if not courses:
                break

            for course in courses:
                self.assertNotIn(course["id"], course_ids, f"Duplicate course ID found: {course['id']}")
                course_ids.add(course["id"])

            page += 1



        
