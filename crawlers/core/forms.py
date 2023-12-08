from typing import List, Optional

from pydantic import BaseModel, Field


class MercadosProximosForm(BaseModel):
    latitude: float = Field(gte=-90, lte=90)
    longitude: float = Field(gte=-180, lte=180)
    raio: int = 10
    redes: Optional[List]
