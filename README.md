# Flowers

Этот проект предоставляет REST API для поиска похожих изображений цветов на основе входного изображения. Система использует свою обученную модель CNN для извлечения признаков и косинусное сходство для поиска в библиотеке изображений.

## Установка

```bash
git clone https://github.com/luckyboyroman/flowers1.git
cd flowers1
```
##№ Взять файлы с весами обучения flower_classifier.h5 и папку Flowers (изображения) с яндекс диска https://disk.yandex.ru/d/q_4yCsml4W-_jQ
## Локальная установка

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Проверка работоспособности
```bash
curl http://localhost:8000/ping
```
## Пример ответа:
```bash
{
  "images/rose1.jpg": 0.98,
  "images/rose2.jpg": 0.97,
  "images/daisy1.jpg": 0.45,
  "images/sunflower1.jpg": 0.40,
  "images/tulip1.jpg": 0.35
}
```
