from pydantic import BaseModel

class PasskeyBeginPayload(BaseModel):
    username: str