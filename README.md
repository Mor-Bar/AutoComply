# AutoComply 🛡️

> Continuous Controls Monitoring (CCM) platform for automated security compliance assessment.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-red.svg)](https://github.com/astral-sh/ruff)

---

## Overview

AutoComply automates the process of verifying security controls against industry frameworks — replacing manual, point-in-time compliance audits with continuous, evidence-based monitoring.

Instead of filling out spreadsheets once a year, AutoComply continuously collects evidence from your environment, maps it to framework controls, and produces a real-time compliance score with actionable findings.

**Supported Frameworks:**
- CIS Controls v8 (active)
- NIST CSF 2.0 (roadmap)
- ISO/IEC 27001:2022 (roadmap)

---

## Key Features

- **Automated Evidence Collection** — Pulls real system data (registry, event logs, services, firewall rules) instead of relying on self-attestation
- **Control Mapping** — Maps collected evidence to specific framework controls and safeguards
- **Compliance Scoring** — Produces quantitative compliance scores per control group and overall
- **Structured Reporting** — Outputs findings in JSON, Markdown, and HTML formats
- **CLI-First Design** — Fully operable from the command line, CI/CD-friendly
- **AI Advisory Layer** *(roadmap)* — Anomaly detection and remediation recommendations

---

## Architecture
```
autocomply/
├── core/          # Domain models and business logic (framework-agnostic)
├── collectors/    # Evidence collectors (Windows, network, cloud)
├── frameworks/    # Control definitions per framework (CIS v8, NIST, ISO 27001)
├── storage/       # Persistence layer (SQLite → PostgreSQL)
├── cli/           # Command-line interface (Typer)
├── reports/       # Report generation (JSON, Markdown, HTML)
└── ai/            # AI advisory layer (roadmap)
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Windows 10/11 or Windows Server 2019+ (for Windows collectors)

### Installation
```bash
# Clone the repository
git clone https://github.com/morba/autocomply.git
cd autocomply

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -e ".[dev]"
```

### Run a Compliance Scan
```bash
# Run full CIS Controls v8 assessment
autocomply scan --framework cis_v8

# Run specific control group
autocomply scan --framework cis_v8 --group IG1

# Generate HTML report
autocomply report --format html --output report.html
```

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 — Foundation | ✅ Complete | Project structure, tooling, domain models |
| 2 — CIS Controls v8 | 🔄 In Progress | Control definitions, Windows evidence collectors |
| 3 — Scoring Engine | 📅 Planned | Compliance calculation, findings generation |
| 4 — Reporting | 📅 Planned | JSON, Markdown, HTML output |
| 5 — REST API | 📅 Planned | FastAPI endpoints, OpenAPI documentation |
| 6 — AI Layer | 📅 Planned | Anomaly detection, remediation advisor |
| 7 — Dashboard | 📅 Planned | React web interface |

---

## Development
```bash
# Run tests
pytest

# Run linter
ruff check src/

# Run formatter
black src/

# Run type checker
mypy src/
```

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

---

## License

MIT License — see [LICENSE](LICENSE) for details.