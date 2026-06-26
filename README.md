# 🚀 AI-Powered Customer Support Ticket Prioritization System

Production-style machine learning system that automatically prioritizes customer support tickets using Natural Language Processing (NLP), FastAPI, Docker, AWS EC2, and GitHub Actions CI/CD.

---

## 📌 Overview

Customer support teams often receive hundreds or thousands of tickets every day. Manual prioritization is slow, inconsistent, and can delay responses to critical incidents.

This project automates ticket classification by combining a Machine Learning model with a rule-based decision engine, then exposes the system through a REST API deployed on AWS.

The complete application is containerized using Docker and automatically deployed to an EC2 instance using GitHub Actions.

---

# ✨ Features

* 🤖 Machine Learning-based ticket prioritization
* 📝 TF-IDF text vectorization
* 🧠 Logistic Regression classifier
* ⚡ Rule-based priority overrides for critical incidents
* 📊 Confidence score for every prediction
* 👨‍💼 Human review recommendation for low-confidence predictions
* 🎯 Automatic team assignment
* 📈 System metrics endpoint
* 📚 Interactive Swagger API documentation
* 🐳 Docker containerization
* ☁️ AWS EC2 deployment
* 🔄 Automated CI/CD pipeline using GitHub Actions

---

# 🏗️ System Architecture

```text
                 Customer Ticket
                        │
                        ▼
               Text Preprocessing
                        │
                        ▼
               TF-IDF Vectorization
                        │
                        ▼
          Logistic Regression Model
                        │
                        ▼
            Rule-Based Validation
                        │
                        ▼
        Priority + Confidence Score
                        │
                        ▼
          Team Assignment Engine
                        │
                        ▼
              FastAPI REST API
                        │
                        ▼
              SQLite Database
```

---

# 🛠️ Technology Stack

| Category         | Technologies   |
| ---------------- | -------------- |
| Language         | Python         |
| API              | FastAPI        |
| Machine Learning | Scikit-learn   |
| NLP              | TF-IDF         |
| Database         | SQLite         |
| Data Processing  | Pandas, NumPy  |
| Containerization | Docker         |
| Cloud            | AWS EC2        |
| CI/CD            | GitHub Actions |
| Server           | Uvicorn        |

---

# 📂 Project Structure

```text
ai-ticket-prioritization-system/

├── main.py
├── model.py
├── database.py
├── text_utils.py
├── retrain.py
├── seed.py
├── evaluate.py
├── requirements.txt
├── Dockerfile
├── model.pkl
├── vectorizer.pkl
├── tickets.db
├── .github/
│   └── workflows/
│       └── docker.yml
└── README.md
```

---

# ⚙️ Machine Learning Pipeline

```
Ticket Description
        │
        ▼
Normalize Text
        │
        ▼
TF-IDF Vectorizer
        │
        ▼
Logistic Regression
        │
        ▼
Prediction + Confidence
        │
        ▼
Rule Engine
        │
        ▼
Final Priority
```

---

# 📡 REST API Endpoints

| Method | Endpoint                 | Description           |
| ------ | ------------------------ | --------------------- |
| GET    | `/`                      | API Status            |
| POST   | `/tickets`               | Create Ticket         |
| GET    | `/tickets`               | Get All Tickets       |
| GET    | `/tickets/{id}`          | Get Ticket            |
| PUT    | `/tickets/{id}`          | Update Ticket         |
| PUT    | `/tickets/{id}/feedback` | Submit Human Feedback |
| DELETE | `/tickets/{id}`          | Delete Ticket         |
| GET    | `/metrics`               | System Metrics        |

---

# 📊 Example Prediction

### Input

```text
Payment gateway completely down for all users.
```

### Output

```json
{
  "priority": "high",
  "confidence": 0.91,
  "used_rule": true,
  "needs_review": false,
  "team": "Critical Response Team"
}
```

---

# 🚀 Running Locally

Clone the repository

```bash
git clone https://github.com/devsutharsystems/ai-ticket-prioritization-system.git

cd ai-ticket-prioritization-system
```

Create virtual environment

```bash
python -m venv venv
```

Activate

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# 🐳 Docker

Build

```bash
docker build -t ai-ticket-app .
```

Run

```bash
docker run -p 8000:8000 ai-ticket-app
```

---

# ☁️ Deployment

The application is deployed on **AWS EC2** using Docker.

Deployment workflow:

```
Developer
    │
    ▼
Git Push
    │
    ▼
GitHub Actions
    │
    ▼
Build Docker Image
    │
    ▼
Push to Docker Hub
    │
    ▼
SSH into EC2
    │
    ▼
Pull Latest Image
    │
    ▼
Restart Container
```

Every push to the `main` branch automatically deploys the latest version of the application.

---

# 📸 Screenshots

## Swagger UI

<img width="969" height="833" alt="Screenshot 2026-05-10 at 3 21 52 PM" src="https://github.com/user-attachments/assets/f88441c8-f88e-4347-acae-cdcc2041774c" />

---

## Ticket Prediction

<img width="490" height="781" alt="Screenshot 2026-05-10 at 3 24 01 PM" src="https://github.com/user-attachments/assets/08f6269e-d58d-4cce-b4a6-7dad1163e34e" />

---

## Metrics Endpoint

<img width="741" height="757" alt="Screenshot 2026-05-10 at 3 25 52 PM" src="https://github.com/user-attachments/assets/02603bcf-29f7-4b4c-bcb7-e48c88a50d8f" />

---

## GitHub Actions CI/CD

<img width="1470" height="838" alt="Screenshot 2026-06-26 at 6 47 32 PM" src="https://github.com/user-attachments/assets/a03f7162-701d-45fa-9dff-a009d504040a" />

---

## Docker Hub Repository

<img width="1470" height="837" alt="Screenshot 2026-06-26 at 6 58 45 PM" src="https://github.com/user-attachments/assets/1896b873-495e-4fc5-b36d-c8c4c9c3ef2e" />

---

## AWS EC2 terminal

<img width="1469" height="109" alt="Screenshot 2026-06-26 at 7 08 18 PM" src="https://github.com/user-attachments/assets/6690e109-8542-4892-82d1-a34d4881afdc" />

---

# 📈 Future Enhancements

* JWT Authentication
* Admin Dashboard
* Model Retraining Pipeline
* PostgreSQL Support
* MLflow Integration
* Monitoring & Logging
* Kubernetes Deployment
* Prometheus & Grafana

---

# 👨‍💻 Author

**Dev Suthar**

AI / Machine Learning Engineering Portfolio Project

---

# ⭐ If you found this project useful, consider giving it a star.
