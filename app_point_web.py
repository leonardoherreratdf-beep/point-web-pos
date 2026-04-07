import streamlit as st
import pandas as pd
from datetime import datetime
from collections import Counter

# --- Configuración de Página Point Servicios ---
st.set_page_config(page_title="Point Servicios - Web POS", layout="wide")

# Estilo Neon/Dark (Personalizado para Point)
st.markdown("""
    <style>
    .main { background-color: #0f0f11; color: white; }
    .stButton>button { width: 100%; background-color: #2ecc71; color: black; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #16161a; color: white; border-color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- Base de Datos en Sesión (Simulación de Nube) ---
if 'productos' not in st.session_state:
    st.session_state.productos = [
        {"cod": "G-923", "nom": "Volante Logitech G923 PS5/PC", "pre": 850000, "cat": "Gaming", "stk": 5},
        {"cod": "PS5-SL", "nom": "Consola PlayStation 5 Slim", "pre": 1200000, "cat": "Gaming", "stk": 8},
        {"cod": "HAS-615", "nom": "Controlador Fiscal Hasar 615", "pre": 540000, "cat": "Fiscal", "stk": 3},
        {"cod": "LOG-MX", "nom": "Mouse Logitech MX Master 3S", "pre": 125000, "cat": "Periféricos", "stk": 12},
        {"cod": "TP-AR1", "nom": "Router TP-Link Archer AX55", "pre": 95000, "cat": "Informática", "stk": 10}
    ]

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- Lógica de Negocio ---
def agregar_al_carrito(idx):
    if st.session_state.productos[idx]['stk'] > 0:
        st.session_state.productos[idx]['stk'] -= 1
        st.session_state.carrito.append(st.session_state.productos[idx])
    else:
        st.error("¡Sin stock disponible!")

def vaciar_carrito():
    st.session_state.carrito = []
    st.success("Venta finalizada y carrito limpio.")

# --- Interfaz Web ---
st.title("🚀 Point Servicios | Tienda Web")
st.subheader("Río Grande - Comodoro Rivadavia")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 📦 Catálogo de Productos")
    # Mostrar productos como tarjetas o tabla
    for i, p in enumerate(st.session_state.productos):
        with st.container():
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            c1.write(f"**{p['nom']}**")
            c2.write(f"${p['pre']:,.0f}")
            c3.write(f"Stock: {p['stk']}")
            if c4.button("Añadir 🛒", key=f"btn_{i}"):
                agregar_al_carrito(i)
                st.rerun()
        st.divider()

with col2:
    st.write("### 🚚 Datos de Envío")
    nombre = st.text_input("Nombre o Razón Social")
    domicilio = st.text_input("Dirección de Entrega")
    localidad = st.selectbox("Localidad", ["Río Grande", "Comodoro Rivadavia", "Ushuaia", "Otros"])
    
    st.write("### 🛒 Resumen de Compra")
    if st.session_state.carrito:
        total = sum(item['pre'] for item in st.session_state.carrito)
        conteo = Counter([item['nom'] for item in st.session_state.carrito])
        
        for nom, cant in conteo.items():
            st.text(f"{cant} x {nom}")
        
        st.metric(label="TOTAL A COBRAR", value=f"${total:,.2f}")
        
        # Generar Ticket de Texto para descargar
        ticket_str = f"POINT SERVICIOS - TICKET\n"
        ticket_str += f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n"
        ticket_str += f"Cliente: {nombre}\n"
        ticket_str += f"Dirección: {domicilio}, {localidad}\n"
        ticket_str += "-"*30 + "\n"
        for nom, cant in conteo.items():
            ticket_str += f"{cant} x {nom}\n"
        ticket_str += "-"*30 + "\n"
        ticket_str += f"TOTAL: ${total:,.2f}\n"
        ticket_str += "GRACIAS POR TU COMPRA"

        st.download_button(
            label="🖨️ Descargar Comanda",
            data=ticket_str,
            file_name=f"ticket_{nombre}.txt",
            mime="text/plain"
        )
        
        if st.button("✅ Finalizar Venta"):
            vaciar_carrito()
            st.rerun()
    else:
        st.info("El carrito está vacío.")