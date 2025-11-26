from abc import ABC, abstractmethod

class Empleado(ABC):
    _id_counter = 1

    def __init__(self, nombre, salario_base):
        self._nombre = nombre
        self._id_empleado = Empleado._id_counter
        Empleado._id_counter += 1
        self._salario_base = salario_base
        self._proyectos = []

    @abstractmethod
    def calcular_salario(self):
        pass

    def calcular_bono(self):
        return 0

    def mostrar_informacion(self):
        return {
            "Nombre": self._nombre,
            "ID": self._id_empleado,
            "Salario base": self._salario_base,
            "Bono": self.calcular_bono(),
            "Salario total": self.calcular_salario(),
            "Proyectos": len(self._proyectos)
        }

    def asignar_proyecto(self, proyecto):
        if isinstance(self, Gerente):
            raise Exception("Los gerentes no pueden ser asignados como miembros de proyectos.")
        if len(self._proyectos) >= self.max_proyectos:
            raise Exception(f"{self._nombre} ya tiene el máximo de proyectos asignados.")
        if proyecto in self._proyectos:
            raise Exception(f"{self._nombre} ya está en este proyecto.")
        self._proyectos.append(proyecto)
        proyecto.agregar_empleado(self)

    @property
    def proyectos(self):
        return self._proyectos


class Desarrollador(Empleado):
    def __init__(self, nombre, salario_base, lenguajes, nivel):
        super().__init__(nombre, salario_base)
        self.lenguajes = lenguajes
        self.nivel = nivel
        self.max_proyectos = 3

    def calcular_bono(self):
        if self.nivel == "Junior":
            return 200
        elif self.nivel == "SemiSenior":
            return 500
        elif self.nivel == "Senior":
            return 1000
        return 0

    def calcular_salario(self):
        return self._salario_base + self.calcular_bono()


class Gerente(Empleado):
    def __init__(self, nombre, salario_base, departamento):
        super().__init__(nombre, salario_base)
        self.departamento = departamento
        self.equipo = []
        self.max_proyectos = 0

    def calcular_bono(self):
        total_equipo = sum([empleado.calcular_salario() for empleado in self.equipo])
        return 0.15 * total_equipo

    def calcular_salario(self):
        return self._salario_base + self.calcular_bono()

    def agregar_al_equipo(self, empleado):
        if isinstance(empleado, (Desarrollador, Diseñador)):
            self.equipo.append(empleado)
        else:
            raise Exception("Solo se pueden agregar Desarrolladores o Diseñadores al equipo.")


class Diseñador(Empleado):
    def __init__(self, nombre, salario_base, herramientas, especialidad):
        super().__init__(nombre, salario_base)
        self.herramientas = herramientas
        self.especialidad = especialidad
        self.max_proyectos = 2

    def calcular_bono(self):
        bono = 0
        if "Figma" in self.herramientas:
            bono += 300
        elif any(tool in self.herramientas for tool in ["Photoshop", "Illustrator"]) and len(self.herramientas) == 1:
            bono += 200
        if len(self.herramientas) >= 3:
            bono += 400
        return bono

    def calcular_salario(self):
        return self._salario_base + self.calcular_bono()


class Proyecto:
    def __init__(self, nombre, presupuesto):
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.empleados = []

    def agregar_empleado(self, empleado):
        if empleado in self.empleados:
            raise Exception(f"{empleado._nombre} ya está en el proyecto {self.nombre}.")
        if len(empleado.proyectos) >= empleado.max_proyectos:
            raise Exception(f"{empleado._nombre} excede su límite de proyectos.")
        self.empleados.append(empleado)

    def costo_total(self):
        return sum([empleado.calcular_salario() for empleado in self.empleados])

    def viabilidad(self):
        return self.costo_total() <= self.presupuesto * 0.7


class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.empleados = []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def mostrar_empleados(self):
        print(f"\nListado de empleados en {self.nombre}")
        print("-" * 60)
        for emp in self.empleados:
            info = emp.mostrar_informacion()
            print(f"Nombre: {info['Nombre']}")
            print(f"ID: {info['ID']}")
            print(f"Salario base: ${info['Salario base']}")
            print(f"Bono: ${info['Bono']}")
            print(f"Salario total: ${info['Salario total']}")
            print(f"Proyectos asignados: {info['Proyectos']}")
            print("-" * 60)

    def eliminar_empleado(self, id_empleado):
        for emp in self.empleados:
            if emp._id_empleado == id_empleado:
                # Eliminarlo también de los proyectos en los que estaba
                for proyecto in emp.proyectos:
                    if emp in proyecto.empleados:
                        proyecto.empleados.remove(emp)
                self.empleados.remove(emp)
                print(f"Empleado con ID {id_empleado} eliminado correctamente.")
                return
        print(f"No se encontró ningún empleado con ID {id_empleado}.")


# ---------------------------------------------------------
empresa = Empresa("dhylanc.a")

while True:
    entrada = input("\nEscribe 'nuevo' para agregar empleado, 'lista' para ver empleados, 'eliminar' para borrar por ID (o 'salir'): ").strip().lower()

    if entrada == "lista":
        empresa.mostrar_empleados()

    elif entrada == "nuevo":
        tipo = input("Tipo (desarrollador, diseñador, gerente): ").strip().lower()
        nombre = input("Nombre: ")
        salario = float(input("Salario base: "))

        if tipo == "desarrollador":
            lenguajes = input("Lenguajes separados por coma: ").split(",")
            nivel = input("Nivel (Junior, SemiSenior, Senior): ")
            empleado = Desarrollador(nombre, salario, [l.strip() for l in lenguajes], nivel)

        elif tipo == "diseñador":
            herramientas = input("Herramientas separadas por coma: ").split(",")
            especialidad = input("Especialidad (UI, UX, Gráfico): ")
            empleado = Diseñador(nombre, salario, [h.strip() for h in herramientas], especialidad)

        elif tipo == "gerente":
            departamento = input("Departamento: ")
            empleado = Gerente(nombre, salario, departamento)

        else:
            print("Tipo no válido.")
            continue

        empresa.agregar_empleado(empleado)
        print(f"{nombre} agregado correctamente.")

    elif entrada == "eliminar":
        try:
            id_empleado = int(input("Ingresa el ID del empleado a eliminar: "))
            empresa.eliminar_empleado(id_empleado)
        except ValueError:
            print("El ID debe ser un número válido.")

    elif entrada == "salir":
        print("Programa terminado.")
        break

    else:
        print("Comando no reconocido.")