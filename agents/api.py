"""
FastAPI REST API Server for Pedersen Commitment Bulletproofs.
"""
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Pedersen Commitment Bulletproofs API",
    description="Rule-based metric screening and in-memory HMAC audit demonstration; does not produce cryptographic range proofs.",
    version="3.0.1",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "pedersen-commitment-bulletproofs", "engine": "rule-based-monitoring", "version": "3.0.1"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
    except Exception as exc:
        from .base import SecurityException
        if isinstance(exc, SecurityException):
            raise HTTPException(status_code=422, detail="Input contains a potentially sensitive identifier") from None
        raise
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except Exception as exc:
        from .base import SecurityException
        if isinstance(exc, SecurityException):
            raise HTTPException(status_code=422, detail="Query contains a potentially sensitive identifier") from None
        raise


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
