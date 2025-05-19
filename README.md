# AACTDashboard

## Setup Instructions

This project is containerized using Docker and Docker Compose. Follow these steps to set up and run the dashboard locally.

### 1. Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose

### 2. Environment Configuration

Create a `.env` file at the root of the repository with the following variables:

```
DATABASE_PASSWORD=your_aact_password
DATABASE_USER=your_aact_user
SECRET_KEY=your_django_secret_key
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_NAME=aact
DATABASE_HOST=aact-db.ctti-clinicaltrials.org
DATABASE_PORT=5432
```

### 3. Build and Run the App

Use Docker Compose to build the images and start the services:

```
docker-compose up --build
```

This will start the Django development server on [http://localhost:8000](http://localhost:8000).

The service will automatically run the necessary migrations and populate user data once during the initial build.

### 4. Log in and View the Dashboard

Enter the following default credentials:

> Username: hector.garcia-chavez@bcm.edu\
> Password: password
