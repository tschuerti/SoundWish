from flask import Flask, request, render_template, redirect, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return 'Demo'

if __name__ == '__main__':
    app.run()