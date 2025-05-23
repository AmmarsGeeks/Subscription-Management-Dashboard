# Subscription Management Dashboard

A comprehensive Django & Django REST Framework application to track subscription services (e.g. Netflix, Spotify) with renewal reminders, cost analysis, and a user-friendly dashboard interface.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Technical Details](#technical-details)  
- [Installation](#installation)  
- [Usage](#usage)  
- [API Endpoints](#api-endpoints)  
- [Folder Structure](#folder-structure)  
- [Screenshots](#screenshots)  

---

## Overview

This application helps users manage their subscriptions by tracking monthly and annual costs, reminding about upcoming renewals, and calculating potential savings if switching from monthly to annual billing. The frontend dashboard provides clear insights with charts and alerts to help users stay on top of their subscriptions.

---

## Features

### Backend (Django + DRF)
- Manage subscriptions with fields like name, price, billing cycle, start date, and renewal date.
- Automatically calculate renewal dates based on billing cycle.
- Validate renewal dates cannot be set in the past.
- API endpoints for listing, creating, and soft-deleting subscriptions.
- Annotation-based cost calculations for efficient data retrieval.
- Annual savings calculation based on switching from monthly to annual billing.

### Frontend
- Dashboard displaying total monthly spend and cost breakdown by subscription.
- Alerts highlighting subscriptions renewing within the next 7 days.
- Bar chart visualization of monthly costs per service.
- Comparison tool displaying potential yearly savings.

---

## Technical Details

- Python 3.12, Django 5.2, Django REST Framework  
- PostgreSQL or SQLite database support  
- Chart.js for frontend chart rendering  
- Decimal precision handled carefully for financial data  
- Clean, modular code structure for easy maintenance and extension  

---

## Installation

1. Clone the repo:  
   ```bash
   git clone <repository_url>
   cd <repository_directory>

### Create and activate a virtual environment:

```bash
    python3 -m venv venv
    source venv/bin/activate
```


### Install dependencies:

```bash
    pip install -r requirements.txt
```


### Run migrations

```bash
    python manage.py migrate
```


### Run the development server:


```bash
    python manage.py runserver
```


## Usage

- Access the dashboard via http://localhost:8000/
- Use API endpoints to manage subscriptions programmatically.


### API Endpoints

1. List Subscriptions
GET /api/subscriptions/
Returns all active subscriptions with calculated monthly and annual costs.

```bash
    curl -X GET http://localhost:8000/api/subscriptions/
```



2. Add Subscription
POST /api/subscriptions/
Create a new subscription.

If renewal_date is omitted, it will be auto-calculated based on start_date and billing_cycle.

You can optionally specify renewal_date manually.

Sample JSON payload:

```bash
   {
  "name": "Netflix",
  "price": "15.99",
  "billing_cycle": "monthly",
  "renewal_date": "2025-05-28"
    }
```

cURL example:

```bash
    curl -X POST http://localhost:8000/api/subscriptions/ \
    -H "Content-Type: application/json" \
    -d '{
    "name": "Netflix",
    "price": "15.99",
    "billing_cycle": "monthly",
    "renewal_date": "2025-05-28"
    }'
```

3. Cancel Subscription

DELETE /api/subscriptions/{id}/
Soft deletes (deactivates) a subscription by setting is_active to False.

Example to cancel subscription with ID 4:

```bash
    curl -X DELETE http://localhost:8000/api/subscriptions/4/
```

## Folder Structure


```bash
    subman/
├── manage.py
├── requirements.txt
├── README.md
├── subman/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── subscriptions/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── subscriptions/
│           ├── base.html
│           └── dashboard.html
└── static/
    └── (css/js/images as needed)
```


## Screenshots

1. Dashboard — Initial State (no data)
![Dashboard Empty](https://i.ibb.co/PsJwkDdT/Screenshot-1446-11-25-at-11-39-42-AM.png)


2. Dashboard — With Subscriptions & Alerts

![Dashboard With Alerts](https://i.ibb.co/wFKfXZPv/Screenshot-1446-11-25-at-11-59-36-AM.png)



## License
    MIT License

