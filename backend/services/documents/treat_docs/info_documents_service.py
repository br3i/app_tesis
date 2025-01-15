import os
import PyPDF2
import re
import time

def extract_text_from_pages(document_path):
    """
    Extrae el texto de todas las páginas de un archivo PDF desde el inicio hasta encontrar el patrón "RESUELVE:".

    Args:
        document_path (str): Ruta al archivo PDF.

    Returns:
        tuple: Texto combinado de todas las páginas desde el inicio hasta encontrar el patrón "RESUELVE:" y el número de la página en la que se encontró.
    """
    total_text = ""
    final_page = None  # Inicializa el número de página donde se encontró "RESUELVE:"
    third_last_page = None
    fallback_page = 0

    replace_patterns = [
        (r"[\n\r\f]", " "), 
        (r"\s{2,}", " ")
    ]
    clean_patterns = [
        (r"^\s*ESPOCH ESCUELA SUPERIOR POLITÉCNICA DE CHIMBORAZO DIRECCIÓN DE SECRETARÍA GENERAL", "")
    ]
    search_patterns = [
        r"unanimidad,.*?RESUELVE\s*:\s*(Art[íi]culo)"
    ]

    with open(document_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

        # Iterar desde la página inicial hasta la última página
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text().strip()
            # print("\n[[info_docs_service]] Texto bruto inicial:", repr(page_text))

            # Primer procesamiento: Replace patterns
            for pattern, replacement in replace_patterns:
                page_text = re.sub(pattern, replacement, page_text)
            # print("\n[[info_docs_service]] Después de replace_patterns:", repr(page_text))

            # Segundo procesamiento: Clean patterns
            for pattern, replacement in clean_patterns:
                page_text = re.sub(pattern, replacement, page_text)
            # print("\n[[info_docs_service]] Después de clean_patterns:", repr(page_text))
            page_text = page_text.strip()
            total_text += page_text  # Concatenar texto de cada página con un espacio en blanco
            # print("\n\n\n[[info_docs_service]] Total_text acumulado:", repr(total_text))
            # time.sleep(3)

            # Actualizar la penúltima página (solo si es válida)
            if page_num == len(reader.pages) - 3:
                third_last_page = page_num
                
            # Buscar el patrón "unanimidad, - - RESUELVE - - : - - Art[ií]culo"
            for search_pattern in search_patterns:
                if re.search(search_pattern, page_text, flags=re.IGNORECASE):
                    final_page = page_num  # Guardar la página donde se encontró el patrón
                    print(f"[[info_docs_service]] Patrón encontrado: {search_pattern} en página {page_num}")
                    break  # Detener la búsqueda después de encontrar el patrón

    total_text = re.sub(r"\…{2,}", "FIRMA", total_text, flags=re.IGNORECASE)
    total_text = re.sub(r"\s{2,}", " ", total_text, flags=re.IGNORECASE)
    if final_page is not None:
        return total_text, final_page
    # Si no se encontró el patrón, devolver la penúltima página
    elif third_last_page is not None:
        return total_text, third_last_page
    else:
        if total_pages <= 2:
            fallback_page = 0
        else:
            fallback_page = total_pages - 3
        return total_text, fallback_page

def extract_text_resolve(document_path, start_page):
    """
    Extrae el texto desde una página específica hasta el final del documento, comenzando en la página especificada,
    sin buscar ningún patrón específico.

    Args:
        document_path (str): Ruta al archivo PDF.
        start_page (int): Número de página desde la cual comenzar a extraer (1-indexed).

    Returns:
        str: El texto completo extraído desde la página especificada hasta el final del documento.
    """
    full_text = ""

    # Lista de patrones para reemplazar en el texto de cada página
    replace_patterns = [
        (r"[\n\r\f]", " "),  # Reemplazar saltos de línea y otros caracteres de nueva línea por un espacio
        (r"\s{2,}", " "),     # Reemplazar múltiples espacios por un solo espacio
        (r"\…{2,}", "FIRMA"),  # Reemplazar secuencias de puntos suspensivos por "FIRMA"
        (r"^ESPOCH ESCUELA SUPERIOR POLITÉCNICA DE CHIMBORAZO DIRECCIÓN DE SECRETARÍA GENERAL", ""),
        (r"^\s*ESPOCH ESCUELA SUPERIOR POLITÉCNICA DE CHIMBORAZO DIRECCIÓN DE SECRETARÍA GENERAL", "")
    ]

    with open(document_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        # Asegurarse de que la página inicial esté dentro de un rango válido
        if start_page < 0 or start_page > len(reader.pages):
            raise ValueError("El número de página inicial está fuera del rango del documento.")

        # Iterar desde la página especificada hasta la última página
        for page_num in range(start_page, len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text().strip()
            #print(f"\n[info_docs_service] Extrayendo texto de la página {page_num + 1}: {repr(page_text)}")
            #time.sleep(10)

            # Aplicar los patrones de reemplazo
            for pattern, replacement in replace_patterns:
                #print(f"[info_docs_service] Reemplazando con '{replacement}': {pattern}")
                page_text = re.sub(pattern, replacement, page_text, flags=re.IGNORECASE)
            #print(f"[info_docs_service] Texto después de reemplazar: {repr(page_text)}")
            #time.sleep(10)

            # Concatenar el texto procesado de cada página
            full_text += page_text
            #print(f"[info_docs_service] Texto acumulado: {repr(full_text)}")
            #time.sleep(20)
    return full_text

def extract_text_from_first_page(document_path):
    """
    Extrae el texto de la primera página de un archivo PDF.

    Args:
        document_path (str): Ruta al archivo PDF.

    Returns:
        str: Texto extraído de la primera página.
    """
    with open(document_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        first_page = reader.pages[0]
        return first_page.extract_text()

def separate_text_into_paragraphs(text):
    # Lista de patrones para dividir el texto
    split_patterns = [
        r'(?=Que,)'  # Captura todo después de "Que," y lo incluye como inicio de cada párrafo
    ]
    
    # Aplicar cada patrón de separación de manera secuencial
    for pattern in split_patterns:
        text = re.sub(pattern, '\n', text)  # Sustituimos el patrón por un salto de línea
    # Limpiar el texto resultante, eliminando saltos de línea innecesarios y espacios
    paragraphs = text.split('\n')  # Dividir el texto en párrafos usando saltos de línea
    # Limpiar y asegurar que los párrafos no estén vacíos
    paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]


    # Devolver los párrafos
    return paragraphs

def process_paragraphs(paragraphs):
    # Lista de patrones para buscar las coincidencias
    search_patterns = [
        r"Que,(.*?)(;|:|,)"
    ]

    # Lista para almacenar las coincidencias
    article_entity = []

    print("Procesando párrafos...")
    for paragraph in paragraphs:
        for pattern in search_patterns:
            matches = re.findall(pattern, paragraph, flags=re.IGNORECASE)
            if matches:
            # Si hay coincidencias, añadirlas a la lista
                for match in matches:
                    article_entity.append(match[0])

    print(f"\n[info_docs_service] Total de coincidencias encontradas: {len(article_entity)}")
    return article_entity

def get_resolution(text):
    search_patterns = [
        r"RESOLUCI[ÓO]N \d{3}\s*\.CP\.\d{4,5}"  # Patrón para encontrar las resoluciones
    ]

    clean_patterns = [
        (r"\s+", ""),  # Eliminar todos los espacios dentro de la resolución
        (r"(RESOLUCI[ÓO]N)(\d+)", r"\1 \2")  # Volver a poner un solo espacio entre "RESOLUCIÓN" y el número
    ]

    # Buscar la primera coincidencia utilizando los patrones de búsqueda
    resolution = None
    for pattern in search_patterns:
        match = re.search(pattern, text)  # Usar re.search para encontrar solo la primera coincidencia
        if match:
            resolution = match.group(0)  # Obtener la coincidencia encontrada
            break  # Detener la búsqueda después de encontrar la primera coincidencia

    if not resolution:
        return None  # Si no se encuentra ninguna resolución

    # Limpiar la resolución encontrada
    for pattern, replacement in clean_patterns:
        resolution = re.sub(pattern, replacement, resolution)

    return resolution


def get_resolve(text):
    """
    Procesa el texto dado buscando el patrón "RESUELVE:", descartando todo lo anterior
    y reemplazando las ocurrencias de ciertas cadenas por un espacio vacío.

    Args:
        text (str): El texto en el cual realizar las modificaciones.

    Returns:
        str: El texto procesado con las modificaciones solicitadas.
    """
    # Buscar "RESUELVE:" y descartar todo el texto antes de él
    #resolve_index = re.search(r"unanimidad.*?RESUELVE:\s*(Art[íi]culo)", text, re.IGNORECASE)
    
    patterns = [
        r"unanimidad,.*?RESUELVE\s*:\s*(Art[íi]culo)",
        r"unanimidad,.*?RESUELVE:\s*(Art[íi]culo)",
        r"RESUELVE:\s*(Art[íi]culo)",
        r"RESUELVE:"
    ]

    resolve_index = None
    i = 0
    for pattern in patterns:
        #print("[info_docs_service] get_resolve :", i)
        i =+ 1
        resolve_index = re.search(pattern, text, flags=re.IGNORECASE)
        if resolve_index:
            break
    
    # Si se encuentra un patrón "RESUELVE:", procesar el texto
    if resolve_index:
        # Extraer el texto desde "RESUELVE:" hasta el final
        text = text[resolve_index.start():]

    # Reemplazar las ocurrencias de las cadenas especificadas por un espacio vacío
    text = re.sub(r"\s{2,}", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[\n\r\f]", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\…{2,}", "FIRMA", text, flags=re.IGNORECASE)

    return text


def get_info_document(document_path):
    if document_path:
        print(f"\n[info_docs_service] Procesando archivo: {document_path}")

        # Extraer texto de la primera página
        text_name_resolution = extract_text_from_first_page(document_path)
        # print("\n\n\Text_name_resolution:\n\n", text_name_resolution)

        # Extraer texto de una página
        total_text, final_page = extract_text_from_pages(document_path)
        # time.sleep(5)
        # print("\n\n[info_docs_service ]Total_text:\n\n", total_text[-10000:]) #total_text[-70000:]
        #print("\n\n\t[info_docs_service ] final_page:", final_page)
        # time.sleep(5)
        resolution = get_resolution(text_name_resolution)
        
        #Imprimir la resolución encontrada
        # print("\n[info_docs_service] Resolución encontrada:", resolution)

        text_resolve = extract_text_resolve(document_path, final_page)

        # print("\n\n\t [info_docs_service] Text_resolve:", text_resolve)
        resolve = get_resolve(text_resolve)

        if resolution:
            resolve = resolution + " resuelve: por " + resolve
        # print("\n\n\n[info_docs_service] RESOLVE:\n", resolve)

        paragraphs = separate_text_into_paragraphs(total_text)
        # print("\n\n\t [info_docs_service] Paragraphs:", paragraphs)
        

        # Procesar los párrafos y extraer los artículos y sus entidades
        # print("[info_documents_service] resolution: ", resolution)
        articles_entities = process_paragraphs(paragraphs)
        #time.sleep(200)


        #Imprimir artículos y entidades
        # if articles_entities:
        #     # print("\nArtículos y Entidades encontradas:")
        #     for i, (article_entity, delimiter) in enumerate(articles_entities):
        #         print(f"{i + 1}: {article_entity.strip()}")
        
        return resolution, articles_entities, resolve, final_page+1
    else:
        print("No se encontro el archivo.")
        return None, None, None, None

