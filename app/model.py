import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
import os
import cv2


class FlowerSearchEngine:
    def __init__(self):
        # Загрузка обученной модели
        self.model = load_model("flower_classifier.h5")

        # Создаём feature extractor (берём слой перед последним)
        self.feature_extractor = tf.keras.Model(
            inputs=self.model.inputs,
            outputs=self.model.layers[-2].output
        )

        # Загружаем тестовую выборку (имитация библиотеки)
        self.test_image_paths = []
        self.test_embeddings = []
        self.load_test_images()

    def load_test_images(self):
        """Загружает тестовые изображения и их эмбеддинги."""
        test_dir = "app/test_images"

        for root, _, files in os.walk(test_dir):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(root, file)
                    img = cv2.imread(img_path)
                    img = cv2.resize(img, (150, 150))
                    img = img / 255.0
                    img = np.expand_dims(img, axis=0)

                    embedding = self.feature_extractor.predict(img)
                    self.test_embeddings.append(embedding.flatten())
                    self.test_image_paths.append(img_path)

        self.test_embeddings = np.array(self.test_embeddings)

    def find_similar(self, query_image_path, top_k=5):
        """Находит топ-5 похожих изображений."""
        query_img = cv2.imread(query_image_path)
        query_img = cv2.resize(query_img, (150, 150))
        query_img = query_img / 255.0
        query_img = np.expand_dims(query_img, axis=0)

        query_embedding = self.feature_extractor.predict(query_img).flatten()

        similarities = cosine_similarity(
            [query_embedding],
            self.test_embeddings
        )[0]

        top_indices = np.argsort(similarities)[::-1][:top_k]

        return {
            self.test_image_paths[i]: float(similarities[i])
            for i in top_indices
        }