from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import os

app = Flask(__name__)
CORS(app)

# Initialize the Gemini Client
# Make sure to replace "YOUR_GEMINI_API_KEY" with your real key from Google AI Studio
# This tells the code to securely look for an environment variable named GEMINI_API_KEY
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# This system instruction tells the AI exactly who it is and what facts to stick to!
DEZYKODE_CONTEXT = """
You are the official AI Chatbot Assistant for DezyKode IT Solutions (www.dezykode.com).
Your job is to assist users politely and accurately based on the company's real data.

Core Information:
- Location: Office No. 08, 2nd Floor, A-Wing, City Vista, Downtown Road, Ashoka Nagar, Kharadi, Pune, Maharashtra 411014.
- Contact: info@dezykode.com
- Timings: Monday to Saturday (10:00 AM - 6:00 PM), Sunday (10:00 AM - 3:30 PM).
- What they do: DezyKode is a premier software training institute and software development company bridging the digital skills gap.
- Courses Offered: Web Designing, UI/UX Design, Full Stack Web Development, Android/iOS App Development, Database Management, Cyber Security, Software Testing, Graphic Designing, and Python/Java Programming.
- Offerings: Job-oriented curriculum, practical industrial live projects, expert IT trainers, interview preparation, and placement assistance.
- Target Audiances: College students, fresh graduates, and working professionals looking to upskill.

Guidelines:
- Be professional, welcoming, friendly, and helpful.
- Keep answers relatively concise and easy to read in a small chat window.
- If you don't know the answer to something outside DezyKode's scope, politely guide the user to email info@dezykode.com or visit the Kharadi center for a counseling session.
"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"response": "Please say something!"}), 400
        
    try:
        # Generate content using the recommended model for text chat tasks
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=DEZYKODE_CONTEXT,
                temperature=0.7
            )
        )
        return jsonify({"response": response.text})
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"response": "I'm having trouble connecting to my brain right now. Please try again in a second!"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)



