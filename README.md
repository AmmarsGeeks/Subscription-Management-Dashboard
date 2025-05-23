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
