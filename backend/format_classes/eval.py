from pydantic import BaseModel, Field
from typing import Optional, List

# Define the ReportEvaluation structure
class ReportEvaluation(BaseModel):
    grade: int = Field(
        ..., 
        description="Overall grade of the report on a scale from 1 to 3 (1 = needs improvement, 3 = complete and thorough)."
    )
    critical_gaps: Optional[List[str]] = Field(
        None, 
        description="List of critical gaps to address if the grade is 1."
    ) 
