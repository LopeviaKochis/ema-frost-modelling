# EMA Frost Modelling ❄️🌡️

Este proyecto tiene como objetivo desarrollar modelos de Machine Learning para la predicción de heladas (meteorológicas y agrícolas) utilizando datos históricos de Estaciones Meteorológicas Automáticas (EMA) entre los años **2018 y 2025**.

El flujo de trabajo abarca desde la limpieza de datos y el análisis exploratorio (EDA) hasta la implementación de modelos de regresión (Random Forest) y sistemas de alerta temprana tipo "semáforo".

## Estructura del Proyecto

```text
.
├── data/
│   ├── raw/                  # Datos crudos horarios (2018-2025)
│   │   ├── temp2m_*.csv      # Temperatura a 2 metros
│   │   ├── radinf_*.csv      # Radiación infrarroja
│   │   ├── HR_*.csv          # Humedad Relativa
│   │   └── ... (pp, press, vel, dir)
│   └── processed/            # Datos limpios y listos para modelar
│       ├── df_clean_v2.csv   # Dataset limpio con imputaciones
│       └── df_model_v2.csv   # Dataset con ingeniería de características (Lags)
├── notebooks/
│   ├── ema_eda_v2.ipynb      # EDA principal: Limpieza, vectores de viento y lags
│   ├── ema_eda.ipynb         # Versión anterior del EDA
│   └── modelling/
│       ├── ema_ml_v2.ipynb   # Modelo Final: Random Forest + Semáforo de Heladas
│       ├── ema_ml.ipynb      # Experimentos base (Regresión Lineal)
│       └── ema_dl.ipynb      # Experimentos de Deep Learning
├── results/                  # Gráficos generados (EDA y Modelado)
├── requirements.txt          # Dependencias del proyecto
└── .gitignore
```

## Instalación y Configuración

1. **Clonar el repositorio** (si aplica) o descargar los archivos.
2. **Crear un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate
   ```
3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Datos y Variables

El modelo utiliza registros horarios de las siguientes variables físicas:

*   **temp2m**: Temperatura del aire a 2 metros (Variable objetivo principal).
*   **tempsup**: Temperatura de superficie.
*   **radinf**: Radiación infrarroja.
*   **HR**: Humedad Relativa.
*   **pp**: Precipitación.
*   **press**: Presión atmosférica.
*   **vel**: Velocidad del viento.
*   **dir**: Dirección del viento (Transformada a componentes vectoriales `dir_sin` y `dir_cos`).

##  Metodología

### 1. Análisis Exploratorio y Preprocesamiento (`ema_eda_v2.ipynb`)
*   **Limpieza:** Manejo de valores nulos mediante interpolación temporal para variables continuas.
*   **Ingeniería de Características:**
    *   Transformación de la dirección del viento (grados) a componentes vectoriales (Seno/Coseno).
    *   Creación de variables de rezago (**Lags**): `temp2m_lag1` (temperatura de la hora anterior) para capturar la inercia térmica.

### 2. Modelamiento (`modelling/ema_ml_v2.ipynb`)
Se evaluaron varios enfoques, seleccionando finalmente un **Random Forest Regressor** debido a su capacidad para capturar no linealidades.

*   **Modelo Base:** Regresión Lineal (Resultados limitados, $R^2 \approx 0.3 - 0.5$).
*   **Modelo Final:** Random Forest con variables de lag.
    *   **Métricas alcanzadas:**
        *   MAE (Error Absoluto Medio): ~0.5 °C
        *   $R^2$: > 0.90

### 3. Sistema de Alerta (Semáforo)
Las predicciones numéricas se convierten en categorías de riesgo para la toma de decisiones:

| Color | Categoría | Definición | Acción |
| :--- | :--- | :--- | :--- |
| 🟢 **Verde** | Normal | $T > 0^\circ C$ | Sin riesgo. |
| 🟡 **Amarillo** | Helada Meteorológica | $0^\circ C \ge T > -2^\circ C$ | Alerta preventiva. |
| 🔴 **Rojo** | Helada Agrícola | $T \le -2^\circ C$ | Daño severo a cultivos. |

## Resultados

Los gráficos de evaluación se encuentran en la carpeta `results/`. El modelo final demuestra una alta capacidad para seguir las tendencias de temperatura nocturna y predecir caídas bruscas asociadas a eventos de helada.

---
*Desarrollado con Python, Pandas y Scikit-Learn# EMA Frost Modelling
