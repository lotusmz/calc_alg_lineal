import numpy as np

class Matriz:
    """Matriz clase y manejo de operaciones"""

    def __init__(self, filas, columnas, datos):
        self.filas = filas
        self.columnas = columnas
        self.datos = datos

    def __str__(self):
        """Convierte matriz a string para mostrarlo"""
        return '\n'.join([' '.join(map(str, fila)) for fila in self.datos])

    def obtener_determinante(self):
        """Obtiene el determinante de la matriz si es cuadrada y de tamaño válido"""
        if self.filas != self.columnas:
            raise ValueError("El determinante solo se puede calcular para matrices cuadradas")

        if self.filas == 1:
            return self.datos[0][0]

        try:
            def submatriz(matriz, fila, columna):
                return [[matriz[i][j] for j in range(len(matriz)) if j != columna] for i in range(len(matriz)) if
                        i != fila]

            return sum((-1) ** c * self.datos[0][c] * Matriz(self.filas - 1, self.columnas - 1,submatriz(self.datos, 0, c)).obtener_determinante() for c in range(self.columnas))

        except Exception as e:
            raise ValueError(f"Error al calcular el determinante: {e}")

    def obtener_inversa(self):
        """Obtiene la inversa de la matriz si es cuadrada y su determinante no es cero"""
        try:
            determinante = self.obtener_determinante()
            if determinante == 0:
                raise ValueError("La matriz no tiene inversa porque su determinante es 0")
        except ValueError as e:
            raise ValueError(f"Error al calcular la inversa: {e}")

        try:
            n = self.filas
            adjunta = [[(-1) ** (i + j) * Matriz(n - 1, n - 1, [fila[:j] + fila[j + 1:] for fila in (
                        self.datos[:i] + self.datos[i + 1:])]).obtener_determinante() for j in range(n)] for i in
                       range(n)]
            inversa = [[adjunta[j][i] / determinante for j in range(n)] for i in range(n)]
            return Matriz(n, n, inversa)
        except Exception as e:
            raise ValueError(f"Error al calcular la inversa: {e}")

    def suma(self, other):
        """Suma de matrices"""
        if self.filas != other.filas or self.columnas != other.columnas:
            raise ValueError("Matrices deben tener las mismas dimensiones")
        resultado = [
            [self.datos[i][j] + other.datos[i][j] for j in range(self.columnas)]
            for i in range(self.filas)
        ]
        return Matriz(self.filas, self.columnas, resultado)

    def resta(self, other):
        """Resta de matrices"""
        if self.filas != other.filas or self.columnas != other.columnas:
            raise ValueError("Matrices deben tener las mismas dimensiones")
        resultado = [
            [self.datos[i][j] - other.datos[i][j] for j in range(self.columnas)]
            for i in range(self.filas)
        ]
        return Matriz(self.filas, self.columnas, resultado)

    def multiplicar_matriz(self, other):
        """Multiplicación de Matrices"""
        if self.columnas != other.filas:
            raise ValueError("El # de columnas de la primera matriz deben == al numero de filas de la segunda matriz")
        resultado = []
        explicacion = []
        for i in range(self.filas):
            fila = []
            for j in range(other.columnas):
                total = 0
                pasos = []
                for k in range(self.columnas):
                    producto = self.datos[i][k] * other.datos[k][j]
                    total += producto
                    pasos.append(f"({self.datos[i][k]}×{other.datos[k][j]})")
                fila.append(total)
                explicacion.append(f"Elemento [{i + 1},{j + 1}]: {' + '.join(pasos)} = {total}")
            resultado.append(fila)
        return Matriz(self.filas, other.columnas, resultado), explicacion

    def multiplicacion_escalar(self, escalar):
        """Multiplicación Escalar"""
        resultado = [
            [element * escalar for element in fila]
            for fila in self.datos
        ]
        return Matriz(self.filas, self.columnas, resultado)


def input_matriz():
    """Maneja el ingreso de la matriz"""
    while True:
        try:
            filas = int(input("Ingrese el # de filas: "))
            columnas = int(input("Ingrese el # de columnas: "))
            if filas <= 0 or columnas <= 0:
                print("Las dimensiones deben ser un # entero positivo")
                continue

            matriz = []
            for i in range(filas):
                while True:
                    fila = input(f"Ingrese los #'s de la fila {i + 1} (separados por un espacio): ").split()
                    if len(fila) != columnas:
                        print(f"Se esperaba {columnas} de valores, se obtuvo {len(fila)}")
                        continue
                    try:
                        matriz.append([float(x) for x in fila])
                        break
                    except ValueError:
                        print("Formato invalido")
            return Matriz(filas, columnas, matriz)
        except ValueError:
            print("Porfavor ingrese #'s validos para las dimensiones")


