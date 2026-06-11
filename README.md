# Customer Retention AI System

## Overview

This project is an AI-powered Customer Retention System built using FastAPI, Machine Learning, LangGraph, and OpenAI.

The application predicts customer churn risk using a trained Machine Learning model and automatically generates personalized retention emails for customers who are at risk of leaving.

The generated emails are validated against Vodafone brand guidelines and review rules before being marked as ready for sending.

---

## Features

### Churn Prediction

* Uses a trained ML model to predict customer churn probability.
* Returns a Healthy status for low-risk customers.
* Triggers an AI retention workflow for high-risk customers.

### Retention Email Generation

* Generates personalized retention emails using OpenAI.
* Uses customer-specific services and account information.
* Follows Vodafone brand guidelines.

### AI Email Validation

* Reviews generated emails against predefined review rules.
* Calculates a validation score.
* Flags emails requiring human review.

### LangGraph Orchestration

* Multi-step orchestration workflow.
* Conditional routing based on churn risk.
* Async execution support.

---

## Architecture

```text
Customer Request
        |
        v
+-------------------+
|   FastAPI API     |
+-------------------+
        |
        v
+-------------------+
| Churn Prediction  |
|   ML Model        |
+-------------------+
        |
        v
  Score < 0.5 ?
     /      \
   Yes      No
   |          |
   v          v
Healthy   LangGraph
             |
             v
      Context Builder
             |
             v
      Email Generation
             |
             v
      Email Validation
             |
             v
      Final Response
```

---

## LangGraph Workflow

### Nodes

#### ML Node

Predicts customer churn probability.

#### Risk Node

Determines:

* High Risk
* Low Risk

#### Context Node

Builds customer context for personalization.

#### LLM Node

Generates retention email using OpenAI.

#### Validation Node

Validates generated email against:

* Vodafone Brand Guidelines
* Vodafone Review Rules

---

## Project Structure

```text
app/
│
├── api/
│   └── v1/
│       └── retention/
│           ├── route.py
│           └── controller.py
│
├── orchestrations/
│   ├── retention_node.py
│   └── retention_orchestration_layer.py
│
├── services/
│   ├── churn_service.py
│   └── llm_service.py
│
├── schema/
│   └── retention.py
│
├── prompts/
│   ├── vodafone_brand_guidelines.md
│   └── vodafone_email_review_rules.md
│
├── ML_models/
│   └── churn_model.pkl
│
├── data/
│   └── Vodafone_Customer_Database.csv
│
└── main.py
```

---

## API Endpoint

### Get Retention Recommendation

```http
GET /api/v1/retention/{customer_id}
```

### Example

```http
GET /api/v1/retention/7590-VHVEG
```

---

## Sample Responses

### Healthy Customer

```json
{
  "customer_id": "2824-AHFTR",
  "status": "Healthy",
  "churn_score": 0.1249
}
```

### Review Required

```json
{
  "customer_id": "7590-VHVEG",
  "status": "REVIEW_REQUIRED",
  "churn_score": 0.8734,
  "validation_score": 72,
  "violations": [
    "Missing service personalization"
  ],
  "generated_email": {
    "subject": "...",
    "email_body": "..."
  }
}
```

### Ready To Send

```json
{
  "customer_id": "7590-VHVEG",
  "status": "READY_TO_SEND",
  "churn_score": 0.8734,
  "validation_score": 95,
  "retention_email": {
    "subject": "...",
    "email_body": "..."
  }
}
```

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
API_KEY=retention_api_key_123
PORT=8000
LOG_LEVEL=INFO
LOG_FILE=app.log
```

---

## Installation

### Create Virtual Environment

```bash
python -m venv env_assignment
```

### Activate Environment

Windows:

```bash
env_assignment\Scripts\activate
```

### Install Dependencies

```bash
cd AI-Assignment
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

---

## Technologies Used

* Python 3.x
* FastAPI
* LangGraph
* OpenAI
* Pandas
* Scikit-Learn
* Joblib
* Pydantic
* Uvicorn

---

## Future Enhancements

* Human Approval UI
* Email Delivery Integration
* Retrieval Augmented Generation (RAG)
* Customer Offer Recommendation Engine
* Monitoring & Observability
* A/B Testing of Retention Campaigns

```
```
