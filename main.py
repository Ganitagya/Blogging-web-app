from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

posts: list[dict] = [
    {
        "id": 1,
        "author": "Akash Mahapatra",
        "title": "FastAPI is awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "June 18, 2026"
    },
    {
        "id": 2,
        "author": "Durga Prasad",
        "title": "Python is great for web development",
        "content": "This framework is really easy to use and super fast. And this is another  motivation for me to learn Python",
        "date_posted": "June 17, 2026"
    }
]

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{posts[0]['title']}</h1>"


@app.get("/api/posts")
def get_posts():
    return posts