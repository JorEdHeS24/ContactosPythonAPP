from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class baseContact(BaseModel):    
    name: str = Field(..., min_length=3)
    telephone: str = Field(..., min_length=7)
    email: Optional[EmailStr] = None




