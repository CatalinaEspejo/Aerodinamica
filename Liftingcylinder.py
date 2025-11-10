import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline

# Parameters
U_inf = 1.0
r = 1

def cylinder(Gam, case):
    # Check for Gamma
    if Gam > 0:
        Gam = -Gam
    
    # Grid
    n = 200
    xlim = 8
    ylim = 8
    X = np.linspace(-xlim, xlim, n)
    Y = np.linspace(-ylim, ylim, n)
    x, y = np.meshgrid(X, Y)
    
    # Velocity components
    vx = U_inf - Gam/(2*np.pi) * y / (x**2 + y**2) + (y**2 - x**2)/((x**2 + y**2)**2)
    vy = Gam/(2*np.pi) * x / (x**2 + y**2) - (2*y*x)/((x**2 + y**2)**2)
    v_loc = np.sqrt(vx**2 + vy**2)
    
    # Pressure
    Cp = 1.0 - (v_loc/U_inf)**2
    
    # Circulation calculation
    
    # Cylinder geometry
    nc = 100
    theta = np.linspace(0, 2*np.pi, nc)
    xc = r * np.cos(theta)
    yc = r * np.sin(theta)
    
    # Interpolation
    itpvx = RectBivariateSpline(X, Y, vx)
    itpvy = RectBivariateSpline(X, Y, vy)
    
    # Ealuation
    vfxc = itpvx.ev(yc, xc)
    vfyc = itpvy.ev(yc, xc)
    
    # Integration
    Int1 = np.trapz(vfxc, xc)
    Int2 = np.trapz(vfyc, yc)

    
    Gamma = - Int1 -  Int2
    
    print(f"Gamma for {case}  = {Gamma}\n")
    
    # Plotting
    
    # Velocity field
    fig1 = plt.figure(0)
    
    ax = plt.axes()
    speed = plt.contourf(x, y, v_loc, levels = np.linspace(0.0, 5.0, 100), extend = "both", cmap = "viridis")
    cbar = plt.colorbar(speed)
    #ax.quiver(x, y, vx, vy, color = "white")
    plt.streamplot(x, y, vx, vy, density = 2, linewidth = 1, arrowsize = 1, arrowstyle = "->")
    plt.title(f"Velocity field for {case}")
    plt.plot(xc, yc, label = "Cylinder", color = "black")
    plt.xlim(-xlim, xlim)
    plt.ylim(-ylim, ylim)
    plt.legend()
    plt.grid()
    ax.set_aspect("equal")
    plt.show()
    
    # Pressure field
    fig2 = plt.figure(0)
    
    ax = plt.axes()
    cp = plt.contourf(x, y, Cp, levels = np.linspace(-2.0, 1.0, 100), extend = "both", cmap = "coolwarm")
    cbar = plt.colorbar(cp)
    plt.title(f"Cp field for {case}")
    plt.plot(xc, yc, label = "Cylinder", color = "black")
    plt.xlim(-xlim, xlim)
    plt.ylim(-ylim, ylim)
    plt.legend()
    plt.grid()
    ax.set_aspect("equal")
    plt.show()

cylinder(0, "Non-lifting Cylinder")
cylinder(4 * np.pi * U_inf * r, "One Stagnation Point")
cylinder(4 * np.pi * U_inf * r * 0.5, "Two Stagnation points")
cylinder(4 * np.pi * U_inf * r * 2, "Unphysical Condition")