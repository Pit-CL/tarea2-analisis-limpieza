# %%
import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats as st

# %%
"""
# Pregunta 1.

Tomamos la base de datos reducida (desde el año 2008 al año 2017) para mejorar la rapidez del script.
Sin embargo este script es capaz de leer toda la base de dato es decir desde el año 1990 al año 2017.
"""

# %%
# En el caso que deseen leer los archivos desde el 90 al 95 lo pueden hacer descomentando el siguiente código:
# path = r'tu_path'
# df_90_95 = (pd.concat(map(pd.read_csv,
#                           glob.glob(os.path.join('', "tu_path/*.csv")))))

# Creo el df con los csv restantes no utf-8 y separados por ;
path_96_2017 = r'E:\driveudd\MDS\Limpieza_de_datos\Tarea-2\nacimientos\nacimientos'
todos_los_csv_96_2017 = glob.glob(os.path.join(path_96_2017, "*.csv"))

df_de_cada_archivo_96_2017 = (pd.read_csv(f, sep=';', encoding='latin1')
                              for f in todos_los_csv_96_2017)
df_general = pd.concat(df_de_cada_archivo_96_2017, ignore_index=True)
df_general

# %%
# Reviso las columnas y tipo de datos
df_general.info()

# %%
"""
# Pregunta 2.

Con el uso de value_counts() podemos obtener el mes con el mayor número de cumpleaños dando como resultado el mes
de Enero con 213.303 nacimientos. Esto quiere decir, que si consideramos un plazo normal de embarazo de 9 meses, el
mes de mayor concepción es Abril, a inicios de la temporada de Otoño de cada año.
"""

# %%
df_general.MES_NAC.value_counts()

# %%
"""
# Pregunta 3.

El día con más cumpleaños es el 15 de Septiembre con 7.864 cumpleaños. Acá también se puede dar la respuesta
considerando sólo el día con más nacimiento, sin considerar el mes, cuyo resultado o moda es el día 14.
"""

# %%
# Creo una nueva columna llamada cumpleanos y le aplico value.counts().

df_general['DIA_NAC'] = df_general['DIA_NAC'].astype(str)
df_general['MES_NAC'] = df_general['MES_NAC'].astype(str)
df_general['cumpleano'] = (df_general['DIA_NAC'] + '-' + df_general['MES_NAC'])
df_general.cumpleano.value_counts()
print('El dia sin considerar el mes de más nacimientos es,', df_general.DIA_NAC.mode())

# %%
"""
# Pregunta 4.

La correlación general entre PESO y TALLA para los años estudiados es de 0.77 lo que indica una muy buena correlación,
es decir, se explica en un 77% el cambio de una variable con relación a la otra. En palabras más simples si se aumenta o
baja en peso, se aumenta o baja en talla.

Con respecto a la covarianza podemos que el valor es 1713, que al ser un valor mayor que cero indica una relación líneal
directa o positiva entre ambas variables. En otras palabras tienden a aumentar o disminuir  a la vez.

La correlación a lo largo de los años estudiados no cambia mayormente. Sin embargo llama la atención el año 2010 y 2011
en donde la correlación entre ambas variables es de 0,85 y 0,82, lo que podría implicar que los datos fueron tomados de
una manera más exacta; ya que es lógico que exista una correlación entre peso y talla.

La covarianza a los largo de los años no sufre mayores variaciones, sin embargo en los años indicados en el párrafo
anterior, también tienen variaciones importantes.
"""

# %%
# Uso la función .corr()
corr_p_t_general = df_general[['PESO', 'TALLA']].corr('spearman')
corr_p_t_general

# %%
corr_p_t_x_ano = df_general.groupby('ANO_NAC')[['PESO', 'TALLA']].corr('spearman')
corr_p_t_x_ano

# %%
cov_p_t_general = df_general[['PESO', 'TALLA']].cov()
cov_p_t_general

# %%
cov_p_t_x_ano = df_general.groupby('ANO_NAC')[['PESO', 'TALLA']].cov()
cov_p_t_x_ano

