import json
import re
from openai import OpenAI
from config.settings import OPENROUTER_BASE_URL, MODELS


def get_client(api_key):
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


SYSTEM_PROMPT = """You are an expert resume writer and ATS (Applicant Tracking System) optimization specialist.

Given a candidate's profile data and a target job description, produce a tailored resume that:

1. **Mirrors exact JD keywords** — copy technical terms, tool names, and skill phrases verbatim from the job description into the resume wherever truthful
2. **Rewrites bullet points** to emphasize relevant experience using strong action verbs and quantified achievements
3. **Selects the most relevant** skills, projects, and certifications for this specific role
4. **Crafts a professional summary** that incorporates key role-specific keywords and phrases from the job description
5. **Maintains honesty** - enhance presentation but never fabricate experience or skills

Rules for ATS optimization:
- Use standard section headings: Summary, Experience, Skills, Education, Projects, Certifications
- **CRITICAL**: Include exact keyword phrases from the job description in every section (summary, skills, bullets, project descriptions)
- List skills using the exact terminology from the job description (e.g., if JD says "scikit-learn", use "scikit-learn" not "sklearn")
- Include both abbreviations and full forms where relevant (e.g., "NLP (Natural Language Processing)")
- Use reverse chronological order for experience
- Start EVERY bullet point with a strong action verb (e.g., Developed, Implemented, Optimized, Deployed, Leveraged, Designed)
- Include metrics and numbers in at least 50% of bullet points (percentages, counts, time savings, accuracy scores)
- In the skills section, list every relevant tool/technology mentioned in the job description that the candidate knows

You MUST respond with ONLY valid JSON (no markdown, no code fences) in this exact structure:
{
  "tailored_summary": "2-3 sentence professional summary tailored to this job",
  "selected_skills": {
    "technical": ["skill1", "skill2"],
    "tools": ["tool1", "tool2"],
    "soft": ["skill1", "skill2"]
  },
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "Location",
      "start_date": "YYYY-MM",
      "end_date": "Present or YYYY-MM",
      "bullets": ["Achievement 1...", "Achievement 2..."]
    }
  ],
  "education": [
    {
      "degree": "Degree Name",
      "institution": "School Name",
      "graduation_date": "Year",
      "gpa": "GPA if notable",
      "highlights": ["highlight1"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "description": "Brief description",
      "technologies": ["tech1", "tech2"],
      "url": "URL if available",
      "bullets": ["What you did..."]
    }
  ],
  "certifications": [
    {
      "name": "Cert Name",
      "issuer": "Issuer",
      "date": "Date",
      "credential_id": "ID"
    }
  ],
  "keyword_analysis": {
    "matched_keywords": ["keywords from JD found in resume"],
    "missing_keywords": ["important JD keywords not in candidate profile"],
    "suggestions": "Brief advice on how to improve the resume further"
  }
}"""


def tailor_resume(api_key, model_name, job_description, profile_data):
    client = get_client(api_key)
    model_id = MODELS[model_name]

    user_message = f"""## Job Description
{job_description}

## Candidate Profile
{json.dumps(profile_data, indent=2)}

Analyze the job description, then produce a tailored resume from the candidate's profile. Respond with ONLY valid JSON."""

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
    )

    if not response.choices:
        raise ValueError("Model returned no response. Try a different model.")

    message = response.choices[0].message
    content = message.content

    if not content:
        refusal = getattr(message, "refusal", None)
        if refusal:
            raise ValueError(f"Model refused the request: {refusal}")
        raise ValueError("Model returned empty content. Try a different model.")

    content = content.strip()

    if content.startswith("```"):
        lines = content.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines)

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Model returned invalid JSON. Try a different model.\n\nRaw response:\n{content[:500]}")
