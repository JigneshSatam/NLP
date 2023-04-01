import os
from chatbot import ChatBot

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cb = ChatBot("foodie")

    @app.route("/")
    def hello() -> str:
        return render_template("index.html")  # bot_response

    @app.route("/chat")
    def chat() -> str:
        user_ip = request.args.to_dict().get("user_ip")
        bot_response = cb.chat(user_ip)
        return jsonify(bot_msg=bot_response)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
