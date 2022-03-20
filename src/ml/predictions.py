import io
from PIL import Image
import requests
from src.cache import redis_client
import time

class ImageClassifier:
    PREDICT_URL = "http://host.docker.internal:8080/predictions/resnet101"

    @classmethod
    def image_to_byte_array(cls, image: Image, image_format: str = "JPEG"):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format=image_format)
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr

    @classmethod
    def predict(cls, img_data: bytes, img_format: str = None, use_cache: bool = True):
        resized_img = img_data.resize((224, 224))
        img_format = img_data.format if img_format is None else img_format
        img_bytes = cls.image_to_byte_array(resized_img, img_format)

        if use_cache:
            cache_data = redis_client.get_data_redis(key=str(img_bytes))
            if cache_data is not None:
                return cache_data
        res = requests.post(cls.PREDICT_URL, data=img_bytes)
        time.sleep(5)
        output = res.json()
        if res.status_code != 200:
            return output
        if use_cache:
            redis_client.save_data_job(key=str(img_bytes), value=output)
        return output
