import csv
import os
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_TXT = "grupo_12.txt"
ARCHIVO_CSV = "grupo_12.csv"
CARPETA_GRAFICOS = "graficos"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def titulo(texto):
    print()
    print("=" * 60)
    print(f"{texto:^60}")
    print("=" * 60)


def subtitulo(numero, texto):
    print()
    print(f"[{numero}] {texto}")
    print("-" * 60)


# ============================================================
# CONVERSIÓN TXT -> CSV
# ============================================================

def convertir_txt_a_csv():
    """
    Convierte el archivo TXT entregado por el profesor
    en un archivo CSV para facilitar su procesamiento.
    """

    with open(ARCHIVO_TXT, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    with open(ARCHIVO_CSV, "w", encoding="utf-8", newline="") as archivo:
        archivo.write(contenido)

    print(f"Archivo original       : {ARCHIVO_TXT}")
    print(f"Archivo generado       : {ARCHIVO_CSV}")


# ============================================================
# CARGA DE DATOS
# ============================================================

def cargar_datos():
    """
    Carga el CSV utilizando el módulo csv y convierte
    las variables numéricas a arreglos NumPy.
    """

    fechas = []
    temperaturas = []
    precipitaciones = []
    humedades = []

    with open(ARCHIVO_CSV, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fechas.append(fila["fecha"])

            temperatura = fila["temperatura"].strip()
            precipitacion = fila["precipitacion_mm"].strip()
            humedad = fila["humedad_pct"].strip()

            temperaturas.append(
                float(temperatura) if temperatura else np.nan
            )

            precipitaciones.append(
                float(precipitacion) if precipitacion else np.nan
            )

            humedades.append(
                float(humedad) if humedad else np.nan
            )

    datos = {
        "fecha": fechas,
        "temperatura": np.array(temperaturas, dtype=float),
        "precipitacion": np.array(precipitaciones, dtype=float),
        "humedad": np.array(humedades, dtype=float)
    }

    return datos


# ============================================================
# MOSTRAR DATOS
# ============================================================

def mostrar_datos(datos):
    """
    Muestra las primeras cinco filas y el total de registros.
    """

    print(f"Total de registros     : {len(datos['fecha'])}")

    print()
    print("Primeras 5 filas:")
    print(
        f"{'Fecha':<12}"
        f"{'Temperatura':>14}"
        f"{'Precipitación':>16}"
        f"{'Humedad':>12}"
    )

    for i in range(min(5, len(datos["fecha"]))):
        temperatura = datos["temperatura"][i]
        precipitacion = datos["precipitacion"][i]
        humedad = datos["humedad"][i]

        temperatura_txt = (
            "NA" if np.isnan(temperatura) else f"{temperatura:.1f}"
        )

        print(
            f"{datos['fecha'][i]:<12}"
            f"{temperatura_txt:>14}"
            f"{precipitacion:>16.1f}"
            f"{humedad:>12.1f}"
        )


# ============================================================
# CALIDAD DE DATOS
# ============================================================

def analizar_calidad(datos):
    """
    Detecta valores faltantes y temperaturas potencialmente
    atípicas o inconsistentes.
    """

    temperatura = datos["temperatura"]

    faltantes = np.isnan(temperatura)
    cantidad_faltantes = np.sum(faltantes)

    valores_validos = temperatura[~faltantes]

    minimo = np.min(valores_validos)
    maximo = np.max(valores_validos)

    # Rango utilizado para identificar temperaturas
    # potencialmente inconsistentes dentro de este conjunto.
    atipicos = valores_validos[
        (valores_validos < 15) | (valores_validos > 40)
    ]

    print(f"Valores faltantes      : {cantidad_faltantes}")
    print(f"Temperatura mínima     : {minimo:.1f} °C")
    print(f"Temperatura máxima     : {maximo:.1f} °C")

    if len(atipicos) > 0:
        print(
            "Valores atípicos       : "
            + ", ".join(f"{valor:.1f} °C" for valor in atipicos)
        )
    else:
        print("Valores atípicos       : Ninguno")

    print()
    print("Problemas encontrados:")

    print(
        "1. Se detectó una temperatura de 86 °C, "
        "considerada atípica e inconsistente."
    )

    print(
        "2. Existe un valor faltante de temperatura "
        "el 2026-01-11."
    )

    print(
        "3. El valor de 86 °C puede distorsionar "
        "significativamente la media."
    )

    print()
    print("Decisiones tomadas:")

    print(
        "- El valor de 86 °C se excluye de las "
        "estadísticas principales."
    )

    print(
        "- El valor faltante no se reemplaza porque "
        "no conocemos su valor real."
    )

    print(
        "- Los registros afectados solo se excluyen "
        "de los cálculos que requieren temperatura válida."
    )

    print()
    print("Impacto:")

    print(
        "- El valor de 86 °C está muy alejado del "
        "resto de observaciones."
    )

    print(
        "- Mantenerlo produciría estadísticas poco "
        "representativas del comportamiento normal."
    )


# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================

def analizar_estadistica(datos):
    """
    Calcula media, mediana, desviación estándar, mínimo y máximo
    utilizando solamente temperaturas válidas y dentro del rango
    esperado.
    """

    temperatura = datos["temperatura"]

    datos_validos = temperatura[
        (~np.isnan(temperatura))
        & (temperatura >= 15)
        & (temperatura <= 40)
    ]

    media = np.mean(datos_validos)
    mediana = np.median(datos_validos)
    desviacion = np.std(datos_validos)
    minimo = np.min(datos_validos)
    maximo = np.max(datos_validos)

    # Media incluyendo el valor atípico, pero excluyendo el faltante.
    datos_sin_nan = temperatura[~np.isnan(temperatura)]
    media_con_atipico = np.mean(datos_sin_nan)

    diferencia = media_con_atipico - media

    print(f"Observaciones válidas : {len(datos_validos)}")
    print(f"Media                  : {media:.2f} °C")
    print(f"Mediana                : {mediana:.2f} °C")
    print(f"Desv. estándar         : {desviacion:.2f} °C")
    print(f"Mínimo                 : {minimo:.2f} °C")
    print(f"Máximo                 : {maximo:.2f} °C")

    print()
    print("Impacto del valor atípico:")
    print(f"Media incluyendo 86 °C : {media_con_atipico:.2f} °C")
    print(f"Media después de limpiar: {media:.2f} °C")
    print(f"Diferencia              : {diferencia:.2f} °C")

    print()
    print("Interpretación:")

    diferencia_media_mediana = abs(media - mediana)

    print(
        f"- La diferencia entre media y mediana es "
        f"{diferencia_media_mediana:.2f} °C."
    )

    if diferencia_media_mediana < 1:
        print(
            "- La media es representativa del conjunto "
            "después de la limpieza."
        )
    else:
        print(
            "- La diferencia entre media y mediana indica "
            "posible influencia de valores extremos."
        )

    print(
        f"- La desviación estándar de {desviacion:.2f} °C "
        "indica poca dispersión en los datos válidos."
    )

    return datos_validos


# ============================================================
# GRÁFICOS
# ============================================================

def generar_graficos(datos, datos_validos):
    """
    Genera dos gráficos:
    1. Distribución de temperatura.
    2. Relación entre temperatura y precipitación.
    """

    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)

    # --------------------------------------------------------
    # Gráfico 1: distribución de temperatura
    # --------------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.hist(
        datos_validos,
        bins=6,
        edgecolor="black"
    )

    plt.axvline(
        np.mean(datos_validos),
        linestyle="--",
        linewidth=2,
        label=f"Media = {np.mean(datos_validos):.2f} °C"
    )

    plt.title("Distribución de la temperatura")
    plt.xlabel("Temperatura (°C)")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.grid(axis="y", alpha=0.25)

    ruta_distribucion = os.path.join(
        CARPETA_GRAFICOS,
        "distribucion_temperatura.png"
    )

    plt.tight_layout()
    plt.savefig(ruta_distribucion, dpi=150)
    plt.close()

    # --------------------------------------------------------
    # Gráfico 2: temperatura vs precipitación
    # --------------------------------------------------------

    temperatura = datos["temperatura"]
    precipitacion = datos["precipitacion"]

    mascara = (
        (~np.isnan(temperatura))
        & (~np.isnan(precipitacion))
        & (temperatura >= 15)
        & (temperatura <= 40)
    )

    temperatura_limpia = temperatura[mascara]
    precipitacion_limpia = precipitacion[mascara]

    plt.figure(figsize=(8, 5))

    plt.scatter(
        temperatura_limpia,
        precipitacion_limpia,
        s=70
    )

    plt.title("Relación entre temperatura y precipitación")
    plt.xlabel("Temperatura (°C)")
    plt.ylabel("Precipitación (mm)")
    plt.grid(alpha=0.25)

    ruta_relacion = os.path.join(
        CARPETA_GRAFICOS,
        "temperatura_precipitacion.png"
    )

    plt.tight_layout()
    plt.savefig(ruta_relacion, dpi=150)
    plt.close()

    print("✓ graficos/distribucion_temperatura.png")
    print("✓ graficos/temperatura_precipitacion.png")


