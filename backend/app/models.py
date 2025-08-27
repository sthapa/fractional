import uuid

from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class Player(SQLModel, table=True):
  id: int = Field(index=True, primary_key=True)
  name: str = Field(index=False)
  position: str = Field(index=False, max_length=3)
  games: int = Field(index=False)
  at_bats: int = Field(index=False)
  runs: int = Field(index=False)
  hits: int = Field(index=False)
  doubles: int = Field(index=False)
  triples: int = Field(index=False)
  home_runs: int = Field(index=False)
  rbi: int = Field(index=False)
  walks: int = Field(index=False)
  strikeouts: int = Field(index=False)
  stolen_bases: int = Field(index=False)
  caught_stealing: int = Field(index=False)
  avg: float = Field(index=False)
  obp: float = Field(index=False)
  slugging: float = Field(index=False)
  ops: float = Field(index=False)
  desc: str | None = Field(index=False)


