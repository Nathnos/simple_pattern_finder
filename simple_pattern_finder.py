"""
A soft version of pattern_finder, without image search.
You'll need odfpy (1.4.0) and python-docx (0.8.10) and PyPDF2 (1.26.0) libs.
No arguments, only input() questions.
"""

import os
import sys

import docx
from odf.opendocument import load
from odf import text, teletype
import PyPDF2


if not sys.warnoptions:#Ignore PdfReadWarning
    import warnings
    warnings.simplefilter("ignore")

def show(dir, file, counter):
    if counter > 0:
        print(os.path.join(dir, file), ": Nombre d'occurences :", counter)

def pdf_analysis(file_name, pattern, path):
    """Finds the pattern in text (and images) for .pdf files"""
    counter = 0
    with open(file_name, "rb") as file:
        read_pdf = PyPDF2.PdfFileReader(file)
        for i in range(read_pdf.getNumPages()):
            counter += read_pdf.getPage(i).extractText().lower().count(pattern)
    show(path, file_name, counter)

def docx_analysis(file, pattern, path):
    """Finds the pattern in text (and images) for .docx files"""
    document = docx.Document(file)
    counter = 0
    for para in document.paragraphs:
        counter += para.text.lower().count(pattern)
    show(path, file, counter)

def odt_analysis(file, pattern, path):
    """Finds the pattern in text (and images) for .odt files"""
    counter = 0
    textdoc = load(file)
    all_paragraphs = textdoc.getElementsByType(text.P)
    for paragraph in all_paragraphs:
        counter += teletype.extractText(paragraph).lower().count(pattern)
    show(path, file, counter)

def txt_analysis(file_name, pattern, path):
    """Tries to finds the pattern in the text of UTF-8 encocded files"""
    try:
        with open(file_name, "r") as file:
            text = file.read().lower()
            counter = text.count(pattern)
            show(path, file_name, counter)
    except UnicodeDecodeError:
        pass

def launch_analysis(dir=".", full_dir =".", pattern="", search_options=None,
                    forbidden=None):
    os.chdir(dir)
    if dir == ".": #First Run
        print("Motif à rechercher : ")
        pattern = input().lower()
        print("Rechercher aussi dans les pdf ? (peut être très long) : o/n")
        in_pdf = True if input().lower() == "o" else False
        print("Rechercher aussi dans tous les sous-dossiers ? : o/n")
        in_sf = True if input().lower() == "o" else False
        print("File/Folder names to ignore (splited by a slash): ")
        forbidden = input().split("/")
        search_options = in_sf, in_pdf#.git/env_pattern_finder
    in_sf, in_pdf = search_options
    for file_or_dir in os.listdir("."):
        if(os.path.isfile(file_or_dir) and file_or_dir not in forbidden):
            file = file_or_dir
            _, ext = os.path.splitext(file)
            if ext == ".docx":
                docx_analysis(file, pattern, full_dir)
            elif ext == ".odt":
                odt_analysis(file, pattern, full_dir)
            elif ext == ".pdf" and in_pdf:
                pdf_analysis(file, pattern, full_dir)
            else: #Tries to open othe files encoded with UTF-8
                txt_analysis(file, pattern, full_dir)
        elif(os.path.isdir(file_or_dir) and in_sf
             and file_or_dir not in forbidden):
            dir = file_or_dir
            launch_analysis(os.path.join(".", dir),
                            os.path.join(full_dir, dir), pattern,
                            search_options, forbidden)
    os.chdir("..")

def main():
    launch_analysis()


if __name__ == "__main__":
    main()
