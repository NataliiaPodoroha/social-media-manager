import time
import google.generativeai as genai
from settings import settings


genai.configure(api_key=settings.GOOGLE_AI_API_KEY)


def generate_ai_reply(
    post_content: str, comment_content: str, replay_delay: int = 0
) -> str:
    time.sleep(replay_delay)

    prompt = (
        f"Generate one relevant reply to the comment "
        f"based on the post content, "
        f"using a conversational and friendly tone.\n\n"
        f"Post: {post_content}\n"
        f"Comment: {comment_content}\n"
        f"Reply:"
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
