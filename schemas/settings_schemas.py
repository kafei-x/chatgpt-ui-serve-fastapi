from pydantic import BaseModel, Field

class Settings(BaseModel):
    name: str = Field(max_length=50)
    value: bool = Field()