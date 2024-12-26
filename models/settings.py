from pydantic import BaseModel, Field
from typing import Optional

class ScraperSettings(BaseModel):
    max_pages: Optional[int] = Field(default=5, ge=1)
    proxy: Optional[str] = None
