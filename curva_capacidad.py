# Importar librerias necesarias 
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# METADATOS DEL RASTER
# Abrir archivo raster 
DEMRst = rasterio.open('DEM.tif')
print(DEMRst.count)
# Mostrar resolución del raster
print(DEMRst.res)
# Mostrar src del raster
print(DEMRst.crs.wkt)


## Asignar los valores del raster como un arreglo numpy
DEMBottom = DEMRst.read(1)
# raster sample
print(DEMBottom[:5,:5])

# Reemplazar valor negativo por np.nan
noDataValue = np.copy(DEMBottom[0,0])
DEMBottom[DEMBottom == noDataValue] = np.nan

# Graficar raster de la zona
plt.figure(figsize = (12,12))
plt.imshow(DEMBottom)
plt.show()

## CALCULO DEL VOLUMEN DE LA TOPOGRAFIA
minElev = np.nanmin(DEMBottom)
maxElev = np.nanmax(DEMBottom)
print('Min bottom elevation %.2f m., max bottom elevation %.2f m.'%(minElev,maxElev))

# Pasos para el calculo
nSteps = 100

# Intervalos de alura presentes en la topografia
elevSteps = np.round(np.linspace(minElev,maxElev,nSteps),2)
print(elevSteps)

# Funcion de elevacion del volumen
def calculateVol(elevStep,elevDem,DEMRst):
    tempDem = elevStep - elevDem[elevDem<elevStep]
    tempVol = tempDem.sum()*DEMRst.res[0]*DEMRst.res[1]
    return tempVol

# Calcular volumenes para cada elevacion
volArray = []
for elev in elevSteps:
    tempVol = calculateVol(elev, DEMBottom, DEMRst)
    volArray.append(tempVol)
    
print("Lake bottom elevations %s"%elevSteps)
volArraymCM = [round(i/1000,6) for i in volArray]
print("Lake volume in thousand of cubic meters %s"%volArraymCM)

# Plot values
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(volArraymCM,elevSteps)
ax.grid()
ax.legend()
ax.set_xlabel('Volumen (1000$m^3$)')
ax.set_ylabel('Elevación (msnm)')
plt.title("Curva altura-capacidad",
          fontsize=15,
          fontweight="bold")
plt.savefig('curva_capacidad.png')
plt.show()


# Crear data frame de la curva de altura capacidad
d = {'cota': elevSteps,
     'volacum': volArraymCM}
df = pd.DataFrame(data=d)

# Exportar a CSV 
df.to_csv("Curva_Capacidad.csv", index=False)
