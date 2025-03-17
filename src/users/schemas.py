from typing import Optional

import phonenumbers
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, field_validator


class UserRead(schemas.BaseUser[int]):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


# class UserCreate(schemas.BaseUserCreate):
#     pass

class UserCreate(schemas.BaseUserCreate):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

    @field_validator("phone")
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                parsed_phone = phonenumbers.parse(v, None)
                if not phonenumbers.is_valid_number(parsed_phone):
                    raise ValueError("Invalid phone number")
                return phonenumbers.format_number(
                    parsed_phone, phonenumbers.PhoneNumberFormat.E164
                )
            except phonenumbers.phonenumberutil.NumberParseException:
                raise ValueError("Invalid phone number")
        return v

    @field_validator("email")
    def validate_email_or_phone(cls, v: Optional[str], values: dict) -> Optional[str]:
        if v is None and values.get("phone") is None:
            raise ValueError("Either email or phone must be provided")
        return v


class UserUpdate(schemas.BaseUserUpdate):
    pass
