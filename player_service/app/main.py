from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from model.player import Player
import uvicorn
import os
from database import database as database
from sqlalchemy.orm import Session

app = FastAPI()

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def player_health():
    return {'message': 'service is active'}


@app.get("/get_players")
async def get_players(db: db_dependency):
    result = db.query(database.Player).offset(0).limit(100).all()
    return result


@app.get("/get_player_by_id")
async def get_player_by_id(player_id: int, db: db_dependency):
    result = db.query(database.Player).filter(database.Player.id == player_id).first()
    print(player_id)
    print(result)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'player with such id is not found. user_id: {player_id}'
        )
    return result


@app.get("/get_player_by_nickname")
async def get_player_by_nickname(player_nickname: str, db: db_dependency):
    result = db.query(database.Player).filter(database.Player.nickname == player_nickname).first()
    print(player_nickname)
    print(result)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'player with such nickname is not found. user_id: {player_nickname}'
        )
    return result


@app.post('/add_player')
async def add_player(player: Player, db: db_dependency):
    db_player = database.Player(
        id=player.id,
        name=player.name,
        age=player.age,
        nickname=player.nickname,
        discipline=player.discipline,
        team=player.team
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


@app.delete("/delete_player")
async def delete_player(player_id: int, db: db_dependency):
    try:
        player_db = db.query(database.Player).filter(database.Player.id == player_id).first()
        db.delete(player_db)
        db.commit()
        return "Success"
    except Exception:
        return "cant find player"


@app.post("/switch_discipline")
async def switch_discipline(player_id: int, new_discipline: str, db: db_dependency):
    try:
        player_db = db.query(database.Player).filter(database.Player.id == player_id).first()
        player_db.discipline = new_discipline
        db.commit()
        return player_db
    except Exception:
        return "cant find player"


@app.post("/switch_team")
async def switch_team(player_id: int, new_team: str, db: db_dependency):
    try:
        player_db = db.query(database.Player).filter(database.Player.id == player_id).first()
        player_db.team = new_team
        db.commit()
        return player_db
    except Exception:
        return "cant find player"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))

