import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import ServiceRequest, Facility, Article, ContactMessage, Feedback

app = FastAPI(title="Sampurna API", description="API untuk platform pengolahan & pemilahan sampah")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "Sampurna API", "status": "ok"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# -----------------------------
# Public content endpoints
# -----------------------------

@app.get("/facilities")
async def list_facilities(city: Optional[str] = None):
    filt = {"city": city} if city else {}
    docs = get_documents("facility", filt, limit=100)
    # Convert ObjectId to str for JSON serializable response
    for d in docs:
        d["_id"] = str(d["_id"])
    return {"items": docs}

@app.get("/articles")
async def list_articles(tag: Optional[str] = None):
    filt = {"tags": {"$in": [tag]}} if tag else {}
    docs = get_documents("article", filt, limit=50)
    for d in docs:
        d["_id"] = str(d["_id"])
    return {"items": docs}

# -----------------------------
# Lead capture & service request
# -----------------------------

@app.post("/service-request")
async def create_service_request(payload: ServiceRequest):
    try:
        inserted_id = create_document("servicerequest", payload)
        return {"id": inserted_id, "status": "submitted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contact")
async def contact(payload: ContactMessage):
    try:
        doc_id = create_document("contactmessage", payload)
        return {"id": doc_id, "received": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def send_feedback(payload: Feedback):
    try:
        doc_id = create_document("feedback", payload)
        return {"id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