# %%
"""
# Pregunta 5.

La correlación para la Edad del Padre y de la Madre es de 0.55, no es una mala correlación sin embargo no es excelente,
por lo tanto sólo podríamos decir que la edad del Padre se explica en un 55% según la edad de la Madre.

Con respecto a la covarianza de 19.44 es mayor que cero por lo que indica relación de linealidad entre ambas variables.

La correlación en el transcurso de los años no varía mayormente, lo que indica que la correlación se mantiene en un
rango del 0.51 al 0.55. Es preciso mencionar que existe una correlación atípica de 0.68 para el año 2013.

La covarianza también tiene poca variación, va desde los valores 14 al 18 aproximadamente, al ser positiva, indica
que ambas variables tienden a aumentar o disminuir a la vez.
"""

# %%
corr_ep_em_general = df_general[['EDAD_P', 'EDAD_M']].corr('spearman')
corr_ep_em_general

# %%
corr_ep_em_x_ano = df_general.groupby('ANO_NAC')[['EDAD_P', 'EDAD_M']].corr('spearman')
corr_ep_em_x_ano

# %%
cov_ep_em_general = df_general[['EDAD_P', 'EDAD_M']].cov()
cov_ep_em_general

# %%
cov_ep_em_x_ano = df_general.groupby('ANO_NAC')[['EDAD_P', 'EDAD_M']].cov()
cov_ep_em_x_ano

# %%
"""
# Pregunta 6.

Para considerar qué recién nacido pertenece a cuál categoría, este informe se basa en la información obtenida desde
la [Bibioteca Nacional de Medicina de los EE.UU](https://medlineplus.gov/spanish/ency/article/001562.htm).

Además de lo anterior se toma el supuesto que los valores de peso 9999 y talla 99 son un error del dataframe, por lo
que no se les considera para gráficos de tal manera de hacerlos entendibles.

En los gráficos podemos notar una gran presencia de outliers, lo que eventualmente podría distorcionar algunos
resultados, por lo que se recomienda un filtrado entre el quartil 1 y 3, sin embargo, como este informe es con
fines académicos, sólo consideramos descartar los valores indicados en el supuesto del párrafo anterior.

Además de lo anterior en el boxplot se pueden notar los rangos intercuartiles de cada variable estudiada, siendo
esta una importante herramienta para decidir cómo trabajar con la información.
"""

# %%
prematuro = df_general.query('SEMANAS < 37 & PESO != 9999 & TALLA != 99')
prematuro.reset_index(inplace=True, drop=True)
prematuro

# %%
a_termino = df_general.query(
    'SEMANAS >= 37 & SEMANAS <= 42 & PESO != 9999 & TALLA != 99')
a_termino.reset_index(inplace=True, drop=True)
a_termino

# %%
post_termino = df_general.query('SEMANAS > 42 & PESO != 9999 & TALLA != 99')
post_termino.reset_index(inplace=True, drop=True)
post_termino

# %%
# Creando diagramas de BOX para el peso y la talla para las tres categorías anteriores
sns.boxplot(prematuro['PESO'])
plt.title('Boxplot PESO prematuro')
plt.show()

# %%
sns.boxplot(prematuro['TALLA'])
plt.title('Boxplot TALLA prematuro')
plt.show()

# %%
sns.boxplot(a_termino['PESO'])
plt.title('Boxplot PESO a término')
plt.show()

# %%
sns.boxplot(a_termino['TALLA'])
plt.title('Boxplot TALLA a término')
plt.show()

# %%
sns.boxplot(post_termino['PESO'])
plt.title('Boxplot PESO post término')
plt.show()

# %%
sns.boxplot(post_termino['TALLA'])
plt.title('Boxplot TALLA post término')
plt.show()

# %%
"""
# Pregunta 7.

Para identificar el comportamiento de los outliers y los rangos IQ y su relación con las variables solicitadas
se realizan nuevos gráficos boxplot. Los que arrojan los siguientes resultados.

Podemos notar un comportamiento bastante similar para todas las variables, teniendo un Q2
en los mismos niveles. Se puede notar la presencia de outliers, en su mayoría en el indicador 1.
"""

