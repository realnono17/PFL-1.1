from .player_schema import PlayerOut
from .club_schema import ClubOut, ClubShort

# Pydantic v2+ forward ref fix: rebuild models after all schemas are imported
PlayerOut.model_rebuild()
ClubOut.model_rebuild()
