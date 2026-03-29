# Resume Maker

Resume Maker is a Streamlit app that tailors ATS-friendly resumes to a job description, scores the result, and exports a PDF.

## Features

- Tailor a resume to a pasted job description with an LLM
- Score the generated resume with a local ATS-style breakdown
- Download a clean, single-column PDF
- Edit and save your reusable profile data
- Review a simple dashboard of logged job descriptions and extracted skills

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API keys

Create a `.env` file in the project root for OpenRouter-backed models:

```env
OPENROUTER_API_KEY=your_api_key_here
```

If you want to use `OpenAI: gpt-oss-120b (free)`, also provide:

```env
GPT_OSS_120B_API_KEY=your_api_key_here
```

You can also supply those keys through Streamlit secrets instead of `.env`.

### 3. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Pages

- `Resume Generator`: paste a job description, pick a model, generate a tailored resume, review ATS feedback, and download the PDF.
- `Edit Profile`: manage personal info, summary, skills, experience, education, projects, and certifications.
- `Dashboard`: review logged requests and commonly extracted skills.

## Project Structure

```text
resume-maker/
|-- app.py
|-- requirements.txt
|-- config/
|   `-- settings.py
|-- data/
|   |-- sample_profile.json
|   `-- profile.json
|-- services/
|   |-- ats_scorer.py
|   |-- llm_service.py
|   |-- pdf_generator.py
|   |-- profile_manager.py
|   `-- usage_logger.py
|-- ui/
|   |-- components.py
|   |-- dashboard.py
|   |-- main_page.py
|   `-- profile_page.py
`-- output/
```

## How It Works

1. Profile data is loaded from JSON.
2. The job description and profile are sent to the selected model.
3. The model returns structured JSON for a tailored resume.
4. A local scorer estimates ATS compatibility based on keywords, sections, formatting, and content quality.
5. The app renders and saves a PDF for download.

## Tech Stack

- Streamlit
- OpenRouter / OpenAI-compatible chat API
- fpdf2
- pandas
- matplotlib