# %%
# Primero debo conocer las variables que componen la columna ESTAB para poder indicar un indicador que
# represente la clase a la cual pertenece.

cat_ESTAB = df_general.ESTAB.unique().T
cat_ESTAB

# %%
# Luego inicio la columna indicador y posteriormente le indico como quiero que se construya.
df_general['indicador'] = ' '
df_general.indicador = (np.where(df_general.ESTAB.isnull(), 0,
                                 (np.where((df_general.ESTAB.str.contains('TRAYECTO') | df_general.ESTAB.str.contains(
                                     'CAMINO')), 2,
                                           np.where(df_general.ESTAB.str.contains
                                                    ('AMBULANCIA'), 1, (np.where((df_general.ESTAB.str.contains
                                                                                  (
                                                                                      'HOS') | df_general.ESTAB.str.contains
                                                                                  ('Hospital')), 3, (np.where(
                                               (df_general.ESTAB.str.contains
                                                ('CL') | df_general.ESTAB.str.contains
                                                ('Clinica') | df_general.ESTAB.str.contains
                                                ('Clínica')), 4, '5')))))))))

# %%
# Reviso que el grupo 1 esté bien identificado.
prueba_para_1 = df_general[(df_general.indicador == '1')]
prueba_para_1

# %%
# Reviso que el grupo 1 esté bien identificado.
prueba_para_2 = df_general[(df_general.indicador == '2')]
prueba_para_2

# %%
# Reviso que el grupo 1 esté bien identificado.
prueba_para_3 = df_general[(df_general.indicador == '3')]
prueba_para_3

# %%
# Reviso que el grupo 1 esté bien identificado.
prueba_para_4 = df_general[(df_general.indicador == '4')]
prueba_para_4

# %%
prueba_para_5 = df_general[(df_general.indicador == '5')]
prueba_para_5

# %%
df_preg7 = df_general[(df_general.indicador == '1') | (df_general.indicador == '2')]
df_preg7_1 = df_preg7[(df_preg7.PESO != 9999)]
g_indicador_PESO = sns.boxplot(x='indicador', y='PESO', data=df_preg7_1)

# %%
df_preg7_2 = df_preg7[(df_preg7.TALLA != 99)]
g_indicador_TALLA = sns.boxplot(x='indicador', y='TALLA', data=df_preg7_2)
plt.show()

# %%
g_indicador_EDAD_M = sns.boxplot(x='indicador', y='EDAD_M', data=df_preg7)
plt.show()

# %%
df_preg7_3 = df_preg7[(df_preg7.EDAD_P < 70)]
g_indicador_EDAD_P = sns.boxplot(x='indicador', y='EDAD_P', data=df_preg7_3)
plt.show()

# %%
"""
# Pregunta 8.

Se agrupan las categorías según el tipo de Establecimiento para cumplir la rúbrica. Otra manera de poder ordenarlos 
es ocupando la variable LOCAL_PART según el documento [del MINSAL](
https://repositoriodeis.minsal.cl/BDPublica/EsquemaRegistroNacimientos.pdf) 

Las categorías son:

* 3 para Hospitales.
* 4 para Clínicas.
* 5 para otros.

Podemos notar que los datos son asimétricos ya que se nota una gran frecuencia de nacimientos en Hospitales vs los otros
tipos de establecimientos. Podemos inferir entonces que la mayoría de los chilenos nace en un hospital y menos de la
mitad de estos lo hacen en una clínica. Otros centros representan una frecuencia casi despreciable vs el grupo 3 y 4.
"""

# %%
df_preg8 = df_general[(df_general.indicador == '3') | (df_general.indicador == '4') | (df_general.indicador == '5')]
sns.displot(df_preg8['indicador'])
plt.show()

