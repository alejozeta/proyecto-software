# ADR-001: Tech Stack and Architecture

## Date
2026-03-17

## Status
Accepted

## Context

Predictiva is a hydrocarbon production forecasting platform developed by a 3-person university team with fixed delivery deadlines (Phase 1 due 2026-04-28). The project must demonstrate professional software engineering practices — CI/CD, containerization, monitoring, API design — while being evaluated by a professor on both the technical result and the team's ability to defend every design decision.

The team needs to select:
1. A backend framework for the REST API
2. A containerization strategy
3. A CI/CD platform
4. A monitoring stack
5. A cloud deployment target
6. An overall application architecture

Constraints:
- 3-person team with limited calendar time per phase (~6 weeks each)
- Must produce a deployable, demonstrable system at each phase
- Professor evaluates architecture decisions, not just working code
- Phase 1 is a mock API + CI/CD + monitoring; Phases 2-3 add data ingestion and ML
- The stack must scale from a mock service (Phase 1) to a full ML pipeline (Phase 3) without rewrites

## Decision

We adopt the following stack and architecture:

- **Backend:** Python 3.12 + FastAPI
- **Containerization:** Docker + Docker Compose
- **Container Registry:** GitHub Container Registry (ghcr.io)
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana
- **Deployment:** Railway or Render
- **Testing:** pytest + httpx
- **Architecture:** 3 vertical layers (API → ML → Data) + 1 horizontal Data Platform layer

## Assumptions

- All team members have basic Python experience
- GitHub is the agreed-upon code hosting platform (university or team decision)
- Railway or Render free/hobby tiers provide sufficient resources for a demo deployment
- The professor values industry-standard tooling and documented trade-offs over exotic or novel choices
- Prometheus client library for Python is stable and integrates with FastAPI without major friction
- The mock API in Phase 1 will share the same endpoint structure, auth mechanism, and response format as the final API in Phase 3

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **Flask** instead of FastAPI | Mature, huge ecosystem, simpler mental model | No native async, no auto-generated OpenAPI docs, manual validation | FastAPI gives us Swagger docs for free (required by spec) and native async for future ML workloads |
| **Django REST Framework** | Batteries-included, admin panel, ORM | Heavy for an API-only service, steep config overhead, slower iteration for a small team | Over-engineered for Phase 1 mock + Phase 2-3 pipeline; we don't need an ORM or admin in Phase 1 |
| **Express.js (Node)** | Fast prototyping, large ecosystem | Team's ML experience is Python-centric; would require two languages when Phase 3 adds ML models | Keeping one language (Python) across API and ML simplifies the codebase and team workflow |
| **Jenkins** instead of GitHub Actions | Very flexible, self-hosted | Requires hosting and maintaining a Jenkins server; complex setup for a 3-person team | GitHub Actions is free for public repos, zero infrastructure, tightly integrated with our GitHub workflow |
| **GitLab CI** | Built-in registry, good CI features | Would require migrating the repository to GitLab or maintaining a mirror | Team already uses GitHub; adding GitLab introduces unnecessary friction |
| **ELK Stack** (Elasticsearch + Logstash + Kibana) instead of Prometheus + Grafana | Powerful log analysis, full-text search on logs | Resource-heavy (Elasticsearch alone needs significant memory), complex setup, overkill for metrics | Prometheus + Grafana is lightweight, purpose-built for metrics, and runs comfortably in Docker Compose on any dev machine |
| **Datadog / New Relic** (SaaS monitoring) | Zero infrastructure, polished UI | Paid beyond free tier, vendor lock-in, less educational value | Open-source stack lets us understand and demonstrate what's happening under the hood — better for academic evaluation |
| **AWS / GCP / Azure** for deployment | Full cloud ecosystem, production-grade | Requires billing setup, IAM complexity, more config surface area than needed | Railway/Render offer one-command deploys from Docker images with free tiers — appropriate for a university demo |
| **Monolithic single-layer architecture** | Simplest to start | Cannot evolve: when ML and data layers arrive in Phase 2-3, the codebase becomes tangled | Layered architecture costs almost nothing in Phase 1 (the layers are just directories) but pays off immediately when new modules land |
| **Microservices architecture** | Strong separation, independent scaling | Massive overhead for a 3-person team: separate repos, service discovery, inter-service communication | The 3-layer monolith gives us clean separation without operational complexity; we can split later if needed |

## Trade-offs

**Gains:**
- Single language (Python) across all phases — API, data processing, and ML
- Automatic OpenAPI/Swagger documentation from FastAPI (required by the spec)
- Entire stack runs locally via `docker compose up` — any team member can develop and demo independently
- GitHub Actions CI/CD requires zero infrastructure to maintain
- Prometheus + Grafana are industry-standard, open-source, and lightweight enough for local development
- Layered architecture provides clean separation for Phase 2-3 without premature complexity
- Railway/Render simplify deployment to a single Docker image push

**Costs:**
- FastAPI is newer than Flask/Django — fewer tutorials targeted at beginners (mitigated by excellent official docs)
- Prometheus is pull-based, which requires the API to expose a metrics endpoint (minor implementation effort)
- Railway/Render free tiers have cold-start latency and resource limits (acceptable for a demo)
- The 3-layer architecture adds directory structure that is mostly empty in Phase 1 (negligible cost)

## Technical Justification

The stack is chosen to minimize friction for a small team under tight deadlines while meeting every Phase 1 requirement:

1. **FastAPI** directly satisfies the spec requirement for online OpenAPI/Swagger docs. Its type-hint-based validation reduces boilerplate. Native async support means the same framework handles the mock API now and real ML inference later without framework migration.

2. **Docker + Compose** is explicitly required by the spec ("all components MUST be containerized"). Compose lets us define the API, Prometheus, and Grafana as a single declarative file — one command to run everything.

3. **GitHub Actions** integrates with our existing GitHub repository with no external service to configure. The spec requires CI to run tests on every PR and CD to deploy automatically — Actions handles both natively.

4. **Prometheus + Grafana** satisfies the monitoring dashboard requirement (latency, uptime, error rate, CPU/memory, alerts). Both run as Docker containers alongside the API, keeping the local dev experience simple.

5. **Railway/Render** provides the simplest path from a Docker image to a public URL, which is required for each delivery.

6. **3-layer architecture** maps directly to the PRD's simplified flow (API → ML → Data) and the project roadmap (Phase 1 = API layer, Phase 2 = Data layer, Phase 3 = ML layer). Each phase adds a layer without restructuring existing code.

## Consequences

- All team members must have Docker installed locally
- The API must expose a `/metrics` endpoint for Prometheus scraping
- CI/CD workflows must be defined in `.github/workflows/` and kept in sync with the Docker build
- Every new component (Phase 2 data module, Phase 3 ML module) will be added as a new layer within the same Docker Compose setup
- ADRs for future decisions (e.g., database choice in Phase 2, ML framework in Phase 3) should reference this ADR as the foundational stack decision
