def get_top_candidate(scores):
    return sorted(scores, key=lambda x: x['overall_score'], reverse=True)[0]
