# Resume Maker

Generate ATS-optimized resumes tailored to any job description in seconds — with scoring, keyword analysis, and ready-to-download PDFs.

## Features

- **Paste a job description** and get a tailored resume in seconds
- **ATS score** with detailed breakdown (keyword match, sections, formatting, content quality)
- **3 free AI models** via OpenRouter (MiniMax M2.5, Qwen3 Next 80B, NVIDIA Nemotron 3 Super)
- **Profile editor** to manage your skills, experience, projects, certifications, and education
- **PDF download** in a clean, single-column ATS-friendly format
- **Keyword analysis** showing matched and missing keywords from the job description

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/resume-maker.git
cd resume-maker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your OpenRouter API key

1. Go to [openrouter.ai](https://openrouter.ai) and create a free account
2. Generate an API key from the [API Keys page](https://openrouter.ai/settings/keys)
3. Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=your_api_key_here
```

> **Note:** If you get a 404 error about guardrails, go to [OpenRouter Privacy Settings](https://openrouter.ai/settings/privacy) and disable "ZDR Endpoints Only". Also make sure "Allowed Providers" is empty (no restrictions).

### 4. Run the app

```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Usage

### Resume Generator (main page)

1. Select an AI model from the dropdown
2. Paste the full job description into the text area
3. Click **Generate Tailored Resume**
4. Review the ATS score and keyword analysis
5. Download the PDF

### Edit Profile

Switch to the **Edit Profile** page to update your:

- Personal information (name, email, phone, links)
- Professional summary
- Skills (technical, tools, soft skills)
- Work experience (with achievement bullets)
- Education
- Projects
- Certifications

Click **Save Profile** to persist your changes.

## Project Structure

```
resume-maker/
├── app.py                      # Streamlit entry point with page navigation
├── .env                        # OpenRouter API key (not committed)
├── requirements.txt            # Python dependencies
│
├── config/
│   └── settings.py             # Model IDs, API URL, file paths
│
├── data/
│   ├── sample_profile.json     # Template profile (copied on first run)
│   └── profile.json            # Your saved profile (gitignored)
│
├── services/
│   ├── llm_service.py          # OpenRouter API integration
│   ├── ats_scorer.py           # ATS scoring engine
│   ├── pdf_generator.py        # PDF generation with fpdf2
│   └── profile_manager.py      # Profile load/save/validate
│
├── ui/
│   ├── main_page.py            # Resume generator page
│   ├── profile_page.py         # Profile editor page
│   └── components.py           # ATS score display components
│
└── output/                     # Generated PDFs
```

## How It Works

1. **Profile data** is stored as JSON and loaded into the app
2. **Job description** is sent along with your profile to the selected LLM via OpenRouter
3. The LLM **analyzes the JD**, selects relevant skills/experience/projects, rewrites bullets with matching keywords, and returns structured JSON
4. **ATS scorer** computes a compatibility score locally (no API call) based on keyword match, section completeness, formatting, and content quality
5. **PDF generator** creates a clean, ATS-friendly resume using fpdf2

## ATS Score Breakdown

| Factor | Weight | What it measures |
|--------|--------|-----------------|
| Keyword Match | 40% | Technical terms from JD found in your resume |
| Section Completeness | 20% | Required sections present (summary, experience, skills, education) |
| Formatting | 20% | ATS-friendly format (always 100% since we generate the PDF) |
| Content Quality | 20% | Action verbs, quantified achievements, appropriate length |

## Models

All models are **free** via OpenRouter:

| Model | Best For |
|-------|----------|
| MiniMax M2.5 | General-purpose, good reasoning |
| Qwen3 Next 80B A3B | Fast responses, strong at structured output |
| NVIDIA Nemotron 3 Super | Complex tasks, large context window (1M tokens) |

## Tech Stack

- **Frontend:** Streamlit
- **AI:** OpenRouter API (OpenAI-compatible)
- **PDF:** fpdf2
- **Language:** Python 3.10+
