from pydantic import BaseModel
from typing import List

class Ingredient(BaseModel):
    nome: str
    quantita: str
    in_scadenza: bool = False

class UserProfile(BaseModel):
    vincoli_salute: List[str] = []
