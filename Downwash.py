# -*- coding: utf-8 -*-
"""
@author: Catalina
"""

import numpy as np
import matplotlib.pyplot as plt
from math import pi

# -------------------------------------------------------------
# Parámetros básicos del ala 
# -------------------------------------------------------------
cl = 0.3004317719988048
V_inf = 10

# taper
tpr = 1

# semienvergadura
b2 = 5.0

# envergadura 
b=2*b2

Croot =0.2*b

Ctip = tpr*Croot

AWing = 2*(0.5*(Croot+Ctip)*b2)

Gamma_0  = (2 * V_inf * AWing *cl )/(b*pi)

# -------------------------------------------------------------
# Cálculo de las distribuciones a lo largo de la envergadura
# -------------------------------------------------------------

# 1. Posiciones a lo largo del semiespacio del ala (de -b/2 a b/2)
y = np.linspace(-b/2, b/2, 200)

# 2. Distribución elíptica de circulación
#    Ecuación: Γ(y) = Γ0 * sqrt(1 - (y / (b/2))²)
Gamma_y = Gamma_0 * np.sqrt(1 - (y / (b/2))**2)

# 3. Downwash constante inducido por la distribución elíptica
#    Ecuación: w = -Γ0 / (2b)
w_const = -Gamma_0 / (2 * b)
w_y = np.full_like(y, w_const)  # Vector horizontal con el mismo valor en todo el ala

# -------------------------------------------------------------
# Gráficas
# -------------------------------------------------------------
plt.figure(figsize=(10, 4))

# --- Gráfica: Distribución elíptica de circulación ---
plt.plot(y, Gamma_y, color='royalblue', linewidth=2.5)
plt.axhline(0, color='k', linestyle='--', linewidth=0.8)
plt.title('Distribución elíptica de circulación', fontsize=13)
plt.ylabel(r'$\Gamma(y)$ [m²/s]', fontsize=11)
plt.xlim(-b/2, b/2)
plt.grid(True, linestyle=':', alpha=0.7)
plt.text(0, Gamma_0*0.92, r'Máximo $\Gamma_0$', ha='center', color='navy')
plt.text(b/2*0.9, 0, 'Extremo del ala', ha='right', va='bottom', color='firebrick')
plt.show()


#--------distribución de la velocidad de downwash-----------

# -----------------------------------------------
Gamma = 5.0       # Circulación (m^2/s)
b = 10.0          # Envergadura total (m)
b_half = b / 2.0  # Semi-envergadura (5 m)

# -----------------------------------------------
# Puntos a lo largo de la envergadura
# -----------------------------------------------
# Construimos el vector 'y' desde -b/2 hasta +b/2, 
# pero sin tocar exactamente las puntas (donde la 
# velocidad inducida se vuelve infinita).
y = np.linspace(-b_half + 0.01, b_half - 0.01, 500)

# -----------------------------------------------
# Cálculo del downwash inducido por los dos vórtices en punta
# -----------------------------------------------
# Cada vórtice induce una velocidad que depende de la distancia
# al punto donde estamos evaluando:
#
#    w(y) = -(Gamma / (2π)) * (1/r1 + 1/r2)
#
# r1: distancia al vórtice derecho  (y = +b/2)
# r2: distancia al vórtice izquierdo (y = -b/2)
#
r1 = b_half - y   # Distancia al vórtice derecho
r2 = b_half + y   # Distancia al vórtice izquierdo

downwash = - (Gamma / (2 * np.pi)) * (1 / r1 + 1 / r2)

# -----------------------------------------------
# Gráfica de la distribución de downwash
# -----------------------------------------------
plt.figure(figsize=(8, 5))

plt.plot(y, downwash, color='royalblue', linewidth=2.5)

plt.title('Downwash distribution')
plt.xlabel('Position along span (m)')
plt.ylabel('Downwash (m/s)')

plt.show()
