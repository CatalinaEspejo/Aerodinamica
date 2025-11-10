# %matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
from math import pi

# ============================================================
# FUNCIÓN PARA IGUALAR ESCALAS EN EJE 3D
# ============================================================
def set_axes_equal(ax):
    """
    Asegura que los ejes de una figura 3D tengan la misma escala.
    Esto permite que esferas y otras geometrías no se distorsionen.
    """
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])

    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)

    plot_radius = 10 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


# ============================================================
# FUNCIÓN DE VELOCIDAD INDUCIDA
# ============================================================
def HSvel(HS, Cpx, Cpy, Cpz, gsingn, k):
    """
    Calcula la velocidad inducida en un punto (Cp) por un vórtice
    """
    tol = 0.00005
    u = v = w = 0
    udw = vdw = wdw = 0

    for i in range(3):
        # Coordenadas relativas
        r1x, r1y, r1z = Cpx - HS[i, 0], Cpy - HS[i, 1], Cpz - HS[i, 2]
        r2x, r2y, r2z = Cpx - HS[i + 1, 0], Cpy - HS[i + 1, 1], Cpz - HS[i + 1, 2]

        # Vector del segmento
        r0x, r0y, r0z = HS[i + 1, 0] - HS[i, 0], HS[i + 1, 1] - HS[i, 1], HS[i + 1, 2] - HS[i, 2]

        # Producto cruzado entre r1 y r2
        r1Xr2_x = r1y * r2z - r1z * r2y
        r1Xr2_y = r1z * r2x - r1x * r2z
        r1Xr2_z = r1x * r2y - r1y * r2x
        norm2 = r1Xr2_x**2 + r1Xr2_y**2 + r1Xr2_z**2

        # Distancias
        r1n = np.sqrt(r1x**2 + r1y**2 + r1z**2)
        r2n = np.sqrt(r2x**2 + r2y**2 + r2z**2)

        # Producto punto
        r0Dr1 = r0x * r1x + r0y * r1y + r0z * r1z
        r0Dr2 = r0x * r2x + r0y * r2y + r0z * r2z

        # Velocidades inducidas
        Gamma = gsingn
        k = Gamma / (4.0 * pi * norm2) * ((r0Dr1 / r1n) - (r0Dr2 / r2n))

        ui, vi, wi = k * r1Xr2_x, k * r1Xr2_y, k * r1Xr2_z

        u += ui
        v += vi
        w += wi

        # Se suman los segmentos longitudinales al downwash
        if i in [0, 2]:
            udw += ui
            vdw += vi
            wdw += wi

    return u, v, w, udw, vdw, wdw


# ============================================================
# PARÁMETROS DEL FLUJO
# ============================================================
Vinf = 10                  # Velocidad del flujo libre
Alpha = 5 * (pi / 180)     # Ángulo de ataque [rad]
rho = 1.225                # Densidad del aire [kg/m³]

# Vector de velocidad libre
Vinf_vector = np.array([Vinf * np.cos(Alpha), 0, Vinf * np.sin(Alpha)])


# ============================================================
# PARÁMETROS GEOMÉTRICOS DEL ALA
# ============================================================
SwA = 45 * (pi / 180)      # Ángulo de flecha
Tpr = 1                    # Relación de estrechamiento
b2 = 5                     # Semienvergadura
b = 2 * b2                 # Envergadura total

DihA = 0 * (pi / 180)      # Ángulo diedro
twist = 0 * (pi / 180)     # Ángulo de torsión

Croot = 0.2 * b            # Cuerda en la raíz
Ctip = Tpr * Croot         # Cuerda en la punta

# Cuerda media geométrica y área
CMG = (2 / 3) * Croot * ((1 + Tpr + Tpr**2) / (1 + Tpr))
AWing = 2 * (0.5 * (Croot + Ctip) * b2)

# Discretización de la superficie
Ny = 5   
Nx = 4   

yb = b2 * np.linspace(0, 1, Ny)
Cx = np.array([0, 1/4, 3/4, 1]) * Croot

# Inicialización de mallas
xgr = np.zeros((Nx, Ny))
ygr = np.zeros((Nx, Ny))
zgr = np.zeros((Nx, Ny))


# ============================================================
# CONSTRUCCIÓN DE LA GEOMETRÍA
# ============================================================
tpr_j = np.linspace(1, Tpr, Ny)
twist_j = np.linspace(0, twist, Ny)
Czr = np.zeros(Nx)

for j in range(Ny):
    ybi = yb[j]
    tpr_loc = tpr_j[j]
    twist_loc = twist_j[j]
    for i in range(Nx):
        xj = tpr_loc * Cx[i]
        zj = tpr_loc * Czr[i]

        
        x_rt = xj * np.cos(twist_loc) + zj * np.sin(twist_loc)
        z_rt = xj * np.sin(twist_loc) + zj * np.cos(twist_loc)

        # Desplazamientos por flecha y diedro
        x_p = x_rt + ybi * np.tan(SwA)
        z_p = z_rt + ybi * np.tan(DihA)

        xgr[i, j], ygr[i, j], zgr[i, j] = x_p, ybi, z_p


# ============================================================
# DEFINICIÓN DEL VÓRTICE
# ============================================================
W_farP = 20 * b
W_vector = np.array([W_farP * np.cos(Alpha), 0, W_farP * np.sin(Alpha)])

xw = np.zeros((2, Ny))
yw = np.zeros((2, Ny))
zw = np.zeros((2, Ny))

