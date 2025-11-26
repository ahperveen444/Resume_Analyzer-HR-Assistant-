from pydantic import BaseModel,Field
from typing import List

class Candidate(BaseModel):
    name : str = Field(description="Full Name of the candidate")
    email : str = Field(description="Email of the candidate")
    skills : list[str] = Field(description="List of all skills(Techinal,Soft or any mentioned) of the candidate")
    experience_years : str = Field(description="Total number of years or months of experience of the candidate. If not mentioned then return 0")
    last_position : str = Field(description="Most recent job title of candidate if no job title,internship found then return fresh candidate. For example no job title, internship found, if experience == 0 then it is a fresh candidate")
    projects : list[str] = Field(description="List of all the projects of the candidate")
    education : str = Field(description="Highest education of the candidate. For example if mentioned Bachelors(BS), Intermediate then Bahelors is the highest. Another example if candidate mentioned Masters(MS),Bachelors then Masters is the highest one. So you have to decide accordingly.")
    summary : str = Field(description="Brief summary of candidate's profile")

class Score(BaseModel):
    name:str = Field(description="Name of the candidate")
    email:str = Field(description="Email of the candidate")
    skill_match:str = Field(description="Skills match from the job requirments. For example job requirments include skills like tech skills: wordpress developer, or any soft skills:(Problem Solving, Adaptability, Creativity, Team Work, etc) and if these skills match candidate skills then it will be skills match")
    experience_match:str = Field(description="Previous experiece of candidate of the job from job his experience. If no experience then return no experience.")
    project_relevance:str = Field(description="Judge candidate's project and tell if his project has any relevance with job. If yes then what and which project. If no poject has any relevance then return no project relevance.")
    overall_score:int = Field(description="You have to give an overall score to candidate based on it's skill match, experience match, project relevance and overall candidate profile.")
    reason:str = Field(description="Reason of why you gave the overall score to candidate.")
