from pydantic import BaseModel, Field
from typing import Optional


class Company(BaseModel):
    """LinkedIn company profile data model."""

    company_name: str = Field(..., description="Name of the company")
    company_description: Optional[str] = Field(
        None, description="Company description or tagline"
    )
    company_website: Optional[str] = Field(
        None, description="URL of the company website"
    )
    industry: Optional[str] = Field(
        None, description="Industry the company operates in"
    )
    location: Optional[str] = Field(None, description="Company headquarters location")
    followers: Optional[str] = Field(None, description="Number of LinkedIn followers")
    employees: Optional[str] = Field(None, description="Company size range")
    # logo_url: Optional[str] = Field(None, description="URL to company logo image")
    # cover_image_url: Optional[str] = Field(
    #     None, description="URL to company cover image"
    # )
    confidence: Optional[float] = Field(
        None, description="Confidence score from 0.1 to 1.0"
    )
