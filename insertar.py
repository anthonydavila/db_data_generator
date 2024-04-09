from faker import Faker
import psycopg2
from tqdm import tqdm

# Configuración de la conexión a la base de datos PostgreSQL
DB_HOST = 'localhost'
DB_NAME = 'tienda_libros'
DB_USER = 'postgres'
DB_PASSWORD = 'horus'

# Función para insertar registros en la base de datos
def insertar_registros():
    # Crear una instancia de Faker
    faker = Faker()

    # Crear una conexión a la base de datos
    try:
        connection = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = connection.cursor()

        # Inicializar la barra de progreso
        with tqdm(total=400000, desc="Insertando registros") as pbar:
            # Generar y agregar registros a la base de datos
            for _ in range(400000):  # Generar 400,000 registros de ejemplo
                titulo = faker.sentence()
                autor = faker.name()
                año = faker.random_int(min=1900, max=2023)
                isbn = faker.isbn13()

                # Insertar en la tabla 'autor'
                query = "INSERT INTO autor (nombre) VALUES (%s)"
                cursor.execute(query, (autor,))

                # Obtener el ID del autor recién insertado
                autor_id = cursor.lastrowid

                # Insertar en la tabla 'book'
                query = "INSERT INTO book (title, year, isbn, autor_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (titulo, año, isbn, autor_id))

                # Actualizar la barra de progreso
                pbar.update(1)

        # Confirmar los cambios y cerrar la conexión
        connection.commit()
        print("Registros insertados correctamente.")

    except (Exception, psycopg2.Error) as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        # Cerrar la conexión
        if connection:
            cursor.close()
            connection.close()

# Llamar a la función para insertar los registros en la base de datos
insertar_registros()
