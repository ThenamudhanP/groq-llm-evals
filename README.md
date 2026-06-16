# LLM Evaluations: Automated Testing & Human Annotation

This repository demonstrates a framework for evaluating Large Language Models (LLMs) across two distinct levels: Automated Unit Testing (Level 1) and Human Annotation / Observability (Level 2). 

This project was originally based on Dave Ebbelaar's LLM Evals tutorial but has been **significantly upgraded and modified** to use modern, open-source, and free-tier tools.

## 🚀 Key Upgrades from the Original Project

1. **Migrated from OpenAI to Groq:** Replaced paid `gpt-4o-mini` calls with Groq's lightning-fast and free `llama-3.1-8b-instant` model.
2. **Upgraded to Langfuse v4:** Rewrote the observability pipeline to use the modern Langfuse v4 SDK (replacing the deprecated `langfuse.decorators` with the streamlined `@observe` syntax).
3. **Manual JSON Parsing:** Replaced OpenAI's proprietary structured output tool with standardized prompt engineering and native Python `json.loads()` for broader compatibility.

## 📁 Project Structure

* `src/level-1-unit-tests.py`: Local automated testing using PyTest logic to verify the LLM categorizes tickets correctly.
* `src/level-2-human-annotation.py`: Cloud observability pipeline that pushes LLM traces, latency metrics, and inputs/outputs to a live Langfuse dashboard for human grading.
* `events/`: Contains the mock JSON customer support tickets used for testing.

## ⚙️ Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install groq langfuse python-dotenv
