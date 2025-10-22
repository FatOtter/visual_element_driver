<!--
Sync Impact Report:
Version change: 0.0.0 → 1.0.0
Modified principles: N/A (initial creation)
Added sections: API-First Design, JSON Data Format, Flask Simplicity, Unreal Engine Integration
Removed sections: N/A
Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md
Follow-up TODOs: None
-->

# Unreal Engine Backend Data Retriever Constitution

## Core Principles

### I. API-First Design
Every endpoint MUST be designed for JSON consumption by Unreal Engine clients; RESTful API patterns required; Clear request/response schemas documented; Versioned API endpoints (v1, v2, etc.); CORS headers configured for cross-origin requests from Unreal Engine applications.

### II. JSON Data Format (NON-NEGOTIABLE)
All API responses MUST be valid JSON; Consistent data structure across all endpoints; Error responses in JSON format with standardized error codes; No HTML or text responses for API endpoints; Content-Type headers properly set to application/json.

### III. Flask Simplicity
Use minimal Flask dependencies; Avoid complex frameworks or ORMs unless absolutely necessary; Single-file applications preferred for simple endpoints; Clear separation between data retrieval and presentation logic; Stateless design for horizontal scaling.

### IV. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced; API contract tests required for all endpoints; Integration tests for Unreal Engine client compatibility; Performance tests for data retrieval endpoints.

### V. Unreal Engine Integration
Endpoints MUST be optimized for Unreal Engine HTTP requests; Response times under 200ms for real-time data; Support for batch data requests; Efficient JSON serialization; Connection pooling and timeout handling; Graceful degradation when services are unavailable.

## Technology Constraints

**Backend Framework**: Flask (Python 3.8+) - lightweight and simple
**Data Format**: JSON only - no XML, HTML, or other formats
**API Style**: RESTful with clear resource-based URLs
**Authentication**: Simple API key or token-based (no complex OAuth)
**Database**: SQLite for development, PostgreSQL for production
**Deployment**: Docker containers preferred for consistency
**Monitoring**: Basic logging and health check endpoints

## Development Workflow

**Code Review Requirements**: All PRs must include API contract tests; JSON response validation required; Performance benchmarks for data endpoints; Documentation updates for new endpoints
**Testing Gates**: Unit tests for all data retrieval functions; Integration tests with mock Unreal Engine clients; Load testing for concurrent requests; API documentation must be updated before merge
**Deployment Process**: Health check endpoints must pass; Database migrations tested; API versioning compatibility verified; Rollback plan documented

## Governance

Constitution supersedes all other practices; Amendments require documentation, approval, migration plan; All PRs/reviews must verify compliance with JSON format requirements; Complexity must be justified with Unreal Engine integration benefits; Use implementation plans for runtime development guidance; API breaking changes require major version increment and migration documentation.

**Version**: 1.0.0 | **Ratified**: 2025-01-27 | **Last Amended**: 2025-01-27
