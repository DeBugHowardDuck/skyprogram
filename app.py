from flask import Flask, render_template, abort, request, jsonify
from coursework2_source.utils import get_posts_all, get_comments_by_post_id, get_post_by_pk, search_for_posts, \
    get_posts_by_user
import os, logging

app = Flask(__name__)

LOGS_DIR = "logs"
LOG_LIFE = os.path.join(LOGS_DIR, "api.log")

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

logging.basicConfig(
    filename=LOG_LIFE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

@app.route("/")
def index():
    posts = get_posts_all()
    return render_template("index.html", posts=posts)

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = get_post_by_pk(post_id)
    if post is None:
        abort(404)
    comments = get_comments_by_post_id(post_id)
    return render_template("post.html", post=post, comments=comments)

@app.route("/search")
def search():
    query = request.args.get("s")
    if not query:
        return render_template("search.html", query="", posts=[])
    posts = search_for_posts(query)
    return render_template("search.html", query=query, posts=posts)

@app.route("/users/<username>")
def user_posts(username):
    posts = get_posts_by_user(username)
    return render_template("user-feed.html", posts=posts, username=username)

@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Страница не найдена</h1><p>Попробуйте вернуться на <a href='/'>главную</a>.</p>", 404

@app.errorhandler(500)
def internal_error(error):
    return "<h1>Ошибка сервера</h1><p>Попробуйте позже.</p>", 500

@app.route("/api/posts")
def api_posts():
    logging.info("запрос /api/posts")
    posts = get_posts_all()
    return jsonify(posts)


@app.route("/api/posts/<int:post_id>")
def api_post_by_id(post_id):
    logging.info(f"Запрос /api/posts/{post_id}")
    post = get_post_by_pk(post_id)
    if post is None:
        return jsonify({"error": "Пост не найден"}), 404
    return jsonify(post)



if __name__ == "__main__":
    app.run(debug=True)