from pydantic import BaseModel


class MovieCreate(BaseModel):
    title: str
    genre: str
    rating: float
    watched: bool
    

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    rating: float
    watched: bool

    class Config:
        from_attributes = True