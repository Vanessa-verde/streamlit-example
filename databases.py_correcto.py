#mongodb+srv://vanessaverde6:hBy1lso1oiwFz36X@prediccion2024.y1yafzs.mongodb.net/
import pandas as pd
import streamlit as st
from pymongo import MongoClient
import certifi
import _thread
import weakref

st.title("Prueba de conexión a MongoDB")

#def my_hash_func(reference_obj):
    #return hash(id(reference_obj))

# Función de conexión a MongoDB
def connection():
    return MongoClient("mongodb+srv://" + st.secrets["DB_USERNAME"] + ":" + st.secrets[
        "DB_PASSWORD"] + "@prediccion2024.y1yafzs.mongodb.net/", tlsCAFile=certifi.where())

conexion = connection()

# Función para obtener datos desde MongoDB
@st.cache_data(ttl=60)
def getData():
    db = conexion.get_database("sample_restaurants")
    collection = db.get_collection("neighborhoods")
    items = collection.find()
    return list(items)
#lectura de datos

@st.cache_data(ttl=60) #guarda los datos en cash y se invalidan despues de 1 minuto
def getData():
    db = conexion.get_database("sample_restaurants")
    collection = db.get_collection("neighborhoods")
    items = collection.find()
    return list(items)

def getSpecificDoc(condicion):
    db = conexion.get_database("sample_restaurants")
    collection = db.get_collection("tareas")
    items = collection.find()
    return list(items)
'''
def insertData():
    db = conexion.get_database("sample_restaurants")
    nuevaCollection = db.create_collection("inventario")
    nuevaCollection.insert.many(newData)
'''
def insertNewData(newData):
    db = conexion.get_database("sample_restaurants")
    collection = db.get_collection("tareas")
    collection.insert_one(newData)


# Obtener datos
datos = getData()

# Crear DataFrame
df = pd.DataFrame(datos)

# Eliminar columna _id
df = df.drop('_id', axis=1)

# Mostrar DataFrame en Streamlit
st.subheader("Primeros 10 datos sin la columna _id")
st.dataframe(df.head(10))

# Cargar DataFrame desde un archivo CSV en la carpeta "datos"
archivo_csv = "datoss/Inventory.csv"
dfInventory = pd.read_csv(archivo_csv)

# Mostrar DataFrame de Inventory
st.subheader("datos")
st.dataframe(dfInventory.head(15))

'''
id:1
name:"tarea1"
puntos:10
materia"materia1"
fechaEntrega:2022-03-26T00:00:00
fechaCreacion:2022-04-01T22:00:00
'''

st.title("Get una tarea")
buscar = {"id" : {"$gt":20}}
st.write(getSpecificDoc(buscar))

# Vamos a insertar nuevos datos en una nueva colección llamada "inventario"
st.title("Insertar nuevas tareas")


# Formulario para ingresar nuevas tareas
with st.form("miFormulario"):
    nombre_tarea = st.text_input("Nombre tarea:")
    puntos = st.number_input("Elige una puntuación:", 0, 10)
    nombre_materia = st.text_input("Nombre materia:")
    fecha_creacion = st.date_input("Fecha creación:")
    fecha_entrega = st.date_input("Fecha entrega:")
    enviado = st.form_submit_button("Enviar datos")

if enviado:
    # Crear un nuevo registro de tarea
    nueva_tarea = {
        "id": 100,
        "name": nombre_tarea,
        "puntos": puntos,
        "materia": nombre_materia,
        "fechaEntrega": str(fecha_entrega),  # Convertir a cadena de texto
        "fechaCreacion": str(fecha_creacion)  # Convertir a cadena de texto
    }

    # Insertar nuevo registro en la colección "inventario"
    insertNewData(nueva_tarea)

# Validar conexión a MongoDB
try:
    conexion.server_info()
    st.success("Conexión exitosa a MongoDB")
except Exception as e:
    st.error(f"Fallo en la conexión a MongoDB: {e}")


from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})



