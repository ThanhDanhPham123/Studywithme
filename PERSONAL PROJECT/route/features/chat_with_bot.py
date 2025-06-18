from google import genai
from flask import render_template, request, Blueprint, session, redirect, url_for
from datetime import datetime
from db import db
from auth import login_required
import re
from markupsafe import Markup

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

def format_ai_response(text):
    # Replace **text** with <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Replace newlines with <br>
    text = text.replace('\n', '<br>')
    # Auto-link URLs
    url_pattern = re.compile(r'(https?://\S+)')
    text = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', text)
    # Example: Highlight "important"
    text = text.replace('important', '<span class="highlight">important</span>')
    return Markup(text)  # Mark as safe for HTML

# AI model client setup
client = genai.Client(api_key="AIzaSyCEt8hchpwxR7p8FnlM_KHyhu3tV8gdRfQ")

@chat_bp.route("/chat_with_bot", methods=["GET", "POST"])
@login_required
def chat_with_bot():
    if "chat_history" not in session:
        session["chat_history"] = []
    username = session.get("username", "there")
    bot_intro = (
        f"Hi {username}! I'm AI Buddy - your study partner — here to help you with anything related to schoolwork, "
        "learning strategies, and extracurricular activities. Whether it's understanding a tricky math concept, "
        "organizing your study schedule, preparing for a competition, or finding ways to improve your skills outside "
        "the classroom, I’ve got your back. If it’s not study- or activity-related, I’ll gently steer us back on track. "
        "Let’s focus and crush your goals together!"
    )

    if request.method == "POST":
        user_input = request.form.get("message", "")
        if user_input:
            archetype_instruction = (
                "You are my dedicated study partner. Only respond to questions that relate to school subjects, "
                "studying techniques, learning goals, or extracurricular activities such as clubs, competitions, sports, "
                "and personal development projects. Politely refuse to answer anything that is off-topic. Your tone should "
                "be helpful, focused, and encouraging, like a supportive peer who wants me to succeed."
                "never provide an empty response, if user input is not related to school subjects, studying techniques, OR EXTRACURRICULAR ACTIVITIES, ALWAYS RESPOND TO THEM WITH AN ANSWER"
            )
            prompt = archetype_instruction + user_input

            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            content_parts = response.candidates[0].content.parts
            response_text = "".join(part.text for part in content_parts if hasattr(part, "text")).strip()
            # Format the AI response for HTML
            formatted_response = format_ai_response(response_text)

            session["chat_history"].append({"role": f'{username}', "text": user_input, "timestamp": datetime.now().isoformat()})
            session["chat_history"].append({"role": "AI Buddy", "text": formatted_response, "timestamp": datetime.now().isoformat()})
            session.modified = True  # Mark session as modified to save changes
            return redirect(url_for("chat.chat_with_bot"))
    chat_history = session.get("chat_history", [])
    if not chat_history:
        chat_history.append({"role": "bot", "text": bot_intro, "timestamp": datetime.now().isoformat()})
        session["chat_history"] = chat_history

    return render_template("chat.html", chat_history=chat_history)

@chat_bp.route("/chat_with_bot/clear", methods=["POST"])
@login_required
def clear_chat_history():
    session.pop("chat_history", None)  # Remove chat history from session
    return redirect(url_for("chat.chat_with_bot"))