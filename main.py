from fastapi import FastAPI
from database import Base, engine
from app.routers import user, post, comment


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])
app.include_router(comment.router, prefix="/comments", tags=["Comments"])
