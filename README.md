# Azure AI Multi-Agent Workforce

This repository contains code, resources, and documentation for the workshop **"Building a Multi-Agent Workforce with Azure AI Foundry"**.

**Table of Contents:**

- [Azure AI Multi-Agent Workforce](#azure-ai-multi-agent-workforce)
  - [📂 Repository Structure](#-repository-structure)
  - [🧠 Prerequisites](#-prerequisites)
  - [🎬 Video Tutorials](#-video-tutorials)
  - [⚙️ Tools \& Technologies](#️-tools--technologies)
  - [💻 Getting Started](#-getting-started)
    - [1. Sign In or Create Azure Account](#1-sign-in-or-create-azure-account)
    - [2. Create an Azure AI Foundry Project](#2-create-an-azure-ai-foundry-project)
    - [3. Set Up Local Python Development Environment](#3-set-up-local-python-development-environment)
    - [4. Clone the Repository](#4-clone-the-repository)
      - [🔱 Fork the Repository](#-fork-the-repository)
      - [💻 Clone with Git](#-clone-with-git)
    - [5. Set Up Azure Credentials (`.env`)](#5-set-up-azure-credentials-env)
      - [⚙️ Configure Environment Variables](#️-configure-environment-variables)
    - [6. Run Application](#6-run-application)
  - [📚 Resources](#-resources)
  - [⭐ Support the project](#-support-the-project)
  - [📝 License](#-license)
  - [💬 Contact](#-contact)

## 📂 Repository Structure

Here are the key areas you might be looking for:

```text
azure-ai-multi-agent-workforce/
├── config/         # Configuration files for managing the project
├── multi-agent/    # Multi-agent examples
├── single-agent/   # Single-agent examples
└── README.md       # Overview and documentation of the repository
```

## 🧠 Prerequisites

- A working [Azure](https://azure.microsoft.com/) subscription
- Access to [Azure AI Foundry](https://ai.azure.com/)
- Basic [Python](<https://www.python.org>) knowledge
- Checkout [🎬 Video Tutorials](#-video-tutorials) & [⚙️ Tools \& Technologies](#️-tools--technologies)

## 🎬 Video Tutorials

- [Create Azure for Students Account with a Voucher – Get $100 Free Credit](https://www.youtube.com/watch?v=bhMGtA7Q4XY)
- [Create Azure Free Account – Get $200 Free Credit](https://www.youtube.com/watch?v=u7GFfv8KEaA&t=56s)

## ⚙️ Tools & Technologies

- [Git](https://git-scm.com/) – Version control system for tracking code changes
- [GitHub](https://github.com) – For accessing and managing the project repository
- [Visual Studio Code (VS Code)](https://code.visualstudio.com) – Recommended code editor for development
- [Python](<https://www.python.org>) - Programming language used for agent development
- [uv](<https://github.com/astral-sh/uv>) - A modern, high-performance Python package manager and installer
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest) – Command-line interface for managing Azure resources
- [Azure Account](https://azure.microsoft.com/) – Required to access and deploy AI services on Microsoft Azure
- Dependencies:
  - [Python](https://www.python.org/downloads) <= 3.13.5
- Python Packages:
  - [azure-ai-agents](https://pypi.org/project/azure-ai-agents/) >= 1.1.0b4
  - [azure-ai-projects](https://pypi.org/project/azure-ai-projects/) >= 1.0.0b12
  - [azure-identity](https://pypi.org/project/azure-identity/) >= 1.24.0b1
  - [python-dotenv](https://pypi.org/project/python-dotenv/) >= 1.1.1

## 💻 Getting Started

### 1. Sign In or Create Azure Account

If you already have an Azure account that works with Azure AI Foundry projects, you're good to go!

Otherwise, you'll need to set one up. Watch this video for a step-by-step walkthrough: [Create Azure Free Account – Get $200 Free Credit](https://www.youtube.com/watch?v=u7GFfv8KEaA&t=56s)

---

### 2. Create an Azure AI Foundry Project

Follow these steps to set up your Azure AI Foundry project:

1. Sign in to the [Azure Portal](https://portal.azure.com).
2. Create a new **Resource Group** to organize your resources.
3. Go to [Azure AI Foundry](https://ai.azure.com/) and sign in.
4. Create a **new project**, making sure to select the **Resource Group** you created earlier.
5. Deploy at least one **AI model** within your project to enable functionality.

---

### 3. Set Up Local Python Development Environment

Install and configure the required [⚙️ Tools & Technologies](#️-tools--technologies) before running the project locally.

These typically include:

- Python (recommended version: 3.10+)
- `pip` / `uv` / `virtualenv` or `conda`
- Git
- Azure CLI
- Other dependencies listed in `requirements.txt`

Make sure to install all dependencies using:

```bash
pip install -r requirements.txt
```

---

### 4. Clone the Repository

#### 🔱 Fork the Repository

Click [**Fork**](https://github.com/dileepadev/cinewave-demo/fork) on GitHub to create your own copy of this repository under your GitHub account.

#### 💻 Clone with Git

Open your terminal and run the following commands:

```bash
git clone https://github.com/dileepadev/cinewave-demo.git
cd cinewave-demo
```

---

### 5. Set Up Azure Credentials (`.env`)

#### ⚙️ Configure Environment Variables

Each subdirectory (such as `multi-agent/` and `single-agent/`) contains its own `.env.example` file. These files define the environment variables required to run the examples in that specific folder.

To get started:

1. **Navigate to the subdirectory you're working with** (e.g., `multi-agent/`).
2. **Copy the example environment file and rename it to `.env`:**

    ```bash
    cp .env.example .env   # On Windows: use copy .env.example .env
    ```

3. **Open the `.env` file** in your text editor and update the values with your Azure credentials and other necessary configuration.

Repeat this process for each subdirectory you plan to run.

---

### 6. Run Application

Follow the instructions in the corresponding subdirectory’s `README.md` or usage guide to run the application.

## 📚 Resources

- [Abbreviation recommendations for Azure resources](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations)
- [Azure documentation](https://learn.microsoft.com/en-us/azure/?product=popular)
- [Azure AI Foundry documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure Identity client library for Python - version 1.25.0](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python)
- [Azure AI Projects client library for Python - version 1.1.0b4](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme?view=azure-python-preview)
- [Azure AI Agents client library for Python - version 1.2.0b4](https://learn.microsoft.com/en-gb/python/api/overview/azure/ai-agents-readme?view=azure-python-preview)
- [What is Azure AI Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview)
- [Quickstart: Get started with Azure AI Foundry (Foundry projects)](https://learn.microsoft.com/en-us/azure/ai-foundry/quickstarts/get-started-code?tabs=python&pivots=fdp-project)
- [Quickstart: Create a new agent](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart?pivots=programming-language-python-azure)
- [Build collaborative, multi-agent systems with Connected Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/connected-agents?pivots=python#limitations)
- [What is Azure AI Foundry?](https://ai.azure.com/doc/azure/ai-foundry/what-is-azure-ai-foundry?tid=84c31ca0-ac3b-4eae-ad11-519d80233e6f)
- [Create Azure for Students Account with a Voucher – Get $100 Free Credit](https://www.youtube.com/watch?v=bhMGtA7Q4XY)
- [Create Azure Free Account – Get $200 Free Credit](https://www.youtube.com/watch?v=u7GFfv8KEaA&t=56s)
- [Get started with Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli?view=azure-cli-latest)

## ⭐ Support the project

If you like this project and want to see future updates, please consider giving it a star on GitHub!

## 📝 License

This project is licensed under the [MIT License](./LICENSE).

## 💬 Contact

If you have any questions or suggestions regarding this project, feel free to open an issue or submit a pull request in this repository.

You can also reach me via email at: **<contact@dileepa.dev>**
