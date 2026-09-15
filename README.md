# Parcial 1 - Inteligencia Artificial - Monica Parra

## Grupo 12

Análisis exploratorio de datos climáticos utilizando Python, NumPy y Matplotlib, ejecutado mediante Docker.

## 1. Descripción del proyecto

El objetivo es realizar un análisis exploratorio sobre un conjunto de datos climáticos asignado al Grupo 12, identificando problemas de calidad, calculando estadísticas descriptivas, generando visualizaciones e interpretando las relaciones entre las variables.

El archivo original entregado para el análisis es `grupo_12.txt`.

Variables:

- `fecha`
- `temperatura`
- `precipitacion_mm`
- `humedad_pct`

## 2. Tecnologías utilizadas

- Python 3.12
- NumPy
- Matplotlib
- Docker
- Docker Compose
- Git
- GitHub

## 3. Estructura del proyecto

```text
parcial1-ia-grupo12/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── analisis.py
├── README.md
├── grupo_12.txt
├── grupo_12.csv
└── graficos/
    ├── distribucion_temperatura.png
    └── temperatura_precipitacion.png
```

## 4. Ejecución

Construcción:

```bash
docker compose build
```

Ejecución:

```bash
docker compose up
```

El programa convierte el archivo TXT a CSV, carga los datos, realiza el análisis estadístico y genera los gráficos.

## 5. Carga y exploración de datos

El conjunto contiene 12 registros.

Las primeras cinco observaciones son:

| Fecha | Temperatura | Precipitación (mm) | Humedad (%) |
| :--- | :---: | :---: | :---: |
| 2026-01-01 | 28 | 10 | 70 |
| 2026-01-02 | 29 | 5 | 68 |
| 2026-01-03 | 27 | 15 | 72 |
| 2026-01-04 | 86 | 20 | 74 |
| 2026-01-05 | 30 | 8 | 69 |

La variable principal seleccionada es temperatura.

## 6. Problemas de calidad de los datos

### Problema 1: Dato faltante
El día 2026-01-11 no tiene temperatura registrada:
`2026-01-11,,22,76`

- Se detectó mediante la revisión de valores vacíos.
- No se imputó un valor porque no existe información adicional suficiente para estimarlo confiablemente.
- El dato faltante reduce la cantidad de observaciones disponibles para el análisis.

### Problema 2: Valor atípico
El día 2026-01-04 presenta una temperatura de 86 °C.

- El resto de las temperaturas válidas se encuentra entre 26 °C y 31 °C.
- El valor fue detectado mediante la revisión del rango y comparación con las demás observaciones.
- Se excluyó de las estadísticas principales, pero no se modificó el archivo original.

### Problema 3: Inconsistencia de rango
El valor de 86 °C también representa una posible inconsistencia de medición o registro porque está muy alejado del comportamiento general de los datos.

- Debe validarse contra la fuente original antes de determinar si corresponde a una medición real, un error de registro o una inconsistencia de unidad.
- No se afirmó una causa específica sin evidencia adicional.

## 7. Estadística descriptiva

Después de excluir el valor de 86 °C y el dato faltante se analizaron 10 temperaturas válidas.

| Estadística | Resultado |
| :--- | :--- |
| **Media** | 28.40 °C |
| **Mediana** | 28.50 °C |
| **Desviación estándar** | 1.43 °C |
| **Mínimo** | 26 °C |
| **Máximo** | 31 °C |

**¿La media es representativa?**
Sí, de manera razonable. La media es 28.40 °C y la mediana es 28.50 °C, por lo que ambas son muy cercanas. La desviación estándar de 1.43 °C también indica una dispersión relativamente baja. Sin embargo, la conclusión debe tomarse con precaución porque solo existen 10 observaciones válidas.

El valor de 86 °C demuestra la importancia de limpiar los datos antes de calcular estadísticas. Con el valor de 86 °C incluido, la media sería 33.64 °C, mientras que después de excluirlo es 28.40 °C. La diferencia es de 5.24 °C.

## 8. Gráfico de distribución

Archivo: `graficos/distribucion_temperatura.png`

