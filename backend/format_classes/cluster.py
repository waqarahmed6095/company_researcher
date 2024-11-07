from pydantic import BaseModel, Field
from typing import List

# Define the simplified structure for clustering output
class DocumentCluster(BaseModel):
    company_name: str = Field(
        ...,
        description="The name or identifier of the company these documents belong to."
    )
    cluster: List[str] = Field(
        ...,
        description="A list of URLs relevant to the identified company."
    )

class DocumentClusters(BaseModel):
    clusters: List[DocumentCluster] = Field(
        ..., 
        description="List of document clusters categorized by company, each containing a list of URLs."
    )
