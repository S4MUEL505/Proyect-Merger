import os
import PyPDF4
import sys
sys.setrecursionlimit(55924096)

def merge_pdfs(input_files, output_file):
    merger = PyPDF4.PdfFileMerger()
    for input_file in input_files:
        merger.append(input_file)
    merger.write(output_file)
    merger.close()

directory = input("Introduce el directorio donde buscar los archivos PDF: ")

def find_combinations(files, sizes, limit, current, result):
    if sum(sizes[i] for i in current) > limit:
        return
    if len(current) == len(files):
        result.add(tuple(files[i] for i in current))
        return
    find_combinations(files, sizes, limit, current + [len(current)], result)
    find_combinations(files, sizes, limit, current, result)

limit = 4 * 1024
pdf_files = []
pdf_sizes = []
for file in os.listdir(directory):
    if file.endswith(".pdf"):
        pdf_files.append(file)
        size = os.path.getsize(os.path.join(directory, file))
        size = round(size / 1024, 2)
        pdf_sizes.append(size)
        print(f"{file} - {size} KB")

combinations = set()
find_combinations(pdf_files, pdf_sizes, limit, [], combinations)
print(f"Estas son las posibles combinaciones de archivos que suman menos de {limit} KB:")
for combination in sorted(combinations):
    total_size = sum([file_size for file in combination])
    if total_size < limit:
        print(", ".join(combination))
    else:
        print("No hubo conjuntos o hubo algún error.")

selection = input("Introduce los nombres de los archivos PDF que quieres combinar, separados por comas: ")
selection = selection.split(",")
selected_files = []
for file in selection:
    file = file.strip()
    if file in pdf_files:
        selected_files.append(file)
    else:
        print(f"{file} no es un archivo PDF válido")

output_file = input("Introduce el nombre del archivo PDF resultante: ")
if not output_file.endswith(".pdf"):
    output_file = output_file + ".pdf"

merge_pdfs(selected_files, output_file)
print(f"Los archivos PDF seleccionados se han combinado en {output_file}")
