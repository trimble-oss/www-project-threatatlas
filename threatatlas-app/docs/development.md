# ThreatAtlas Development & Contributing Guide

Welcome! This guide is for developers looking to contribute to the ThreatAtlas codebase or set up a localized development environment.

---

## 🛠 Tech Stack

- **Frontend**: React + TypeScript, shadcn/ui, ReactFlow
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL 16
- **Package Managers**: `pnpm` (Node), `pdm` (Python)

---

## 💻 Local Development Setup

If you want to contribute to the code, follow these steps to run the services locally.

### 1. Prerequisites
- **Node.js** (v18+) & **pnpm**
- **Python** (v3.11+) & **pdm**
- **Docker** (for running the database locally)

### 2. General Setup
```bash
git clone https://github.com/OWASP/www-project-threatatlas.git
cd www-project-threatatlas/threatatlas-app
cp .env.example .env
```

### 3. Start the Database
```bash
docker compose up -d postgres
```

### 4. Backend Setup (FastAPI)
```bash
cd backend
pdm install
pdm run migrate
pdm run start:dev
```
The API will be available at [http://localhost:8000](http://localhost:8000).

### 5. Frontend Setup (React)
```bash
cd ../frontend
pnpm install
pnpm dev
```
The UI will be available at [http://localhost:5173](http://localhost:5173).

---

## 🚀 Pull Request Process

1. **Fork** the repository and create your branch from `main`.
2. **Format and Lint**:
   - Backend: `pdm run ruff check .`
   - Frontend: `pnpm lint`
3. **Tests**: Ensure tests pass via `pdm run pytest` or `pnpm test`.
4. **Sign-off**: Contributions are licensed under [Apache 2.0](LICENSE.md).

---

## 🏗 Project Structure

```text
threatatlas-app/
├── frontend/           # React + TypeScript
├── backend/            # FastAPI + Alembic
└── docs/               # Documentation files
```

---

## 💬 Community & Support

- **OWASP Slack**: Join #project-threatatlas.
- **Reporting Issues**: Use GitHub Issues for bugs or feature requests.
- **Code of Conduct**: We follow the [OWASP Code of Conduct](https://owasp.org/www-policy/operational/code-of-conduct).
