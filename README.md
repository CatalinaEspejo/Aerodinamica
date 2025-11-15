# Aerodinamica

### **Downwash**
El modelo elíptico produce un downwash constante a lo largo de toda la envergadura, una propiedad exclusiva de la distribución de circulación ideal. En este caso, el valor del downwash se calcula como:

\[
w = -\frac{\Gamma_0}{2b}
\]

lo que implica que todas las secciones del ala experimentan el mismo ángulo de flujo inducido.

<p align="center">
<img width="613" height="264" alt="Figure 2025-11-15 164356" src="https://github.com/user-attachments/assets/0f80f7d3-4cd2-44fd-8a7a-80dca7b6b807" />
</p>


### **Circulación (Γ)**
Representación de elcampo de velocidades inducido por un vórtice con una circulación alrededor de un cilindro. En la figura se observa cómo las líneas de flujo giran en sentido horario, coherente con el signo negativo de la circulación. Los vectores más cercanos al cilindro muestran mayor intensidad, mientras que el campo se atenúa al alejarse del centro.
<p align="center">
<img width="253" height="248" alt="Circulación" src="https://github.com/user-attachments/assets/a9c67224-9453-4ef0-808c-b5ad7d47a3ae" />
</p>

### **Análisis del flujo alrededor de un cilindro con circulación**
Comportamiento del flujo potencial alrededor de un cilindro para distintos valores de circulación. A través de la simulación numérica se observaron los cambios en el campo de velocidades y en la distribución de presión.
<p align="center">
<img width="315" height="264" alt="Figure 2025-11-11 141245" src="https://github.com/user-attachments/assets/7949ce8b-de09-4610-a583-50110fdf1c5a" />
</p>
<p align="center">
<img width="324" height="264" alt="Figure 2025-11-11 141321" src="https://github.com/user-attachments/assets/cba1673b-3543-4386-8208-240d892e792c" />
</p>
<p align="center">
<img width="315" height="264" alt="Figure 2025-11-11 141339" src="https://github.com/user-attachments/assets/08b46f62-65dc-4905-86ff-ee89efb153e6" />
</p>
<p align="center">
<img width="324" height="264" alt="Figure 2025-11-11 141356" src="https://github.com/user-attachments/assets/da0defcc-6ab1-4a89-81cb-1937e81d69fb" />
</p>
<p align="center">
<img width="315" height="264" alt="Figure 2025-11-11 141412" src="https://github.com/user-attachments/assets/fe90e137-0229-40b9-a8ee-8acb0ec4dd6e" />
</p>
<p align="center">
<img width="324" height="264" alt="Figure 2025-11-11 141427" src="https://github.com/user-attachments/assets/dc5209ef-9c59-49ac-996a-23bc584481fd" />
</p>

### **Aplicación del método de paneles de vórtices en un perfil plano**
Implementación simplificada del método de paneles de vórtices para un perfil plano, mostrando la ubicación de los vórtices y puntos de colocación sobre la cuerda del perfil.
<p align="center">
<img width="576" height="288" alt="Figure_111" src="https://github.com/user-attachments/assets/9a926041-5b60-4604-8946-bb92506568c4" />
</p>

Se calculó el coeficiente de sustentación utilizando el método de paneles para un ángulo de ataque de α = 5° con una discretización de 5 paneles. El resultado numérico obtenido fue: 
- **CL** =  0.5488762704231447
- Solución del sistema **Γ** = [2.46376836 1.09500816 0.70393382 0.46928921 0.27375204]

### **elipsoide de Rankine**
Flujo alrededor de un cuerpo elíptico generado por una fuente y un sumidero, ubicados en x=-1 y x=1 respectivamente. La interacción entre estos elementos produce un cuerpo de Rankine cuya superficie está delimitada por los puntos de estancamiento, los cuales se localizaron en x=-1.159 y x=1.159 donde la velocidad del flujo se anula.

<p align="center">
<img width="333" height="264" alt="Figure 2025-11-13 114925" src="https://github.com/user-attachments/assets/8c72118a-164d-41cc-8e7f-a116047fabbf" />
</p>
<p align="center">
<img width="324" height="264" alt="Figure 2025-11-13 114917" src="https://github.com/user-attachments/assets/506cc55c-b113-4310-a3d1-19af99c030a9" />
</p>

### **Discretización del ala mediante el método de Horseshoe Vortex**
<p align="center">
<img width="268" height="237" alt="Figure 2025-11-13 123500" src="https://github.com/user-attachments/assets/0c5b6060-c082-4de3-a7c8-5ef1c8b9df3b" />
</p>

### **Aplicación del método de paneles de vórtices en un perfil camber**
Implementación simplificada del método de paneles de vórtices para un perfil con curvatura (camber), mostrando la ubicación de los vórtices ubicados a 1/4 de la longitud del panel, los puntos de colocación a 3/4 del panel, así como los vectores unitarios normal y tangente definidos sobre la cuerda del perfil.
<p align="center">
<img width="500" height="300" alt="vectores" src="https://github.com/user-attachments/assets/c2c2f333-085d-4539-be7e-1e23e81f6f75" />
</p>

Ademas, se presenta la distribución del coeficiente de presión ΔCp obtenida tanto mediante la solución analítica como mediante el método numérico implementado.

<p align="center">
<img width="450" height="250" alt="Figure_1" src="https://github.com/user-attachments/assets/0fa0585f-c5a5-4d5e-910a-697c89c9a36b" />
</p>

Se calculó el coeficiente de sustentación utilizando el método de paneles para un ángulo de ataque de α = 0° con una discretización de 500 paneles. El resultado numérico obtenido fue:

- **CL (numérico)** = 1.2309  
- **CL (analítico)** = 1.2566  

El porcentaje de error obtenido fue de **2.04%**, lo que indica una muy buena aproximacion entre la solución numérica y la solucion analítica.