def get_escalar():
    """Obtiene el escalar ingresado"""
    while True:
        try:
            return float(input("Ingrese el valor del escalar: "))
        except ValueError:
            print("Valor invalido")


def realizar_operacion(operacion, matrices, escalares=None):
    """Ejecuta la operación de matrices y su paso a paso"""
    resultado = matrices[0]
    pasos = []

    for i in range(1, len(matrices)):
        try:
            if operacion == '+':
                nuevo_resultado = resultado.suma(matrices[i])
                simbolo_op = '+'
            elif operacion == '-':
                nuevo_resultado = resultado.resta(matrices[i])
                simbolo_op = '-'
            elif operacion == '*':
                # Revisa si la operación es escalar
                actual_es_escalar = isinstance(resultado, (int, float))
                prox_es_escalar = isinstance(matrices[i], (int, float))

                if actual_es_escalar or prox_es_escalar:
                    # Maneja la multiplicación escalar
                    if actual_es_escalar and prox_es_escalar:
                        # Ambos son escalares
                        nuevo_resultado = resultado * matrices[i]
                        explicacion = []
                        simbolo_op = '×'
                    elif actual_es_escalar:
                        # Escalar * Matriz
                        escalar = resultado
                        matriz = matrices[i]
                        nuevo_resultado = matriz.multiplicacion_escalar(escalar)
                        explicacion = []
                        simbolo_op = '× scalar'
                    else:
                        # Matriz * Escalar
                        escalar = matrices[i]
                        nuevo_resultado = resultado.multiplicacion_escalar(escalar)
                        explicacion = []
                        simbolo_op = '× scalar'
                else:
                    # Multiplicación de matriz
                    nuevo_resultado, explicacion = resultado.multiplicar_matriz(matrices[i])
                    pasos.extend(explicacion)
                    simbolo_op = '×'

                pasos.append(f"{resultado}\n{simbolo_op}\n{matrices[i]}\n=\n{nuevo_resultado}\n")
                resultado = nuevo_resultado
            pasos.append(f"{resultado}\n{simbolo_op}\n{matrices[i]}\n=\n{nuevo_resultado}\n")
            resultado = nuevo_resultado
        except ValueError as e:
            print(f"Error: {e}")
            return None

    print("\nSOLUCIÓN PASO A PASO:")
    for paso in pasos:
        print(paso)
    return resultado


def mostrar_propiedades():
    """Muestra las propiedades de multiplicaciones"""
    print("\nPropiedades de multiplicación:")
    print("1. (A × B) × C = A × (B × C) (Asociativa)")
    print("2. (kA) × B = A × (kB) = k(A × B) (Compatibilidad escalar)")
    print("3. A × (B + C) = A × B + A × C (Distributiva izquierda)")
    print("4. (A + B) × C = A × C + B × C (Distributiva derecha)\n")


def menu_inicio():
    """Menú de Opciones"""
    while True:
        print("\nCalculadora de Algebra Linear")
        print("1. Sumar matrices")
        print("2. Restar matrices")
        print("3. Multiplicar matrices/escalares")
        print("4. Propiedades de multiplicación")
        print("5. Obtener determinante")
        print("6. Obtener inversa de una matriz")
        print("7. Exit")

        opcion = input("Seleccione una opción: ")

        if opcion == '7':
            break

        if opcion == '6':
            matriz = input_matriz()
            try:
                inversa = matriz.obtener_inversa()
                print("La inversa de la matriz es:")
                print(inversa)
            except ValueError as e:
                print(f"Error: {e}")
            continue

        if opcion == '5':
            matriz = input_matriz()
            try:
                determinante = matriz.obtener_determinante()
                print(f"El determinante de la matriz es: {determinante}")
            except ValueError as e:
                print(f"Error: {e}")
            continue

        if opcion == '4':
            mostrar_propiedades()
            continue

        operaciones = {'1': '+', '2': '-', '3': '*'}.get(opcion)
        if not operaciones:
            print("Opción invalida")
            continue

        try:
            contador = int(input("Cuantas matrices/escalares? (min 2): "))
            if contador < 2:
                print("Minimo 2 operandos requeridos")
                continue
        except ValueError:
            print("Número invalido")
            continue

        operandos = []
        for i in range(contador):
            if operaciones == '*' and input(f"El operando {i + 1} es escalar (e) o matriz (m)? ").lower() == 'e':
                operandos.append(get_escalar())
            else:
                operandos.append(input_matriz())

        resultado = realizar_operacion(operaciones, operandos)
        if resultado:
            print("\nRESULTADO:")
            print(resultado)


if __name__ == "__main__":
    menu_inicio()