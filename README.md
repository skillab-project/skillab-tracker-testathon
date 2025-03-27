# Skillab Tracker

<img src="media/logo.png">

---

A **configurable** and **extensible** tracker that **fetches**, **preprocesses**, **stores** and **serves** data from different sources for skill related entities such as Courses, Job Listings, Employee Profiles, Organizational Profiles and more.

This is a stripped-down version designed specifically for testing. It includes only a database dump of records from open sources, with many modules—such as data miners, skill and occupation extraction, translations, and others—omitted to reduce the Docker build size and simplify installation.

## How to install for testing

Prerequisites:

1. Python (most likely any 3.x.x version will do) with the venv module installed
2. Docker

```bash
# Create enviroment file
cp .env.example.dev .env

# Create python virtual enviroment
python -m venv venv
source ./venv/bin/activate

# Run postgresql and load dump using Docker
docker compose up 

# Run tests
python manage.py test

# Run the server in development mode
python manage.py runserver
```

Visit the [Swagger Documentation page](http://localhost:8000/api/docs) to view the available endpoints.

For more information on how to conduct testing visit the [testing page](docs/testing.md).
