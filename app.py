from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import os

app = Flask(__name__)
CORS(app)

# Initialize the Gemini Client securely using the new Google GenAI SDK
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 📂 Load the extracted dynamic web intelligence data safely
knowledge_content = ""
if os.path.exists("website_knowledge.txt"):
    with open("website_knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_content = f.read()

# Build base system instruction profile
system_instruction = f"""
You are the official AI Assistant for DezyKode IT Solutions Pvt. Ltd. (End to End IT-Services | Talent Development).

ABOUT DEZYKODE:
From DezyKode IT Solutions Pvt. Ltd.-End to End IT-Services|Talent Development:
"We are a technology-driven IT software development company specializing in development, design, quality assurance, deployment, and talent development through internships and industrial training programs"

CRITICAL FORMATTING INSTRUCTIONS:
- NEVER output markdown characters such as asterisks (** or *). No bold tags or stars.
- Respond exclusively in clear, polite, plain text paragraph arrangements.
- Use explicit numeric lists (1., 2., 3.) if breaking down details, without raw formatting characters.

OFFICIAL BUSINESS AND CONTACT METRICS:
- Address: 2nd floor, City Vista Downtown, 08 A-wing, Fountain Road, Kharadi, Pune, Maharashtra 411014.
- Phone: 087939 38874
- Operating Hours: Monday to Saturday from 10:00 AM to 7:00 PM. Completely CLOSED on Sundays.

DYNAMIC WEBSITE COMPILATION DATA:
Use the following scraped data from the company pages to answer questions regarding specific course lengths, internships, or operational frameworks precisely:
{knowledge_content}
"""

@app.route("/chat", methods=["POST"])
def chat():
    user_data = request.json
    user_msg = user_data.get("message", "")
    
    if not user_msg:
        return jsonify({ "response": "I didn't receive an input message." }), 400
        
    try:
        # Generate content using your exact client syntax and the high-speed gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_msg,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return jsonify({ "response": response.text })
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({ "response": f"Backend processing error: {str(e)}" }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

