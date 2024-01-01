from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        from_attributes: True


class Token(BaseModel):
    access_token: str
    token_type: str
