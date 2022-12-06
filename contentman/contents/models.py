import contentful
import contentful_management
from pydantic import BaseModel, Field


def create_management_client(token):
    return contentful_management.Client(token)


class Client(BaseModel):
    token: str = Field(description="API Token")
    space_id: str = Field(description="Space ID")
    space_name: str = Field(description="Space Name")
    environment_id: str = Field(description="Environment ID")
    class Config:
        arbitrary_types_allowed = True

    @property
    def client(self):
        return create_management_client(self.token)


class AbstractEntity(Client):
    @property
    def entity_objects(cls):
        raise NotImplementedError() 

    def list(self, **query):
        return self.entity_objects.all(query=query)
    

class ContentType(AbstractEntity):
    @property
    def entity_objects(self):
        return self.client.content_types(self.space_id, self.environment_id)


class Entry(AbstractEntity):
    @property
    def entity_objects(self):
        return self.client.entries(self.space_id, self.environment_id)
