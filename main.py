from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Mensagem": "Bem-vindo à API do Hospital"}