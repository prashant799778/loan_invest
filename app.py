from flask import Flask

app = Flask(__name__)

# here is how we are handling routing with flask:
@app.route('/')
def index():
    return "Hello World!", 200

# include this for local dev

if __name__ == '__main__':
    app.run()