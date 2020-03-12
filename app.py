# Import necessary libraries
from flask import Flask, render_template, redirect, request


# Create instance of Flask app
app = Flask(__name__)


# Create routes that render the HTML templates
@app.route("/")
def index():
    return render_template("index.html")


# Preview locally on http://127.0.0.1:5000/
if __name__ == "__main__":
    app.run(debug=True)
