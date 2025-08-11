# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 19:46:29 2025

@author: camil
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle, FancyBboxPatch

# Constante de Coulomb
k = 9e9  # Nm²/C²

# Posiciones fijas de las 4 cargas
posiciones = [
    [-1.0, -1.0],
    [1.0, -1.0],
    [1.0, 1.0],
    [-1.0, 1.0]
]

# Cargas iniciales (rango -1 a 1 µC para sliders)
cargas_valores = [0, 0, 0, 0]

def calcular_fuerzas_totales(xq, yq, q_vals):
    F_total = np.array([0.0, 0.0])
    vectores = []
    for i, r in enumerate(posiciones):
        q = q_vals[i] * 1e-6  # µC -> C
        r_vec = np.array([xq, yq]) - np.array(r)
        r_mag = np.linalg.norm(r_vec)
        if r_mag < 1e-5:
            F = np.array([0.0, 0.0])
        else:
            # Factor 1e-9 para mantener escalas visuales razonables
            F = k * q * 1e-9 / r_mag**3 * r_vec
        vectores.append(F)
        F_total += F
    return vectores, F_total

# Figura principal y layout
plt.style.use('default')
fig, ax = plt.subplots(figsize=(9, 6), facecolor='white')
# Dejamos espacio a la derecha para sliders y la caja de la fórmula
plt.subplots_adjust(left=0.1, right=0.65, bottom=0.15)

# Ejes del plano
ax.set_facecolor('white')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_title("Visualización fuerza eléctrica entre cargas puntuales", pad=20)
ax.grid(True, linestyle=':', alpha=0.7)

# Dibujar cargas
for i, r in enumerate(posiciones):
    ax.plot(*r, 'ko', markersize=10)
    ax.text(r[0]+0.1, r[1]+0.1, f'q{i+1}', fontsize=12, weight='bold')

# Punto de prueba inicial
xq0, yq0 = 0.0, 0.0
vectores, F_total = calcular_fuerzas_totales(xq0, yq0, cargas_valores)

# Flechas individuales y resultante
flechas = []
for i, F in enumerate(vectores):
    color = 'blue' if cargas_valores[i] > 0 else 'red'
    flecha = ax.quiver(xq0, yq0, *F, angles='xy', scale_units='xy',
                       scale=1e-5, color=color, width=0.005)
    flechas.append(flecha)

flecha_total = ax.quiver(xq0, yq0, *F_total, angles='xy', scale_units='xy',
                         scale=1e-5, color='green', width=0.007)

# Sliders
sliders = []
labels = ['x', 'y', 'q1 (µC)', 'q2 (µC)', 'q3 (µC)', 'q4 (µC)']
inits = [0.0, 0.0] + cargas_valores
limits = [(-1.0, 1.0), (-1.0, 1.0)] + [(-1.0, 1.0)] * 4

# Posición vertical de los sliders (columna derecha)
y_pos_inicial = 0.70
delta_y = 0.08

for i, (label, val, (vmin, vmax)) in enumerate(zip(labels, inits, limits)):
    ax_slider = plt.axes([0.75, y_pos_inicial - i*delta_y, 0.2, 0.04], facecolor='#f5f5f5')
    step = 0.25 if i >= 2 else 0.1
    s = Slider(
        ax=ax_slider,
        label=label,
        valmin=vmin,
        valmax=vmax,
        valinit=val,
        valstep=step,
        track_color='#dddddd',
        facecolor='#1f77b4'
    )
    ax_slider.xaxis.label.set_color('black')
    ax_slider.tick_params(axis='both', colors='black')
    sliders.append(s)

# Leyenda
legend_elements = [
    Rectangle((0,0), 1, 1, color='blue', label='Fuerza de repulsión'),
    Rectangle((0,0), 1, 1, color='red', label='Fuerza de atracción'),
    Rectangle((0,0), 1, 1, color='green', label='Fuerza resultante')
]
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.25, 1),
          framealpha=1, edgecolor='black')

# === Caja con la Ley de Coulomb en la columna derecha, debajo de los sliders ===
# Calculamos la parte inferior del último slider para ubicar la caja debajo
ultimo_slider_bottom = y_pos_inicial - (len(labels)-1)*delta_y
margen_bajo = 0.02      # separación desde el borde inferior de la figura
altura_caja = max(0.18, ultimo_slider_bottom - 0.02)  # altura visible (ajustable)
# Eje para la caja (columna derecha, ancho similar al de sliders)
ax_formula = fig.add_axes([0.7, margen_bajo, 0.26, altura_caja])
ax_formula.set_axis_off()

box = FancyBboxPatch(
    (0, 0), 1, 1,
    transform=ax_formula.transAxes,
    linewidth=1, edgecolor='black',
    facecolor='white', boxstyle="round,pad=0.12"
)
ax_formula.add_patch(box)

ax_formula.text(0.5, 0.72, "Ley de Coulomb — Fuerza eléctrica",
                ha='center', va='center', fontsize=10, weight='bold',
                transform=ax_formula.transAxes)
ax_formula.text(
    0.5, 0.42,
    r"$\vec{F}_{12} =k\dfrac{q_1 q_2}{r^2}\,\hat{u}_r$",
    ha='center', va='center', fontsize=12, transform=ax_formula.transAxes
)
ax_formula.text(
    0.5, 0.14,
    r"$k \approx 9\times10^{9}\ \dfrac{Nm^2}{C^2}$",
    ha='center', va='center', fontsize=9, transform=ax_formula.transAxes
)

# Función de actualización
def update(val):
    xq = sliders[0].val
    yq = sliders[1].val
    q_vals = [s.val for s in sliders[2:]]

    vectores, F_total = calcular_fuerzas_totales(xq, yq, q_vals)

    for i, F in enumerate(vectores):
        flechas[i].set_UVC(*F)
        flechas[i].set_offsets([xq, yq])
        flechas[i].set_color('blue' if q_vals[i] > 0 else 'red')

    flecha_total.set_UVC(*F_total)
    flecha_total.set_offsets([xq, yq])
    fig.canvas.draw_idle()

for s in sliders:
    s.on_changed(update)


fig.text(0.5, 0.01, u"© Domenico Sapone, Camila Montecinos", 
         ha='center', va='bottom', fontsize=9, color='gray')


plt.show()
