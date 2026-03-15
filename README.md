# Event Analytics Platform

A production-style event analytics platform built with Django, React, MySQL, Redis, Celery, Docker, and CI/CD.

## Overview
This project is a mini analytics SaaS product inspired by Google Analytics, Mixpanel, and Amplitude.

Applications can send events such as `page_view`, `signup`, `login`, `purchase`, and `button_click` through an API. The platform stores raw event data, processes analytics in the background, and displays insights on a dashboard.

## Core Features
- Event ingestion API
- Application management
- API key authentication
- Analytics dashboard
- Background event aggregation
- API Rate Limiter
- Docker + CI/CD

## Tech Stack
- Backend: Python, Django, Django REST Framework
- Frontend: React
- Database: MySQL
- Async Processing: Redis, Celery
- DevOps: Docker, GitHub Actions
