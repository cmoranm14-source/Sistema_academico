from abc import ABC, abstractmethod

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# =====================================================================
# CLASE BASE (ABSTRACTA)
# =====================================================================
# Solo dice QUÉ métodos debe tener todo controlador.
# CÓMO se hace cada uno lo escribe cada controlador, de la forma más simple.
class CrudBase(ABC):

    @abstractmethod
    def leer(self):
        pass

    @abstractmethod
    def obtener(self, id_registro):
        pass

    @abstractmethod
    def buscar(self, texto):
        pass

    @abstractmethod
    def siguiente(self):
        pass

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def actualizar(self, id_registro, datos):
        pass

    @abstractmethod
    def eliminar(self, id_registro):
        pass


# =====================================================================
# CONTROLADOR DE CLIENTES
# =====================================================================
class EstudianteController(CrudBase):

    def __init__(self, archivo="data/estudiantes.json"):
        self.gestor = GestorJSON(archivo)

        # Leemos el JSON y convertimos cada diccionario en un objeto Estudiante
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for estudiante in self.lista:
            datos.append(estudiante.a_diccionario())
        self.gestor.guardar(datos)

    def carnets_registrados(self, excepto_id=None):
        """CONJUNTO de carnets ya usados: preguntar 'x in conjunto' es instantáneo."""
        return {r.carnet.upper() for r in self.lista if r.id != excepto_id}

    def validar(self, datos, id_actual=None):
        """Devuelve un mensaje de error, o None si todo está bien."""
        # Al crear, estos campos son obligatorios.
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "carnet"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        # Validamos que el email sea correcto y no esté repetido.
        if "email" in datos:
            email = str(datos["email"]).strip().lower()

            if not es_email_valido(email):
                return f"Email inválido: '{email}'"

            # CONJUNTO: guarda los emails de los demás estudiantes.
            emails_usados = {e.email.strip().lower() for e in self.lista if e.id != id_actual}

            if email in emails_usados:
                return "Ese email ya está registrado"

        # Validamos que el carnet no esté vacío ni repetido.
        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip().upper()
            if carnet == "":
                return "El carnet es obligatorio"
            if carnet in self.carnets_registrados(id_actual):
                return "Ese carnet ya está registrado"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_registro):
        try:
            id_registro = int(id_registro)
        except (TypeError, ValueError):
            return None

        for estudiante in self.lista:
            if estudiante.id == id_registro:
                return estudiante

        return None

    def buscar(self, texto):
        texto = str(texto).strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for estudiante in self.lista:
            if (texto in estudiante.nombre.lower()
                or texto in estudiante.apellido.lower()
                    or texto in estudiante.email.lower()
                    or texto in estudiante.carnet.lower()
                    or texto in estudiante.carrera.lower()):
                encontrados.append(estudiante)
        return encontrados

    def siguiente(self):
        mayor = 0
        for estudiante in self.lista:
            if estudiante.id > mayor:
                mayor = estudiante.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        estudiante = Estudiante(self.siguiente(),
                                str(datos["nombre"]).strip().title(),
                                str(datos["apellido"]).strip().title(),
                                str(datos["email"]).strip().lower(),
                                str(datos["carnet"]).strip().upper(),
                                str(datos.get("carrera", "")).strip().title())
        self.lista.append(estudiante)
        self.guardar()
        return True, f"Estudiante creado: {estudiante.etiqueta()}"

    def actualizar(self, id_registro, datos):
        estudiante = self.obtener(id_registro)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_registro}"
        if not datos:
            return False, "No se indicó ningún cambio"

        # CONJUNTO: campos que se pueden modificar.
        permitidos = {"nombre", "apellido", "email", "carnet", "carrera"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        # Validamos antes de modificar el estudiante.
        error = self.validar(datos, estudiante.id)
        if error:
            return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "carrera"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            elif campo == "carnet":
                valor = valor.upper()
            setattr(estudiante, campo, valor)

        self.guardar()
        return True, f"Estudiante {id_registro} actualizado"

    def eliminar(self, id_registro):
        estudiante = self.obtener(id_registro)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_registro}"
        
        self.lista.remove(estudiante)
        self.guardar()
        return True, f"Estudiante {id_registro} eliminado"

    def carreras(self):
        """CONJUNTO: obtiene las carreras distintas, sin repetirlas."""
        return sorted({e.carrera for e in self.lista if e.carrera.strip()})

