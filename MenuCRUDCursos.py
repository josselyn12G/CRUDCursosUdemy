# ==========================================================
# SISTEMA CRUD DE CURSOS - SQL SERVER CON PYTHON
# Autor: Freire, Guevara y Llanos
# Descripción:
# Aplicación en consola que permite insertar, consultar,
# actualizar y eliminar cursos en SQL Server.
# Incluye validación de campos obligatorios y manejo de errores.
# ==========================================================

# 1. Importar la biblioteca necesaria para la conexión
import pyodbc

# =====================================================
# 2. CONFIGURACIÓN DE PARÁMETROS DE CONEXIÓN
# =====================================================
# Nombre del servidor 
NAME_SERVER = '.\\SQLEXPRESS'
# Nombre de la base de datos
DATABASE = 'UDEMYTEST1'
# Credenciales para autenticación SQL Server
USERNAME = 'pythonconsultor'
PASSWORD = 'UDLA'
# Controlador ODBC utilizado
CONTROLADOR_ODBC = 'SQL Server'
# =====================================================
# 3. CADENA DE CONEXIÓN
# =====================================================

# 3.1 Conexión mediante autenticación SQL Server
connection_string = f'DRIVER={CONTROLADOR_ODBC};SERVER={NAME_SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

# ==========================================================
# 2. FUNCIONES DE VALIDACIÓN
# ==========================================================

# Función para solicitar un texto obligatorio.
def pedir_texto_obligatorio(mensaje, max_longitud=None):
    # Se repite hasta que el usuario ingrese un valor válido.
    while True:
        # Se solicita el dato al usuario y se eliminan espacios al inicio y al final.
        valor = input(mensaje).strip()
        # Se valida que el campo no esté vacío.
        if valor == "":
            # Se muestra un mensaje cuando el campo está vacío.
            print("Error: este campo es obligatorio y no puede estar vacío.")
        # Se valida que el texto no supere la longitud máxima permitida.
        elif max_longitud and len(valor) > max_longitud:
            # Se muestra error si el texto excede el límite de caracteres.
            print(f"Error: el texto no puede superar {max_longitud} caracteres.")
        else:
            # Si el dato es válido, se retorna el valor.
            return valor


# Función para solicitar un número entero obligatorio.
def pedir_entero_obligatorio(mensaje):
    # Se repite hasta que el usuario ingrese un número entero válido.
    while True:
        try:
            # Se solicita el dato, se eliminan espacios y se convierte a entero.
            valor = int(input(mensaje).strip())
            # Se valida que el número entero sea positivo mayor a cero.
            if valor <= 0:
                # Se muestra error si el valor es cero o negativo.
                print("Error: el ID debe ser un número entero positivo.")
            else:
                # Se retorna el número entero ingresado.
                return valor
        except ValueError:
            # Se muestra error si el dato ingresado no es un número entero.
            print("Error: debe ingresar un número entero válido.")


# Función para solicitar un número decimal obligatorio.
def pedir_decimal_obligatorio(mensaje):
    # Se repite hasta que el usuario ingrese un número decimal válido.
    while True:
        try:
            # Se solicita el dato, se eliminan espacios y se convierte a decimal.
            valor = float(input(mensaje).strip())
            # Se valida que el precio sea mayor a cero.
            if valor <= 0:
                # Se muestra error si el precio es cero o negativo.
                print("Error: el valor debe ser mayor a cero.")
            else:
                # Se retorna el número decimal válido.
                return valor
        except ValueError:
            # Se muestra error si el dato ingresado no es numérico.
            print("Error: debe ingresar un número decimal válido.")


# ==========================================================
# 3. FUNCIÓN INSERTAR REGISTRO
# ==========================================================

