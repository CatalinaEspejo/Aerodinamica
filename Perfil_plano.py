import numpy as np
import matplotlib.pyplot as plt

# Parámetros 
c = 1
qinf = 18.24
rho = 1.225  # kg/m3
alfa = np.radians(5)

N = 5
dc = c / N

# Definición de puntos 
x_panel = np.linspace(0, c, N+1)
x = x_panel[:-1] + 0.25*dc      # puntos de vórtice (1/4 ds)
xf = x_panel[:-1] + 0.75*dc     # puntos de colocación (3/4 ds)
y = np.zeros(N)

print("x vortex (1/4 ds):", np.round(x, 3))
print("x collocation (3/4 ds):", np.round(xf, 3))

# Matriz Q 
gamma = np.ones(N)
q = np.zeros((N, N))  

for i in range(N):
    for pos in range(N):
        diferencia = x[pos] - xf[i]
        q[i, pos] = (1 / diferencia) * (dc / 2)

print("\nMatriz Q:")
print(np.round(q, 4))

# Resolver sistema 
sln = np.linalg.solve(q, gamma)
sln = (-1) * sln / (qinf * np.sin(alfa) * dc * np.pi)

deltaL = rho * qinf * (-sln)
L = np.sum(deltaL)

cl = (2 * np.sum(sln)) / qinf
print('\ncl =', cl)
print('\nSolución del sistema:')
print(sln)

# -------- Gráfica --------
plt.figure(figsize=(8,4))
plt.plot(x_panel, np.zeros_like(x_panel), 'k-', linewidth=1.5)
plt.plot(x, y, 'bo', label='Vortices (1/4)')
plt.plot(xf, y, 'ro', label='Puntos de Colocacion (3/4)')

plt.grid()
plt.axis('equal')
plt.legend()
plt.xlabel('$x/c$')
plt.ylabel('$y/c$')
plt.title('método de paneles de vórtices')
plt.show()
