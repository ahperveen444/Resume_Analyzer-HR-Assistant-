from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from langchain_core.output_parsers import JsonOutputParser
from .output_parsers import score_json_parser
from .prompt_templates import candidate_score_prompt


class Score(BaseModel):
    name:str = Field(description="Name of the candidate")
    email:str = Field(description="Email of the candidate")
    skill_match:str = Field(description="Skills match from the job requirments. For example job requirments include skills like tech skills: wordpress developer, or any soft skills:(Problem Solving, Adaptability, Creativity, Team Work, etc) and if these skills match candidate skills then it will be skills match")
    experience_match:str = Field(description="Previous experiece of candidate of the job from job his experience. If no experience then return no experience.")
    project_relevance:str = Field(description="Judge candidate's project and tell if his project has any relevance with job. If yes then what and which project. If no poject has any relevance then return no project relevance.")
    overall_score:int = Field(description="You have to give an overall score to candidate based on it's skill match, experience match, project relevance and overall candidate profile.")
    reason:str = Field(description="Reason of why you gave the overall score to candidate.")

model = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
score_json_parser = JsonOutputParser(pydantic_object=Score)

candidate_score_chain = candidate_score_prompt | model | score_json_parser
