import pandas as pd
#import kaggle
import os
import random

## Configurar Kaggle
#os.environ['KAGGLE_CONFIG_DIR'] = 'C:/Users/salce/.kaggle'
#dataset = 'singhnavjot2062001/11000-medicine-details'
#kaggle.api.dataset_download_files(dataset, path='.', unzip=True)




# Cosas a hacer

## Separar "Medicine Name" en tres columnas, Nombre, cantidad, presentacion, imagen del medicamento.
## Separar "Composicion" en dos columnas, nombre_comp, cantidad_comp.
## Hacer graficas Usos, Efectos secundarios, "Excellent Review %,Average Review %,Poor Review %", monufactura.
## Recomendacion por componetes y usos.



#data = pd.read_csv("Medicine_Details.csv", index_col=False)
#new_df = data[["Medicine Name", "Composition"]]
#new_df[['Nombre', 'Dosis', 'Forma']] = new_df['Medicine Name'].str.split(' ', n=2, expand=True)
#neww = new_df['Medicine Name'].str.split(' ', n=2, expand=True)
#print(neww.iloc[100:110, :])

import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import webbrowser

# Cargar los datos
data = pd.read_csv("Medicine_Details.csv", index_col=False)

# Limpiar espacios en blanco en los nombres de las columnas
data.columns = data.columns.str.strip()

# Imprimir las columnas disponibles
print("Columnas disponibles:", data.columns.tolist())

# Renombrar las columnas "Usos" y "Efectos secundarios"
data.rename(columns={'Usos': 'Uses', 'Efectos secundarios': 'Side_effects'}, inplace=True)

# Limpiar espacios en blanco en la columna "Medicine Name"
data['Medicine Name'] = data['Medicine Name'].str.strip()

# Función para separar nombre, dosis y presentación
def separar_nombre_dosis_presentacion(medicamento):
    partes = medicamento.split()
    if len(partes) < 2:
        return pd.Series([medicamento, None, None])  # Devuelve el nombre y None para dosis y presentación
    
    # La última parte es la presentación, la penúltima es la dosis
    presentacion = partes[-1]
    dosis = partes[-2]
    
    # El resto es el nombre
    nombre = ' '.join(partes[:-2])
    
    # Si la presentación tiene más de una palabra (ejemplo: "Nasal Spray")
    if len(partes) > 3:
        presentacion = ' '.join(partes[-2:])
        dosis = partes[-3]
    
    return pd.Series([nombre, dosis, presentacion])

# Aplicar la función de separación
data[['Nombre', 'Dosis', 'Presentación']] = data['Medicine Name'].apply(separar_nombre_dosis_presentacion)

# Separar "Composition" en dos columnas: nombre_comp, cantidad_comp
data[['nombre_comp', 'cantidad_comp']] = data['Composition'].str.split(' ', n=1, expand=True)

# Eliminar filas donde 'Nombre' esté vacío
data = data[data['Nombre'].notnull() & (data['Nombre'] != '')]

# Eliminar duplicados
data = data.drop_duplicates(subset=['Nombre', 'Uses'])

# Ajustar las opciones de visualización de pandas
pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
pd.set_option('display.max_rows', None)     # Mostrar todas las filas
pd.set_option('display.width', 1000)         # Ancho máximo de la salida
pd.set_option('display.max_colwidth', 200)   # Ancho máximo de las columnas

# Mostrar las primeras filas del nuevo DataFrame con nombres de columnas de forma bonita
headers = ["Nombre", "Dosis", "Presentación"]  # Encabezados más claros
print(tabulate(data[['Nombre', 'Dosis', 'Presentación']].head(10), headers=headers, tablefmt='pretty', showindex=False))

