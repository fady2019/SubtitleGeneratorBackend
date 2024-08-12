from dtos.dto import DTO


class UserDTO(DTO):
    first_name: str
    id: str
    last_name: str
    username: str
    email: str
