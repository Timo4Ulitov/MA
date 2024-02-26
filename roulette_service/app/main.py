from fastapi import FastAPI, HTTPException, status
import uvicorn
import os
import random

app = FastAPI()


balance = 0


@app.get("/health", status_code=status.HTTP_200_OK)
async def roulette_health():
    return {'message': 'service is active'}


@app.get("/deposit")
async def deposit(amount: int):
    global balance
    balance += amount
    return f"Your current balance is {balance}"


@app.post("/roll")
async def roll(amount: int, point: str):
    global balance
    if amount > balance:
        raise HTTPException(
            status_code=404,
            detail=f'You dont have enough money, ur current balance: {balance}'
        )
    if point != "red" and point != "black" and point != "green":
        raise HTTPException(
            status_code=404,
            detail=f'u cant choose this point'
        )
    result = random.random(0, 36)
    if result == 0 and point == "green":
        balance += (amount * 10)
    elif (result % 2 == 0 and point == "black") or (result % 2 == 1 and point == "red"):
        balance += amount
    else:
        balance -= amount
        print("Ha-ha, loser")
    return result

@app.post("/cash_up")
async def cash_up():
    global balance
    balance = 0
    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))

