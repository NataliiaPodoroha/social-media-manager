# Project Name

## Overview

This project is a web application that allows users to register, log in, create posts, and comment on posts. It includes features such as JWT authentication, moderation of comments and posts, and an automatic comment reply feature.

## Features

- **User Registration and Login**: Users can register and log in to the application using JWT authentication.
- **Post Management API**: Users can create, read, update, and delete posts.
- **Comment Management API**: Users can create, read, update, and delete comments on posts.
- **Content Moderation**: Posts and comments are checked for offensive language and blocked if necessary.
- **Comment Analytics**: Provides analytics on the number of comments added to posts over a specified period.
- **Automatic Comment Reply**: Users can enable automatic replies to comments on their posts. The reply is generated after a delay and is relevant to the post and the comment.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-repo/project-name.git
    cd project-name
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    alembic upgrade head
    ```

5. Create a `.env` file in the root directory of the project.


6. Generate a `SECRET_KEY` for JWT authentication by running the following command:
    ```sh
    openssl rand -hex 32
    ```

7. Obtain your `GOOGLE_AI_API_KEY` by visiting [Google AI Studio](https://aistudio.google.com/apikey) and create a new API key.


8. Add the generated `SECRET_KEY` and `GOOGLE_AI_API_KEY` to the `.env` file. Example:
    ```env
    SECRET_KEY=your_generated_secret_key
    GOOGLE_AI_API_KEY=your_google_ai_api_key
    ```

9. Refer to the `.env.sample` file for an example of how to structure your `.env` file.


## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Usage

### User Registration and Login

- **Register**: `POST /api/register`
- **Login**: `POST /api/login`

### Post Management

- **Create Post**: `POST /api/posts`
- **Get All Posts**: `GET /api/posts`
- **Get Single Post**: `GET /api/posts/{post_id}`
- **Update Post**: `PUT /api/posts/{post_id}`
- **Delete Post**: `DELETE /api/posts/{post_id}`

### Comment Management

- **Create Comment**: `POST /api/comments`
- **Get Comments by Post**: `GET /api/posts/{post_id}/comments`
- **Get Comments by User**: `GET /api/users/{user_id}/comments`
- **Delete Comment**: `DELETE /api/comments/{comment_id}`

### Comment Analytics

- **Get Comment Analytics**: `GET /api/comments-daily-breakdown?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`

### Automatic Comment Reply

- **Enable Auto Reply**: Users can enable automatic replies to comments on their posts. The reply is generated after a delay and is relevant to the post and the comment.

## Testing

To run the tests, use the following command:
```sh
pytest