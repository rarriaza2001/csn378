from flask import Flask, request
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# Add "greetings" route
# Read "GREETING" environment variable and return its value
@app.route("/greetings")
def greetings():
    return os.getenv("GREETING")

# Add "listcontents" route
# Read contents of "hostfolder" and return the contents


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001) # Change port to 5001
