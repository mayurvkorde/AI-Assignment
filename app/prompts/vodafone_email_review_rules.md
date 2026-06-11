# Vodafone Retention Email Review Rules

## Purpose

Validate generated retention emails before they are sent to customers.

---

## Validation Objectives

The email must:

* Follow Vodafone brand guidelines.
* Be factually consistent with customer data.
* Be professional and customer-focused.
* Contain no hallucinated information.
* Be safe for customer communication.

---

## Mandatory Checks

### Brand Compliance

Verify that the email:

* Uses a friendly tone.
* Uses a professional tone.
* Uses a positive tone.
* Uses a respectful tone.

---

### Personalisation

Verify that:

* Referenced services exist in customer data.
* Referenced contract information exists in customer data.
* Referenced tenure information exists in customer data.
* No unsupported customer details are introduced.

---

### Hallucination Detection

Fail validation if the email contains:

* Discounts not present in input.
* Promotions not present in input.
* Rewards not present in input.
* Cashback not present in input.
* Gifts not present in input.
* Credits not present in input.
* Pricing changes not present in input.
* Service upgrades not present in input.

---

### Restricted Topics

Fail validation if the email mentions:

* Churn score
* Churn prediction
* Machine learning
* Artificial intelligence
* Internal systems
* Internal models
* Internal analytics

---

## Scoring

Score the email from 0 to 100.

Scoring Criteria:

* Brand Compliance: 30 points
* Personalisation Accuracy: 30 points
* Factual Accuracy: 20 points
* Professional Tone: 20 points

---

## Decision Rules

Score >= 80

Result:

{
"passed": true,
"human_review_required": false
}

Score < 80

Result:

{
"passed": false,
"human_review_required": true
}

---

## Output Format

Return valid JSON:

{
"score": 0,
"passed": false,
"human_review_required": true,
"violations": []
}