for j in range(Ny):
    xw[0, j] = xgr[1, j] + W_vector[0]
    yw[0, j] = ygr[1, j] + W_vector[1]
    zw[0, j] = zgr[1, j] + W_vector[2]
    xw[1, j], yw[1, j], zw[1, j] = xgr[1, j], ygr[1, j], zgr[1, j]


# ============================================================
# CÁLCULO DE PUNTOS DE COLOCACIÓN Y NORMALES
# ============================================================
xcp = np.zeros(Ny - 1)
ycp = np.zeros(Ny - 1)
zcp = np.zeros(Ny - 1)
unvx = np.zeros(Ny - 1)
unvy = np.zeros(Ny - 1)
unvz = np.zeros(Ny - 1)
RHS = np.zeros(Ny - 1)

for j in range(Ny - 1):
    # Definición de panel
    p1x, p1y, p1z = xgr[0, j], ygr[0, j], zgr[0, j]
    p2x, p2y, p2z = xgr[0, j + 1], ygr[0, j + 1], zgr[0, j + 1]
    p3x, p3y, p3z = xgr[2, j], ygr[2, j], zgr[2, j]
    p4x, p4y, p4z = xgr[2, j + 1], ygr[2, j + 1], zgr[2, j + 1]

    # Punto de colocación (centro del cuarto de cuerda)
    xcpi = (p3x + p4x) / 2
    ycpi = (p3y + p4y) / 2
    zcpi = (p3z + p4z) / 2

    # Vector normal
    Ax, Ay, Az = xcpi - p1x, ycpi - p1y, zcpi - p1z
    Bx, By, Bz = xcpi - p2x, ycpi - p2y, zcpi - p2z

    nvx, nvy, nvz = By * Az - Bz * Ay, Bz * Ax - Bx * Az, Bx * Ay - By * Ax
    mnv = np.sqrt(nvx**2 + nvy**2 + nvz**2)

    xcp[j], ycp[j], zcp[j] = xcpi, ycpi, zcpi
    unvx[j], unvy[j], unvz[j] = nvx / mnv, nvy / mnv, nvz / mnv

    # Condición de impermeabilidad
    RHS[j] = -np.dot(Vinf_vector, np.array([nvx, nvy, nvz])) / mnv


# ============================================================
# CÁLCULO DE COEFICIENTES INFLUENCIALES (MATRICES A Y B)
# ============================================================
HS_i = np.zeros((4, 3))
a_coeffs = np.zeros((Ny - 1, Ny - 1))
b_coeffs = np.zeros((Ny - 1, Ny - 1))

for j in range(Ny - 1):
    xcpi, ycpi, zcpi = xcp[j], ycp[j], zcp[j]
    unvxi, unvyi, unvzi = unvx[j], unvy[j], unvz[j]

    for k in range(Ny - 1):
        # Coordenadas del vórtice
        HS_i[0, :] = [xw[0, k], yw[0, k], zw[0, k]]
        HS_i[1, :] = [xw[1, k], yw[1, k], zw[1, k]]
        HS_i[2, :] = [xw[1, k + 1], yw[1, k + 1], zw[1, k + 1]]
        HS_i[3, :] = [xw[0, k + 1], yw[0, k + 1], zw[0, k + 1]]

        gsing = 1
        u_hs, v_hs, w_hs, ud_hs, vd_hs, wd_hs = HSvel(HS_i, xcpi, ycpi, zcpi, gsing, k)

        # Imagen reflejada
        HS_i[:, 1] *= -1
        u_hsL, v_hsL, w_hsL, ud_hsL, vd_hsL, wd_hsL = HSvel(HS_i, xcpi, ycpi, zcpi, -gsing, k)

        # Superposición
        u_hs += u_hsL
        v_hs += v_hsL
        w_hs += w_hsL
        ud_hs += ud_hsL
        vd_hs += vd_hsL
        wd_hs += wd_hsL

        a_coeffs[j, k] = unvxi * u_hs + unvyi * v_hs + unvzi * w_hs
        b_coeffs[j, k] = unvxi * ud_hs + unvyi * vd_hs + unvzi * wd_hs


# ============================================================
# SOLUCIÓN DE LAS ECUACIONES
# ============================================================
Gammas = np.linalg.solve(a_coeffs, RHS)
ws = np.dot(b_coeffs, Gammas)

# Cálculo de sustentación e inducida
L = 0.0
Di = 0.0

for j in range(Ny - 1):
    Delta_y = ygr[0, j + 1] - ygr[0, j]
    Delta_L = rho * Vinf * Gammas[j] * Delta_y
    Delta_D = rho * ws[j] * Gammas[j] * Delta_y
    L += Delta_L
    Di += Delta_D

CL = 2 * L / (0.5 * rho * Vinf**2 * AWing)
print("Coeficiente de Sustentación (CL):", CL)


# ============================================================
# VISUALIZACIÓN 3D
# ============================================================
fig1 = plt.figure()
ax = plt.axes(projection='3d')
ax.set_proj_type('ortho')
set_axes_equal(ax)

# Superficie y vórtices
ax.plot_wireframe(xgr, ygr, zgr, color='black')
ax.plot_wireframe(xgr, -ygr, zgr, color='black')
ax.plot_wireframe(xw, yw, zw, color='blue', alpha=0.2)
ax.plot_wireframe(xw, -yw, zw, color='blue', alpha=0.2)

# Puntos de control y normales
ax.scatter3D(xcp, ycp, zcp, color='red', s=100)
ax.quiver(xcp, ycp, zcp, unvx, unvy, unvz, arrow_length_ratio=0.1)

ax.set_xlabel('$X$')
ax.set_ylabel('$Y$')
ax.set_zlabel('$Z$')
plt.show()
