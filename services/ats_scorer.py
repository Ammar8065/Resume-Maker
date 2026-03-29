import re

# Common filler words to ignore
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "must", "it", "its",
    "you", "your", "we", "our", "they", "their", "this", "that", "these",
    "those", "as", "if", "not", "no", "so", "up", "out", "about", "into",
    "over", "after", "before", "between", "under", "through", "during",
    "above", "below", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "than", "too", "very", "just", "also", "well",
    "back", "even", "still", "new", "way", "who", "which", "where", "when",
    "what", "how", "any", "only", "own", "same", "while", "able", "work",
    "working", "role", "team", "experience", "including", "across", "using",
    "etc", "per", "via", "within", "without", "strong", "short",
    "excellent", "good", "great", "looking", "join", "opportunity",
    "responsibilities", "requirements", "qualifications", "preferred",
    "required", "minimum", "years", "year", "plus", "company", "position",
    "candidate", "ideal", "based", "part", "full", "time", "along", "note",
    "send", "links", "like", "real", "world", "closely", "build", "assist",
    "create", "basic", "apply", "offer", "focused", "growth", "flexible",
    "into", "key", "relevant", "hands", "understand", "understanding",
    "knowledge", "exposure", "personal", "academic", "proficiency",
}

# Known technical terms, tools, and skills that should always be extracted
TECHNICAL_TERMS = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "go",
    "rust", "scala", "kotlin", "swift", "ruby", "php", "sql", "nosql",
    # ML/DS
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "neural network", "neural networks", "reinforcement learning",
    "supervised learning", "unsupervised learning", "feature engineering",
    "model training", "model deployment", "data science", "data analysis",
    "data engineering", "data pipeline", "data pipelines", "data visualization",
    "statistical analysis", "predictive modeling", "a/b testing", "ab testing",
    "exploratory data analysis", "eda", "etl", "time series",
    # Frameworks/Libraries
    "tensorflow", "pytorch", "scikit-learn", "sklearn", "pandas", "numpy",
    "matplotlib", "plotly", "seaborn", "keras", "xgboost", "lightgbm",
    "langchain", "hugging face", "transformers", "opencv", "spacy", "nltk",
    "spark", "pyspark", "hadoop", "airflow", "dbt", "fastapi", "flask",
    "django", "react", "node.js", "next.js",
    # Cloud/DevOps
    "aws", "azure", "gcp", "google cloud", "cloud platforms", "docker",
    "kubernetes", "ci/cd", "mlops", "devops", "terraform", "linux",
    # Databases
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "sql server", "bigquery", "snowflake", "redshift",
    # Tools
    "git", "github", "jupyter", "power bi", "tableau", "looker",
    "looker studio", "excel", "google sheets", "jira", "confluence",
    "n8n", "apache kafka",
    # Concepts
    "api", "apis", "rest", "restful", "microservices", "agile", "scrum",
    "version control", "unit testing", "regression", "classification",
    "clustering", "random forest", "gradient boosting", "lstm",
    "cnn", "rnn", "gan", "rag", "llm", "large language model",
    "prompt engineering", "fine-tuning", "embeddings",
    "data warehousing", "dashboards", "reporting", "automation",
    "web scraping", "data cleaning", "data wrangling",
    "cross-functional", "stakeholder", "mentorship", "collaboration",
}

ACTION_VERBS = {
    "achieved", "administered", "analyzed", "built", "collaborated",
    "configured", "created", "decreased", "delivered", "designed",
    "developed", "directed", "drove", "enabled", "engineered",
    "established", "executed", "expanded", "generated", "grew",
    "identified", "implemented", "improved", "increased", "integrated",
    "launched", "led", "managed", "migrated", "optimized", "orchestrated",
    "pioneered", "planned", "produced", "reduced", "refactored",
    "redesigned", "resolved", "revamped", "scaled", "secured",
    "simplified", "spearheaded", "streamlined", "strengthened",
    "supervised", "transformed", "upgraded",
}


def extract_keywords(text):
    """Extract meaningful keywords from text - technical terms, tools, and skills."""
    text_lower = re.sub(r"[.,;:!?()]+(?=\s|$)", " ", text.lower())
    text_lower = re.sub(r"\s+", " ", text_lower).strip()
    found = set()

    for term in sorted(TECHNICAL_TERMS, key=len, reverse=True):
        if term in text_lower:
            found.add(term)

    words = re.findall(r"[a-z#+./]+", text_lower)
    for word in words:
        if word not in STOP_WORDS and len(word) > 2 and word not in found:
            found.add(word)

    generic = {
        "the", "and", "you", "use", "get", "set", "run", "see", "let",
        "put", "top", "end", "day", "lot", "big", "old", "own", "try",
        "help", "want", "make", "take", "give", "come", "keep", "tell",
        "show", "find", "know", "think", "look", "want", "need", "feel",
        "leave", "call", "turn", "start", "move", "live", "believe",
        "bring", "happen", "write", "provide", "sit", "stand", "lose",
        "pay", "meet", "play", "hear", "grow", "open", "walk", "win",
        "teach", "offer", "consider", "appear", "buy", "wait", "serve",
        "die", "expect", "stay", "fall", "read", "involving", "welcome",
        "junior", "senior", "lead", "principal", "level", "r",
    }
    found -= generic
    found -= STOP_WORDS

    multi_word = {keyword for keyword in found if " " in keyword or "/" in keyword or "-" in keyword}
    fragments_to_remove = set()
    for keyword in list(found):
        if " " not in keyword and "/" not in keyword and "-" not in keyword:
            for multi_word_keyword in multi_word:
                parts = re.split(r"[\s\-/]", multi_word_keyword)
                if keyword in parts:
                    fragments_to_remove.add(keyword)
                    break
    found -= fragments_to_remove

    return found


