from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
import webbrowser

custom_page_size = (600, 800)
margin = 50

def create_summary_pdf(df: pd.DataFrame, output_path: str):
    c = canvas.Canvas(output_path, pagesize=custom_page_size)

    current_area = None
    max_lines_per_page = 45

    page_width, page_height = custom_page_size

    for area, group in df.groupby('area'):
        c.setFont("Helvetica-Bold", 16)
        area_title = area
        x_position = (page_width - c.stringWidth(area_title, "Helvetica-Bold", 16)) / 2  # Centralizando
        c.drawString(x_position, page_height - 70, area_title)
        c.setFont("Helvetica", 12)
        y_position = page_height - 90

        for _, row in group.iterrows():
            title_lines = row['titulo'].split('\n')
            for line in title_lines:
                if y_position < 50:
                    c.showPage()
                    y_position = page_height - 70
                c.setFont("Helvetica-Bold", 12)
                x_position = margin
                line = " " + line.strip() + " "
                while c.stringWidth(line, "Helvetica-Bold", 12) > page_width - (2 * margin):
                    c.drawString(x_position, y_position, line[:-2])
                    line = " " + line[-2:].strip() + " "
                    y_position -= 15
                c.drawString(x_position, y_position, line)
                y_position -= 15

            authors_lines = row['autores'].split(', ')
            if y_position < 50:
                c.showPage()
                y_position = page_height - 70
            c.setFont("Helvetica-Oblique", 10)
            x_position = margin
            authors_line = " " + ", ".join(authors_lines).strip() + " "
            while c.stringWidth(authors_line, "Helvetica-Oblique", 10) > page_width - (2 * margin):
                c.drawString(x_position, y_position, authors_line[:-2])
                authors_line = " "
                y_position -= 15
            c.drawString(x_position, y_position, authors_line)
            y_position -= 20

            y_position -= 15

        y_position -= 40

    c.save()

    webbrowser.open(output_path)

if __name__ == "__main__":
    csv_path = r'D:\Projects\Projeto clone para teste\projeto-summary\trabalhos4.csv'

    df = pd.read_csv(csv_path, delimiter=';')
    create_summary_pdf(df, 'output.pdf')
