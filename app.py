from flask import Flask, render_template, request
from users_database import add_new_user, show_employees

app = Flask(__name__)

add_new_user()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_companies")
def get_companies():
    hashtag = request.args.get('hashtag')
    if hashtag == 'Other':
        return render_template("autocomplete.html", set(hashtags))
    return show_employees(hashtag)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
