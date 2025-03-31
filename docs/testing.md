# Skillab Tracker

---

## Overview

Automated testing via coding is the preferred approach as it ensures reproducibility and aids project maintenance, particularly during merges. However, semantic aspects of the application that cannot be tested through code should be verified manually via the documentation page.

## Types of testing that can be conducted

### Data Integrity Testing

Data Integrity Testing ensures that data remains accurate, consistent, unaltered, and free from unnecessary data or duplications during storage, retrieval, and processing.

Examples of test cases:
* Check for Duplicate Data in API Responses. (Easy)
* Validate Unique Entries. (Easy)
* Verify endpoints return the same information every time when identical filters are applied. (Easy)

### Accuracy Testing

Accuracy testing refers to the process of evaluating how close a system's output is to the correct or expected result.

Examples of test cases:
* Accurate set of extracted skills and occupations based on the information provided. (Hard)
* Propagation and backpropagation returns expected results. (Medium)

<sub> Most likely the accuracy of the extracted skills can only be conducted manually and not automated. </sub>

### Completeness Testing 

Completeness testing ensures that all required functionalities, data, or conditions in a system are fully implemented and accounted for.

Examples of test cases:
* Missing skills while there is information to be extracted from. (Easy)

### Logic Testing

Ensure that the filtering logic implemented at the endpoints functions as expected.

Examples of test cases:
* AND/OR Logic: Confirm that the filtering operators (AND, OR) behave correctly when applied. (Easy)
* Keyword Filtering: Verify that keyword-based filters return the correct results.(Easy)
* ID Filtering: Ensure that an id is present in the results when it is used for filtering. (Easy)

## Procedure

### Manual Testing

You can only test the application's semantic meaning manually by inspecting the API's responses. The [Swagger Documentation page](http://localhost:8000/api/docs) helps you create requests and view their results. To report a bug, submit the CURL command copied from the documentation page, optionally accompanied by a screenshot.

#### Example of manual testing

For example, by inspecting the list of returned courses, we can notice that the skills extraction for a specific course worked like expected. Or the skills are associated to the course's title and description. This is part of the *Data Integrity Testing*.

Course Title: Security and DevOps
Skills:
* monitor logging operations
* tools for software configuration management 
* DevOps
* coordinate security

![course.png](course.png)

### Automated Testing

For writing tests, we recommend using **Django's test client** along with **Python's built-in unittest framework**. However, you are free to use your preferred testing framework and dependencies.

#### Example of automated testing 
The first test validates that single-keyword searching works as expected in job listings and is part of the *Logic Testing*.
The second test ensures that there are no duplicates returned in the course listings and is part of the *Data Integrity Testing*.

You can also view the following tests in `api/tests.py`.

```python
from unittest import TestCase
from django.test import Client


class JobsTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_jobs_keyword(self):
        #This test checks whether the job search API correctly filters jobs based on a given keyword, in this case "software".

        keyword = "software"
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

```

You can run the tests by executing the following command in your terminal: `python manage.py test` 

Documentation sources for testing:
* https://docs.djangoproject.com/en/5.1/topics/testing/ 

### Proposed Tests:

- **Validate Uniqueness of Entries:** Ensure that the combination of `source` and `source_id` is unique for each result.
- **Consistency of Endpoint Responses:** Verify that queries with identical filters consistently return the same results across multiple requests.
- **Propagation Behavior:** Validate that the propagation mechanism correctly returns all descendants (including children, grandchildren, and further descendants) of the selected skill or occupation.
- **Back Propagation Behavior:** Confirm that back propagation returns all ancestors of the selected skill or occupation accurately.
- **Extraction of Skills:** Ensure that when sufficient information is available, the relevant skills are correctly extracted.
- **Logical Operator Functionality (AND/OR):** Validate that filtering operators (AND, OR) are correctly applied to different fields (e.g., keywords, skill IDs, occupation IDs) and produce accurate results.
- **Keyword Filtering Accuracy:** Verify that filters based on keywords return the expected results.
- **ID Filtering Integrity:** Ensure that when filtering by ID (e.g., skill ID), the ID is present in all results returned.
- **Accuracy of Extracted Skills:** Confirm that the skills extracted based on the title and description match the results accurately.

