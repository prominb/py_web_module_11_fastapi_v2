from fastapi import FastAPI

app = FastAPI()


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}


# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}