from langchain_core.output_parsers import JsonOutputParser
from .models import Candidate,Score

json_parser = JsonOutputParser(pydantic_object=Candidate)
score_json_parser = JsonOutputParser(pydantic_object=Score)
