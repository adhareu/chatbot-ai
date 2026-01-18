import os
from openai import OpenAI
from app.services.memory_store import get_history, append_message

SYSTEM_PROMPT = "You are a helpful AI assistant."

def generate_reply(message: str, session_id: str) -> str:
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Add user message to memory
        append_message(session_id, "user", message)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(get_history(session_id))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content

        # Add assistant reply to memory
        append_message(session_id, "assistant", reply)

        return reply

    except Exception as e:
        print("AI Error:", e)
        return "AI service is currently unavailable."
