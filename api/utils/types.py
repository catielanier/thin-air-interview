from typing import TypedDict, List

class Shirt(TypedDict):
    id: int
    description: str
    price: int

ShirtList = List[Shirt]