from pydantic import BaseModel, Field

class AdvisoryReport(BaseModel):
    season: str = Field(description="The matching season for the crop advisory (e.g., Kharif, Rabi)")
    recommended_crop: str = Field(description="Primary crop recommendation based on specific soil and region")
    second_option_crop: str = Field(description="A secondary backup crop recommendation")
    avoid_crop: str = Field(description="A crop to strictly avoid planting for this soil and season")
    expected_profit_min: int = Field(description="Expected minimum yield profit per acre in INR")
    expected_profit_max: int = Field(description="Expected maximum yield profit per acre in INR")
    confidence_score: float = Field(default=0.7, ge=0.0, le=1.0, description="Confidence of the model recommendation")
    final_advisory: str = Field(description="A 3 paragraph structured justification. MUST be fully translated into the requested language.")
