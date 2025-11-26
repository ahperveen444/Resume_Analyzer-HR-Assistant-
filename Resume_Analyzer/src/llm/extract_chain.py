from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from langchain_core.output_parsers import JsonOutputParser
from .prompt_templates import candidate_extract_prompt

class Candidate(BaseModel):
    name : str = Field(description="Full Name of the candidate")
    email : str = Field(description="Email of the candidate")
    skills : list[str] = Field(description="List of all skills(Techinal,Soft or any mentioned) of the candidate")
    experience_years : str = Field(description="Total number of years or months of experience of the candidate. If not mentioned then return 0")
    last_position : str = Field(description="Most recent job title of candidate if no job title,internship found then return fresh candidate. For example no job title, internship found, if experience == 0 then it is a fresh candidate")
    projects : list[str] = Field(description="List of all the projects of the candidate")
    education : str = Field(description="Highest education of the candidate. For example if mentioned Bachelors(BS), Intermediate then Bahelors is the highest. Another example if candidate mentioned Masters(MS),Bachelors then Masters is the highest one. So you have to decide accordingly.")
    summary : str = Field(description="Brief summary of candidate's profile")

model = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
json_parser = JsonOutputParser(pydantic_object=Candidate)

candidate_extract_chain = candidate_extract_prompt | model | json_parser
