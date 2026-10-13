"""
FastAPI REST API Server for Bulletproofs Non-Interactive Zero-Knowledge Range Proof & Confidential Asset Agent.
"""
from typing import Dict, Any
from .models import FrontierPayload
from .agents import BulletproofsCoordinator

coordinator = BulletproofsCoordinator()


def create_app():
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel

        app = FastAPI(
            title="Bulletproofs Non-Interactive Zero-Knowledge Range Proof & Confidential Asset Agent",
            description="Evaluates illustrative numeric thresholds; does not implement cryptographic commitments or Bulletproofs.",
            version="2.0.1",
        )

        class TaskRequest(BaseModel):
            task_id: str = "TASK-2026-001"
            target_identifier: str = "TARGET-BIO-KEY"
            primary_metric: float = 28.5
            secondary_metric: float = 14.2
            status_descriptor: str = "DISCORDANT_ANOMALY"
            is_critical_flag: bool = True
            attributes: Dict[str, Any] = {}

        class ChatRequest(BaseModel):
            query: str

        @app.get("/health")
        def health():
            return {"status": "HEALTHY", "system": "pedersen-commitment-bulletproofs", "domain": "Rule-Based Monitoring Demonstration", "version": "2.0.0-FRONTIER"}

        @app.post("/api/audit")
        def api_audit(req: TaskRequest):
            payload = FrontierPayload(
                task_id=req.task_id,
                target_identifier=req.target_identifier,
                primary_metric=req.primary_metric,
                secondary_metric=req.secondary_metric,
                status_descriptor=req.status_descriptor,
                is_critical_flag=req.is_critical_flag,
                attributes=req.attributes,
            )
            return coordinator.process(payload)

        @app.post("/api/chat")
        def api_chat(req: ChatRequest):
            return {"response": coordinator.query_supervisory_chat(req.query)}

        return app
    except ImportError:
        return None
