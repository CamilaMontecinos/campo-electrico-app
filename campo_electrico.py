# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 22:07:20 2025

@author: camil
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constante de Coulomb
k = 9e9  # Nm^2/C^2

# Posiciones fijas de las 4 cargas
posiciones = np.array([
    [-1.0, -1.0],
    [1.0, -1.0],
    [1.0, 1.0],
    [-1.0, 1.0]
])

def calcular_fuerzas_totales(xq, yq, q_vals):
    F_total = np.array([0.0, 0.0])
    vectores = []
    for i, r in enumerate(posiciones):
        q = q_vals[i] * 1e-6
        r_vec = np.array([xq, yq]) - np.array(r)
        r_mag = np.linalg.norm(r_vec)
        if r_mag < 1e-5:
            F = np.array([0.0, 0.0])
        else:
            F = k * q * 1e-9 / r_mag**3 * r_vec
        vectores.append(F)
        F_total += F
    return vectores, F_total

st.title("Campo eléctrico generado por 4 cargas fijas")

xq = st.slider("Posición x de la carga de prueba", -1.5, 1.5, 0.0, 0.1)
yq = st.slider("Posición y de la carga de prueba", -1.5, 1.5, 0.0, 0.1)

q_vals = []
for i in range(4):
    q = st.slider(f"Carga q{i+1} (μC)", -5.0, 5.0, [1.0, -1.0, 1.0, -1.0][i], 0.1)
    q_vals.append(q)

vectores, F_total = calcular_fuerzas_totales(xq, yq, q_vals)

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_title("Flechas de fuerza eléctrica")

# Dibuja cargas
for i, r in enumerate(posiciones):
    ax.plot(*r, 'ko')
    ax.text(r[0]+0.1, r[1]+0.1, f'q{i+1}', fontsize=10, weight='bold')

# Dibuja vectores
for i, F in enumerate(vectores):
    color = 'blue' if q_vals[i] > 0 else 'red'
    ax.quiver(xq, yq, *F, angles='xy', scale_units='xy', scale=1e-5, color=color)

# Vector total
ax.quiver(xq, yq, *F_total, angles='xy', scale_units='xy', scale=1e-5, color='green')

st.pyplot(fig)
