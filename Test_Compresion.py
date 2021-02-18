import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# CARGAMOS LA BASE DE DATOS
data = pd.read_excel("Diagrama2.xlsx")
columnas = data.columns

# DEFINIMOS TODAS LAS VARIABLES
pen = np.zeros(10)  # variable que contiene las pendientes
plt.clf()
# LE = []  # variable que contiene los limites elasticos
LEy = []
cont = 0
px = []  # acumula la coordenada x de los puntos
py = []  # acumula la coordenada y de los puntos
line = np.linspace(0, 6.4, 100)  # hay que cambiarla en caso de que sea fuerza o elongacion
contar = 0
escalar = 0  # usado para la seleccion de las diferentes pendientes
leyenda = ['giroide32', 'giroide33', 'giroide42', 'giroide43', 'giroide52', 'giroide53', 'giroide62', 'giroide63',
           'giroide72', 'giroide73']
ultimo = data.apply(pd.Series.last_valid_index)

# DEFINIMOS TODAS LAS FUNCIONES


def tellme(s):

    print(s)
    plt.title(s, fontsize=16)
    plt.draw()

# funcion que calcula la pendiente


def pendiente(x1, y1, x2, y2):

    slope = (y2 - y1) / (x2 - x1)
    return slope

# funcion que ajusta un polinomio


def regresion(grado):

    k = 0
    model = np.empty(10, np.poly1d)
    for i, j in zip(columnas[0:ensayos:2], columnas[1:ensayos:2]):
        model[k] = np.poly1d(np.polyfit(data[i][0:ultimo[i]], data[j][0:ultimo[j]], grado))
        k = k+1
    return model


def probando():

    while True:
        pts = []
        while len(pts) < 2:
            tellme('Seleccione dos puntos')
            pts = np.asarray(plt.ginput(2, timeout=-1))
            if len(pts) < 2:
                tellme('pocos puntos hagalo de nuevo')
                time.sleep(1)  # Wait a second

        ph = plt.axline(pts[0, :], pts[1, :])

        tellme('toque el teclado para salir')
        if plt.waitforbuttonpress():

            px.append(pts[0, 0])
            py.append(pts[0, 1])
            pen[contar] = np.asarray(pendiente(pts[0, 0], pts[0, 1], pts[1, 0], pts[1, 1]))
            break
        ph.remove()


def limite_elastico():

    while True:
        plt.axline([px[escalar]+0.2, py[escalar]], slope=pen[escalar])  # el primer punto desplazado en x
        tellme('seleccione el límite elástico, luego pulse enter')
        le = np.asarray((plt.ginput(1, timeout=-1)))
        LEy.append(le[0, 1])
        tellme('Esta conforme con el punto?,presione enter')
        if plt.waitforbuttonpress():
            break


def ten_el(sup=9, long_in=30):

    for i, j in zip(columnas[0:ensayos:2], columnas[1:ensayos:2]):

        data[i] = (data[i]/long_in)*100
        data[j] = data[j]/sup

    return data



# PROGRAMA


tellme('ingrese la cantidad de curvas que quiere analizar, maximo 10 ')

ensayos = input()
ensayos = int(ensayos) * 2


data = ten_el()  # Pasa los valores fuerza-desplazamiento a tension-elongacion
ud = []  # Almacena los ultimos valores no NAN de todas las columnas
ultimo_val = data.apply(lambda x: x[x.notnull()].values[-1])
for i in range(0, 20, 2):
    ud.append(ultimo_val[i])

poly = regresion(8)  # se le pasa como parametro el grado del polinimio
# print(poly)
metodo = False

if metodo:

    for p in range(2):

        for i, j in zip(columnas[0:ensayos:2], columnas[1:ensayos:2]):
            plt.clf()
            plt.setp(plt.plot(data[i], data[j]))
            tellme('click para comenzar')
            plt.waitforbuttonpress()
            if p < 1:
                probando()
                contar = contar + 1
            else:
                limite_elastico()
                escalar = escalar + 1


else:

    for p in range(2):

        L = []
        ma = []
        for i in range(0, ensayos//2, 1):
            plt.clf()
            # line = np.linspace(0, ud[i], 100)  # 2.1 por como esta en la base de datos
            plt.setp(plt.plot(line, poly[i](line)))
            plt.xlabel('E[%]')
            plt.ylabel('Kgf/cm^2')
            plt.legend([leyenda[i]])
            tellme('Click para comenzar')
            plt.waitforbuttonpress()

            if p < 1:
                probando()
                contar = contar + 1
            else:
                limite_elastico()
                escalar = escalar + 1


# GRAFICO DE BARRAS CON EL VALOR DE LOS LIMITES ELASTICOS

plt.clf()
c = ['red', 'blue']
ley = ensayos/2
ley = int(ley)
leyenda = ['G-32', 'G-33', 'G-42', 'G-43', 'G-52', 'G-53', 'G-62', 'G-63', 'G-72', 'G-73']
plt.xlabel('configuraciones')
plt.ylabel('T[Kgf/cm^2]')
plt.title('Límite Elástico Convencional')
# plt.yticks(np.linspace(0,max(ma),20))
plt.bar(leyenda[0:ley], height=LEy, color=c, width=0.8)
plt.show()

# Graficos
plt.figure(figsize=[7, 7])
leyenda = ['giroide32', 'giroide33', 'giroide42', 'giroide43', 'giroide52', 'giroide53', 'giroide62', 'giroide63',
           'giroide72', 'giroide73']
L = []
ma = []
for i in range(0, ensayos//2, 1):
    # line = np.linspace(0, ud[i], 100)
    plt.plot(line, poly[i](line))
    plt.legend([leyenda[i]])
    L.append(leyenda[i])
    ma.append(max(poly[i](line)))

plt.xlabel('mm')
plt.ylabel('Kgf')
plt.title('Curva tension deformacion')
plt.legend(L)
plt.yticks(np.linspace(0, max(ma), 30))
plt.grid()
plt.show()

# GRAFICO DE BARRAS CON EL VALOR DE LOS MODULOS DE ELASTICIDAD 
pen = list(pen)
plt.clf()
c = ['red', 'blue']
leyenda = ['G-32', 'G-33', 'G-42', 'G-43', 'G-52', 'G-53', 'G-62', 'G-63', 'G-72', 'G-73']
plt.xlabel('configuraciones')
plt.ylabel('M[Kgf/cm^2]')
plt.title('Módulo Elástico')
plt.bar(leyenda[0:10], height=pen, color=c, width=0.8)
plt.show()

'''

# REVISAR

Ur = []
for i in range(ensayos//2):

    Ur.append((LEy[i]**2)/(2*pen[i]))

# GRAFICO DE BARRAS CON EL VALOR DE RESILIENCIA
urc = ensayos//2
plt.clf()
c = ['red', 'blue']
leyenda = ['G-32', 'G-33', 'G-42', 'G-43', 'G-52', 'G-53', 'G-62', 'G-63', 'G-72', 'G-73']
plt.xlabel('configuraciones')
plt.ylabel('Ur')
plt.title('Resiliencia')
plt.bar(leyenda[0:urc], height=Ur, color=c, width=0.8)
plt.show()
'''