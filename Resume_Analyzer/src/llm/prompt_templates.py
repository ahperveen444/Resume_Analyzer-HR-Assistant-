from langchain_core.prompts import PromptTemplate
from .output_parsers import json_parser, score_json_parser

candidate_extract_prompt = PromptTemplate(
    template="""You are a professional HR Assistant. You have to extract information from the following resumes:
    {text}.
    You have to extract the information from the resumes in the following format:
    {format}""",
    input_variables = ['text'],
    partial_variables = {'format' : json_parser.get_format_instructions()}
)

candidate_score_prompt = PromptTemplate(
    template = """
You are an HR Evaluation Model.
The job requirments are : {job_requirments}
All candidates are : {candidates}
Score each candidate from 1-100 for the job requirements.
Return the output in following format:
{format}
""",
input_variables=['job_requirments','candidates'],
partial_variables={'format':score_json_parser.get_format_instructions()}

)
