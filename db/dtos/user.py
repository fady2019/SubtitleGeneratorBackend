from typing import Optional

from db.dtos.dto import DTO


class UserDTO(DTO):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    id: Optional[str] = None


class UpdateUserDTO(DTO):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
