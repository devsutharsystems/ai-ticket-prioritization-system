# AI Ticket Prioritization System

AI-powered ticket prioritization system built using FastAPI, Scikit-learn, and SQLite to automatically classify and prioritize support tickets.

---

## Problem Statement

Support teams often receive thousands of tickets daily.

Manual prioritization leads to:
- Delays
- Human inconsistency
- Misclassification
- Slow response for critical incidents

This project automates ticket prioritization using machine learning and rule-based logic.

---

## Solution Overview

The system combines:

- TF-IDF vectorization
- Logistic Regression classification
- Rule-based overrides
- Confidence scoring

to determine:

- Ticket priority
- Responsible team
- Review requirements
- Confidence score

---

## Features

- Automatic ticket prioritization
- ML-based classification pipeline
- Rule-based escalation system
- Confidence threshold review flag
- FastAPI backend
- SQLite database integration
- REST API endpoints
- Swagger API documentation

---

## Tech Stack

- Python
- FastAPI
- Scikit-learn
- SQLite
- Pandas
- NumPy
- Uvicorn

---

## Project Structure

```bash
ai-ticket-prioritization/
│
├── model/
├── database/
├── routes/
├── schemas/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tickets` | Create new ticket |
| GET | `/tickets` | Fetch all tickets |
| GET | `/tickets/{id}` | Fetch ticket by ID |
| PUT | `/tickets/{id}` | Update ticket |
| DELETE | `/tickets/{id}` | Delete ticket |
| GET | `/metrics` | View system metrics |

---

## Run Locally

Clone repository:

```bash
git clone https://github.com/devsutharsystems/ai-ticket-prioritization.git
cd ai-ticket-prioritization
```

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI server:

```bash
uvicorn main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Preview

## Swagger Documentation

<img width="969" height="833" alt="Screenshot 2026-05-10 at 3 21 52 PM" src="https://github.com/user-attachments/assets/f88441c8-f88e-4347-acae-cdcc2041774c" />

---

## Ticket Creation Endpoint

<img width="490" height="781" alt="Screenshot 2026-05-10 at 3 24 01 PM" src="https://github.com/user-attachments/assets/08f6269e-d58d-4cce-b4a6-7dad1163e34e" />

---

## Metrics Endpoint

<img width="741" height="757" alt="Screenshot 2026-05-10 at 3 25 52 PM" src="https://github.com/user-attachments/assets/02603bcf-29f7-4b4c-bcb7-e48c88a50d8f" />

---

## Example Prediction

### Input Ticket

```text
payment gateway completely down for all users
```

### Output

```json
{
  "priority": "high",
  "confidence": 0.91,
  "review_required": false,
  "assigned_team": "Critical Response Team"
}
```

---

## Future Improvements

- Docker deployment
- JWT authentication
- Admin dashboard
- Redis caching
- CI/CD integration
- Cloud deployment

---

## Author

Developed by Dev Suthar

