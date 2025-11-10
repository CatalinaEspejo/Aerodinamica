# ==========================================================
#   CÁLCULO DE LA CIRCULACIÓN (Γ) 
# ==========================================================
# Este script calcula la circulación de un campo de vórtice
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt 
from math import pi 
from scipy.interpolate import RectBivariateSpline   # (aunque aquí no se usa directamente)

# --------------------------------------------
# Definición de la malla de puntos del dominio
# --------------------------------------------
n = 30                   # Número de puntos por eje en la grilla
maxv = 3                 # Límite máximo del dominio
minv = -3                # Límite mínimo del dominio

X = np.linspace(minv, maxv, n)   # Coordenadas X del dominio
Y = np.linspace(minv, maxv, n)   # Coordenadas Y del dominio
x, y = np.meshgrid(X, Y)         # Malla bidimensional (X,Y)

# --------------------------------------------
# Definición del cilindro
# --------------------------------------------
nc = 30                   # Número de puntos sobre la circunferencia
r = 1                     # Radio del cilindro

theta = np.linspace(0, 2*pi, nc)   # Ángulo polar (0 a 2π)
dtheta = theta[1] - theta[0]       # Incremento angular (Δθ)
xc = r * np.cos(theta)             # Coordenadas X de la circunferencia
yc = r * np.sin(theta)             # Coordenadas Y de la circunferencia

# --------------------------------------------
# Campo de velocidades inducido por circulación
# --------------------------------------------
Gam = -2.0                        # Circulación impuesta (valor negativo)
vx = np.zeros((n,n))              # Componente de velocidad en X
vy = np.zeros((n,n))              # Componente de velocidad en Y

# Cálculo de la velocidad inducida en cada punto (xi, yi)
for i in range(n):
  xi = X[i]
  for j in range(n):
    yi = Y[j]
    rxy = xi**2 + yi**2           # Radio cuadrado desde el origen
    fact = 2*pi*rxy               # Factor común para evitar repetición
    vx[j,i] = (Gam*yi)/fact       # Componente x de la velocidad inducida
    vy[j,i] = -(Gam*xi)/fact      # Componente y de la velocidad inducida

# --------------------------------------------
# Velocidad sobre el contorno
# --------------------------------------------
fact = 2*pi*r**2
vfxc = (Gam*yc)/fact              # Componente tangencial en X sobre el cilindro
vfyc = -(Gam*xc)/fact             # Componente tangencial en Y sobre el cilindro

# Derivadas del contorno para integración (dx, dy)
dxc = -r * np.sin(theta) * dtheta
dyc =  r * np.cos(theta) * dtheta

# --------------------------------------------
# Integración de la circulación (método trapecio)
# --------------------------------------------
int1 = np.trapz(vfxc, xc)
int2 = np.trapz(vfyc, yc)
Gamma = -(int1 + int2)            # Circulación total calculada

# --------------------------------------------
# Integración aproximada por sumatoria discreta
# --------------------------------------------
intap1 = 0.0
intap2 = 0.0

for i in range(nc):
  intap1 += vfxc[i] * dxc[i]
  intap2 += vfyc[i] * dyc[i]
Gammap = -(intap1 + intap2)       # Circulación aproximada

# --------------------------------------------
# Resultados en consola
# --------------------------------------------
print('gamma = ', Gamma)          # Resultado usando trapecio
print('Gammap = ', Gammap)        # Resultado usando sumatoria
print('Gammat = ', 2*pi)          # Valor teórico (para comparación)

# --------------------------------------------
# Visualización del campo de velocidades
# --------------------------------------------
Fig = plt.figure(0)
ax = plt.axes()
# ax.scatter(x,y, c='red', marker='o', s=4**2)   
ax.quiver(x, y, vx, vy, color='black')           # Vectores del campo total
plt.plot(xc, yc, 'bo')                           # Contorno del cilindro
ax.quiver(xc, yc, vfxc, vfyc, color='blue')      # Vectores tangenciales en el contorno
ax.quiver(xc, yc, dxc, dyc, color='green')       # Vectores diferenciales (dx, dy)
plt.grid()
plt.gca().set_aspect('equal', 'box')
plt.show()                                       # Mostrar figura


