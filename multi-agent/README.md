# 📁 Multi-Agent

This folder contains multi-agent examples and runtime components for the **Azure AI Multi-Agent Workforce** project. It demonstrates how to compose multiple specialized agents, wire shared utilities, and run multi-agent scenarios for experimentation and demos.

## 🎯 Purpose

* Showcase agent-to-agent collaboration patterns.
* Illustrate splitting responsibilities among specialized agents (e.g., knowledge, sales, inventory, store management).
* Provide runnable multi-agent scenarios you can build upon and iterate.

## 🗂️ Layout

* **`.env` / `.env.example`** — Local environment file and template (copy `.env.example` to `.env`).
* **`.python-version`** — Preferred Python version for contributors.
* **`pyproject.toml` / `uv.lock`** — Project metadata and lockfile for reproducible installs.
* **`main.py`** — Optional convenience entrypoint for a default multi-agent demo.
* **`scenario_1/`, `scenario_2/`, `scenario_3/`, `scenario_4/`** — Independent scenario directories with agent implementations, settings, and example data/diagrams.
* **`core/`** (inside each scenario) — Shared lightweight utilities like `azure_client.py`, `conversation_manager.py`, and `cleanup_utils.py`.
* **`agents/`** (inside each scenario) — Role-specific agent modules.
* **`data/`** — Sample data used by some scenarios (e.g., `sales_data.csv`).
* **`diagrams/`** — Draw.io diagrams documenting agent roles and workflows.

## 🚀 Quick Start

1. **Copy the environment template and update secrets:**

   ```powershell
   cp .env.example .env
   # Then edit .env with your API keys and endpoints
   ```

2. **Create and activate a Python virtual environment:**

   * Using `venv`:

     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1   # PowerShell
     .\.venv\Scripts\activate.bat   # Command Prompt
     pip install --upgrade pip
     pip install -e .
     ```

   * Or, if using `uv` tooling:

   *(dependencies are in `pyproject.toml`.)*

     ```bash
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1   # PowerShell
     .\.venv\Scripts\activate.bat   # Command Prompt
     uv sync
     ```

3. **Run a scenario demo (from `multi-agent` directory or repo root):**

   ```powershell
   python scenario_1/main.py
   python scenario_2/main.py
   python scenario_3/main.py
   python scenario_4/main.py
   python scenario_[x]/main.py # Example implementation for scenario number *x* (e.g., `scenario_1/main.py`).
   ```

Many scenarios accept CLI options or read `settings.py` inside their folder for configuration.

## 🗂️ Scenarios — Overview

* **`scenario_1/`** — Basic demo with diagrams illustrating agent roles and conversation flows. Great for conceptual experiments.

* **`scenario_2/`** — Fitness & wellness (agents: `fit_agent`, `diet_agent`, `workout_agent`). Demonstrates multi-role coordination and small toolsets.

* **`scenario_3/`** — Retail/inventory (agents: `inventory_agent`, `sales_agent`, `store_manager_agent`, `knowledge_agent`). Interacts with sample data and OpenAPI-like inventory tools.

* **`scenario_4/`** — Education / knowledge work (agents: `azure_docs_agent`, `study_buddy_agent`). Showcases retrieval and synthesis workflows.

*Check the `diagrams/` folders to visualize roles and flows.*

## ⚙️ Per-Scenario Configuration

* Edit `scenario_X/settings.py` to customize local paths or override environment values.
* `core/azure_client.py` uses environment variables or `settings.py` for API keys/endpoints.
* For production, use secure secret stores (e.g., Azure Key Vault).

## 🛠 Important Utilities

* `core/conversation_manager.py` — Orchestrates agent conversation state & message formatting.
* `core/cleanup_utils.py` — Cleans up state during tests or local runs.
* `core/azure_client.py` — Wraps cloud API calls, centralizing client code.

## 💡 Development Tips

* Run scenario scripts from repo root to avoid module resolution issues.
* Use `scenario_3/data/` sample data for retail tests.
* Update `.env.example` and per-scenario docs when adding environment variables.

## 🐞 Troubleshooting

* **Module import errors:** Ensure you ran `pip install -e .` and run scripts from repo root.
* **Missing environment variables:** Copy `.env.example` → `.env` and fill secrets, or export them in your shell.
* **Cloud API permissions:** Verify credentials and update client libraries.

## 🔍 Logging & Observability

Agents and core utilities log to console by default. Increase verbosity via scenario `main.py` logging configs or environment variables.

## 🤝 Contributing

* Keep scenarios small and focused on specific collaboration or integration patterns.
* Add unit tests for new `core/` utilities and agent tools.
* Update `diagrams/` when agent responsibilities change.

## 🔒 Security

* Never commit secrets — `.gitignore` excludes `.env`.
* Use least-privilege credentials and role-based access for cloud resource interaction.
* For production, migrate secrets to secure stores like Azure Key Vault.

## 🚀 Next Steps & Ideas

* Add integration tests mocking Azure clients.
* Integrate Azure Key Vault + Managed Identity in `core/azure_client.py` for secure local runs.
* Experiment with new agent roles (e.g., an ObservabilityAgent monitoring logs and suggesting actions).
