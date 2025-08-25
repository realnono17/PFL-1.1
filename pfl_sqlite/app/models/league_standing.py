from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.club import Club
from app.models.competition import Competition

class LeagueStanding(Base):
    __tablename__ = "league_standings"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)

    played = Column(Integer, default=0)
    won = Column(Integer, default=0)
    drawn = Column(Integer, default=0)
    lost = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    goal_difference = Column(Integer, default=0)
    points = Column(Integer, default=0)

    club = relationship("Club", backref="league_standings")
    competition = relationship("Competition", backref="standings")

    @property
    def club_name(self):
        return self.club.name if self.club else None