# Función para insertar un nuevo curso en la tabla Cursos.
def insertar_registro(conexion):
    try:
        # Se muestra el título de la operación.
        print("\n\tINSERTAR CURSO\n")
        # Se solicita el ID del curso, validando que sea entero positivo.
        idcurso = pedir_entero_obligatorio("Ingrese ID del curso: ")
        # Se solicita el nombre del curso, validando que no esté vacío y no supere 255 caracteres.
        nombre = pedir_texto_obligatorio("Ingrese nombre del curso: ", max_longitud=255)
        # Se solicita la descripción, validando que no esté vacía y no supere 500 caracteres.
        descripcion = pedir_texto_obligatorio("Ingrese descripción: ", max_longitud=500)
        # Se solicita el precio por hora, validando que sea decimal y mayor a cero.
        precio_hora = pedir_decimal_obligatorio("Ingrese precio por hora: ")
        # Se solicita el tipo de curso, validando que no esté vacío y no supere 50 caracteres.
        tipo_curso = pedir_texto_obligatorio("Ingrese tipo de curso: ", max_longitud=50)
        # Se crea el cursor para ejecutar comandos SQL.
        cursor = conexion.cursor()
        # Se consulta si ya existe un curso con el mismo ID.
        cursor.execute("SELECT COUNT(*) FROM Cursos WHERE IDCurso = ?", (idcurso,))
        # Se obtiene el resultado de la consulta.
        existe = cursor.fetchone()[0]
        # Se valida si el ID ya existe.
        if existe > 0:
            # Se muestra mensaje específico si el curso ya está registrado.
            print("\nError: ya existe un curso registrado con ese ID.")
            return
        # Sentencia SQL parametrizada para evitar SQL Injection.
        sql = """
            INSERT INTO Cursos 
            (IDCurso, NombreCurso, Descripcion, PrecioxHora, TipoCurso)
            VALUES (?, ?, ?, ?, ?)
        """
        # Se ejecuta el INSERT enviando los valores como parámetros.
        cursor.execute(sql, (idcurso, nombre, descripcion, precio_hora, tipo_curso))
        # Se confirman los cambios en la base de datos.
        conexion.commit()
        # Se muestra mensaje de éxito.
        print("\nCurso insertado correctamente.")
    except pyodbc.IntegrityError as e:
        # Se captura un error de integridad, como clave primaria duplicada.
        print("\nError de integridad: no se pudo insertar el curso.")
        print("Detalle:", e)
    except Exception as e:
        # Se revierte cualquier cambio pendiente si ocurre un error inesperado.
        conexion.rollback()
        # Se captura cualquier otro error inesperado.
        print("\nError al insertar:", e)

# ==========================================================
# 4. FUNCIÓN CONSULTAR REGISTROS
# ==========================================================

# Función para consultar todos los cursos registrados.
def consultar_registros(conexion):
    try:
        # Se muestra el título de la operación.
        print("\n\tLISTA DE CURSOS\n")
        # Se crea el cursor para ejecutar la consulta.
        cursor = conexion.cursor()
        # Consulta SQL para obtener todos los cursos.
        sql = """
            SELECT IDCurso, NombreCurso, Descripcion, PrecioxHora, TipoCurso
            FROM Cursos
        """
        # Se ejecuta la consulta SQL.
        cursor.execute(sql)
        # Se obtienen todos los registros encontrados.
        registros = cursor.fetchall()
        # Se imprime una línea separadora para la tabla.
        print("-" * 100)
        # Se imprimen los encabezados de la tabla con formato alineado.
        print(f"{'ID':<5} {'NOMBRE':<25} {'DESCRIPCIÓN':<30} {'PRECIO/HORA':>12} {'TIPO':<15}")
        # Se imprime otra línea separadora.
        print("-" * 100)
        # Se valida si no existen registros.
        if len(registros) == 0:
            # Se muestra mensaje cuando la tabla está vacía.
            print("No existen cursos registrados.")
        else:
            # Se recorre cada registro obtenido de la base.
            for r in registros:
                # Se imprime cada fila con formato de tabla.
                print(
                    f"{r.IDCurso:<5} "
                    f"{r.NombreCurso:<25} "
                    f"{str(r.Descripcion):<30} "
                    f"{float(r.PrecioxHora):>12.2f} "
                    f"{r.TipoCurso:<15}"
                )
        # Se imprime línea final de la tabla.
        print("-" * 100)
        # Se imprime el total de registros encontrados.
        print(f"Total de registros: {len(registros)}\n")
    except Exception as e:
        # Se captura cualquier error durante la consulta.
        print("\nError al consultar:", e)


