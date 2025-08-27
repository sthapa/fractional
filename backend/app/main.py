import json, os, logging
import time
from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, create_engine, select
from models import Player


def get_session():
  with Session(engine) as session:
    yield session


SessionDep = Annotated[Session, Depends(get_session)]

time.sleep(5)

engine = None


def init_db():
  # db engine setup
  global engine
  pg_url = os.getenv("DATABASE_URL")
  connect_args = {}
  engine = create_engine(pg_url, connect_args=connect_args)


@asynccontextmanager
async def lifespan(app: FastAPI):
  # setup db
  init_db()
  if 'INITIALIZE_DB' in os.environ and os.environ['INITIALIZE_DB'].upper() == 'TRUE':
    print("Initializing DB")
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    print("Initialized")
    with open('data/players.json') as f:
      players = json.loads(f.read())
      session = Session(engine)
      id = 1
      for player in players:
        player['id'] = id
        id += 1
        session.add(Player(**player))
      session.commit()
    print("Loaded players")
  yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
  logging.error(f"{request}: {exc_str}")
  content = {'status_code': 10422, 'message': exc_str, 'data': None}
  return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/")
async def root():
  return {"message": "Hello World"}


@app.get("/players")
async def get_players(session: SessionDep) -> list[Player]:
  players = session.exec(select(Player)).all()
  if not players:
    raise HTTPException(status_code=404, detail="Player not found")
  return list(players)


@app.get("/player/{id}")
async def get_player(id: int, session: SessionDep) -> Player:
  player = session.exec(select(Player).where(Player.id == id)).first()
  if not player:
    raise HTTPException(status_code=404, detail="Player not found")
  return player


@app.post("/player/{id}")
async def update_player(id: int, player: Player, session: SessionDep) -> Player:
  db_player = session.exec(select(Player).where(Player.id == id)).first()
  print(id)
  print(db_player)
  if not db_player:
    raise HTTPException(status_code=404, detail="Player not found")
  player_data = player.model_dump(exclude_unset=True)
  db_player.sqlmodel_update(player_data)
  session.add(db_player)
  session.commit()
  session.refresh(db_player)
  return player

