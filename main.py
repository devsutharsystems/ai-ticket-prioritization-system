from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from database import create_table, get_connection
import pickle
from text_utils import normalize_text

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

create_table()

app = FastAPI()

class Ticket(BaseModel):
    title: Annotated[str, Field(..., description='Whats the issue?', examples=['Payment Issue'])]
    description: Annotated[str, Field(..., description='Elaborate your query')]

class TicketUpdate(BaseModel):
    title: Annotated[Optional[str], Field(default=None)]
    description: Annotated[Optional[str], Field(default=None)]

def process_ticket(description: str):
    description = description.lower()

    ml_priority, confidence = get_ml_priority(description)
    final_priority, used_rule = apply_rule(description, ml_priority)

    review = needs_review(confidence, used_rule)
    team = assign_team(final_priority)

    return {
        "description": description,
        "priority": str(final_priority),
        "confidence": float(confidence),
        "used_rule": int(used_rule),
        "needs_review": int(review),
        "team": team
    }

def apply_rule(description: str, ml_priority: str):
    description = description.lower()

    HIGH_HINTS = ["all users", "system-wide", "completely", "entire", "global"]
    LOW_HINTS = ["visually", "ui", "alignment", "spacing", "typo"]

    CRITICAL_PATTERNS = [
        "crash",
        "data lost",
        "data corrupted",
        "security breach",
        "unauthorized access",
        "not responding"
    ]

    if any(hint in description for hint in LOW_HINTS):
        return "low", True
    
    if any(hint in description for hint in HIGH_HINTS):
        return "high", True

    if any(word in description for word in CRITICAL_PATTERNS):
        return "high", True
    
    return ml_priority, False



def get_ml_priority(description: str):

    vec = vectorizer.transform([normalize_text(description)])

    probs = model.predict_proba(vec)[0]
    classes = model.classes_

    index = probs.argmax()

    priority = classes[index]
    confidence = probs[index]

    return priority, confidence

def needs_review(confidence: float, used_rule: bool) -> bool:
    if used_rule:
        return False
    return confidence < 0.6

def assign_team(priority: str) -> str:
    mapping = {
        "high": "Critical Response Team",
        "medium": "Backend Team",
        "low": "UI/UX Team"
    }
    return mapping.get(priority, "General Support")

@app.get("/")
def root():
    return {
        "message": "AI Ticket Prioritization System is running",
        "docs": "/docs",
        "metrics": "/metrics"
    }
        
@app.get("/tickets")
def view_tickets():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()

    return [
        {
            "ID": row[0],
            "title": row[1],
            "description": row[2],
            "priority": row[3],
            "team": assign_team(row[3]),
            "confidence": float(row[4]) if row[4] is not None else None,
            "used_rule": bool(row[5]) if row[5] is not None else False,
            "needs_review": bool(row[6]) if row[6] is not None else False
        }
        for row in rows
    ]
    
@app.get("/metrics")
def get_metrics():

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tickets")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tickets WHERE corrected_priority IS NOT NULL")
        corrected = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tickets WHERE used_rule = 1")
        rules_used = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tickets WHERE needs_review = 1")
        needs_review_count = cursor.fetchone()[0]

    accuracy = 0
    if total > 0:
        accuracy = (total - corrected) / total

    return {
        "total_tickets": total,
        "corrected_tickets": corrected,
        "rule_usage": rules_used,
        "needs_review": needs_review_count,
        "approx_accuracy": accuracy
    }    

@app.post("/tickets")
def create_ticket(ticket: Ticket):

    result = process_ticket(ticket.description)

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO tickets 
            (title, description, priority, confidence, used_rule, needs_review) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                ticket.title, 
                result["description"], 
                result["priority"],
                result["confidence"],
                result["used_rule"],
                result["needs_review"]
            )
        )

        ticket_id = cursor.lastrowid
        conn.commit()

    return {
        "ID": ticket_id,
        "title": ticket.title,
        **result
    }

@app.get("/tickets/{id}")
def get_by_id(id: int):
    
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets WHERE id = ?", (id,))
        row = cursor.fetchone()

    if not row:    
        raise HTTPException(status_code=404, detail="ID not found")
    
    return {
        "ID": row[0],
        "title": row[1],
        "description": row[2],
        "priority": row[3],
        "team": assign_team(row[3]),
        "confidence": float(row[4]) if row[4] is not None else None,
        "used_rule": bool(row[5]) if row[5] is not None else False,
        "needs_review": bool(row[6]) if row[6] is not None else False
    }

@app.put("/tickets/{id}")
def update_ticket(id: int, ticket: TicketUpdate):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM tickets WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Ticket not found")

        updated_data = ticket.model_dump(exclude_none=True)

        if "description" in updated_data:
            result = process_ticket(updated_data["description"])

            updated_data.update({
                "description": result["description"],
                "priority": result["priority"],
                "confidence": result["confidence"],
                "used_rule": result["used_rule"],
                "needs_review": result["needs_review"]
            })

        if not updated_data:
            raise HTTPException(status_code=400, detail="No data provided")

        query = ", ".join([f"{k} = ?" for k in updated_data.keys()])
        values = list(updated_data.values()) + [id]

        
        cursor.execute(f"UPDATE tickets SET {query} WHERE id = ?", values)
        conn.commit()


    return {"id": id, "updated_fields": updated_data}

@app.put("/tickets/{id}/feedback")
def update_feedback(id: int, corrected_priority: str):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM tickets WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Ticket not found")

        
        cursor.execute(
            "UPDATE tickets SET corrected_priority = ? WHERE id = ?",
            (corrected_priority, id)
        )

        conn.commit()

    return {"id": id, "corrected_priority": corrected_priority}


@app.delete("/tickets/{id}")
def delete_ticket(id: int):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM tickets WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Ticket not found")

        cursor.execute("DELETE FROM tickets WHERE id = ?", (id,))
        conn.commit()

    return {"deleted_id": id}


            

