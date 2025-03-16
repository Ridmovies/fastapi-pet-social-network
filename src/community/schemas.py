from pydantic import BaseModel

class CommunityBase(BaseModel):
    name: str
    description: str


class CommunityRead(CommunityBase):
    id: int
    creator_id: int
    members: list

class CommunityCreate(CommunityBase):
    pass


class CommunityUpdate(BaseModel):
    pass
