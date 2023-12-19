import os
import PyPDF4
# import sys
# sys.setrecursionlimit(55924096)

# Se define una función para combinar varios archivos PDF
def merge_pdfs(input_files, output_file):
    merger = PyPDF4.PdfFileMerger() # Se crea un objeto PdfFileMerger de PyPDF4
    for input_file in input_files: # Se añade cada archivo PDF al objeto
        merger.append(input_file)
    merger.write(output_file) # Se escribe el archivo PDF combinado...
    merger.close() # ...y se cierra
# Se pide al usuario que introduzca el directorio donde se encuentran los archivos PDF
directory = input("Introduce el directorio donde buscar los archivos PDF: ")
# Se define una función para encontrar todas las combinaciones de archivos que sumen menos de 4 MB
def find_combinations(files, sizes, limit, current, result):
    if sum(sizes[i] for i in current) > limit: # Se comprueba si la suma de los tamaños de los archivos actuales supera el límite
        return # Termina la recursión
    if len(current) == len(files): # Se comprueba si se han recorrido todos los archivos
        result.add(tuple(files[i] for i in current)) # Se añade la combinación actual al resultado
        return # Termina la recursión
    find_combinations(files, sizes, limit, current + [len(current)], result) # Se prueba a añadir el siguiente archivo a la combinación actual
    find_combinations(files, sizes, limit, current, result) # Se prueba a no añadir el siguiente archivo a la combinación actual
# Se define el límite de 4 MB en kilobytes
limit = 4 * 1024
pdf_files = [] # Se crea una lista vacía para almacenar los nombres de los archivos PDF
pdf_sizes = [] # Se crea una lista vacía para almacenar los tamaños de los archivos PDF en kilobytes
for file in os.listdir(directory): # Se recorre los archivos del directorio
    if file.endswith(".pdf"): # Se comprueba si el archivo es un PDF
        pdf_files.append(file) # Se añade el nombre del archivo a la lista
        size = os.path.getsize(os.path.join(directory, file)) # Se obtiene el tamaño del archivo en bytes
        size = round(size / 1024, 2) # El tamaño se convierte a kilobytes
        pdf_sizes.append(size) # Se añade el tamaño del archivo a la lista
        print(f"{file} - {size} KB") # Se muestra el nombre y el tamaño del archivo
# Se crea una lista vacía para almacenar las posibles combinaciones de archivos
combinations = set()
find_combinations(pdf_files, pdf_sizes, limit, [], combinations) # Se llama a la función para encontrar todas las combinaciones de archivos que sumen menos de 4 MB
print(f"Estas son las posibles combinaciones de archivos que suman menos de {limit} KB:") # Se muestran las posibles combinaciones de archivos
for combination in sorted(combinations):
    total_size = sum([file_size for file in combination]) # Si la combinación creada no sobrepasa los 4mb se agrega las combinaciones
    if total_size < limit:
        print(", ".join(combination))
    else:
        print("No hubo conjuntos o hubo algún error.")
# Se piden los nombres de los archivos a unir separados por comas
selection = input("Introduce los nombres de los archivos PDF que quieres combinar, separados por comas: ")
selection = selection.split(",") # Se convierte la selección a una lista
selected_files = [] # Se crea la lista vacía para almacenar los nombres de los archivos seleccionados
for file in selection: # Se recorre la selección
    file = file.strip() # Se eliminan los espacios en blanco
    if file in pdf_files: # Se comprueba si el archivo esta en la lista de pdfs
        selected_files.append(file) # Se añade el nombre del archivo a la lista de archivos seleccionados
    else:
        print(f"{file} no es un archivo PDF válido") # Se muestra un mensaje de error en caso de que no esté en la lista
# Se pide al usuario que ingrese el nombre del archivo resultante
output_file = input("Introduce el nombre del archivo PDF resultante: ")
if not output_file.endswith(".pdf"): # Se comprueba si el archivo termina en .pdf
    output_file = output_file + ".pdf" # Si no, se le añade
# Se llama a la función para combinar los pdfs
merge_pdfs(selected_files, output_file)
print(f"Los archivos PDF seleccionados se han combinado en {output_file}") # Se muestra un mensaje de confirmación
