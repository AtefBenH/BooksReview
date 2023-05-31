from flask import Flask
app = Flask(__name__)
app.secret_key = "NoSecretOnGitHub"
DATABASE = "books_blog_schema"