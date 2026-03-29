# Past Work Log

## Session 1 — March 29, 2026

### Initial Setup
- Created full project structure: `config/`, `data/`, `services/`, `ui/`, `output/`
- Set up `.env` for OpenRouter API key, `.gitignore`, and `requirements.txt`
- Dependencies: `streamlit`, `openai`, `fpdf2`, `python-dotenv`

### Core Services Built
1. **Profile Manager** (`services/profile_manager.py`)
   - Load/save/validate user profile as JSON
   - Auto-copies sample profile on first run

2. **LLM Service** (`services/llm_service.py`)
   - Integrates with OpenRouter API (OpenAI-compatible SDK)
   - 3 free models: MiniMax M2.5, Qwen3 Next 80B, NVIDIA Nemotron 3 Super
   - System prompt instructs the LLM to analyze JD, match keywords, rewrite bullets, and return structured JSON
   - Handles empty responses, refusals, invalid JSON with clear error messages

3. **ATS Scorer** (`services/ats_scorer.py`)
   - Local scoring (no API call needed), 4 factors:
     - Keyword Match (40%): extracts real technical terms from JD using a curated dictionary of 100+ known tech terms, then checks resume for matches
     - Section Completeness (20%): checks for required sections (summary, experience, skills, education)
     - Formatting (20%): always 100 since we generate the PDF ourselves
     - Content Quality (20%): checks for action verbs, quantified achievements, resume length
   - Returns matched/missing keywords for visual display

4. **PDF Generator** (`services/pdf_generator.py`)
   - ATS-friendly single-column layout using fpdf2
   - Helvetica font, proper section headings with divider lines
   - Handles Unicode sanitization (smart quotes, em dashes, etc.)
   - Returns `bytes` for Streamlit download button

### User Profile Populated
- Loaded Ammar Shahid's real resume data into `data/sample_profile.json` and `data/profile.json`
- 3 experience entries, 3 projects, 21 skills, education from UMT

### Streamlit UI
- **Two-page layout** using `st.navigation`:
  - **Resume Generator** (default): model selector, JD text area, generate button, ATS score display with color-coded breakdown, keyword tags (green=matched, red=missing), AI suggestions, PDF download button
  - **Edit Profile**: full-width form with bordered cards for each entry, 2-column layout for personal info, add/remove buttons for experience/education/projects/certifications
- API key reads from `.env` only (not shown in UI)

### Bugs Fixed
- Unicode bullet character (`U+2022`) not supported by Helvetica → replaced with dash
- `bytearray` from fpdf2 not accepted by Streamlit → converted to `bytes`
- OpenRouter 404 due to privacy/guardrail settings → documented fix (disable ZDR, clear provider restrictions)
- ATS keyword extractor was grabbing garbage bigrams ("a data", "a short") → rewrote with curated technical term dictionary + fragment deduplication
- LLM returning `None` content → added error handling for empty responses, refusals, and malformed JSON
