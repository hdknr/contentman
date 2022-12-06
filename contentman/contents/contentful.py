import contentful
import contentful_management
from pydantic import BaseModel, Field


def create_management_client(token):
    return contentful_management.Client(token)


def crate_client(space_id, token):
    return contentful.Client(space_id, token)


def contenttype_list(management_client, space_id, environment_id):
    return management_client.content_types(space_id, environment_id).all()


class Management(BaseModel):
    token: str = Field(description="Mangement API Token")
    space_id: str = Field(description="Space ID")
    space_name: str = Field(description="Space Name")
    environment_id: str = Field(description="Environment ID")

    class Config:
        arbitrary_types_allowed = True

    @property
    def client(self):
        return create_management_client(self.token)

    @property
    def cotennttype_set(self):
        return contenttype_list(self.client, self.space_id, self.environment_id)
