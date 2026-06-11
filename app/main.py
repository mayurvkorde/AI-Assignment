from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from app.api.v1 import api_router
from app.config.constant import API_PREFIX, MODEL_NAME
import logging
from contextlib import asynccontextmanager
from app.services.churn_service import ChurnService
import pandas as pd
import joblib
from app.services.llm_service import LLMService
import os

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Load application resources during startup and release them during shutdown."""

    churn_model = joblib.load("app/ML_models/churn_model.pkl")
    app.state.churn_model = churn_model

    app.state.churn_service = ChurnService(churn_model)
    app.state.customer_data = pd.read_csv("app/data/Vodafone_Customer_Database.csv")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY  is not configured")

    app.state.llm_service = LLMService(api_key,MODEL_NAME)
    logger.info("Churn model loaded")
    try:
        yield
    finally:
        app.state.churn_model = None
        app.state.churn_service = None
        app.state.customer_data = None
        app.state.llm_service = None


app = FastAPI(
    title="Retention",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

app.include_router(api_router, prefix=API_PREFIX)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=80000,
    )