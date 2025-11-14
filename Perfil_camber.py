import numpy as np
import matplotlib.pyplot as plt

# Parámetros del perfil
# número de paneles 
# para visualizar la grafica del cp vs x (n = 500) 
n = 10       
c = 1.0           # cuerda
e = 0.1*c        
rho = 1.225        # densidad del aire [kg/m³]
V = 1.0            # velocidad libre
alpha = np.radians(0)
U_inf = V * np.cos(alpha)
W_inf = V * np.sin(alpha)
Q_inf = 0.5 * rho * V**2

# Línea de la cuerda y línea de curvatura
x = np.linspace(0.001, c, n)
eta = 4 * e * (x / c) * (1 - x / c)  
xc = (np.linspace(0.001, c, n-1))/c 

# Puntos de vortice y colocacion 
vx = np.zeros(n-1)
vy = np.zeros(n-1)
cx = np.zeros(n-1)
cy = np.zeros(n-1)
nx = np.zeros(n-1)
ny = np.zeros(n-1)
tx = np.zeros(n-1)
ty = np.zeros(n-1)

for k in range(n - 1):
    dy = eta[k + 1] - eta[k]
    dx = x[k + 1] - x[k]
    ds = np.sqrt(dy**2 + dx**2)
    alfai = np.arctan(-dy / dx)

    # Vórtice (1/4 ds)
    vx[k] = x[k] + (ds / 4) * np.cos(alfai)
    vy[k] = eta[k] - (ds / 4) * np.sin(alfai)

    # Punto de colocación (3/4 ds)
    cx[k] = x[k] + (3 * ds / 4) * np.cos(alfai)
    cy[k] = eta[k] - (3 * ds / 4) * np.sin(alfai)

    # Vectores unitarios
    nx[k] = np.sin(alfai)
    ny[k] = np.cos(alfai)
    tx[k] = np.cos(alfai)
    ty[k] = -np.sin(alfai)

# Funcion de influencia vortice 2D
def vor2d(x, z, x1, z1, gamma=1.0):
    rx = x - x1
    rz = z - z1
    r = np.sqrt(rx**2 + rz**2)
    if r < 1e-5:
        return 0.0, 0.0
    v = 0.5 / np.pi * gamma / r
    u = v * (rz / r)
    w = v * (-rx / r)
    return u, w

# Matriz de influencia A y vector RHS
A = np.zeros((n - 1,  n - 1))
RHS = np.zeros(n - 1)

for i in range(n - 1):
    for j in range(n - 1):
        u, w = vor2d(cx[i], cy[i], vx[j], vy[j], 1.0)
        A[i, j] = u * nx[i] + w * ny[i]
    RHS[i] = -U_inf * nx[i] - W_inf * ny[i]

# Solucion del sistema 
gamma = np.linalg.solve(A, RHS)

#---- Calculo de los coefientes --------
dx = c / (n-1)
DL = rho * V * gamma
DCP = DL / dx / Q_inf

# Solución analítica del delta Cp
DCP_analit = np.zeros(n-1)
for i in range(n-1):
    DD = 32.0 * e / c * np.sqrt(x[i] / c * (1 - x[i] / c))
    DCP_analit[i] = 4.0 * np.sqrt((c - x[i]) / x[i]) * alpha + DD

# Coeficiente de sustentación
BL = np.sum(DL)
CL = BL / (Q_inf * c)
CL_analit = 2.0 * np.pi * (alpha + 2 * e / c)

# Figura 1: distribucion de los vortices y puntos de estancamiento
plt.figure(figsize=(7, 5))
plt.plot(x, eta, '-', color='k')
plt.plot(vx, vy, 'm.', label='Vórtices (1/4 ds)')
plt.plot(cx, cy, 'o', label='Puntos de colocación (3/4 ds)')
plt.quiver(cx, cy, nx, ny, color='r', scale=18, label='Vectores normales')
plt.quiver(cx, cy, tx, ty, color='g', scale=18, label='Vectores tangentes')
plt.axis('equal')
plt.grid()
plt.legend()
plt.xlabel('$x/c$')
plt.ylabel('$η/c$')
plt.title('Método de Paneles de Vórtices')
plt.show()

# Figura 2: distribucion del delta_cp vs x/c
plt.figure(figsize=(8, 5))
plt.plot(xc, DCP, 'orange', label='Numérico')
plt.plot(xc, DCP_analit, 'r-', label='Analítico')
plt.grid()
plt.xlabel('$x/c$')
plt.ylabel('$ΔC_p$')
plt.title('Distribución de ΔCp vs x/c a lo largo de la cuerda')
plt.legend()
plt.show()

# Resultados 
print("\n ------ Resultado metodo de vortices -------- ")
print(f"Ángulo de ataque: 0°")
print(f"CL (numérico)   = {CL:.4f}")
print(f"CL (analítico)  = {CL_analit:.4f}\n")

print("i    x/c     ΔCp(num)    ΔCp(analit)")
for i in range(n-1):
    print(f"{i+1:2d}   {xc[i]:6.3f}     {DCP[i]:9.4f}     {DCP_analit[i]:9.4f}")

print("\n--- Matriz de influencia A ---")
print(A)
print("\n--- Vector solución (Γ) ---")
print(gamma)

# ---- Guardar datos ----
data = np.column_stack((vx, vy, cx, cy, nx, ny, tx, ty, gamma, DCP))
header = 'vx,vy,cx,cy,nx,ny,tx,ty,gamma,DeltaCp'
np.savetxt('paneles_vortices.txt', data, delimiter=',', header=header, comments='')
print("\nDatos guardados en 'paneles_vortices.txt'")

