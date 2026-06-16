import os
import json
from dotenv import load_dotenv
from groq import Groq

# 1. The new Langfuse v4 Import Syntax!
from langfuse import observe, get_client

# 2. Load environment variables
load_dotenv()

# 3. Initialize Groq and Langfuse (v4 style)
langfuse = get_client()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def load_event(filename: str) -> dict:
    """Load test event from JSON file"""
    with open(f"events/{filename}", "r") as f:
        return json.load(f)


# --------------------------------------------------------------
# In Langfuse v4, @observe() automatically captures the inputs
# and outputs of the function without needing extra manual code!
# --------------------------------------------------------------
@observe()
def process_customer_message(message: str):
    """Process customer message with LangFuse tracing"""

    prompt = f"""
    You are a customer service AI that analyzes customer inquiries.
    Analyze the following inquiry and respond strictly in JSON format with exactly two keys:
    1. "category": Must be exactly one of these: "complaint", "feature_request", "billing", "other".
    2. "response": Your professional draft response to the customer.

    Do not include any markdown formatting.

    Customer Message: "{message}"
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        temperature=0,
    )

    raw_output = chat_completion.choices[0].message.content.strip()
    result = json.loads(raw_output)

    return result


def run_evaluation_pipeline():
    test_files = ["billing_test.json", "feature_request_test.json", "failing_test.json"]

    print("🚀 Running Level 2 Pipeline (Langfuse v4) and sending traces...\n")

    for filename in test_files:
        event = load_event(filename)
        message = event["message"]

        # Because this function has @observe(), Langfuse is tracking it
        result = process_customer_message(message)

        print(f"Ticket: {filename}")
        print(f"Category: {result.get('category')}")
        print(f"Response: {result.get('response')}\n")
        print("-" * 50)

    # Flush ensures all data is successfully uploaded to the web dashboard before the script closes
    langfuse.flush()


if __name__ == "__main__":
    run_evaluation_pipeline()