# =====================================================================
# CONTROLADOR DE PRODUCTOS
# =====================================================================
class MateriaController(CrudBase):

    def __init__(self, archivo="data/materias.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for materia in self.lista:
            datos.append(materia.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()

            # CONJUNTO: evita códigos repetidos.
            codigos_usados = {m.codigo.upper() for m in self.lista if m.id != id_actual}
            if codigo == "":
                return "El código es obligatorio"

            if codigo in codigos_usados:
                return "Ese código de materia ya existe"

        if "creditos" in datos:
            try:
                creditos = int(datos["creditos"])
            except (TypeError, ValueError):
                return "Los créditos deben ser un número entero"
            if not 1 <= creditos <= 10:
                return "Los créditos deben estar entre 1 y 10"
        if "cupos" in datos:
            try:
                cupos = int(datos["cupos"])
            except (TypeError, ValueError):
                return "Los cupos deben ser un número entero"
            if not 0 <= cupos <= Materia.CUPOS_MAXIMOS:
                return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"
            
        if "nombre" in datos:
            nombre = str(datos["nombre"]).strip().title()
            for otro in self.lista:
                if otro.nombre == nombre and otro.id != id_actual:
                    return f"Ya existe un materia llamado {nombre}"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_registro):
        try:
            id_registro = int(id_registro)
        except (TypeError, ValueError):
            return None

        for materia in self.lista:
            if materia.id == id_registro:
                return materia
        return None

    def buscar(self, texto):
        texto = str(texto).strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for materia in self.lista:
            if (texto in materia.nombre.lower()
                or texto in materia.codigo.lower()):
                    encontrados.append(materia)
        return encontrados

    def siguiente(self):
        mayor = 0
        for materia in self.lista:
            if materia.id > mayor:
                mayor = materia.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error
        materia = Materia(self.siguiente(),
                        str(datos["nombre"]).strip().title(),
                        str(datos["codigo"]).strip().upper(),
                        int(datos.get("creditos", 1)),
                        int(datos.get("cupos", 0)))
        self.lista.append(materia)
        self.guardar()
        return True, f"Materia creada: {materia.etiqueta()}"

    def actualizar(self, id_materia, datos):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe la materia {id_materia}"
        if not datos:
            return False, "No se indicó ningún cambio"

        desconocidos = set(datos) - {"nombre", "codigo", "creditos", "cupos"}
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_materia)
        if error:
            return False, error
            
        if "nombre" in datos:
            materia.nombre = str(datos["nombre"]).strip().title()
        if "codigo" in datos:
            materia.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos:
            materia.creditos = int(datos["creditos"])
        if "cupos" in datos:
            materia.cupos = int(datos["cupos"])

        self.guardar()
        return True, f"Materia {id_materia} actualizada"

    def eliminar(self, id_registro):
        materia = self.obtener(id_registro)
        if materia is None:
            return False, f"No existe la materia {id_registro}"
 
        self.lista.remove(materia)
        self.guardar()
        return True, f"Materia {id_registro} eliminada"

    def materias_sin_cupos(self):
        return [materia for materia in self.lista if materia.cupos == 0]