# ==========================================================
# 5. FUNCIÓN ACTUALIZAR REGISTRO
# ==========================================================

# Función para actualizar los datos de un curso existente.
def actualizar_registro(conexion):
    try:
        # Se muestra el título de la operación.
        print("\n\tACTUALIZAR CURSO\n")
        # Se solicita únicamente el ID del curso que se desea actualizar.
        idcurso = pedir_entero_obligatorio("Ingrese ID del curso a actualizar: ")
        # Se crea el cursor para ejecutar consultas SQL.
        cursor = conexion.cursor()
        # Se consulta si existe un curso con el ID ingresado.
        sql_buscar = """
            SELECT IDCurso, NombreCurso, Descripcion, PrecioxHora, TipoCurso
            FROM Cursos
            WHERE IDCurso = ?
        """
        # Se ejecuta la consulta enviando el ID como parámetro.
        cursor.execute(sql_buscar, (idcurso,))
        # Se obtiene el registro encontrado.
        curso = cursor.fetchone()
        # Se valida si no existe ningún curso con ese ID.
        if curso is None:
            # Se muestra un mensaje específico y se finaliza la función.
            print("\nError: no existe un curso con el ID ingresado.")
            return
        # Se muestran los datos actuales del curso antes de actualizar.
        print("\nCurso encontrado:")
        print(f"ID: {curso.IDCurso}")
        print(f"Nombre actual: {curso.NombreCurso}")
        print(f"Descripción actual: {curso.Descripcion}")
        print(f"Precio actual: {curso.PrecioxHora}")
        print(f"Tipo actual: {curso.TipoCurso}")
        # Se solicitan los nuevos datos solo si el curso existe.
        # Se valida que el nuevo nombre no supere 255 caracteres.
        nombre = pedir_texto_obligatorio("\nNuevo nombre: ", max_longitud=255)
        # Se solicita la nueva descripción, validando que no esté vacía y no supere 500 caracteres.
        descripcion = pedir_texto_obligatorio("Nueva descripción: ", max_longitud=500)
        # Se solicita el nuevo precio, validando que sea mayor a cero.
        precio_hora = pedir_decimal_obligatorio("Nuevo precio por hora: ")
        # Se solicita el nuevo tipo de curso, validando que no esté vacío y no supere 50 caracteres.
        tipo_curso = pedir_texto_obligatorio("Nuevo tipo de curso: ", max_longitud=50)
        # Sentencia SQL para actualizar el curso.
        sql_actualizar = """
            UPDATE Cursos
            SET NombreCurso = ?, 
                Descripcion = ?, 
                PrecioxHora = ?, 
                TipoCurso = ?
            WHERE IDCurso = ?
        """
        # Se ejecuta el UPDATE con los nuevos valores.
        cursor.execute(sql_actualizar, (nombre, descripcion, precio_hora, tipo_curso, idcurso))
        # Se confirman los cambios en la base de datos.
        conexion.commit()
        # Se muestra mensaje de éxito.
        print("\nCurso actualizado correctamente.")
    except Exception as e:
        # Se revierte cualquier cambio pendiente si ocurre un error.
        conexion.rollback()

        # Se captura cualquier error durante la actualización.
        print("\nError al actualizar:", e)

# ==========================================================
# 6. FUNCIÓN ELIMINAR REGISTRO
# ==========================================================

