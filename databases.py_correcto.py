#mongodb+srv://vanessaverde6:hBy1lso1oiwFz36X@prediccion2024.y1yafzs.mongodb.net/
import pandas as pd
import streamlit as st
from pymongo import MongoClient
import certifi

st.title("Prueba de conexión a Mongo DB")

def connection():
    return MongoClient("mongodb+srv://vanessaverde6:hBy1lso1oiwFz36X@prediccion2024.y1yafzs.mongodb.net/", tlsCAFILE=certifi.where())

conexion = connection()

def getData():
    db = conexion.get_database("sample_restaurants")
    collection = db.get_collection("neighborhoods")
    items = collection.find()
    return list(items)

datos = getData()
st.subheader(datos)
st.dataframe(pd.DataFrame(datos))


