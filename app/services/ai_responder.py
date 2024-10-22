import time
import google.generativeai as genai
from sqlalchemy.orm import Session
from app.models.user import User
from settings import settings


genai.configure(api_key=settings.GOOGLE_AI_API_KEY)


def generate_ai_reply(
    post_content: str, comment_content: str, user_id: int, db: Session
) -> str:
    user = db.query(User).filter(User.id == user_id).first()

    if user and user.auto_reply:
        time.sleep(user.reply_delay or 0)

    prompt = (
        f"Generate one relevant reply to the comment based on the post content, "
        f"using a conversational and friendly tone.\n\n"
        f"Post: {post_content}\n"
        f"Comment: {comment_content}\n"
        f"Reply:"
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
