from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from model import FlowerSearchEngine
import os

app = FastAPI()
search_engine = FlowerSearchEngine()


# Эндпоинт для поиска похожих изображений
@app.post("/search")
async def search_similar_images(file: UploadFile = File(...)):
    try:
        # Сохраняем загруженное изображение временно
        temp_path = "temp_image.jpg"
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # Ищем похожие изображения
        result = search_engine.find_similar(temp_path)

        # Удаляем временный файл
        os.remove(temp_path)

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


# Проверка работоспособности
@app.get("/ping")
async def ping():
    return {"status": "ok"}