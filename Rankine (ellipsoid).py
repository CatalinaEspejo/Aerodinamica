import numpy as np 
from math import pi
import matplotlib.pyplot as plt

n = 200
X = np.linspace(-4,4,n)
Y = np.linspace(-4,4,n)   
x,y =np.meshgrid(X,Y)

m = 5.0
Uinf = 5.0

# posicion de la fuente 
xs = -1.0
ys = 0.0

# Posición del sumidero
x_sink = 1.0     
y_sink = 0.0

u = Uinf + m/(2*pi) * ((x - xs) /((x-xs)**2 + (y-ys)**2)) - m/(2*pi)*((x - x_sink)/((x - x_sink)**2 + (y - y_sink)**2))
v = m/(2*pi) * ((y - ys) /((x-xs)**2+ (y-ys)**2)) - m/(2*pi)*((y - y_sink)/((x - x_sink)**2 + (y - y_sink)**2))

# velocidad local 
vloc = np.sqrt((u**2 + v**2))

# coeficiente de presion 
cp =  1.0 - ((u**2 + v**2)/Uinf**2)
 
# Puntos de estancamiento 
xss = (xs-m/(2*pi*Uinf))
xssi = (x_sink+m/(2*pi*Uinf))
print('xss=',xss)

#streamlines
pssi = Uinf*y +m/(2*pi)*np.arctan2((y-ys),(x-xs)) - m/(2*pi)*np.arctan2((y - y_sink), (x - x_sink))

# -----------Figura 1, Velocidades ------------
firg1 = plt.figure(0)
ax = plt.axes()
plt.title("Velocity field (m/s)")
contcp = plt.contourf(x,y,vloc,levels=np.linspace(-2.0,1.0,100),extend = 'both')
cbar = plt.colorbar(contcp)

# Pintar los puntos de sumidero y fuente
ax.scatter(xs, ys, c= 'red', marker='o', s=7**2, label='sink and source')
ax.scatter(xss, ys, c= 'b', marker='o', s=7**2, label='Stagnation points')
ax.scatter(x_sink, y_sink, c= 'red', marker='o', s=7**2)
ax.scatter(xssi, y_sink, c= 'b', marker='o', s=7**2)

# pintar las velocidades 
#ax.quiver(x,y, u,v, color = 'white')

plt.streamplot(x,y,u,v,density = 2, linewidth =1, arrowsize =1,arrowstyle = '->')

# elipsoide 
a = (xssi - xss)/2
b = np.sqrt(m/(pi*Uinf))
x_ellipse = np.linspace(xss, xssi, 200)
y_ellipse = b*np.sqrt(1 - ((x_ellipse - (xss+xssi)/2)**2)/a**2)
ax.plot(x_ellipse, y_ellipse, 'k', linewidth=2)
ax.plot(x_ellipse, -y_ellipse, 'k', linewidth=2)

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.legend()

# Relacion de aspecto 
ax.set_aspect('equal' ,'box')
plt.grid()
plt.show()

# ---------- Figura 2, Coeficiente de presión ----------
firg1 = plt.figure(0)
ax = plt.axes()
plt.title("Pressure Coefficient (Cp) Distribution")
contcp = plt.contourf(x,y,cp,levels=np.linspace(-2.0,1.0,100),extend = 'both')
cbar = plt.colorbar(contcp)

# Elipsoide 
a = (xssi - xss)/2
b = np.sqrt(m/(pi*Uinf))
x_ellipse = np.linspace(xss, xssi, 200)
y_ellipse = b*np.sqrt(1 - ((x_ellipse - (xss+xssi)/2)**2)/a**2)
ax.plot(x_ellipse, y_ellipse, 'k', linewidth=2)
ax.plot(x_ellipse, -y_ellipse, 'k', linewidth=2)


# Pintar los puntos de sumidero y fuente 
ax.scatter(xs, ys, c= 'red', marker='o', s=7**2, label='sink and source')
ax.scatter(xss, ys, c= 'b', marker='o', s=7**2, label='Stagnation points')
ax.scatter(x_sink, y_sink, c= 'red', marker='o', s=7**2)
ax.scatter(xssi, y_sink, c= 'b', marker='o', s=7**2)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.legend()

# Relacion de aspecto 
ax.set_aspect('equal' ,'box')
plt.grid()
plt.show()
