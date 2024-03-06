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

    max_width = page_width - (margin *2)

    for area, group in df.groupby('area'):
        c.setFont("Times-Bold", 16)  # Alterando a fonte para Times New Roman e negrito
        area_title = area
        x_position = (page_width - c.stringWidth(area_title, "Times-Bold", 16)) / 2  # Centralizando
        c.drawString(x_position, page_height - 70, area_title)
        c.setFont("Times-Roman", 12)  # Alterando a fonte para Times New Roman
        y_position = page_height - 90

        for _, row in group.iterrows():
            title_lines = row['titulo'].split('\n')
            for line in title_lines:
                if y_position < 50:
                    c.showPage()
                    y_position = page_height - 70
                c.setFont("Times-Bold", 12)  # Alterando a fonte para Times New Roman e negrito
                x_position = margin
                line = " " + line.strip() + " "
                words = line.split()
                new_line = ''
                for word in words:
                    width = c.stringWidth(new_line + " " + word)
                    if width <= max_width:
                        new_line += " " + word
                    else:
                        c.drawString(x_position, y_position, new_line.strip())
                        y_position -= 15
                        new_line = word
                # while c.stringWidth(line, "Times-Bold", 12) > page_width - (2 * margin):
                #     line = line[:-2]
                
                c.setLineWidth(page_width - (margin * 2))
                c.drawString(x_position, y_position, new_line)
                y_position -= 15

            authors_lines = row['autores'].split(', ')
            if y_position < 50:
                c.showPage()
                y_position = page_height - 70
            c.setFont("Times-Italic", 10)  # Alterando a fonte para Times New Roman e itálico
            x_position = margin
            authors_line = " " + ", ".join(authors_lines).strip() + " "
            while c.stringWidth(authors_line, "Times-Italic", 10) > page_width - (2 * margin):
                authors_line = authors_line[:-2]
            c.drawString(x_position, y_position, authors_line)
            y_position -= 20

            y_position -= 15

        c.showPage()

    c.save()

    webbrowser.open(output_path)

if __name__ == "__main__":
    csv_path = r'trabalhos4.csv'

    df = pd.read_csv(csv_path, delimiter=';')
    create_summary_pdf(df, 'output.pdf')
