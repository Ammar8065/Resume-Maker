import os
from fpdf import FPDF
from config.settings import OUTPUT_DIR


def sanitize(text):
    """Replace Unicode characters that Helvetica can't render with ASCII equivalents."""
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u2022": "-",
        "\u00a0": " ",
        "\u2032": "'",
        "\u2033": '"',
        "\u00b2": "2",
        "\u00b3": "3",
        "\u2248": "~",
        "\u2264": "<=",
        "\u2265": ">=",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", errors="replace").decode("latin-1")


class ResumePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def section_heading(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 30, 30)
        self.cell(0, 7, title.upper(), new_x="LMARGIN", new_y="NEXT")
        y = self.get_y()
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.3)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(3)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 4.5, sanitize(text))
        self.ln(1)

    def bullet_point(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(50, 50, 50)
        bullet_indent = self.l_margin + 4
        text_indent = bullet_indent + 4
        text_width = self.w - self.r_margin - text_indent

        self.set_x(bullet_indent)
        self.cell(4, 4.5, "-")
        self.set_x(text_indent)
        self.multi_cell(text_width, 4.5, sanitize(text))
        self.ln(0.5)

    def entry_header(self, left_text, right_text):
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(30, 30, 30)
        self.cell(0, 5, sanitize(left_text))
        self.set_font("Helvetica", "", 9)
        self.set_text_color(80, 80, 80)
        right_text = sanitize(right_text)
        w = self.get_string_width(right_text) + 2
        self.set_x(self.w - self.r_margin - w)
        self.cell(w, 5, right_text, new_x="LMARGIN", new_y="NEXT")

    def entry_subheader(self, left_text, right_text=""):
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 5, sanitize(left_text))
        if right_text:
            right_text = sanitize(right_text)
            w = self.get_string_width(right_text) + 2
            self.set_x(self.w - self.r_margin - w)
            self.cell(w, 5, right_text, new_x="LMARGIN", new_y="NEXT")
        else:
            self.ln(5)


def generate_resume_pdf(tailored_data, personal_info):
    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_margins(18, 15, 18)
    pdf.set_y(15)

    name = personal_info.get("full_name", "Your Name")
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 9, sanitize(name), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    contact_parts = []
    if personal_info.get("email"):
        contact_parts.append(personal_info["email"])
    if personal_info.get("phone"):
        contact_parts.append(personal_info["phone"])
    if personal_info.get("location"):
        contact_parts.append(personal_info["location"])
    if personal_info.get("linkedin"):
        contact_parts.append(personal_info["linkedin"])
    if personal_info.get("github"):
        contact_parts.append(personal_info["github"])
    if personal_info.get("portfolio"):
        contact_parts.append(personal_info["portfolio"])

    if contact_parts:
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(80, 80, 80)
        contact_line = "  |  ".join(contact_parts)
        pdf.cell(0, 5, sanitize(contact_line), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    summary = tailored_data.get("tailored_summary", "")
    if summary:
        pdf.section_heading("Professional Summary")
        pdf.body_text(summary)
        pdf.ln(2)

    experience = tailored_data.get("experience", [])
    if experience:
        pdf.section_heading("Experience")
        for i, exp in enumerate(experience):
            title = exp.get("title", "")
            company = exp.get("company", "")
            location = exp.get("location", "")
            start = exp.get("start_date", "")
            end = exp.get("end_date", "")
            date_str = f"{start} - {end}" if start else end

            pdf.entry_header(title, date_str)
            pdf.entry_subheader(company, location)

            for bullet in exp.get("bullets", []):
                pdf.bullet_point(bullet)

            if i < len(experience) - 1:
                pdf.ln(2)
        pdf.ln(2)

    skills = tailored_data.get("selected_skills", {})
    has_skills = False
    if isinstance(skills, dict):
        has_skills = any(skills.values())
    elif isinstance(skills, list):
        has_skills = bool(skills)

    if has_skills:
        pdf.section_heading("Skills")
        if isinstance(skills, dict):
            for category, skill_list in skills.items():
                if skill_list:
                    label = category.replace("_", " ").title()
                    pdf.set_font("Helvetica", "B", 9.5)
                    pdf.set_text_color(30, 30, 30)
                    pdf.cell(pdf.get_string_width(f"{label}: ") + 1, 4.5, f"{label}: ")
                    pdf.set_font("Helvetica", "", 9.5)
                    pdf.set_text_color(50, 50, 50)
                    pdf.multi_cell(0, 4.5, sanitize(", ".join(skill_list)))
                    pdf.ln(1)
        elif isinstance(skills, list):
            pdf.body_text(", ".join(skills))
        pdf.ln(2)

    projects = tailored_data.get("projects", [])
    if projects:
        pdf.section_heading("Projects")
        for i, proj in enumerate(projects):
            name_str = proj.get("name", "")
            techs = proj.get("technologies", [])
            tech_str = f" ({', '.join(techs)})" if techs else ""

            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(30, 30, 30)
            pdf.cell(0, 5, sanitize(f"{name_str}{tech_str}"), new_x="LMARGIN", new_y="NEXT")

            desc = proj.get("description", "")
            if desc:
                pdf.set_font("Helvetica", "I", 9)
                pdf.set_text_color(80, 80, 80)
                pdf.multi_cell(0, 4.5, sanitize(desc))

            for bullet in proj.get("bullets", []):
                pdf.bullet_point(bullet)

            if i < len(projects) - 1:
                pdf.ln(1)
        pdf.ln(2)

    education = tailored_data.get("education", [])
    if education:
        pdf.section_heading("Education")
        for edu in education:
            degree = edu.get("degree", "")
            institution = edu.get("institution", "")
            grad_date = edu.get("graduation_date", "")
            gpa = edu.get("gpa", "")

            pdf.entry_header(degree, grad_date)
            sub = institution
            if gpa:
                sub += f" | GPA: {gpa}"
            pdf.entry_subheader(sub)

            for highlight in edu.get("highlights", []):
                pdf.bullet_point(highlight)
        pdf.ln(2)

    certs = tailored_data.get("certifications", [])
    if certs:
        pdf.section_heading("Certifications")
        for cert in certs:
            cert_name = cert.get("name", "")
            issuer = cert.get("issuer", "")
            date = cert.get("date", "")
            line = cert_name
            if issuer:
                line += f" - {issuer}"
            pdf.entry_header(line, date)
            pdf.ln(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "resume.pdf")
    pdf_bytes = bytes(pdf.output())
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    return pdf_bytes
