from pydantic import Field

from common.models.base import ImmutableBaseModel


class KarenSecrets(ImmutableBaseModel):
    host: str
    port: int = Field(gt=0, le=65535)
    auth: str
