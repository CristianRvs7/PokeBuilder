import httpx

from src.database.db_config import SessionLocal
from src.models.db_schema import Moves


MOVE_LIST_URL = "https://pokeapi.co/api/v2/move?limit=2000"


def get_description(move_data):
    for entry in move_data["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            return entry["flavor_text"].replace("\n", " ").replace("\f", " ")

    return "No description available"


def seed_moves():
    db = SessionLocal()

    try:
        response = httpx.get(
            MOVE_LIST_URL,
            timeout=30
        )

        response.raise_for_status()

        moves_list = response.json()["results"]

        print(f"Moves found: {len(moves_list)}")

        for index, move_info in enumerate(moves_list, start=1):

            try:
                response = httpx.get(
                    move_info["url"],
                    timeout=30
                )

                response.raise_for_status()

                move_data = response.json()

                existing_move = (
                    db.query(Moves)
                    .filter(
                        Moves.pokeapi_id == move_data["id"]
                    )
                    .first()
                )

                if existing_move:
                    print(
                        f"[{index}/{len(moves_list)}] "
                        f"{move_data['name']} already exists"
                    )
                    continue

                move = Moves(
                    pokeapi_id=move_data["id"],
                    name=move_data["name"],
                    power=move_data["power"],
                    accuracy=move_data["accuracy"],
                    pp=move_data["pp"],
                    damage_class=move_data["damage_class"]["name"],
                    type=move_data["type"]["name"],
                    description=get_description(move_data)
                )

                db.add(move)
                db.commit()

                print(
                    f"[{index}/{len(moves_list)}] "
                    f"{move_data['name']} added"
                )

            except Exception as error:
                db.rollback()

                print(
                    f"Error loading {move_info['name']}: {error}"
                )

    finally:
        db.close()


if __name__ == "__main__":
    seed_moves()