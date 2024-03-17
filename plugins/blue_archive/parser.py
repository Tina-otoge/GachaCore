import json

import requests

from .models import Student, db

RAW_DATA_URL = (
    "https://github.com/SchaleDB/SchaleDB/raw/main/data/en/students.json"
)


def main(stop_at=-1):
    response = requests.get(RAW_DATA_URL)
    data = response.json()
    # with open("students.json") as f:
    #     data = json.load(f)
    with db.create_session() as session:
        db_ids = [student.id for student in session.query(Student.id).all()]
    for student in data:
        with db.create_session() as session:
            if student["Id"] in db_ids:
                print(
                    f"Skipping {student['Name']} (#{student['Id']})"
                    " already in db"
                )
                continue
            print(student["Name"], student["Id"])
            year = student["SchoolYear"]
            year = {
                "3年生": "3rd Year",
            }.get(year, year)
            if not year:
                year = None
            age = student["CharacterAge"]
            age.replace("歳", " years old")
            student = Student(
                id=student["Id"],
                name=student["Name"],
                family_name=student["FamilyName"],
                age=age,
                schale_page=student["PathName"],
                game_id=student["DevName"],
                year=year,
                background=student["CollectionBG"],
                intro=student["ProfileIntroduction"],
                hobby=student["Hobby"],
                birthday=student["Birthday"],
                height=student["CharHeightMetric"],
            )
            session.add(student)
            session.commit()
        if stop_at > 0:
            stop_at -= 1
        if stop_at == 0:
            break


def search_unique_values(data):
    schools = set()
    clubs = set()
    squad_types = set()
    tactic_role = set()
    position = set()
    bullet_type = set()
    armor_type = set()
    weapon_type = set()
    school_year = set()
    age = set()
    for student in data:
        schools.add(student["School"])
        clubs.add(student["Club"])
        squad_types.add(student["SquadType"])
        tactic_role.add(student["TacticRole"])
        position.add(student["Position"])
        bullet_type.add(student["BulletType"])
        armor_type.add(student["ArmorType"])
        weapon_type.add(student["WeaponType"])
        name = student["Name"]
        personal_name = student["PersonalName"]
        if name != personal_name:
            print(f"{name=} - {personal_name=}")
        school_year.add(student["SchoolYear"])
        age.add(student["CharacterAge"])
    print(
        f"{schools=}",
        f"{clubs=}",
        f"{squad_types=}",
        f"{tactic_role=}",
        f"{position=}",
        f"{bullet_type=}",
        f"{armor_type=}",
        f"{weapon_type=}",
        f"{school_year=}",
        f"{age=}",
        sep="\n",
    )
