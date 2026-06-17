from markdown_pdf import MarkdownPdf, Section

pdf = MarkdownPdf()

with open("calculus_project_report.md", "r", encoding="utf-8") as f:
    text = f.read()

pdf.add_section(Section(text))
pdf.save("calculus_project_report.pdf")
print("PDF created successfully.")
