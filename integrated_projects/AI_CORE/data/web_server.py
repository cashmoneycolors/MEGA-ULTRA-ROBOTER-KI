from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    return send_file('dashboard.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