# =====================================================================
# CONTROLADOR DE MATRICULAS
# =====================================================================
class MatriculaController(CrudBase):

    def __init__(self, estudiantes, materias, archivo="data/matriculas.json"):
        # Utiliza los mismos controladores que main.py.
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Matricula.desde_diccionario(datos))

        # Permite consultar las matrículas desde MateriaController.
        self.materias.matriculas = self

    def guardar(self):
        datos = []
        for matricula in self.lista:
            datos.append(matricula.a_diccionario())
        self.gestor.guardar(datos)

    def leer(self):
        return self.lista

    def obtener(self, id_registro):
        try:
            id_registro = int(id_registro)
        except (TypeError, ValueError):
            return None

        for matricula in self.lista:
            if matricula.id == id_registro:
                return matricula
        return None

    def buscar(self, texto):
        texto = str(texto).strip().lower()
        encontradas = []
        if texto == "":
            return encontradas

        for matricula in self.lista:
            if (texto in matricula.periodo.lower()
                or texto in matricula.id_estudiante.lower()
                or texto in matricula.id_materia.lower()):
                    encontradas.append(matricula)
        return encontradas

    def siguiente(self):
        mayor = 0
        for matricula in self.lista:
            if matricula.id > mayor:
                mayor = matricula.id
        return mayor + 1

    def crear(self, datos):
        """Registra una matrícula y descuenta un cupo."""
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
            materia_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return False, "Los IDs deben ser números enteros"

        periodo = str(datos.get("periodo", "")).strip()
        if not periodo:
            return False, "El periodo académico es obligatorio"

        # CONJUNTOS: comprobar que los IDs existen.
        ids_estudiantes = {e.id for e in self.estudiantes.leer()}
        ids_materias = {m.id for m in self.materias.leer()}

        if estudiante_id not in ids_estudiantes:
            return False, f"No existe el estudiante {estudiante_id}"

        if materia_id not in ids_materias:
            return False, f"No existe la materia {materia_id}"

        materia = self.materias.obtener(materia_id)

        # TUPLA: identifica estudiante, materia y periodo.
        combinacion = (estudiante_id, materia_id, periodo.lower())

        combinaciones_existentes = {(m.estudiante_id, m.materia_id, m.periodo.lower()) for m in self.lista}
        if combinacion in combinaciones_existentes:
            return False, ("El estudiante ya está matriculado en esa materia durante ese periodo")
        if materia.cupos <= 0:
            return False, f"La materia {materia.nombre} no tiene cupos"

        matricula = Matricula(self.siguiente(),
                            estudiante_id,
                            materia_id,
                            periodo)
        
        materia.cupos -= 1
        self.lista.append(matricula)
        self.materias.guardar()
        self.guardar()
        return True, f"Matrícula {matricula.id} registrada correctamente"

    def actualizar(self, id_registro, datos):
        return False, ("Las matrículas no se pueden modificar directamente: retire la matrícula y registre otra.")

    def registrar_nota(self, id_registro, nota):
        matricula = self.obtener(id_registro)
        if matricula is None:
            return False, f"No existe la matrícula {id_registro}"
        if not Materia.es_nota_valido(nota):
            return False, "La nota debe ser un número entre 0 y 20"
        matricula.nota = float(nota)
        self.guardar()
        return True, f"Nota registrada exitosamente {id_registro}"
    
    def eliminar(self, id_registro):  #retirar matricula
        matricula = self.obtener(id_registro)
        if matricula is None:
            return False, f"No existe la matrícula {id_registro}"
        materia = self.materias.obtener(matricula.materia_id)
        if materia is not None:
            # Evita superar el máximo permitido al devolver el cupo.
            if materia.cupos >= Materia.CUPOS_MAXIMOS:
                return False, "No se puede devolver el cupo: se superaría el máximo"
            materia.cupos += 1
            self.materias.guardar()

        self.lista.remove(matricula)
        self.guardar()
        return True, f"Matrícula {id_registro} retirada correctamente"

    def certificado(self, id_estudiante):
        estudiante = self.estudiantes.obtener(id_estudiante)
        if estudiante is None:
            return None
        # DICCIONARIOS: permiten localizar estudiantes y materias por su ID.
        estudiantes_por_id = {e.id: e for e in self.estudiantes.leer()}
        materias_por_id = {m.id: m for m in self.materias.leer()}
        estudiante = estudiantes_por_id.get(int(id_estudiante))
        if estudiante is None:
            return None
        texto = "CERTIFICADO ACADÉMICO\n"
        texto += f"Estudiante: {estudiante.nombre_completo()}\n"
        texto += f"Carnet: {estudiante.carnet}\n"
        texto += f"Carrera: {estudiante.carrera}\n"
        texto += "-" * 45 + "\n"

        matriculas_estudiante = [m for m in self.lista if m.estudiante_id == estudiante.id]
        if not matriculas_estudiante:
            texto += "El estudiante no tiene matrículas registradas.\n"
            return texto
        for matricula in matriculas_estudiante:
            materia = materias_por_id.get(matricula.materia_id)
            if materia is not None:
                texto += (
                    f"Materia: {materia.nombre}\n"
                    f"Periodo: {matricula.periodo}\n"
                    f"Nota: {matricula.nota:.2f}\n"
                    f"Estado: {matricula.estado()}\n"
                    + "-" * 45 + "\n")
        return texto

    def matriculas_por_estudiante(self, estudiante_id):
        """Filtra y devuelve las matrículas de un alumno."""
        try:
            estudiante_id = int(estudiante_id)
        except (TypeError, ValueError):
            return []

        filtradas = []
        for m in self.lista:
            if m.estudiante_id == estudiante_id:
                filtradas.append(m)
        return filtradas

    def promedio_por_estudiante(self, id_estudiante):
        matriculas = self.matriculas_por_estudiante(id_estudiante)
        if not matriculas:
            return None
        return sum(m.nota for m in matriculas) / len(matriculas)

