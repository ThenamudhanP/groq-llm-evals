import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load our environment variables (including the GROQ_API_KEY)
load_dotenv()

# Initialize the Groq client instead of OpenAI
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def load_event(filename: str) -> dict:
    """Helper function to load the saved JSON tickets."""
    # Note: If your 'events' folder is inside a 'src' folder,
    # you might need to adjust this path to "src/events/{filename}"
    with open(f"events/{filename}", "r") as f:
        return json.load(f)


# --------------------------------------------------------------
# Define the example workflow using Groq
# --------------------------------------------------------------

def process_customer_message(message: str) -> dict:
    """
    Sends the customer message to Groq's Llama 3 model.
    We ask the model to return a structured JSON response manually.
    """
    prompt = f"""
    You are a customer service AI that analyzes customer inquiries.
    Analyze the following inquiry and respond strictly in JSON format with exactly two keys:
    1. "category": Must be exactly one of these: "complaint", "feature_request", "billing", "other".
    2. "response": Your professional draft response to the customer.

    Do not include any markdown formatting like ```json or text before/after the JSON string.

    Customer Message: "{message}"
    """

    # Calling Groq's super fast free model
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        temperature=0,  # We keep it 0 so the output is consistent
    )

    # Get the raw text string from the AI
    raw_output = chat_completion.choices[0].message.content.strip()

    # Convert that text string into a Python dictionary
    parsed_json = json.loads(raw_output)

    # We create a simple class-like object matching what Dave's assertions expect
    class StructuredOutput:
        def __init__(self, data):
            self.category = data.get("category")
            self.response = data.get("response")

    return StructuredOutput(parsed_json)


# --------------------------------------------------------------
# Individual test functions (Dave's exact tests!)
# --------------------------------------------------------------

def test_billing_categorization():
    event = load_event("billing_test.json")
    result = process_customer_message(event["message"])
    assert result.category == "billing"
    assert len(result.response) > 10


def test_feature_request_categorization():
    event = load_event("feature_request_test.json")
    result = process_customer_message(event["message"])
    assert result.category == "feature_request"
    assert len(result.response) > 10


def test_support_categorization():
    event = load_event("failing_test.json")
    result = process_customer_message(event["message"])
    # Dave purposely coded this to expect "complaint" so we can watch it fail!
    assert result.category == "complaint"
    assert len(result.response) > 5


# --------------------------------------------------------------
# Run all tests
# --------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_billing_categorization,
        test_feature_request_categorization,
        test_support_categorization,
    ]
    passed = 0

    print("🚀 Starting Local LLM Evaluation Drills...\n")

    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__} passed successfully!")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} failed (as expected or due to misclassification).")
        except Exception as e:
            print(f"⚠️ Error running {test.__name__}: {e}")

    print(f"\nFinal Results: {passed}/{len(tests)} tests passed.")