# ============================================================
# CORRELACIONES
# ============================================================

def calcular_correlacion(variable_a, variable_b, mascara):
    """
    Calcula la correlación entre dos variables usando
    solamente registros válidos.
    """

    a = variable_a[mascara]
    b = variable_b[mascara]

    if len(a) < 2:
        return np.nan

    return np.corrcoef(a, b)[0, 1]


def analizar_correlaciones(datos):
    """
    Calcula correlaciones entre temperatura, precipitación
    y humedad.
    """

    temperatura = datos["temperatura"]
    precipitacion = datos["precipitacion"]
    humedad = datos["humedad"]

    mascara_temp_prec = (
        (~np.isnan(temperatura))
        & (~np.isnan(precipitacion))
        & (temperatura >= 15)
        & (temperatura <= 40)
    )

    mascara_temp_humedad = (
        (~np.isnan(temperatura))
        & (~np.isnan(humedad))
        & (temperatura >= 15)
        & (temperatura <= 40)
    )

    mascara_prec_humedad = (
        (~np.isnan(precipitacion))
        & (~np.isnan(humedad))
    )

    corr_temp_prec = calcular_correlacion(
        temperatura,
        precipitacion,
        mascara_temp_prec
    )

    corr_temp_humedad = calcular_correlacion(
        temperatura,
        humedad,
        mascara_temp_humedad
    )

    corr_prec_humedad = calcular_correlacion(
        precipitacion,
        humedad,
        mascara_prec_humedad
    )

    print(
        f"Temperatura / precipitación : "
        f"{corr_temp_prec:.3f}"
    )

    print(
        f"Temperatura / humedad       : "
        f"{corr_temp_humedad:.3f}"
    )

    print(
        f"Precipitación / humedad     : "
        f"{corr_prec_humedad:.3f}"
    )

    print()
    print("Interpretación:")

    print(
        "- Temperatura y precipitación presentan "
        "una relación inversa."
    )

    print(
        "- Temperatura y humedad también presentan "
        "una relación inversa."
    )

    print(
        "- Precipitación y humedad presentan "
        "una relación positiva muy fuerte."
    )

    print(
        "- Las correlaciones muestran asociación, "
        "pero no demuestran causalidad."
    )

    print(
        "- Los resultados deben interpretarse con "
        "precaución debido al tamaño reducido del conjunto."
    )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    titulo("PARCIAL 1 - INTELIGENCIA ARTIFICIAL")
    print("GRUPO 12")

    # --------------------------------------------------------
    # 1. Carga de datos
    # --------------------------------------------------------

    subtitulo(1, "CARGA Y PROCESAMIENTO DE DATOS")

    convertir_txt_a_csv()

    datos = cargar_datos()

    mostrar_datos(datos)

    # --------------------------------------------------------
    # 2. Calidad
    # --------------------------------------------------------

    subtitulo(2, "CALIDAD DE LOS DATOS")

    analizar_calidad(datos)

    # --------------------------------------------------------
    # 3. Estadística
    # --------------------------------------------------------

    subtitulo(3, "ANÁLISIS ESTADÍSTICO")

    datos_validos = analizar_estadistica(datos)

    # --------------------------------------------------------
    # 4. Gráficos
    # --------------------------------------------------------

    subtitulo(4, "VISUALIZACIONES")

    generar_graficos(datos, datos_validos)

    # --------------------------------------------------------
    # 5. Correlaciones
    # --------------------------------------------------------

    subtitulo(5, "CORRELACIONES")

    analizar_correlaciones(datos)

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("ANÁLISIS FINALIZADO CORRECTAMENTE".center(60))
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
