import numpy as np 
from math import pi
import matplotlib.pyplot as plt

n = 200
X = np.linspace(-4,4,n) 
Y = np.linspace(-4,4,n)  
x,y =np.meshgrid(X,Y)

m = 5.0
Uinf = 5.0 
xs = -1.0 
ys = 0.0

# primero vamos a encontrar la velocidad local 
u = Uinf + m/(2*pi) * ((x - xs) /((x-xs)**2 + (y-ys)**2))
v = m/(2*pi) * ((y - ys) /((x-xs)**2+ (y-ys)**2))

# velocidad local
vloc = np.sqrt((u**2 + v**2))

# coeficiente de presion 
cp =  1.0 - ((u**2 + v**2)/Uinf**2) 
 
# punto de estancamiento 
xss = (xs-m/(2*pi*Uinf))
print('xss=',xss)

#barido hasta 30 grados 
theta =  np.linspace(pi,30*pi/180,25)

# posiciones de la fuente 
yf = (m/2 - m/(2*pi)*theta)/Uinf;
xf = (xs - yf/np.tan(theta));


#streamlines
pssi = Uinf*y +m/(2*pi)*np.arctan2((y-ys),(x-xs));

# ----------- Grafica ------------
firg1 = plt.figure(0)
ax = plt.axes()

contcp = plt.contourf(x,y,cp,levels=np.linspace(-2.0,1.0,100),extend = 'both')
#contcp = plt.contourf(x,y,vloc,levels=np.linspace(-2.0,1.0,100),extend = 'both')
cbar = plt.colorbar(contcp)
ax.scatter(xs, ys, c= 'red', marker='o', s=7**2)
ax.scatter(xss, ys, c= 'b', marker='o', s=7**2)
ax.quiver(x,y, u,v, color = 'white')
plt.streamplot(x,y,u,v,density = 2, linewidth =1, arrowsize =1,arrowstyle = '->')
ax.contour(x,y,pssi,levels = [-m/2,m/2],colors ='g')

# relacion de aspecto de la cajita 
ax.set_aspect('equal' ,'box')

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

plt.grid()
plt.show()


