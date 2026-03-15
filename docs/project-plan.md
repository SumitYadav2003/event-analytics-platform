# Project Plan

## What are we building?
A production-style Event Analytics Platform where applications send events like:
- page_view
- signup
- login
- purchase
- button_click

## Main modules
- Django backend
- React frontend
- MySQL database
- Redis + Celery worker
- Django admin
- Analytics dashboard
- API Rate Limiter

## Core entities
- Application
- Event
- AggregatedMetric

## Add-on
- API Rate Limiter to protect the event ingestion API from abuse and overload.
