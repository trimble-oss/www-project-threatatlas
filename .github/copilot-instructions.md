# Copilot instructions for OWASP ThreatAtlas

This file gives concise, repo-specific guidance to help Copilot-style assistants work effectively in this repository.

---

## 1) Build, test, and lint commands

Backend (FastAPI, Python / pdm)
- Install dependencies: `pdm install`
- Run dev server: `pdm run start:dev` (uvicorn with reload)
- Run DB migrations: `pdm run migrate` (alembic upgrade head)
- Run tests (full): `pdm run pytest` or `pdm run pytest tests/ -v --tb=short`
- Run a single backend test file: `pdm run pytest tests/test_products.py::test_some_name`
- Lint/format check: `pdm run ruff check .`

Frontend (React + TypeScript / pnpm)
- Install deps: `pnpm install`
- Dev server: `pnpm dev` (Vite) — default at http://localhost:5173
- Build: `pnpm build` (or `pnpm run build:check` to run `tsc -b && vite build`)
- Run tests (vitest): `pnpm test`
- Run a single frontend test file: `pnpm test -- ./src/__tests__/components/ThreatCard.test.tsx` or use `-t` / `--testNamePattern` to run by name
- Lint: `pnpm lint` (eslint)

Docker / Compose
- Quick local run: from `threatatlas-app/` run `docker compose up -d`
- Useful compose variants: `docker-compose.dev.yml`, `docker-compose.tls.yml` (see `threatatlas-app/`)

CI
- GitHub Actions runs: backend pytest job (uses postgres:16, redis) and frontend vitest job (`.github/workflows/ci.yml`).

---

## 2) High-level architecture (big picture)

- Monorepo-like layout with two primary app folders under `threatatlas-app/`:
  - `backend/` — FastAPI app (Python 3.11, pdm), SQLAlchemy models, Alembic migrations, redis-backed services, OpenAI/Anthropic hooks and optional AI features.
  - `frontend/` — React + TypeScript app built with Vite, pnpm, Tailwind/shadcn UI, ReactFlow for diagrams, and Vitest for unit tests.
- Persistence & infra: PostgreSQL is the primary DB; Redis used for caching/collaboration; Alembic manages schema migrations.
- Deploy options: Docker Compose for local or production-ish stacks; Caddy and Keycloak artifacts are included for TLS and OIDC demo setups (`threatatlas-app/caddy/`, `threatatlas-app/keycloak/`).
- CI mirrors local setup: runs backend tests against ephemeral Postgres/Redis services and frontend tests using Node + pnpm.
- AI/assistant: backend has `app/ai/` and alembic migrations for AI tables; frontend contains `useAIChat` hook and `AIChatSheet` UI components — AI is optional and configured at runtime.

---

## 3) Key repository conventions and patterns

- Package managers: **pdm** for Python backend, **pnpm** for frontend. Respect scripts defined in `pyproject.toml` and `package.json`.
- Environment files: copy `.env.example` into `.env` for local dev in both backend and frontend.
- Tests:
  - Backend test directory: `threatatlas-app/backend/tests/` (pytest config in `pyproject.toml`)
  - Frontend tests: `src/__tests__/` (Vitest)
  - CI sets TEST_DATABASE_URL and REDIS_URL environment variables for backend tests; local test runs may need similar envs or the postgres service started via Docker.
- Migrations: Alembic lives under `backend/alembic/` with versioned scripts — use `pdm run migrate` to apply.
- Single-file edits & patches: prefer making surgical edits and running the appropriate local test command for the affected area (backend: specific pytest node; frontend: vitest single-file or test name).
- AI-related code: changes touching `backend/app/ai/*` or frontend `useAIChat`/`AIChatSheet` should consider DB migrations (there are ai-related alembic versions) and provider config in the UI. Treat AI features as opt-in hooks requiring secrets/config.
- OIDC / SSO: Keycloak realm JSON present at `threatatlas-app/keycloak/realm-threatatlas.json` — used in docs for SSO flows.

---

## Where Copilot should look first
- `threatatlas-app/docs/development.md` — local dev steps and commands.
- `threatatlas-app/backend/pyproject.toml` and `threatatlas-app/frontend/package.json` — canonical scripts and test/lint commands.
- `threatatlas-app/backend/tests/` and `threatatlas-app/frontend/src/__tests__/` — examples of how tests are structured.
- `threatatlas-app/backend/alembic/` — DB migrations and schema-change history.
- `.github/workflows/ci.yml` — CI expectations (services, test commands, node/python versions).

---

If this file already exists, consider preserving any custom guidance and merging the sections above rather than overwriting.

Last updated: 2026-06-04
