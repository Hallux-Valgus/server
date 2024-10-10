import os
from ..SessionManager import SessionManager
from model.Image import Image

class ImageService:
    static_path:str
    def __init__(self, static_path):
        self.static_path = static_path
    
    def create_image(self, code:str, filename:str):
        with SessionManager() as db:
            image_data = Image(user_code = code, image_path = os.path.join(self.static_path, "Img", filename))
            db.add(image_data)
            db.commit()
            db.refresh(image_data)
            db.close()
            
        return image_data