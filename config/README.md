# 📁 `config/`

This directory centralizes runtime configuration, environment templates, and lightweight maintenance scripts for the **Azure AI Multi-Agent Workforce** project.

## 🎯 Purpose

* Isolate environment variables, project settings, and small utility scripts from the main application logic.
* Provide a centralized, consistent way to manage configuration across local development and deployment environments.
* Allow changes to runtime behavior without modifying application source code.

## 📦 Contents

* **`.env`**
  Local environment file (excluded from version control). Populate this with secrets and runtime values used by the application.

* **`.env.example`**
  Template showing required and optional environment variables, along with expected formats.
  👉 Copy this to `.env` and update the values before running the app.

* **`settings.py`**
  Loads configuration values (typically from `.env` or OS environment) and exposes them as constants or config objects.

  * Avoid hardcoding secrets or logic here — only read and expose values.

* **`delete_agents.py`**
  Maintenance script for removing agents and related resources created during development or testing.

* **`delete_threads.py`**
  Script to delete conversation threads or session data — helpful for cleaning up test artifacts or resetting the local state.

## 🚀 Quick Start

1. **Create your local `.env` file:**

   * PowerShell:

     ```bash
     cp .env.example .env
     ```

   * Command Prompt:

     ```cmd
     copy .env.example .env
     ```

   > Edit the new `.env` file and fill in required values like API keys, resource names, endpoints, etc.

2. **Ensure your Python environment is ready:**

   * Use the project's virtual environment or your preferred Python 3.10+ interpreter.

3. **Run maintenance scripts (optional):**

   From the repo root or the `config/` directory:

   ```bash
   python config/delete_agents.py
   python config/delete_threads.py
   ```

   > Use `-h` or `--help` with scripts (if supported) to view usage options.

4. **Use settings in your code:**

   ```python
   from config import settings
   print(settings.OPENAI_API_KEY)
   ```

## 🔐 Security & Best Practices

* **Never commit `.env`** to version control. It should be included in `.gitignore`.
* **For production**, store secrets securely using services like Azure Key Vault or a secret manager.
* **Fail fast**: validate environment variables at startup to catch missing or invalid values early.
* **Keep `settings.py` clean**: Avoid embedding logic or global dicts — use clearly named constants.

## 🛠️ Troubleshooting

* **"Missing environment variable"**
  → Ensure `.env` exists and is correctly populated.

* **"Module not found" or script errors**
  → Run scripts from the **repo root** or ensure your project is in the `PYTHONPATH`.

* **Unexpected config behavior**
  → Double-check spelling and casing of environment variable names.

## 🤝 Contributing

* Update `.env.example` when adding new required environment variables.
* Keep `settings.py` declarative, focused, and well-commented.
* Write maintenance scripts with safe defaults and clear CLI help. Avoid destructive operations without confirmation.

## 📌 Notes

* This directory is intentionally minimal and environment-agnostic.
* For production deployments:

  * Store secrets in a managed secret store.
  * Keep per-environment config files separate (e.g., staging, production).
  * Use CI/CD pipelines to inject secure runtime configurations.
