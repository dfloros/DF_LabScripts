import os
import PyPDF4
from PyPDF4 import PdfFileReader, PdfFileWriter


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)
        
if __name__ == '__main__':
    paths = sorted([i for i in os.listdir('.') if '.pdf' in i])
    if len(paths) > 0:
        merge_pdfs(paths, output='merged.pdf')
    else:
        print("No PDFs in this folder. Use this on easily sorted PDFs. It will merge all files in the current directory.")