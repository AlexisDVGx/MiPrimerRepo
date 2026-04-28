from funcion_n import suma, resta, multiplicacion
import numpy as np
import matplotlib.pyplot as mat
a = suma(1,2)
print(a)
b = resta(1,2)
print(b)
c = multiplicacion(1,2)
print(c)

x = np.linspace(0,10)
grafica = x + 2

mat.figure()
mat.plot(x,grafica)
mat.legend()
mat.grid()
mat.show()

mat.savefig("Grafica.eps")