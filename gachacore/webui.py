import dataclasses

import flask
from flask import Flask

from plugins.azur_lane.gacha import AzurLaneGacha
from plugins.blue_archive.gacha import BlueArchiveGacha

gachas = {x.SLUG: x for x in [AzurLaneGacha, BlueArchiveGacha]}

webui = Flask(__name__)


def get_page():
    return flask.request.args.get("page", default=1, type=int)


def get_filters(filters):
    return {
        field.name: flask.request.args.get(field.name, type=field.type)
        for field in dataclasses.fields(filters)
    }


@webui.route("/<gacha>/")
def index(gacha):
    gacha = gachas[gacha]
    page = get_page()
    user_filters = get_filters(gacha.SEARCH)
    filters = gacha.SEARCH(**user_filters)
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
        gacha=gacha,
    )


@webui.route("/<gacha>/<id>")
def detail(gacha, id):
    gacha = gachas[gacha]
    return flask.render_template(
        "test_details.html.j2", item=gacha.get_gacha_item(id)
    )
