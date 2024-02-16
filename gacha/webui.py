import flask
from flask import Flask


webui = Flask(__name__)


def get_page():
    return flask.request.args.get("page", default=1, type=int)


@webui.route("/")
def index():
    from modules.azur_lane import gacha

    page = get_page()
    items = gacha.get_gacha_items(page)
    return flask.render_template("test.html.j2", items=items)
