import requests
import os
import io
from models.plate_reader import PlateReader


class PlateReaderWeb:
    def __init__(self, url=None):
        self.url = url or os.getenv("PLATE_READER_URL")
        if not self.url:
            raise ValueError("URL for PlateReader should be specified upon init")
        self.plate_reader = PlateReader.load_from_file(
            "./model_weights/plate_reader_model.pth"
        )

    def predict(self, image_name: str) -> str:
        res = requests.get(self.url + image_name)
        if res.status_code // 100 == 2:
            return self.plate_reader.read_text(io.BytesIO(res.content))
        else:
            return {"error": res.status_code}

    def predict_batch(self, image_names: list[str]) -> list[str]:
        return [self.predict(image_name) for image_name in image_names]
  
