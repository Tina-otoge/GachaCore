import dataclasses

import flask
from flask import Flask

from plugins.azur_lane import api

webui = Flask(__name__)


def get_page():
    return flask.request.args.get("page", default=1, type=int)


def get_filters(filters):
    return {
        field.name: flask.request.args.get(field.name, type=field.type)
        for field in dataclasses.fields(filters)
    }


@webui.route("/")
def index():
    from plugins.azur_lane import gacha

    filters = api.ShipFilters

    page = get_page()
    filters = get_filters(filters)
    filters = api.ShipFilters(**filters)
    paged = gacha.get_gacha_items(filters, page)
    return flask.render_template(
        "test.html.j2",
        paged=paged,
        filters={
            field.name: {
                "value": getattr(filters, field.name, None),
                "type": field.type,
            }
            for field in dataclasses.fields(filters)
        },
    )


@webui.route("/<id>")
def detail(id):
    from plugins.azur_lane import gacha

    return flask.render_template(
        "test_details.html.j2", item=gacha.get_gacha_item(id)
    )
