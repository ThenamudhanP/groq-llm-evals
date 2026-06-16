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

2. Environment Variables (Important!)
For security reasons, the .env file containing API keys is not uploaded to this repository. You must create your own.

Create a new file in the root directory named .env.

Get a free API key from GroqCloud.

Get free API keys from Langfuse.

Add the following to your .env file:

Plaintext
GROQ_API_KEY="your_groq_api_key_here"

LANGFUSE_SECRET_KEY="your_langfuse_secret_key_here"
LANGFUSE_PUBLIC_KEY="your_langfuse_public_key_here"
LANGFUSE_HOST="[https://us.cloud.langfuse.com](https://us.cloud.langfuse.com)" # Or the region you selected
💻 How to Run
Run Level 1 (Unit Tests):
This will execute the local tests. You will see two tests pass and one intentionally fail (to demonstrate error catching).

Bash
python src/level-1-unit-tests.py
Run Level 2 (Human Annotation):
This will process the tickets and send the trace data to your Langfuse web dashboard.

Bash
python src/level-2-human-annotation.py
Once this script finishes, log into your Langfuse dashboard to view the traces, latency, and add human scoring!
