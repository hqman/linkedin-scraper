from pydantic import BaseModel, Field
from typing import Optional


class Profile(BaseModel):
    """LinkedIn company profile data model."""

    profile_name: str = Field(..., description="Name of the profile")
    profile_description: Optional[str] = Field(
        None, description="Profile description or tagline"
    )
    about: Optional[str] = Field(
        None, description="About section text from the profile"
    )
    profile_website: Optional[str] = Field(
        None, description="URL of the profile website"
    )
    industry: Optional[str] = Field(
        None, description="Industry the profile operates in"
    )
    location: Optional[str] = Field(None, description="Profile headquarters location")

    confidence: Optional[float] = Field(
        None, description="Confidence score from 0.1 to 1.0"
    )
