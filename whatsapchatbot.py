from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from transformers import pipeline


chatbot_ai = pipeline("text-generation", model="bigscience/bloomz-560m")


# Store conversation history
conversation_history = []

# Flask app
app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    global conversation_history
    incoming_msg = request.values.get('Body', '').strip()

    # Append user message to history
    conversation_history.append(f"User: {incoming_msg}\n")

    # Create prompt for AI including history
    prompt = "".join(conversation_history) + "Bot:"

    # Generate AI response
    response = chatbot_ai(prompt, max_new_tokens=50, truncation=True)
    bot_reply = response[0]['generated_text'].split("Bot:")[-1].strip()

    # Append bot reply to history
    conversation_history.append(f"Bot: {bot_reply}\n")

    # Send reply
    resp = MessagingResponse()
    resp.message(bot_reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