# Definición de la función para graficar gráficos circulares simplificados
def plot_top_pie_chart(data, column, top_n=10):
    top_data = data[column].value_counts().nlargest(top_n)
    plt.figure(figsize=(8, 6))
    top_data.plot.pie(autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.axis('equal')  # Para que el gráfico sea un círculo
    plt.title(f'Top {top_n} en {column}')
    plt.show()

# Graficar Uses (gráfico circular simplificado)
if 'Uses' in data.columns:
    plot_top_pie_chart(data, 'Uses')
else:
    print("La columna 'Uses' no se encuentra en el DataFrame.")

# Graficar Side_effects (gráfico circular simplificado)
if 'Side_effects' in data.columns:
    plot_top_pie_chart(data, 'Side_effects')
else:
    print("La columna 'Side_effects' no se encuentra en el DataFrame.")

# Graficar Reseñas (gráfico circular simplificado)
review_columns = ['Excellent Review %', 'Average Review %', 'Poor Review %']
if all(col in data.columns for col in review_columns):
    plt.figure(figsize=(8, 6))
    mean_reviews = data[review_columns].mean()
    top_reviews = mean_reviews.nlargest(3)
    top_reviews.plot.pie(autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.axis('equal')
    plt.title('Reseñas Promedio')
    plt.show()
else:
    print("Una o más columnas de reseñas no se encuentran en el DataFrame.")

# Graficar Manufacturer (gráfico circular simplificado)
if 'Manufacturer' in data.columns:
    plot_top_pie_chart(data, 'Manufacturer')
else:
    print("La columna 'Manufacturer' no se encuentra en el DataFrame.")

# Función para buscar el URL de la imagen del medicamento principal
def buscar_imagen_medicamento(nombre_medicamento):
    medicamento = data[data['Nombre'].str.contains(nombre_medicamento, na=False, case=False)]
    if not medicamento.empty:
        return medicamento.iloc[0]['Image URL']  # Retorna el URL de la imagen del primer medicamento encontrado
    return None

# Ejemplo de uso de la función de búsqueda
medicamento_principal = 'Paracetamol'  # Cambia esto por el medicamento que desees buscar
url_imagen = buscar_imagen_medicamento(medicamento_principal)

# Abrir el URL de la imagen en el navegador
if url_imagen:
    print(f"Abrir URL de la imagen para '{medicamento_principal}': {url_imagen}")
    webbrowser.open(url_imagen)
else:
    print(f"No se encontró imagen para el medicamento '{medicamento_principal}'.")



### Farmacias Ficticias

#df1 = new_df.sample(n=len(new_df)//2, replace=True).reset_index(drop=True)
#df2 = new_df.sample(n=len(new_df)//2, replace=True).reset_index(drop=True)
#df3 = new_df.sample(n=len(new_df)//2, replace=True).reset_index(drop=True)
#
#df1['DataFrame'] = 'farmacia1'
#df2['DataFrame'] = 'farmacia2'
#df3['DataFrame'] = 'farmacia3'
#
#df_combined = pd.concat([df1, df2, df3])
#
#df = df_combined.pivot_table(index='DataFrame', columns='Medicine Name', values='Composition', aggfunc=lambda x: x.iloc[0])
#
#print("DataFrame combinado y pivotado:")
#print(df.iloc[:, 454:455])




## Programa funcional con la base de datos antigua.


### Nombres de las farmacias
#
#Nom_far = ["Farmacia1","Farmacia2","Farmacia3"]
#
#
### Leer el archivo CSV con la base de datos
#
#df = pd.read_csv('Medicine_Details.csv')
#df.index = Nom_far
#
#
### Entrada de datos (falta arreglar para la interfaz)
#
##       Med = input("Medicamento a buscar:").capitalize()
#
###Me dicamentos que han dado problemas y con lo que se estudian diferentes casos
#
#Med = "Enalapril"
##Med = "asdasd"
##Med = "Alprazolam"
##Med = "Aspirina"
##Med = "Amoxicilina con ácido clavulánico"
##Med = "Paracetamol"


#Med = "Anbid 500 Tablet"
#
#print("Medicamento a buscar:", Med)
#
#
### Almacenar datos de los resultado de busqueda
#
#Med_bus_1 = {}
#Com_bus_1 = {}
#Med_sim_bus_2 = {}
#similar_med = {}
#
#
### Busqueda del medicamento en la farmacia y sus componentes
#
#if Med in df:
#    df_Med = df[Med]
#    for idx, val in df_Med.items():
#        if pd.isnull(val):
#            Med_bus_1[idx] = val
#            Med_sim_bus_2[idx] = val
#        else:
#            Med_bus_1[idx] = "Esta"
#            val = val.replace("[","").replace("]","").replace("'","").split(', ')
#            Com_bus_1[idx] = val
#else:
#    Med_bus_1 = "No se encontro medicamento"
#    Com_bus_1 = "No se encontro medicamento"
#
#ser_Med_bus_1 = pd.Series(Med_bus_1)
#df_Com_bus_1 = pd.Series(Com_bus_1)
#
#
#if not Med_sim_bus_2:
#    if not similar_med:
#        Med_sim_bus_2 = "No hace falta"
#        similar_med = "No hace falta"
#
#ser_Med_sim_bus_2 = pd.Series(Med_sim_bus_2)
#
#
### Búsqueda de un medicamento similar en farmacias donde no está el original
#
#nan_indices= ser_Med_sim_bus_2[pd.isnull(ser_Med_sim_bus_2)].index 
#
#for idx_far in nan_indices: 
#    for idx, val in df_Com_bus_1.items(): 
#        for comp in val:
#            valores_indice = df.loc[idx_far].to_list()
#            for i in valores_indice:
#                if isinstance(i, str):
#                    i = eval(i)
#                    for sub_i in i:
#                        if sub_i == comp:
#                            valor = str(i)
#                            indice = idx_far
#                            columna_encontrada = df.columns[(df.loc[indice] == valor)].tolist()
#                            similar_med[idx_far] = columna_encontrada
#
#if not similar_med:
#    idx_far = 0
#    similar_med[idx_far] = "No se encontro similar en ninguna farmacia"
#
#ser_similar_med = pd.Series(similar_med)
#
#
### Busqueda del medicamento en la farmacia y sus componentes
#
#print("-"*40)
#print("*En que farmacia esta el medicamento*")
#print(ser_Med_bus_1.to_string())
#print("-"*40)
#print("*Componentes del medicamento*")
#print(df_Com_bus_1.to_string())
#print("-"*40)
#
### Busqueda de los componentes del medicamento en otras farmacias
#
#print("*Farmacia donde no esta el medicamento*")
#print(ser_Med_sim_bus_2.to_string())
#print("-"*40)
#
### Búsqueda de un medicamento similar en farmacias donde no está el original
#
#print("*Farmacia donde existe uno similar*")
#print (ser_similar_med.to_string())
#
#
#"""
#
#*Ejemplo de salida*
#run Codigo.py:
#
#Medicamento a buscar: Enalapril
#----------------------------------------
#*En que farmacia esta el medicamento*
#Farmacia1    Esta
#Farmacia2     NaN
#Farmacia3     NaN
#----------------------------------------
#*Componentes del medicamento*
#Farmacia1    [Enalapril maleato]
#----------------------------------------
#*Farmacia donde no esta el medicamento*
#Farmacia2   NaN
#Farmacia3   NaN
#----------------------------------------
#*Farmacia donde existe uno similar*
#Farmacia2    [Diazepam]
#Farmacia3    [Diazepam]
#
#"""
#