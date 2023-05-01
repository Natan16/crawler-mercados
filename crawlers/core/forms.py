from pydantic import BaseModel, Field
from typing import List, Optional

class MercadosProximosForm(BaseModel):
    latitude: float = Field(gte=-90, lte=90)
    longitude: float = Field(gte=-180, lte=180)
    raio_em_km: int = 10
    redes: Optional[List]
