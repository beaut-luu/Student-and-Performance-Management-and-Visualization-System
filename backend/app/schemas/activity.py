from pydantic import BaseModel, Field


class ActivityIn(BaseModel):
    org_id: int = Field(..., description="发布方")
