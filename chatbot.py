import streamlit as st 
import groq

# TENER NUESTRO MODELO DE IA 
MODELOS = ["llama3-8b-8192", "llama3-70b-8192"]

# CONFIGURAR PÁGINA
def configurar_pagina():
    st.set_page_config("Chatbot de Chris", page_icon="🌐​")
    st.title("Bienvenidos a la Inteligencia Artificial de Christian Giannattasio")

# MOSTRAR EL SIDEBAR CON LOS MODELOS 
def mostrar_sidebar(): 
    st.sidebar.title("¡Elige tu modelo preferido!")
    modelo_elegido = st.sidebar.selectbox("¿Cuál deseas?", MODELOS, index=0)
    st.write(f"Elegiste el modelo: {modelo_elegido}")
    return modelo_elegido

# CREAR CLIENTE GROQ
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

# INICIALIZAR EL ESTADO DE LOS MENSAJES
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# MOSTRAR HISTORIAL DEL CHAT
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

# OBTENER MENSAJE DE USUARIO
def obtener_mensaje_usuario():
    return st.chat_input("Envía un mensaje")

# AGREGAR MENSAJE AL HISTORIAL
def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

# MOSTRAR MENSAJE EN PANTALLA
def mostrar_mensaje_historial(role, content):
    with st.chat_message(role):
        st.markdown(content)

# OBTENER RESPUESTA DEL MODELO
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content

# FLUJO DE LA APP 
def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    Cliente = crear_cliente_groq()
    inicializacion_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    mostrar_historial_chat()

    if mensaje_usuario:
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensaje_historial("user", mensaje_usuario)

        mensaje_modelo = obtener_respuesta_modelo(Cliente, modelo, st.session_state.mensajes)

        agregar_mensaje_al_historial("assistant", mensaje_modelo)
        mostrar_mensaje_historial("assistant", mensaje_modelo)

if __name__ == "__main__":
    ejecutar_app()
