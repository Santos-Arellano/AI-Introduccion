# Sistema de Red Bayesiana con Motor de Inferencia por Enumeración

## Descripción del Proyecto

Este proyecto implementa un **Motor de Inferencia por Enumeración** para Redes Bayesianas, desarrollado con programación orientada a objetos en Python.

## 📚 Información del Proyecto

- **Curso**: Inteligencia Artificial
- **Profesor**: Ing. Laura Juliana Mora Páez Msc
- **Grupo**: [5]
- **Integrantes**: 
- Alejandra Abaunza Suárez 
- Daniel Santiago Avila Medina
- Santos Alejandro Arellano Olarte
- Jeison Camilo Alfonso Moreno

## Características Principales

### 1. Estructura de Red Bayesiana
- **Clase Nodo**: Representa nodos individuales con sus padres, hijos y tablas de probabilidad condicional
- **Clase Arco**: Representa conexiones dirigidas entre nodos
- **Clase RedBayesiana**: Gestiona la estructura completa de la red, incluyendo:
  - Carga desde archivos
  - Validación de integridad (detección de ciclos)
  - Visualización de estructura
  - Gestión de tablas de probabilidad

### 2. Motor de Inferencia
- Implementa **inferencia por enumeración exacta**
- Calcula probabilidades condicionales: P(consulta | evidencia)
- Genera **traza detallada** del proceso de inferencia
- Maneja múltiples variables de evidencia

### 3. Funcionalidades
- Carga de estructura y probabilidades desde archivos de texto
- Validación automática de la red
- Interfaz interactiva por consola
- Visualización de tablas de probabilidad
- Ejemplos de prueba predefinidos

## Estructura de Archivos

```
proyecto/
│
├── nodo.py                    # Clase Nodo
├── arco.py                    # Clase Arco
├── red_bayesiana.py          # Clase RedBayesiana
├── motor_inferencia.py       # Motor de Inferencia
├── main.py                   # Programa principal
│
├── estructura.txt            # Archivo de estructura de la red
├── probabilidades.txt        # Archivo de probabilidades
│
└── README.md                 # Este archivo
```

## Formato de Archivos

### Archivo de Estructura (estructura.txt)

Cada línea representa un arco de la red:
```
nodo_padre nodo_hijo
```

Ejemplo:
```
# Comentarios comienzan con #
Lluvia Cesped_Mojado
Aspersor Cesped_Mojado
```

### Archivo de Probabilidades (probabilidades.txt)

```
NODO: nombre_nodo
valores_padres | valor_nodo | probabilidad
```

Ejemplo:
```
NODO: Lluvia
| True | 0.2
| False | 0.8

NODO: Cesped_Mojado
True True | True | 0.99
True False | True | 0.90
False True | True | 0.90
False False | True | 0.01
```

## Uso del Sistema

### Ejecución de Pruebas y Ejemplos

- Suite de pruebas automatizadas:

```bash
python test_suite.py
```

- Archivos de ejemplo en la raíz del proyecto:
  - `estructura.txt`: estructura de la red (Lluvia-Aspersor-Césped Mojado)
  - `probabilidades.txt`: CPTs correspondientes

- Ejemplos adicionales de estructuras (no utilizados por las pruebas) están en `examples/`.

## Ejemplo de Red Incluido

Red clásica de **Lluvia-Aspersor-Césped Mojado**:

```
    Lluvia      Aspersor
       \          /
        \        /
         \      /
      Cesped_Mojado
```

### Variables:
- **Lluvia**: {True, False} - P(Lluvia=True) = 0.2
- **Aspersor**: {True, False} - P(Aspersor=True) = 0.1
- **Cesped_Mojado**: {True, False} - Depende de Lluvia y Aspersor

### Consultas de Ejemplo:

1. **P(Lluvia | Césped Mojado)**: ¿Llovió dado que el césped está mojado?
2. **P(Aspersor | Césped Mojado)**: ¿Está el aspersor encendido dado que el césped está mojado?
3. **P(Césped Mojado | Lluvia, Aspersor)**: Probabilidad de césped mojado dadas condiciones específicas

## Algoritmo de Inferencia por Enumeración

El motor implementa el algoritmo:

```
P(X|e) = α · Σ_y P(X, e, y)
```

Donde:
- **X**: Variable(s) de consulta
- **e**: Evidencia (variables observadas)
- **y**: Variables ocultas (no observadas)
- **α**: Constante de normalización

### Proceso:
1. Identificar variables ocultas
2. Enumerar sobre todas las combinaciones de variables ocultas
3. Para cada combinación, calcular probabilidad conjunta
4. Sumar probabilidades
5. Normalizar resultado

## Características del Diseño OOP

### Encapsulación
- Cada clase maneja sus propios datos y comportamiento
- Atributos privados con métodos de acceso controlado

### Modularidad
- Clases independientes con responsabilidades bien definidas
- Fácil extensión y mantenimiento

### Reutilización
- Clases genéricas aplicables a cualquier dominio
- No dependen de dominios específicos

### Abstracción
- Interfaces claras entre componentes
- Complejidad oculta al usuario final

## Extensiones Posibles

1. **Algoritmos adicionales**: 
   - Eliminación de variables
   - Muestreo de Gibbs
   - Inferencia aproximada

2. **Interfaz gráfica**:
   - Visualización de la red
   - Editor interactivo

3. **Optimizaciones**:
   - Caché de resultados
   - Paralelización
   - Estructuras de datos eficientes

4. **Validaciones**:
   - Verificación de probabilidades (sumen 1)
   - Detección de inconsistencias

## Requisitos

- Python 3.7 o superior
- No requiere bibliotecas externas

## Autores

[Nombres de los estudiantes del grupo]

## Documentación Técnica

### Clase Nodo
- Representa una variable aleatoria en la red
- Almacena relaciones (padres/hijos)
- Gestiona tabla de probabilidad condicional (CPT)

### Clase Arco
- Representa dependencia causal entre variables
- Mantiene referencias a nodos origen y destino
- Actualiza automáticamente relaciones bidireccionales

### Clase RedBayesiana
- Contenedor principal de la estructura
- Gestiona carga/validación
- Proporciona operaciones sobre toda la red

### Clase MotorInferencia
- Implementa algoritmo de enumeración
- Genera traza detallada del proceso
- Calcula probabilidades condicionales y marginales

## Complejidad

- **Temporal**: O(2^n) donde n es el número de variables ocultas
- **Espacial**: O(n) para la estructura de la red

## Pruebas y Validación

El sistema incluye:
- Validación automática de la red (ciclos, probabilidades)
- Suite de pruebas predefinidas
- Ejemplos verificables contra cálculos manuales

## Soporte

Para problemas o preguntas, contactar a los autores del proyecto.

---

**Proyecto 3 - Sistemas Basados en Reglas**  
**Motor de Inferencia por Enumeración para Redes Bayesianas**