# Función para eliminar un curso por ID.
def eliminar_registro(conexion):
    try:
        # Se muestra el título de la operación.
        print("\n\tELIMINAR CURSO\n")
        # Se solicita el ID del curso a eliminar.
        idcurso = pedir_entero_obligatorio("Ingrese ID del curso a eliminar: ")
        # Se crea el cursor para ejecutar el DELETE.
        cursor = conexion.cursor()
        # Sentencia SQL para eliminar el curso por su ID.
        sql = "DELETE FROM Cursos WHERE IDCurso = ?"
        # Se ejecuta la eliminación enviando el ID como parámetro.
        cursor.execute(sql, (idcurso,))
        # Se valida si no se eliminó ningún registro.
        if cursor.rowcount == 0:
            # Se muestra mensaje si el curso no existe.
            print("\nError: no existe un curso con el ID ingresado.")
            return
        # Se confirman los cambios en la base de datos.
        conexion.commit()
        # Se muestra mensaje de éxito.
        print("\nCurso eliminado correctamente.")
    except pyodbc.IntegrityError as e:
        # Se revierte la transacción si ocurre un error.
        conexion.rollback()
        # Se convierte el error a texto para analizarlo.
        mensaje_error = str(e)
        # En SQL Server, el error 547 suele indicar conflicto con FOREIGN KEY.
        if "547" in mensaje_error:
            # Mensaje específico cuando no se puede eliminar por dependencia.
            print("\nError: no se puede eliminar el curso porque tiene registros relacionados en otra tabla.")
            print("Debe eliminar primero los registros dependientes o revisar las relaciones de clave foránea.")
        else:
            # Mensaje general de integridad.
            print("\nError de integridad al eliminar el curso.")
            print("Detalle:", e)
    except Exception as e:
        # Se revierte cualquier cambio pendiente si ocurre un error inesperado.
        conexion.rollback()

        # Se muestra el error general.
        print("\nError al eliminar:", e)


# ==========================================================
# 7. MENÚ PRINCIPAL
# ==========================================================

# Función que muestra el menú de opciones del sistema CRUD
def mostrar_opciones_crud():
    # Encabezado del menú
    print("\n\t----------------------------")
    print("\t   SISTEMA CRUD CURSOS")
    print("\t----------------------------")

    # Opciones disponibles
    print("\t1. Crear curso")
    print("\t2. Consultar cursos")
    print("\t3. Actualizar curso")
    print("\t4. Eliminar curso")
    print("\t5. Salir\n")

# ==========================================================
# 8. PROGRAMA PRINCIPAL
# ==========================================================

# Se inicializa la variable conexión en None para evitar errores si falla la conexión.
conexion = None

try:
    # Se intenta establecer la conexión con SQL Server.
    conexion = pyodbc.connect(connection_string)
    # Se muestra mensaje si la conexión fue exitosa.
    print("\nConexión exitosa a la base de datos.\n")
    # Se inicia el ciclo principal del menú.
    while True:
        # Se muestran las opciones del CRUD.
        mostrar_opciones_crud()
        # Se solicita al usuario seleccionar una opción.
        opcion = input("Seleccione una opción (1-5): ").strip()
        # Si la opción es 1, se llama a la función insertar.
        if opcion == '1':
            insertar_registro(conexion)
        # Si la opción es 2, se llama a la función consultar.
        elif opcion == '2':
            consultar_registros(conexion)
        # Si la opción es 3, se llama a la función actualizar.
        elif opcion == '3':
            actualizar_registro(conexion)
        # Si la opción es 4, se llama a la función eliminar.
        elif opcion == '4':
            eliminar_registro(conexion)
        # Si la opción es 5, se termina el programa.
        elif opcion == '5':
            print("\nSaliendo del programa...")
            break
        # Si la opción no corresponde al menú, se muestra error.
        else:
            print("Opción inválida. Debe seleccionar una opción entre 1 y 5.")
except pyodbc.Error as e:
    # Se captura error de conexión o error propio de SQL Server.
    print("\nError de conexión o de base de datos:")
    print(e)
except Exception as e:
    # Se captura cualquier otro error inesperado.
    print("\nError inesperado:")
    print(e)
finally:
    # Se valida que la conexión exista antes de intentar cerrarla.
    if conexion is not None:
        # Se cierra la conexión con la base de datos.
        conexion.close()
        # Se muestra mensaje confirmando el cierre.
        print("\nConexión cerrada.")