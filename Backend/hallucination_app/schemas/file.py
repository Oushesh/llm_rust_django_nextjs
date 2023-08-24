from typing import Optional
from typing import List
from ninja import Schema


class InputFileIN(Schema):
    path: str
    type: str
