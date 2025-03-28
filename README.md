# Skillab Tracker

<img src="media/logo.png">

---

A **configurable** and **extensible** tracker that **fetches**, **preprocesses**, **stores** and **serves** data from different sources for skill related entities such as Courses, Job Listings, Employee Profiles, Organizational Profiles and more.

Skillab Tracker is a tool built to gather, preprocess, store, and deliver data across a diverse range of skill-related domains. By centralizing information from multiple sources, it enables the creation of unified datasets for comprehensive analytics and reporting. Skillab Tracker can integrate data on entities such as organizations, projects, academic papers, official project reports, online courses, job postings, internet profiles, legal policies, and law publications, providing a robust foundation for deep insights and informed decision-making. The Skillab Tracker is developed in Python, leveraging the Django Ninja framework, an extension of Django designed for building APIs with greater ease and flexibility. As outlined in the architecture section, Skillab Tracker also integrates various libraries from the Python ecosystem for networking, text parsing, data manipulation and scientific analysis, enhancing its functionality.

Note: This is a stripped-down version designed specifically for testing. It includes only a database dump of records from open sources, with many modules—such as data miners, skill and occupation extraction, translations, and others—omitted to reduce the Docker build size and simplify installation.

## How to install for testing

Prerequisites:

1. Python (most likely any 3.x.x version will do) with the venv module installed
2. Docker

Installation steps:

```bash
# Clone the repository
git clone https://github.com/skillab-project/skillab-tracker-testathon.git

# Go into the created folder
cd /skillab-tracker-testathon

# Create enviroment file
cp .env.example.dev .env

# Create python virtual enviroment and install requirements
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

# Run postgresql and load dump using Docker
docker compose up -d

# Run tests (the server doesn't need to be running)
python manage.py test

# Run the server in development mode
python manage.py runserver
```

Visit the [Swagger Documentation page](http://localhost:8000/api/docs) to view the available endpoints when the server is running.

For more information on how to conduct testing visit the [testing page](docs/testing.md).
