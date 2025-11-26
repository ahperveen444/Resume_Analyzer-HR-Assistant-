from src.pipeline.analyzer import run_analysis
from src.pipeline.ranker import get_top_candidate
from src.llm.email_generation import send_email

scores = run_analysis()
best = get_top_candidate(scores)

print("Best Candidate:", best)

email = best["email"]
query = f"Draft an interview email to {email}"
send_email(query)
