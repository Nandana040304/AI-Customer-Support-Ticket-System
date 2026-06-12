import google.generativeai as genai
import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def categorize_ticket(description):

    prompt = f"""
    Categorize the following support ticket.

    Categories:
    Billing
    Technical
    Account
    Delivery
    Other

    Ticket:
    {description}

    Return only category name.
    """

    response = model.generate_content(
        prompt
    )

    return response.text.strip()

def generate_ai_response(description):

    prompt = f"""
    You are a customer support assistant.

    Generate a professional support response.

    Ticket:
    {description}
    """

    response = model.generate_content(
        prompt
    )

    return response.text.strip()