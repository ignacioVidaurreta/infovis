## 3 Formas de Visualizar un Dataset
Formas de visualizar la información en `datasets/argentina_1869-2020.tsv`

**Nota: Algunas provincias tienen valores es NULL que quiere decir que no hay datos para ciertos años. En esos casos se toma la decisión de tomarlos como si fuesen 0**

### Choropleth Map con slider
La idea de este mapa es que nos muestre la información de forma geográfica
y podemos observar la evolución de estos datos a través del tiempo con un slider.
![Choropleth Map de Argentina](../media/choropleth_ARG.png "Ejemplo de Mapa")

### Small Multiples
Esta visualización puede ser muy útil para observar cómo evolucionan los datos a traves del tiempo. La idea sería mostrarlo en una grilla 5x4 y cada una coloreada con el color de su región.
![Ejemplo de Small Multiples](../media/small_multiples.png "Ejemplo de Small Multiples")

### Stacked Area Chart
Esta visualización nos puede dar a simple vista, qué provincias son las predominantes en cuanto al dato a estudiar a través del tiempo. Dado que son 24 colores la representación puede ser complicada. Entonces quizá lo mejor sería agregar por región y observar la cantidad de población por región, repetir colores o no mostrar todos sino los que tengan mayor cantidad de información (aunque conservar la mayor cantidad de datos que pueda conservar)

A la hora de pensar un gráfico así también se me ocurrió quizá hacer un *bar chart* pero la desventaja de este gráfico es que no encontré forma de mostrarlo a través del tiempo sin usar un slider que no me parecía tan útil como su alternativa que era el *stacked area chart*. La ventaja del *bar chart* es que podes colorear los *bins* por región, entonces si en algún momento necesitase graficar la información en un año específico, seguramente utilizaría este tipo de gráfico.

![Ejemplo de Stacked Area Chart](../media/stacked_area_graph.png "Ejemplo Stacked Area Chart")