- El gráfico muestra que la mayoría de las temperaturas se concentra entre 26 °C y 31 °C.
- El valor de 86 °C se encuentra separado del comportamiento general y puede identificarse como un valor sospechoso.

## 9. Relación entre temperatura y precipitación

Archivo: `graficos/temperatura_precipitacion.png`

La correlación entre temperatura y precipitación es aproximadamente: **-0.710**

- Esto representa una relación lineal negativa relativamente fuerte dentro de este pequeño conjunto.
- Las observaciones con mayor temperatura tienden a estar asociadas con menores valores de precipitación.
- Sin embargo, correlación no significa causalidad. No se puede afirmar que la temperatura cause directamente cambios en la precipitación únicamente con estos datos.

## 10. Correlaciones

| Variables | Correlación |
| :--- | :---: |
| Temperatura - Precipitación | -0.710 |
| Temperatura - Humedad | -0.713 |
| Precipitación - Humedad | 0.997 |

- La relación entre precipitación y humedad es muy alta y positiva (0.997).
- La temperatura presenta relaciones negativas con precipitación (-0.710) y humedad (-0.713).
- Estas relaciones representan asociaciones estadísticas y no demuestran causalidad.

## 11. Interpretación para Cartago

Los datos muestran una temperatura promedio limpia de 28.40 °C y una desviación estándar de 1.43 °C. La precipitación y la humedad presentan una correlación de 0.997, indicando que dentro de este conjunto ambas variables se comportan de manera muy similar.

La relación negativa de -0.710 entre temperatura y precipitación indica que los registros con mayor temperatura tienden a coincidir con menores niveles de precipitación. Sin embargo, solo se analizaron 12 días, por lo que estos resultados no pueden representar por sí solos el comportamiento climático general de Cartago.

## 12. Patrón no obvio

El patrón más destacado es la correlación de 0.997 entre precipitación y humedad. También resulta importante observar que un único valor, 86 °C, modifica el promedio de 28.40 °C a 33.64 °C. Esto demuestra que los valores atípicos pueden cambiar considerablemente las conclusiones estadísticas.

## 13. Recomendación

Se recomienda implementar una validación de calidad antes de utilizar los datos para tomar decisiones. Se deben considerar especialmente:

- Validar el registro de 86 °C.
- Investigar el dato faltante del 2026-01-11.
- Utilizar inicialmente la temperatura promedio limpia de 28.40 °C.
- Considerar la desviación estándar de 1.43 °C para detectar cambios relevantes.
- Ampliar el análisis más allá de los 12 registros disponibles.

## 14. Limitaciones

- Solo existen 12 registros.
- Solo hay 10 temperaturas válidas.
- Existe un dato faltante.
- Existe un valor sospechoso de 86 °C.
- El periodo de observación es demasiado corto para representar todo el comportamiento climático de Cartago.
- Las correlaciones no permiten establecer causalidad.
- No se dispone de otras variables meteorológicas importantes.

## 15. Datos adicionales necesarios

Para mejorar el análisis serían útiles:

- Datos de varios meses o años.
- Temperatura máxima, mínima y promedio.
- Precipitación diaria.
- Humedad relativa.
- Velocidad y dirección del viento.
- Presión atmosférica.
- Radiación solar.
- Ubicación exacta de la estación.
- Información del instrumento utilizado para las mediciones.

## 16. Conclusión

El análisis permitió identificar problemas de calidad, calcular estadísticas descriptivas y estudiar relaciones entre las variables.

La temperatura válida presenta:
- **Media:** 28.40 °C
- **Mediana:** 28.50 °C
- **Desviación estándar:** 1.43 °C
- **Mínimo:** 26 °C
- **Máximo:** 31 °C

Se identificó un valor sospechoso de 86 °C y un dato faltante de temperatura.

Las principales correlaciones fueron:
- **Temperatura - precipitación:** -0.710
- **Temperatura - humedad:** -0.713
- **Precipitación - humedad:** 0.997

Los resultados son útiles como exploración inicial, pero el tamaño reducido de la muestra impide realizar generalizaciones climáticas confiables.

## 17. Archivos generados

- `grupo_12.csv`
- `graficos/distribucion_temperatura.png`
- `graficos/temperatura_precipitacion.png`
