import os
import glob
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from pydantic import BaseModel,Field
from langchain_core.output_parsers import JsonOutputParser
from supabase import create_client
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import(
    build_resource_service,
    get_gmail_credentials,
)
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_API_KEY"))
# loader = DirectoryLoader(
#     path='Resumes',
#     glob='*.pdf',
#     loader_cls=PyPDFLoader
# )


# print(text)
# print(len(docs))

# Setting Gmail Credentials
credentials_gmail = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials2.json",
)
api_resource_gmail = build_resource_service(credentials=credentials_gmail)

toolkit_gmail = GmailToolkit(api_resource=api_resource_gmail)
tools_gmail = toolkit_gmail.get_tools()



model = ChatOpenAI(model = "gpt-4o-mini")

class Candidate(BaseModel):
    name : str = Field(description="Full Name of the candidate")
    email : str = Field(description="Email of the candidate")
    skills : list[str] = Field(description="List of all skills(Techinal,Soft or any mentioned) of the candidate")
    experience_years : str = Field(description="Total number of years or months of experience of the candidate. If not mentioned then return 0")
    last_position : str = Field(description="Most recent job title of candidate if no job title,internship found then return fresh candidate. For example no job title, internship found, if experience == 0 then it is a fresh candidate")
    projects : list[str] = Field(description="List of all the projects of the candidate")
    education : str = Field(description="Highest education of the candidate. For example if mentioned Bachelors(BS), Intermediate then Bahelors is the highest. Another example if candidate mentioned Masters(MS),Bachelors then Masters is the highest one. So you have to decide accordingly.")
    summary : str = Field(description="Brief summary of candidate's profile")

json_parser = JsonOutputParser(pydantic_object=Candidate)

prompt = PromptTemplate(
    template="""You are a professional HR Assistant. You have to extract information from the following resumes:
    {text}.
    You have to extract the information from the resumes in the following format:
    {format}""",
    input_variables = ['text'],
    partial_variables = {'format' : json_parser.get_format_instructions()}
)

chain = prompt | model | json_parser

resumes = glob.glob("Resumes/*.pdf")

candidates = []

for filepath in resumes:
    loader = PyPDFLoader(filepath)
    docs = loader.load()
    text = "\n".join(d.page_content for d in docs)
    result = chain.invoke({'text':text})
    # print(result)
    # data = supabase.table("candidates").insert(result).execute()
    # candidates.append(data)
    candidates.append(result)
    print("Candidate Data inserted in Database")

class Score(BaseModel):
    name:str = Field(description="Name of the candidate")
    email:str = Field(description="Email of the candidate")
    skill_match:str = Field(description="Skills match from the job requirments. For example job requirments include skills like tech skills: wordpress developer, or any soft skills:(Problem Solving, Adaptability, Creativity, Team Work, etc) and if these skills match candidate skills then it will be skills match")
    experience_match:str = Field(description="Previous experiece of candidate of the job from job his experience. If no experience then return no experience.")
    project_relevance:str = Field(description="Judge candidate's project and tell if his project has any relevance with job. If yes then what and which project. If no poject has any relevance then return no project relevance.")
    overall_score:int = Field(description="You have to give an overall score to candidate based on it's skill match, experience match, project relevance and overall candidate profile.")
    reason:str = Field(description="Reason of why you gave the overall score to candidate.")

# class ScoreList(BaseModel):
#     result : Score[list] = Field(description="You have to give each candidate result as mentioned in Score as a list.")

score_json_parser = JsonOutputParser(pydantic_object=Score)

# job_requirments = input("Enter Job Requirments: ")
job_requirments = ("""
About the Role

We are seeking a highly skilled AI Automations Engineer with deep expertise in low-code/no-code automation platforms, including n8n, relay.app, and similar workflow tools. The ideal candidate is a systems thinker who can design, optimize, and maintain scalable automation workflows that power AI-driven operations across the business.
This role requires excellent English communication, a strong sense of ownership, and the ability to collaborate and problem-solve in a fast-paced environment. Candidates must be available to work during North American business hours.
                   
Key Responsibilities:

Design, build, and maintain automation workflows using n8n, relay.app, Zapier, and other low/no-code platforms.
Integrate LLMs, APIs, datasets, and third-party tools into robust, reliable automation systems.
Translate business needs into end-to-end automation architectures with clear logic, system maps, and documentation.
Develop and optimize AI-powered workflows, including prompt engineering, data routing, memory management, and agent-style logic.
Troubleshoot, refine, and scale existing automation processes for performance, reliability, and cost efficiency.
Work closely with engineering, product, and operations teams to deliver automation solutions aligned with business outcomes.
Write clean scripts in Python when custom logic or integrations are needed.
Apply machine learning fundamentals to improve automation reasoning, model selection, and data handling.
Maintain security, privacy, and compliance best practices across all automation environments.

Required Skills & Qualifications:
                   
Expert-level proficiency in n8n and relay.app (must have hands-on experience building complex workflows).
Strong experience with low-code/no-code automation ecosystems and API integrations.
Fluent English—written and spoken—with the ability to communicate technical concepts clearly.
Systems thinking: ability to design holistic automation architectures that scale.
Experience with Python, including building small scripts and API-based integrations.
Understanding of machine learning concepts (model types, vector databases, retrieval, embeddings, etc.).
Strong debugging and problem-solving skills.
Ability to work independently and manage multiple automation projects simultaneously.
Availability to work full-time or part-time during North American hours.""")

prompt_score = PromptTemplate(
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

candidates_str = "\n\n".join([str(c) for c in candidates])

chain_score = prompt_score | model | score_json_parser

final_results = []
for c in candidates:
    result_score = chain_score.invoke({'job_requirments' : job_requirments,'candidates' : str(c)})
    # data = supabase.table("candidates_score").insert(result_score).execute()
    final_results.append(result_score)
    print("Candidates Scores Data Inserted")

# print(final_results)

   

best_candidate = sorted(final_results, key=lambda x: x['overall_score'], reverse=True)
# print(f"The top candidate for this job is : ",best_candidate)

email_best_candidate = best_candidate[0]['email']
overall_score_best_candidate = best_candidate[0]['overall_score']
print(f"Email : {email_best_candidate}\nOverall Score : {overall_score_best_candidate}")


prompt_gmail = PromptTemplate(
    template="""You are a professional email assistant. Your task is to write a professional, well formatted email to candidate for the interview as he is shortlisted for the job he has applied. You have to do which user will tell you to do. Here is what user says:
    {query}   
""",
input_variables=['query']
)

# tool binding
llm_with_tool = model.bind_tools(tools_gmail)
query = f"Draft an email to {email_best_candidate} for interview as he is shortlisted for the job applied."

#chain
chain = prompt_gmail | llm_with_tool

response = chain.invoke(query)

# print(response)

# list of tools into name
tool_map = {t.name: t for t in tools_gmail}

# tool calls
if response.tool_calls:
    for call in response.tool_calls:
        tool_name = call["name"]
        tool_args = call["args"]

        tool = tool_map[tool_name]

        # execute tool
        result = tool.invoke(tool_args)
        print("Action Completed Successfully")
else:
    print("No tool calls.")


