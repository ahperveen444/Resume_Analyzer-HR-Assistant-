import glob
from src.llm.extract_chain import candidate_extract_chain
from src.llm.scoring_chain import candidate_score_chain
from src.utils.pdf_extractor import extract_text_from_pdf
from src.data.job_requirments import job_requirments

def run_analysis():
    resumes = glob.glob("Resumes/*.pdf")
    extracted_candidates = []
    final_scores = []

    for path in resumes:
        text = extract_text_from_pdf(path)
        result = candidate_extract_chain.invoke({"text": text})
        extracted_candidates.append(result)

    for c in extracted_candidates:
        score = candidate_score_chain.invoke({
            "job_requirments": job_requirments,
            "candidates": str(c)
        })
        final_scores.append(score)

    return final_scores
