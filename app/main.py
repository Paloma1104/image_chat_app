from fastapi import FastAPI
import os
app = FastAPI()

@app.get("/images")
def list_images():
    if not os.path.exists("uploads"):
        return []

    return os.listdir("uploads")
