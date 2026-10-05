# SDR Research & Post-Call Coaching MVP

Docker-ready prototype for SDR pre-call research and post-call coaching.

## Includes
- Pre-call company research workflow
- Company snapshot, recent changes, growth signals, conversation angles and discovery gaps
- Avoma-style transcript upload/paste
- Post-call discovery analysis
- Research → Call comparison
- Evidence-oriented coaching
- Next Call Plan
- No overall call-quality score

## Prototype limitation
Research currently uses clearly labelled demo/mock data and transcript analysis uses transparent local rules. It does not yet connect to live web research, an LLM API, Avoma, a database, or external company-information providers.

## Local
Copy .env.example to .env, then run:
docker compose up --build

Open http://localhost:8000

## Render
Build: pip install -r requirements.txt
Start: python app/server.py
The server reads PORT and binds to 0.0.0.0.

## Production next step
Company name → reliable source retrieval → source validation → evidence store → AI synthesis → Pre-Call Brief.

Avoma transcript → structured extraction → discovery analysis → Research vs Call comparison → evidence-based coaching → Next Call Plan.

Never present unsupported company claims as facts.
