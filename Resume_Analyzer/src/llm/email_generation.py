from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import build_resource_service, get_gmail_credentials
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from config import GMAIL_CLIENT_SECRET, GMAIL_TOKEN

def get_gmail_tools():
    creds = get_gmail_credentials(
        token_file=GMAIL_TOKEN,
        client_secrets_file=GMAIL_CLIENT_SECRET,
        scopes=["https://mail.google.com/"]
    )
    service = build_resource_service(credentials=creds)
    toolkit = GmailToolkit(api_resource=service)
    return toolkit.get_tools()

email_prompt = PromptTemplate(
    template="""Create a professional interview email: {query}""",
    input_variables=['query']
)

def send_email(query):
    tools = get_gmail_tools()
    model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
    chain = email_prompt | model
    response = chain.invoke({"query": query})
    for call in response.tool_calls or []:
        tool = {t.name: t for t in tools}[call["name"]]
        tool.invoke(call["args"])
