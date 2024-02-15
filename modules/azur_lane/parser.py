import requests
from bs4 import BeautifulSoup

from .models import Ship, Skin, SkinVariant, db

RAW_DATA_URL = "https://github.com/AzurAPI/azurapi-js-setup/raw/autoupdate/ship/dist/ship-list.json"
WIKI_URL = "https://azurlane.koumakan.jp"


def main(stop_at=-1):
    response = requests.get(RAW_DATA_URL)
    data = response.json()
    with db.create_session() as session:
        db_ids = [ship.id for ship in session.query(Ship.id).all()]

    def report_progress(n):
        print("=" * 20)
        print(f"Processed {n} / {len(db_ids)} ships")
        print("=" * 20)

    for n, ship in enumerate(data.values()):
        print(ship)
        if ship["id"] in db_ids:
            print(f"Skipping {ship['name']} already in db")
            continue
        if len(ship["id"]) == 4 and ship["id"][0] == "3":
            print(
                f"Skipping {ship['name']} as it is a Unreleased/Retrofitted ship (3XXX)"
            )
            continue
        wiki_url = f"{WIKI_URL}/wiki/{ship['name']}/Gallery"
        soup = BeautifulSoup(requests.get(wiki_url).text, "html.parser")
        skins = []
        for skin in soup.find_all(class_="shipskin"):
            name = skin.find(class_="shipskin-name").text
            if "µ" in name and "µ" not in ship["name"]:
                # name = "µ"
                continue
            else:
                name = name.split(":", 1)[1].strip()

            bg = skin.find(class_="shipskin-bg").find("img")["src"]

            chibi_container = skin.find(class_="shipskin-chibi")
            if chibi_container is None:
                chibi = None
            else:
                chibi = skin.find(class_="shipskin-chibi").find("img")["src"]

            variants = []

            variants_soup = skin.find_all(class_="shipskin-image")

            def get_variant(name, soup):
                img_tag = soup.find("img")
                # check if srcset exists
                if img_tag.get("srcset"):
                    img = img_tag["srcset"].split(" ")[-2]
                else:
                    img = img_tag["src"]
                thumb = soup.find("img")["src"]
                return {"name": name, "img": img, "thumb": thumb}

            if len(variants_soup) == 1:
                variants = [get_variant(name, variants_soup[0])]
            else:
                variants = [
                    get_variant(variant.parent["data-title"], variant)
                    for variant in variants_soup
                ]
            print(f"{name=}, {bg=}, {chibi=}, {variants}")
            skins.append(
                {
                    "name": name,
                    "bg": bg,
                    "chibi": chibi,
                    "variants": variants,
                }
            )
        ship.update({"skins": skins})
        with db.create_session() as session:
            ship_model = Ship(
                id=ship["id"],
                name=ship["name"],
                rarity=Ship.Rarity(ship["rarity"]),
                type=Ship.Type(ship["type"]),
                affiliation=Ship.Affiliation(ship["nationality"]),
            )
            session.add(ship_model)
            for skin in skins:
                skin_model = Skin(
                    ship_id=ship["id"],
                    name=skin["name"],
                    bg_url=skin["bg"],
                    chibi_url=skin["chibi"],
                )
                session.add(skin_model)
                for variant in skin["variants"]:
                    variant_model = SkinVariant(
                        skin_ship_id=ship["id"],
                        skin_name=skin["name"],
                        name=variant["name"],
                        img_url=variant["img"],
                        thumb_url=variant["thumb"],
                    )
                    session.add(variant_model)
            session.commit()

        if n == stop_at:
            break

        if n % 10 == 0:
            report_progress(n)


if __name__ == "__main__":
    main()
