from pydantic import BaseModel, Field


class X509AttrsPM(BaseModel):
    C: str = Field(default="US", min_length=2, max_length=2)
    ST: str = Field(default="Washington", min_length=2, max_length=256)
    L: str = Field(default="Seattle", min_length=2, max_length=256)
    O: str = Field(default="Organization", min_length=2, max_length=256)
    OU: str = Field(default="Organization Unit", min_length=2, max_length=256)
    CN: str = Field(default="localhost", min_length=2, max_length=256)
    DNS: str = Field(default="localhost", min_length=2, max_length=256)


__all__ = [
    "X509AttrsPM",
]
