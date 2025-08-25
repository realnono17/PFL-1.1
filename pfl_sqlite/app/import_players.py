import os
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.player import Player
from app.models.club import Club
from app.utils.player_mapping import map_position, map_boolean
from app.country_multiplier import country_multiplier

# 🧠 Compute tier-scaled market value
def compute_player_value(ovr: int, country_multiplier_val: float = 1.0) -> float:
    if ovr < 50:
        return 0
    elif 50 <= ovr <= 59:
        base = 100_000 + ((ovr - 50) / 9) * (500_000 - 100_000)
    elif 60 <= ovr <= 69:
        base = 600_000 + ((ovr - 60) / 9) * (5_000_000 - 600_000)
    elif 70 <= ovr <= 79:
        base = 5_000_000 + ((ovr - 70) / 9) * (20_000_000 - 5_000_000)
    elif 80 <= ovr <= 89:
        base = 20_000_000 + ((ovr - 80) / 9) * (80_000_000 - 20_000_000)
    elif 90 <= ovr <= 95:
        base = 80_000_000 + ((ovr - 90) / 5) * (135_000_000 - 80_000_000)
    else:
        base = 135_000_000
    return round(base * country_multiplier_val)
# Add this just below compute_player_value()
def compute_wage(market_value: float) -> int:
    return round(market_value * 0.10)  # ~0.04% of value per matchday


def get_or_create_club(db: Session, club_name: str):
    club = db.query(Club).filter(Club.name == club_name).first()
    if not club:
        club = Club(name=club_name)
        db.add(club)
        db.commit()
        db.refresh(club)
    return club

def clean_row(row):
    return {k: (v if pd.notna(v) else None) for k, v in row.items()}

def import_players(file_path: str):
    db = SessionLocal()
    filename = os.path.basename(file_path).replace(".csv", "").strip()
    club_name = filename

    df = pd.read_csv(file_path, sep=";", dtype=str, encoding="utf-8-sig")
    df = df.dropna(how="all").dropna(axis=1, how="all")
    df.columns = df.columns.str.strip().str.lower()

    is_single_player = len(df) == 1
    club = None if is_single_player else get_or_create_club(db, club_name)

    column_mapping = {
        "overallstats": "overall_stats",
        "offensiveawareness": "offensive_awareness",
        "ballcontrol": "ball_control",
        "tightpossession": "tight_possession",
        "lowpass": "low_pass",
        "loftedpass": "lofted_pass",
        "finishing": "finishing",
        "heading": "heading",
        "placekicking": "place_kicking",
        "curl": "curl",
        "speed": "speed",
        "acceleration": "acceleration",
        "kickingpower": "kicking_power",
        "jump": "jump",
        "physicalcontact": "physical_contact",
        "balance": "balance",
        "stamina": "stamina",
        "defensiveawareness": "defensive_awareness",
        "ballwinning": "ball_winning",
        "aggression": "aggression",
        "gkawareness": "gk_awareness",
        "gkcatching": "gk_catching",
        "gkclearing": "gk_clearing",
        "gkreflexes": "gk_reflexes",
        "gkreach": "gk_reach",
        "weakfootusage": "weak_foot_usage",
        "weakfootacc": "weak_foot_accuracy",
        "form": "form",
        "injuryresistance": "injury_resistance",
    }
    df.rename(columns=column_mapping, inplace=True)

    for _, row in df.iterrows():
        row = clean_row(row)
        player_data = {
            "pes_id": int(row.get("id") or 0),
            "name": row.get("name"),
            "country": row.get("country"),
            "height": row.get("height"),
            "weight": row.get("weight"),
            "age": row.get("age"),
            "foot": "Left" if str(row.get("foot", "")).strip().lower() == "left" else "Right",
            "overall_stats": int(row.get("overall_stats") or 0),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "club_id": None if is_single_player else club.id,
        }

        for pos in ["gk", "cb", "lb", "rb", "dmf", "cmf", "lmf", "rmf", "amf", "lwf", "rwf", "ss", "cf"]:
            player_data[pos] = map_position(row.get(pos))

        for stat in [
            "offensive_awareness", "ball_control", "dribbling", "tight_possession", "low_pass", "lofted_pass",
            "finishing", "heading", "place_kicking", "curl", "speed", "acceleration", "kicking_power", "jump",
            "physical_contact", "balance", "stamina", "defensive_awareness", "ball_winning", "aggression",
            "gk_awareness", "gk_catching", "gk_clearing", "gk_reflexes", "gk_reach",
            "weak_foot_usage", "weak_foot_accuracy", "form", "injury_resistance"
        ]:
            player_data[stat] = int(row.get(stat) or 0)

        for skill in [
            "trickster", "mazing_run", "speeding_bullet", "incisive_run", "long_ball_expert", "early_cross",
            "long_ranger", "scissors_feint", "double_touch", "flip_flap", "marseille_turn", "sombrero",
            "cross_over_turn", "cut_behind_and_turn", "scotch_move", "step_on_skillcontrol", "heading_special",
            "long_range_drive", "chipshot_control", "long_range_shot", "knuckle_shot", "dipping_shots",
            "rising_shots", "acrobatic_finishing", "heel_trick", "first_time_shot", "one_touch_pass",
            "through_passing", "weighted_pass", "pinpoint_crossing", "outside_curler", "rabona", "no_look_pass",
            "low_lofted_pass", "gk_low_punt", "gk_high_punt", "long_throw", "gk_long_throw", "penalty_specialist",
            "gk_penalty_saver", "gamesmanship", "man_marking", "track_back", "interception", "acrobatic_clear",
            "captaincy", "super_sub", "fighting_spirit"
        ]:
            player_data[skill] = map_boolean(row.get(skill))

        try:
            code = int(player_data.get("country") or 0)
        except ValueError:
            code = 0
        multiplier = country_multiplier.get(code, country_multiplier.get("default", 1.0))
        ovr = player_data["overall_stats"]
        player_data["market_value"] = compute_player_value(ovr, multiplier)
        player_data["wage"] = compute_wage(player_data["market_value"])


        player = db.query(Player).filter(Player.name == player_data["name"], Player.pes_id == player_data["pes_id"]).first()
        if player:
            for k, v in player_data.items():
                setattr(player, k, v)
            print(f"🔄 Updated: {player.name}")
        else:
            new_player = Player(**player_data)
            db.add(new_player)
            print(f"✅ Added: {new_player.name}")

        db.commit()
    db.close()

if __name__ == "__main__":
    csv_file = input("Enter path to CSV file: ").strip()
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
    else:
        import_players(csv_file)
