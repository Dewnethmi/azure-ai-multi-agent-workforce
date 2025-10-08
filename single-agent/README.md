# 📁 Single-Agent

This directory contains a minimal, single-agent example and supporting utilities for the **Azure AI Multi-Agent Workforce** project. It is designed for local development, experimentation, and serves as a reference implementation for building a single autonomous agent.

## 🎯 Purpose

* Demonstrate a simple single-agent runtime and associated tooling.
* Provide a lightweight example to learn agent design, tool usage, and message flow before progressing to multi-agent scenarios.
* Keep single-agent examples isolated from the main multi-agent application.

## 🗂️ Layout

* **`.env`** — Local environment overrides (not checked into source control).
* **`.env.example`** — Template listing required environment variables.
* **`.python-version`** — Preferred Python interpreter version (for pyenv or similar tools).
* **`pyproject.toml`** — Project metadata and dependency declarations.
* **`uv.lock`** — Lockfile used by local tooling (e.g., `uv`).
* **`agent[x]/main.py`** — Example implementation for agent number *x* (e.g., `agent1/main.py`).

## 🚀 Quick Start

1. **Copy the environment template:**

   * PowerShell:

     ```powershell
     cp .env.example .env
     ```

   * Command Prompt:

     ```cmd
     copy .env.example .env
     ```

   Then, edit `.env` and add required API keys, endpoints, and other settings.

2. **Prepare the Python environment:**

   * Use the Python version specified in `.python-version` or ensure Python 3.10+ is installed.

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

3. **Run the demo agent:**

   ```bash
   python agent1/main.py
   python agent2/main.py
   ```

## 📝 Development Notes

* Keep secrets out of version control; `.env` should remain local-only.
* Prefer creating small, explicit utility functions in `agentX/tools.py` rather than embedding side-effect code directly in agents.
* Use `pyproject.toml` to manage dependencies, and pin versions in CI for reproducible builds.

## 🛠 Troubleshooting

* **Module not found:** Run scripts from the repository root or ensure the project root is on your `PYTHONPATH`.
* **Missing environment variables:** Make sure `.env` exists and contains required keys or export them in your shell.
* **Runtime errors:** Check console logs for error details; agent examples include intent and error logging.

## 🤝 Contributing

* Keep examples focused, minimal, and easy to understand.
* Update `.env.example` whenever adding new required environment variables.
* Add tests when introducing new tools or agent behaviors.
