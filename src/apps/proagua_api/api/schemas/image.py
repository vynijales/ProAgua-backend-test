from typing import Optional

from ninja import Schema

class ImageOut(Schema):
    file: str
    description: Optional[str]

class ImageIn(Schema):
    file: str
    description: Optional[str]

