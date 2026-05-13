from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING, Dict
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.club_schema import ClubShort


class PlayerBase(BaseModel):
    name: str
    country: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    age: Optional[int] = None
    foot: Optional[str] = None
    market_value: Optional[float] = None
    wage: Optional[float] = None

    # Core attributes
    overall_stats: Optional[int] = None
    offensive_awareness: Optional[int] = None
    ball_control: Optional[int] = None
    dribbling: Optional[int] = None
    tight_possession: Optional[int] = None
    low_pass: Optional[int] = None
    lofted_pass: Optional[int] = None
    finishing: Optional[int] = None
    heading: Optional[int] = None
    place_kicking: Optional[int] = None
    curl: Optional[int] = None
    speed: Optional[int] = None
    acceleration: Optional[int] = None
    kicking_power: Optional[int] = None
    jump: Optional[int] = None
    physical_contact: Optional[int] = None
    balance: Optional[int] = None
    stamina: Optional[int] = None
    defensive_awareness: Optional[int] = None
    ball_winning: Optional[int] = None
    aggression: Optional[int] = None

    # Weak foot & form
    weak_foot_usage: Optional[int] = None
    weak_foot_accuracy: Optional[int] = None
    form: Optional[int] = None
    injury_resistance: Optional[int] = None

    # Playing positions
    gk: Optional[str] = None
    cb: Optional[str] = None
    lb: Optional[str] = None
    rb: Optional[str] = None
    dmf: Optional[str] = None
    cmf: Optional[str] = None
    lmf: Optional[str] = None
    rmf: Optional[str] = None
    amf: Optional[str] = None
    lwf: Optional[str] = None
    rwf: Optional[str] = None
    ss: Optional[str] = None
    cf: Optional[str] = None

    # Skills
    trickster: Optional[bool] = None
    mazing_run: Optional[bool] = None
    speeding_bullet: Optional[bool] = None
    incisive_run: Optional[bool] = None
    long_ball_expert: Optional[bool] = None
    early_cross: Optional[bool] = None
    long_ranger: Optional[bool] = None
    scissors_feint: Optional[bool] = None
    double_touch: Optional[bool] = None
    flip_flap: Optional[bool] = None
    marseille_turn: Optional[bool] = None
    sombrero: Optional[bool] = None
    cross_over_turn: Optional[bool] = None
    cut_behind_and_turn: Optional[bool] = None
    scotch_move: Optional[bool] = None
    step_on_skillcontrol: Optional[bool] = None
    heading_special: Optional[bool] = None
    long_range_drive: Optional[bool] = None
    chipshot_control: Optional[bool] = None
    long_range_shot: Optional[bool] = None
    knuckle_shot: Optional[bool] = None
    dipping_shots: Optional[bool] = None
    rising_shots: Optional[bool] = None
    acrobatic_finishing: Optional[bool] = None
    heel_trick: Optional[bool] = None
    first_time_shot: Optional[bool] = None
    one_touch_pass: Optional[bool] = None
    through_passing: Optional[bool] = None
    weighted_pass: Optional[bool] = None
    pinpoint_crossing: Optional[bool] = None
    outside_curler: Optional[bool] = None
    rabona: Optional[bool] = None
    no_look_pass: Optional[bool] = None
    low_lofted_pass: Optional[bool] = None
    gk_low_punt: Optional[bool] = None
    gk_high_punt: Optional[bool] = None
    long_throw: Optional[bool] = None
    gk_long_throw: Optional[bool] = None
    penalty_specialist: Optional[bool] = None
    gk_penalty_saver: Optional[bool] = None
    gamesmanship: Optional[bool] = None
    man_marking: Optional[bool] = None
    track_back: Optional[bool] = None
    interception: Optional[bool] = None
    acrobatic_clear: Optional[bool] = None
    captaincy: Optional[bool] = None
    super_sub: Optional[bool] = None
    fighting_spirit: Optional[bool] = None


class PlayerCreate(PlayerBase):
    club_id: Optional[int] = None


class PlayerUpdate(PlayerBase):
    pass


class PlayerOut(PlayerBase):
    id: int
    club_id: Optional[int]
    club: Optional["ClubShort"] = None
    created_at: datetime
    updated_at: datetime
    positions: Optional[Dict] = None

    class Config:
        from_attributes = True
