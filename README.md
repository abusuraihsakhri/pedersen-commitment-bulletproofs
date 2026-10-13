# Pedersen Commitment Bulletproofs

A Python rule-based monitoring demonstration with a standalone browser interface, CLI, FastAPI API, and in-memory HMAC audit trail.

**Important scope limitation:** Despite the repository name, this implementation **does not generate or verify Pedersen commitments, Bulletproof range proofs, or other zero-knowledge proofs**. Its numeric thresholds are illustrative and **not derived from NIST standards or validated for security, medical, or operational decisions**. The eight `enrichment.py` modules are similarly threshold-based placeholders, not cryptographic or formal-verification implementations.

## Browser demonstration

Serve the static directory locally (ES modules require an HTTP origin in common browsers):

```bash
python -m http.server 8080 --directory web
```

Open `http://127.0.0.1:8080/`. The page evaluates the same three demonstration rules as the primary Python supervisor without a backend service, external fonts, accounts, or form-data transmission. The JSON result can be downloaded locally. GitHub Actions includes a Pages deployment workflow, subject to repository Pages configuration; use a live URL only after deployment has been verified.

Rules: primary metric **>25**, secondary metric **>12**, and case-insensitive descriptor keywords (`DISCORDANT`, `ANOMALY`, `MUTANT`, `VIOLATION`, `FAIL`, `REJECT`). An explicit critical flag escalates the result. These are arbitrary example thresholds. The alternate legacy `bulletproofs_engine` module has a separate secondary threshold of **>10**.

## Python installation

Requires Python 3.9+.

```bash
python -m pip install -e ".[api,test]"
pytest -v
```

CLI examples:

```bash
pedersen-commitment-bulletproofs audit --task-id T1 --target KEY-01 --primary 28 --secondary 13 --status DISCORDANT
pedersen-commitment-bulletproofs chat "status"
pedersen-commitment-bulletproofs batch -i sample.csv -o results.csv
pedersen-commitment-bulletproofs verify-audit
pedersen-commitment-bulletproofs serve --host 127.0.0.1 --port 8000
```

The `python cli.py` form also works. The default installed command uses `agents/`; the legacy command can still be invoked through `python -m bulletproofs_engine.cli`.

Batch CSV fields: `task_id`, `target_identifier`, `primary_metric`, `secondary_metric`, `status_descriptor`, and `is_critical_flag`. Invalid numerical records are skipped with a warning.

## REST API

The optional FastAPI server exposes `GET /health`, `GET /metrics`, `POST /api/audit`, `POST /api/chat`, and `GET /api/audit/logs`. API docs are at `http://127.0.0.1:8000/docs` during local development. Do not expose the server publicly without independently implementing authentication, access controls, request limits, and persistent logging.

The `/api/chat` endpoint is a deterministic mock, not an actual language-model inference service. Other provider names are rejected rather than silently falling back to the mock.

## Audit and privacy limitations

The server computes an HMAC-SHA256 chain over audit metadata using `AUDIT_SECRET_KEY`. Provide a randomly generated secret in deployment. Without one, the application warns and uses an ephemeral key. The audit log, keys, and task registry are **in memory only**: they do not survive restarts, and `verify-audit` in a new CLI process cannot verify entries from a previous process. HMAC integrity is not proof of regulatory compliance, secure persistence, or independent attestation.

Regex-based identifier screening covers common examples of emails, phone numbers, MRNs, dates of birth, and similar patterns. It is **not comprehensive de-identification**, a HIPAA Safe Harbor implementation, or a guarantee that personal data cannot enter the service. Do not submit real patient or sensitive data.

For Docker Compose, set `AUDIT_SECRET_KEY` in your shell or a private `.env` file:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
docker compose up --build
```

Do not commit this value. An audit key present in earlier repository history should be considered exposed and must not be reused.

## Quality checks and technology

```bash
python -m pip check
python -m compileall -q agents bulletproofs_engine cli.py enrichment.py simulator.py
pytest -v
node --check web/app.mjs
node --test tests/web.test.mjs
```

The Python code uses Pydantic, with FastAPI and Uvicorn for the optional API. The browser uses native JavaScript (no Pyodide or Python runtime); HTML, CSS, and JS are kept relative for static hosting. CI tests Python 3.10–3.12 and the browser evaluation module.

## License

MIT — see [LICENSE](LICENSE).
