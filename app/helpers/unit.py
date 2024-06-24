import base64
from typing import Optional

from app.models.Tickets import Tickets


class Unit:
    def __init__(self, test_id: Optional[int] = None, name: Optional[str] = None, description: Optional[str] = None,
                 configuration: Optional[str] = None, img: Optional[bytes] = None, file: Optional[bytes] = None):
        self.id = test_id
        self.name = name
        self.description = description
        self.configuration = configuration
        self.img = Unit.encode_image_to_base64(img) if img else None
        self.file = file

    @staticmethod
    def encode_image_to_base64(image: Optional[bytes]) -> Optional[str]:
        return base64.b64encode(image).decode('utf-8') if image else None

    @staticmethod
    def get_unit(unit_id: int) -> Optional['Unit']:
        unit = Tickets.query.filter_by(id=unit_id).first()
        return Unit(test_id=unit.id, name=unit.name, description=unit.description,
                    configuration=unit.configuration, img=unit.img, file=unit.file) if unit else None
