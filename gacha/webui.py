import flask
from flask import Flask

webui = Flask(__name__)


@webui.route("/")
def index():
    from modules.azur_lane import gacha

    return flask.render_template("test.html.j2", items=gacha.get_gacha_items())
