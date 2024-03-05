from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
import pandas as pd

class SummaryService:
    def __init__(self):
        self._y_position = 750

    def create_summary_pdf(self, df: pd.DataFrame) -> bytes:
        buffer = BytesIO()
        summary_pdf = canvas.Canvas(buffer, pagesize=letter)
        summary_pdf.setFont("Helvetica-Bold", 12)

        areas = df['Area'].unique()

        for area in areas:
            self._write_area_on_pdf(summary_pdf, area)
            papers = df[df['Area'] == area]
            for _, row in papers.iterrows():
                self._write_title_on_pdf(summary_pdf, str(row['Title']))
                self._write_authors_on_pdf(summary_pdf, str(row['Authors']))

        summary_pdf.save()

        return buffer.getvalue()

    def _write_area_on_pdf(self, summary_pdf: canvas.Canvas, area: str):
        summary_pdf.setFont("Helvetica-Bold", 16)
        if self._y_position < 60:
            summary_pdf.showPage()
            self._y_position = 750
        summary_pdf.drawString(100, self._y_position, f"Área: {area}")
        self._y_position -= 20

    def _write_title_on_pdf(self, summary_pdf: canvas.Canvas, title: str):
        summary_pdf.setFont("Helvetica-Bold", 12)
        title_lines = simpleSplit(
            f"{title}",
            summary_pdf._fontname,
            summary_pdf._fontsize,
            400,
        )
        for line in title_lines:
            if self._y_position < 50:
                summary_pdf.showPage()
                self._y_position = 750
                summary_pdf.setFont("Helvetica-Bold", 12)
            summary_pdf.drawString(165, self._y_position, line)
            self._y_position -= 20

    def _write_authors_on_pdf(self, summary_pdf: canvas.Canvas, authors: str):
        summary_pdf.setFont("Helvetica-Bold", 10)
        authors_lines = simpleSplit(
            f"Autores: {authors}",
            summary_pdf._fontname,
            summary_pdf._fontsize,
            400,
        )
        for line in authors_lines:
            if self._y_position < 50:
                summary_pdf.showPage()
                self._y_position = 750
                summary_pdf.setFont("Helvetica-Bold", 10)
            summary_pdf.drawString(165, self._y_position, line)
            self._y_position -= 20
