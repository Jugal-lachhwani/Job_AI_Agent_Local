from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import json

# 1. The Job Listing Table
class JobListing(SQLModel, table=True):
    id: str = Field(primary_key=True)  # The LinkedIn Job ID
    title: str
    company_name: str
    location: str
    apply_url: str
    description: str
    posted_date: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to analysis
    analysis: Optional["JobAnalysis"] = Relationship(back_populates="job")

# 2. The Analysis Table
class JobAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: str = Field(foreign_key="joblisting.id")
    
    summary: str
    required_skills_json: str = Field(default="[]")  # Store list as JSON string
    similarity_score: int
    feedback: str
    
    # Relationship back to job
    job: Optional[JobListing] = Relationship(back_populates="analysis")
    
    @property
    def skills(self) -> List[str]:
        return json.loads(self.required_skills_json)
    
    @skills.setter
    def skills(self, value: List[str]):
        self.required_skills_json = json.dumps(value)

# 3. Search History Table
class SearchHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_query: str
    resume_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)