def compute_keyword_score(jd_text, resume_text):
    jd_keywords = extract_keywords(jd_text)
    resume_lower = resume_text.lower()

    if not jd_keywords:
        return 100, [], []

    matched = [keyword for keyword in jd_keywords if keyword in resume_lower]
    missing = [keyword for keyword in jd_keywords if keyword not in resume_lower]

    score = int((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 100
    return score, sorted(matched), sorted(missing)


def compute_section_score(resume_sections):
    required = ["personal_info", "summary", "experience", "skills", "education"]
    optional = ["projects", "certifications"]

    present = []
    missing = []

    for section in required:
        if resume_sections.get(section):
            present.append(section)
        else:
            missing.append(section)

    for section in optional:
        if resume_sections.get(section):
            present.append(section)

    req_score = (len([section for section in required if section in present]) / len(required)) * 80
    opt_score = (len([section for section in optional if section in present]) / len(optional)) * 20

    return int(req_score + opt_score), present, missing


def compute_content_quality_score(resume_text, experience_bullets):
    suggestions = []
    scores = []

    if experience_bullets:
        action_count = sum(
            1 for bullet in experience_bullets
            if bullet.strip().split()[0].lower().rstrip("ed,s") in ACTION_VERBS
            or bullet.strip().split()[0].lower() in ACTION_VERBS
        )
        verb_ratio = action_count / len(experience_bullets)
        scores.append(verb_ratio * 100)
        if verb_ratio < 0.7:
            suggestions.append("Start more bullet points with strong action verbs")
    else:
        scores.append(0)
        suggestions.append("Add work experience with achievement bullets")

    if experience_bullets:
        quant_count = sum(1 for bullet in experience_bullets if re.search(r"\d+", bullet))
        quant_ratio = quant_count / len(experience_bullets)
        scores.append(quant_ratio * 100)
        if quant_ratio < 0.5:
            suggestions.append("Add more metrics and numbers to quantify achievements")
    else:
        scores.append(0)

    word_count = len(resume_text.split())
    if word_count < 150:
        scores.append(40)
        suggestions.append("Resume content is too short - add more detail")
    elif word_count > 1000:
        scores.append(70)
        suggestions.append("Resume may be too long - consider trimming to 1-2 pages")
    else:
        scores.append(100)

    return int(sum(scores) / len(scores)) if scores else 50, suggestions


def compute_ats_score(job_description, tailored_data):
    resume_parts = []
    resume_parts.append(tailored_data.get("tailored_summary", ""))

    skills = tailored_data.get("selected_skills", {})
    if isinstance(skills, dict):
        for category in skills.values():
            if isinstance(category, list):
                resume_parts.extend(category)
    elif isinstance(skills, list):
        resume_parts.extend(skills)

    experience_bullets = []
    for exp in tailored_data.get("experience", []):
        resume_parts.append(exp.get("title", ""))
        resume_parts.append(exp.get("company", ""))
        bullets = exp.get("bullets", [])
        experience_bullets.extend(bullets)
        resume_parts.extend(bullets)

    for proj in tailored_data.get("projects", []):
        resume_parts.append(proj.get("name", ""))
        resume_parts.append(proj.get("description", ""))
        resume_parts.extend(proj.get("technologies", []))
        resume_parts.extend(proj.get("bullets", []))

    for cert in tailored_data.get("certifications", []):
        resume_parts.append(cert.get("name", ""))
        resume_parts.append(cert.get("issuer", ""))

    for edu in tailored_data.get("education", []):
        resume_parts.append(edu.get("degree", ""))
        resume_parts.append(edu.get("institution", ""))
        resume_parts.extend(edu.get("highlights", []))

    resume_text = " ".join(resume_parts)

    resume_sections = {
        "personal_info": True,
        "summary": bool(tailored_data.get("tailored_summary")),
        "experience": bool(tailored_data.get("experience")),
        "skills": bool(skills),
        "education": bool(tailored_data.get("education")),
        "projects": bool(tailored_data.get("projects")),
        "certifications": bool(tailored_data.get("certifications")),
    }

    kw_score, matched, missing = compute_keyword_score(job_description, resume_text)
    section_score, present_sections, missing_sections = compute_section_score(resume_sections)
    content_score, content_suggestions = compute_content_quality_score(resume_text, experience_bullets)
    format_score = 100

    overall = int(
        kw_score * 0.40
        + section_score * 0.20
        + format_score * 0.20
        + content_score * 0.20
    )

    return {
        "overall_score": overall,
        "breakdown": {
            "keyword_match": {
                "score": kw_score,
                "weight": "40%",
                "matched": matched,
                "missing": missing,
            },
            "section_completeness": {
                "score": section_score,
                "weight": "20%",
                "present": present_sections,
                "missing": missing_sections,
            },
            "formatting": {
                "score": format_score,
                "weight": "20%",
                "issues": [],
            },
            "content_quality": {
                "score": content_score,
                "weight": "20%",
                "suggestions": content_suggestions,
            },
        },
    }
