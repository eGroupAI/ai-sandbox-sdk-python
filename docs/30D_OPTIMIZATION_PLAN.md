# 30-Day Optimization Plan (Python SDK)

## Outcome Target

- Deliver a stable SDK that minimizes integration effort and improves supportability in production.
- Keep first successful API call under 10 minutes and first streaming chat integration under 30 minutes.

## P0 (Day 1-14): Reliability and Contract Hardening

| Workstream | Task | Files | Acceptance |
| --- | --- | --- | --- |
| API Contract Alignment | Align endpoint paths/methods with current backend contract and integration docs | `src/ai_sandbox_sdk/client.py`, `openapi/ai-sandbox-v1.yaml`, `docs/INTEGRATION.md` | 11 API operations validated with no mismatch |
| Safe Retry Policy | Default retries to idempotent methods, add explicit option for write retries | `src/ai_sandbox_sdk/client.py`, `README.md` | Fault-injection test shows no duplicate write operations |
| Error Observability | Standardize `ApiError` usage with trace id logging examples | `src/ai_sandbox_sdk/client.py`, `README.md`, `docs/INTEGRATION.md` | Error guide includes status/body/trace_id handling |
| QA Baseline | Add unit tests for retry policy, SSE parser path, and request serialization | `src/ai_sandbox_sdk/*.py`, `tests/*` (new), `pyproject.toml` | CI test stage green with critical-path coverage target |
| CI/CD Guardrails | Add lint/test/build workflow and release check gates | `.github/workflows/ci.yml` (new), `pyproject.toml` | PRs blocked when checks fail |

## P1 (Day 15-30): Developer Experience and Growth

| Workstream | Task | Files | Acceptance |
| --- | --- | --- | --- |
| Example Expansion | Upgrade quickstart to full flow (agent -> channel -> SSE -> KB) | `examples/quickstart.py`, `README.md` | Example runs with env vars only |
| Visual Docs Upgrade | Extend README with troubleshooting and common error recipes | `README.md`, `docs/INTEGRATION.md` | Reduced onboarding friction in pilot feedback |
| Release Quality | Add structured release checklist and compatibility notes | `CHANGELOG.md`, `CONTRIBUTING.md` | Every release includes migration notes |
| Security Posture | Add dependency audit and secret scanning process | `.github/workflows/ci.yml`, `SECURITY.md` | No unresolved high-severity issue before release |

## Language File Checklist

- `README.md`
- `docs/INTEGRATION.md`
- `docs/30D_OPTIMIZATION_PLAN.md`
- `src/ai_sandbox_sdk/client.py`
- `src/ai_sandbox_sdk/__init__.py`
- `examples/quickstart.py`
- `openapi/ai-sandbox-v1.yaml`
- `pyproject.toml`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

## Definition of Done (DoD)

- [ ] 11/11 API operations pass production integration validation.
- [ ] SSE flow yields chunk data and stops on `[DONE]` across regression tests.
- [ ] Retry defaults prevent duplicate non-idempotent writes.
- [ ] CI workflow enforces lint + build + test on all PRs.
- [ ] README quickstart runs directly with `AI_SANDBOX_BASE_URL` and `AI_SANDBOX_API_KEY`.