# %%
"""
# Pregunta 9.

Para el cálculo del intervalo de confianza se utiliza la función interval del módulo Scipy de la librería Stats, ya
que por lo indicado en rúbrica se toma el supuesto que son distribuidos de manera normal.

Según estos resultados obtenemos los intervalos de confianza para la variable TALLA de
(49.36214187378248, 49.37036414499677) y para la variable PESO (3325.952812290933, 3327.49922931851).

Por lo tanto podemos inferir que los datos que están fuera de estos intervalos se consideran potencialmente atípicos,
por lo que que dependiendo del tipo de análisis que se realice podemos considerarlos o no.

En lo relacionado a los rangos intercuartiles para la variable TALLA, estos valores se encuentran entre 48 y 51,
diferente a lo entregado por el intervalo de confianza. aunque sin embargo y dependiendo de la pregunta a responder se
podrá ocupar un método u otro.

Con respecto a la variable PESO, sus valores intercuartiles se encuentran entre 3040 y 3660; quizás es aquí en donde
más difiera un resultado de un método sobre otro, por lo se recomienda escoger el que responda de mejor manera la
pregunta asociada.

[Fuente](https://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data)
"""

# %%
IC95_TALLA = st.t.interval(0.95, len(df_general['TALLA']), loc=df_general['TALLA'].mean(),
                           scale=df_general['TALLA'].sem())
IC95_TALLA

# %%
IC95_PESO = st.t.interval(0.95, len(df_general['PESO']), loc=df_general['PESO'].mean(), scale=df_general['PESO'].sem())
IC95_PESO

# %%
# con un describe obtengo inmediatamente el Q1 y el Q3.
df_general['TALLA'].describe()

# %%
df_general['PESO'].describe()

# %%
"""
# Pregunta 10.

Para determinar las características de los bebés, primero que todo se crean dos nuevos df con las características
solicitadas, es decir, para edades mayores a 40 y edades de la Madre menores a 18 años.

Luego de esto y aplicando la función describe, podemos identificar el comportamiento de algunas de las características
como son PESO, TALLA y SEMANAS, de esta manera se identifica si la edad tiene influencia sobre esta variables.

En estas últimas características podemos identificar que para las madres menores a 18 años el PESO de sus bebés tiene
un mínimo de 3.04 y un máximo de 3.65 kilos para la información entre el Q1 y el Q3.

Para las madres sobre 40 y la variables PESO se identifica que el rango entre Q1 y Q3 va desde los 2.9 kilos hasta los
3.6 kilos. 

Se puede notar que al menos en lo referente a los rangos intercuartiles no existe una mayor diferencia entre aquellas
madres que tiene bajo 18 y aquellas que tiene sobre 40.

Con respecto al promedio entre ambas podemos notar que tampoco existe una mayor diferencia ya que por el lado de la
madre menor a 18 años el promedio se encuentra en 3.29 kilos y en las madres de 40 en 3.31 kilos. 

En lo referente a las semanas de gestación podemos notar que el rango se encuentra entre 38 y 40 semanas para las
madres menores a 18 y entre 38 y 39 para las madres sobre 40; por lo que nuevamente no se notan mayores diferencias.

Por último y lo que guarda relación con la TALLA indica que para madres menores a 18 años la TALLA del bebé va entre
48 y 51 kilos y para las madres sobre 40 años también entre los 48 y 51 años.

Por lo tanto se puede concluir que indistintamente de las edades estudiadas el hijo nace prácticamente con las mismas
características, por lo que no se podría considerar un impedimento ser madre a los 40 años.
"""

# %%
# Nuevos df que identifican las características solicitadas.
df_madre_menor_18 = df_general[(df_general.EDAD_M < 18)]
df_madre_mayor_40 = df_general[(df_general.EDAD_M > 40)]

# %%
# Describe del PESO del bebé para madres menores a 18 años.
df_madre_menor_18.PESO.describe()

# %%
# Describe del PESO del bebé para madres mayores a 40 años.
df_madre_mayor_40.PESO.describe()

# %%
# Describe para SEMANAS para madres menores a 18 años.
df_madre_menor_18.SEMANAS.describe()

# %%
# Describe para SEMANAS para madres mayores a 40 años.
df_madre_mayor_40.SEMANAS.describe()

# %%
# Describe para TALLA para madres menores a 18 años.
df_madre_menor_18.TALLA.describe()

# %%
# Describe para TALLA para madres mayores a 40 años.
df_madre_mayor_40.TALLA.describe()
