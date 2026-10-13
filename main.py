
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error,
    imprimir_info, confirmar)
from views import EstudianteController, MateriaController, MatriculaController

# =====================================================================
# CONTROLADORES
# =====================================================================

# Se crea un solo controlador de cada tipo.
# Matriculas recibe los mismos estudiantes y materias.
estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)

# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================

def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    """Devuelve un entero o None si el usuario escribió otra cosa."""
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    """Muestra el resultado que devuelve el controlador."""
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    """Muestra una lista de estudiantes, materias o matrículas."""
    if not objetos:
        imprimir_info(vacio)
        return

    for objeto in objetos:
        print(f"  {objeto}")

    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    """Muestra los campos de un objeto."""
    for clave, valor in objeto.a_diccionario().items():
        nombre_campo = str(clave).replace("_", " ").capitalize()
        print(f"  {nombre_campo:<16}: {valor}")


# =====================================================================
# MENÚ DE ESTUDIANTES
# =====================================================================

def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")

    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: "),
    }

    mostrar_resultado(*estudiantes.crear(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(
        estudiantes.leer(),
        "Todavía no hay estudiantes registrados."
    )
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")

    encontrados = estudiantes.buscar(termino)
    mostrar_lista(encontrados, "No se encontraron estudiantes.")
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")

    estudiante = estudiantes.obtener(pedir_entero("Id: "))

    if estudiante is None:
        imprimir_error("Estudiante no encontrado")
    else:
        mostrar_detalle(estudiante)

    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)

    if estudiante is None:
        imprimir_error("Estudiante no encontrado")
        return pausa()

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}

    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*estudiantes.actualizar(id_estudiante, cambios))
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)

    if estudiante is None:
        imprimir_error("Estudiante no encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante.etiqueta()}")

    if confirmar("¿Confirma la eliminación?"):
        mostrar_resultado(*estudiantes.eliminar(id_estudiante))
    else:
        imprimir_info("Operación cancelada")

    pausa()


# =====================================================================
# MENÚ DE MATERIAS
# =====================================================================

def crear_materia():
    imprimir_titulo("CREAR MATERIA")

    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Código: "),
        "creditos": input("Créditos: "),
        "cupos": input("Cupos disponibles: "),
    }

    mostrar_resultado(*materias.crear(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavía no hay materias registradas.")
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o código: ")

    encontrados = materias.buscar(termino)
    mostrar_lista(encontrados, "No se encontraron materias.")
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")

    materia = materias.obtener(pedir_entero("Id: "))

    if materia is None:
        imprimir_error("Materia no encontrada")
    else:
        mostrar_detalle(materia)

    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")

    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)

    if materia is None:
        imprimir_error("Materia no encontrada")
        return pausa()

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}

    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*materias.actualizar(id_materia, cambios))
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")

    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)

    if materia is None:
        imprimir_error("Materia no encontrada")
        return pausa()

    imprimir_info(f"Se eliminará: {materia.etiqueta()}")

    if confirmar("¿Confirma la eliminación?"):
        mostrar_resultado(*materias.eliminar(id_materia))
    else:
        imprimir_info("Operación cancelada")

    pausa()


# =====================================================================
# MENÚ DE MATRÍCULAS
# =====================================================================

def registrar_matricula():
    imprimir_titulo("REGISTRAR MATRÍCULA")

    imprimir_info("Estudiantes disponibles:")
    mostrar_lista(estudiantes.leer(), "No hay estudiantes registrados.")

    imprimir_info("Materias disponibles:")
    mostrar_lista(materias.leer(), "No hay materias registradas.")

    estudiante_id = pedir_entero("\nId del estudiante: ")
    materia_id = pedir_entero("Id de la materia: ")

    if estudiante_id is None or materia_id is None:
        imprimir_error("Los IDs deben ser números enteros")
        return pausa()

    periodo = input("Periodo académico (ej. 2026-2): ").strip()

    datos = {
        "estudiante_id": estudiante_id,
        "materia_id": materia_id,
        "periodo": periodo,
    }

    mostrar_resultado(*matriculas.crear(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")

    mostrar_lista(
        matriculas.leer(),
        "Todavía no hay matrículas registradas."
    )
    pausa()


def registrar_nota():
    imprimir_titulo("REGISTRAR NOTA")

    mostrar_lista(
        matriculas.leer(),
        "No hay matrículas para registrar notas."
    )

    id_matricula = pedir_entero("\nId de la matrícula: ")

    if id_matricula is None:
        imprimir_error("El ID debe ser un número entero")
        return pausa()

    nota = input("Nota (de 0 a 20): ").strip()

    mostrar_resultado(
        *matriculas.registrar_nota(id_matricula, nota)
    )
    pausa()


def generar_certificado():
    imprimir_titulo("CERTIFICADO ACADÉMICO")

    id_estudiante = pedir_entero("Id del estudiante: ")

    if id_estudiante is None:
        imprimir_error("El ID debe ser un número entero")
        return pausa()

    texto = matriculas.certificado(id_estudiante)

    if texto is None:
        imprimir_error("Estudiante no encontrado")
    else:
        print()
        print(texto)

    pausa()


def retirar_matricula():
    imprimir_titulo("RETIRAR MATRÍCULA")

    mostrar_lista(
        matriculas.leer(),
        "No hay matrículas registradas."
    )

    id_matricula = pedir_entero("\nId de la matrícula: ")

    if id_matricula is None:
        imprimir_error("El ID debe ser un número entero")
        return pausa()

    matricula = matriculas.obtener(id_matricula)

    if matricula is None:
        imprimir_error("Matrícula no encontrada")
        return pausa()

    imprimir_info(f"Se retirará: {matricula.etiqueta()}")

    if confirmar("¿Confirma el retiro de la matrícula?"):
        mostrar_resultado(
            *matriculas.retirar_matricula(id_matricula)
        )
    else:
        imprimir_info("Operación cancelada")

    pausa()


# =====================================================================
# RESUMEN DEL SISTEMA
# =====================================================================

def resumen():
    imprimir_titulo("RESUMEN ACADÉMICO")

    carreras = sorted(estudiantes.carreras())
    sin_cupos = materias.materias_sin_cupos()
    aprobadas = matriculas.matriculas_aprobadas()

    print(f"  Estudiantes registrados : {len(estudiantes.leer())}")
    print(f"  Materias registradas    : {len(materias.leer())}")
    print(f"  Matrículas registradas  : {len(matriculas.leer())}")
    print(f"  Matrículas aprobadas    : {len(aprobadas)}")

    print("\nCarreras registradas:")
    if carreras:
        for carrera in carreras:
            print(f"  - {carrera}")
    else:
        print("  Ninguna")

    print("\nMaterias sin cupos disponibles:")
    mostrar_lista(sin_cupos, "Todas las materias tienen cupos.")

    pausa()


# =====================================================================
# MENÚS: OPCIÓN -> (TEXTO, FUNCIÓN)
# =====================================================================

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por ID", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por ID", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Registrar matrícula", registrar_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota),
    "4": ("Generar certificado", generar_certificado),
    "5": ("Retirar matrícula", retirar_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    """Utiliza el mismo bucle para los tres submenús."""
    while True:
        imprimir_titulo(titulo)

        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")

        print()
        tecla = input("Opción: ").strip()

        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = opciones[tecla]

        if funcion is None:
            break

        funcion()


# =====================================================================
# MENÚ PRINCIPAL
# =====================================================================

def main():
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")
        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("MATERIAS", MENU_MATERIAS)
        elif tecla == "3":
            ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)
        elif tecla == "4":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego 👋!")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
