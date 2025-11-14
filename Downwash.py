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