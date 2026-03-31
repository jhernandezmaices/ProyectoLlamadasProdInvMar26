# LlamadasProduccion

## Descripción

Proyecto para extraer datos de llamadas telefónicas desde estados de cuenta en PDF y visualizar la comunicación entre colaboradores mediante grafos de red.

## Estructura del Proyecto

```
LlamadasProduccion/
├── PDFs de Estados de Cuenta
│   ├── Jaime 6871200911.pdf          # Estado de cuenta línea 6871200911
│   ├── Mario Delgado 3757560275.pdf  # Estado de cuenta línea 3757560275
│   ├── Mario Samuel 3321831266.pdf   # Estado de cuenta línea 3321831266
│   └── Telcel Unisem.pdf             # Cuenta consolidada múltiples líneas
├── Archivos CSV Generados
│   ├── ConcentradoLlamadas.csv       # Llamadas de 3 líneas individuales
│   ├── TelcelConcentradoLlamadas.csv # Llamadas de cuenta consolidada
│   ├── ConcentradoLlamadasTotal.csv  # Combinación de ambos archivos
│   └── ConcentradoProdInv.csv        # Llamadas con nombres de colaboradores
├── Scripts Python
│   ├── extract_calls.py              # Extracción de PDFs individuales
│   ├── extract_telcel.py             # Extracción de cuenta consolidada
│   └── grafo_comunicacion.py         # Generación de grafo de red
└── Resultados
    └── GrafoComunicacion.png         # Visualización de red de comunicación
```

## Extracción de Datos

### PDFs Individuales (Jaime, Mario Delgado, Mario Samuel)
- Archivo: `extract_calls.py`
- Extrae: NumeroOrigen, NumeroDestino, Fecha, Hora, Duracion
- Excluye llamadas entrantes (marcadas como "ENTRANTE")

### Cuenta Consolidada (Telcel Unisem)
- Archivo: `extract_telcel.py`
- Procesa múltiples líneas telefónicas
- Mismo formato de salida

### Concatenación
- Une `ConcentradoLlamadas.csv` + `TelcelConcentradoLlamadas.csv`
- Resultado: `ConcentradoLlamadasTotal.csv`

### Asignación de Colaboradores
- Mapping manual de números a nombres de colaboradores
- Resultado: `ConcentradoProdInv.csv`

## Generación de Grafo

### Script: `grafo_comunicacion.py`

**Entrada:** `ConcentradoProdInv.csv`

**Procesamiento:**
1. Agrega comunicaciones por par de colaboradores
2. Calcula peso: `num_llamadas + (duracion_total / 10)`
3. Crea grafo con NetworkX

**Visualización:**
- Nodos = Colaboradores (tamaño proporcional a conexiones)
- Líneas = Comunicación (grosor = intensidad)
- Etiquetas = Llamadas y duración

**Salida:** `GrafoComunicacion.png`

## Comandos Útiles

```bash
# Extraer llamadas de PDFs individuales
python3 extract_calls.py

# Extraer llamadas de Telcel Unisem
python3 extract_telcel.py

# Generar grafo de comunicación
python3 grafo_comunicacion.py
```

## Dependencias

```bash
pip install pandas matplotlib networkx
```

## Métricas del Proyecto

- Total llamadas extraídas: 198
- Colaboradores en la red: 10
- Conexiones entre colaboradores: 24

## Colaboradores Identificados

| Número | Nombre |
|--------|--------|
| 6871200911 | Jaime |
| 3757560275 | Mario Delgado |
| 3321831266 | Mario Hernández |
| 4622209603 | Victor |
| 4622510684 | Dulce |
| 4626213387 | Oscar |
| 4626213388 | Natalio |
| 4615469058 | Daniel |
| 4621032945 | Raymundo |
| 4622201013 | Mario Villegas |
| 4622201016 | José Manuel Meza |