import os
import PyPDF2

while True:
    pdf_file = input("Ścieżka:\n> ")
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    pdf_writer = PyPDF2.PdfFileWriter()
    with open(pdf_file, "rb") as opened:
        page_to_rotate = int(input("Numer strony:\n> ")) - 1
        rotations = int(input("Ile razy obrócić stronę w prawo? (1/2/3)\n> "))
        print()
        for pagenum in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pagenum)
            if pagenum == page_to_rotate:
                if rotations == 1:
                    page.rotateClockwise(90)
                elif rotations == 2:
                    page.rotateClockwise(180)
                elif rotations == 3:
                    page.rotateClockwise(270)
            pdf_writer.addPage(page)
    new_file = os.path.join(
        os.path.dirname(pdf_file), "__" + os.path.basename(pdf_file)
    )
    with open(new_file, "wb") as opened:
        pdf_writer.write(opened)
