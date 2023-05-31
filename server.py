from flask_app import app
from flask_app.controllers import users, books, likes, comments
from flask import request, render_template

# CATCH ANY UNDEFINED ROUTE
@app.errorhandler(404)
def page_not_found(error):
    route = request.path
    return render_template('404.html', route = route)


if __name__ == "__main__":
    app.run(debug=True)