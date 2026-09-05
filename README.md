# Pedersen Commitment Bulletproofs

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture  
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Pedersen Commitment Bulletproofs** is an advanced analytical and computational platform implementing Bulletproofs non-interactive zero-knowledge range proof & confidential asset agent. It provides a multi-worker evaluation engine with cryptographic audit trails and PHI (Protected Health Information) outbound guards.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.
- **Multi-Worker Evaluation**: Three specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) for comprehensive analysis.
- **Enrichment Suite**: 8 domain-specific engines for performance benchmarking, side-channel analysis, interoperability testing, and more.

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/pedersen-commitment-bulletproofs.git
cd pedersen-commitment-bulletproofs

# Install dependencies
pip install -e .

# Optional: Install FastAPI/uvicorn for REST API server
pip install fastapi uvicorn
```

---

## 💻 CLI Quickstart & Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. System Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task identifier (default: TASK-2026-001)
- `--target`: Target entity identifier (default: KEY-TARGET-01)
- `--primary`: Primary metric value, float (default: 28.5)
- `--secondary`: Secondary metric value, float (default: 14.2)
- `--critical`: Flag for critical escalation (default: False)
- `--status`: Status descriptor, e.g. NOMINAL, DISCORDANT (default: DISCORDANT)

### Input Data Schema (CSV Batch)

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task identifier | Required |
| `target_identifier` | Target entity identifier | Required |
| `primary_metric` | Primary measurement value (float) | Required |
| `secondary_metric` | Secondary measurement value (float) | Required |
| `is_critical_flag` | Critical escalation flag (true/false) | Optional |
| `status_descriptor` | Status code descriptor | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, DOBs, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition. Integrity verification recomputes HMAC signatures to detect any field tampering.
* **Secure Key Management:** The audit secret key is loaded from the `AUDIT_SECRET_KEY` environment variable. If not set, an ephemeral random key is generated (with a warning) — ensuring no hardcoded secrets in source code.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Environment Variables

| Variable | Description | Default |
|:---------|:------------|:--------|
| `AUDIT_SECRET_KEY` | HMAC secret key for audit trail signing | Random ephemeral (not persisted) |
| `MODEL_PROVIDER` | LLM provider selection | mock |

---

## 🧪 Testing & Verification

Run the full automated test suite:

```bash
pytest -v
```

Run with coverage:

```bash
pytest -v --tb=short
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 100
```

---

## 🐳 Container Deployment

```bash
docker build -t pedersen-commitment-bulletproofs .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key pedersen-commitment-bulletproofs
```

Or using Docker Compose:

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
pedersen-commitment-bulletproofs/
├── agents/                      # Core agent modules (Pydantic models, workers, API)
│   ├── __init__.py
│   ├── api.py                   # FastAPI REST endpoints
│   ├── base.py                  # Security, PHI guard, HMAC audit trail
│   ├── llm_factory.py           # LLM provider factory
│   ├── models.py                # Pydantic data models
│   ├── supervisor.py            # Multi-worker orchestrator
│   └── workers.py               # Specialized evaluation workers
├── bulletproofs_engine/         # Alternative engine implementation
│   ├── __init__.py
│   ├── agents.py                # Sub-agent implementations
│   ├── cli.py                   # CLI entry point
│   ├── engine.py                # Core domain engine
│   ├── models.py                # Dataclass models
│   └── server.py                # FastAPI server factory
├── tests/                       # Test suite
│   ├── test_bulletproofs_engine.py
│   ├── test_enrichment.py
│   ├── test_enrichment_fix.py
│   ├── test_pedersen_commitment_bulletproofs.py
│   └── test_security_and_validation.py
├── cli.py                       # Main CLI entry point
├── simulator.py                 # High-throughput simulation
├── enrichment.py                # Enrichment feature suite
├── pyproject.toml               # Project configuration
├── Dockerfile                   # Container build
├── docker-compose.yml           # Container orchestration
└── web/
    └── index.html               # Web dashboard
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
