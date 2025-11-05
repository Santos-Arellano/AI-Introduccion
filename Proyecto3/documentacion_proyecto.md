# Documentación del Proyecto
## Sistema de Red Bayesiana con Motor de Inferencia por Enumeración

---

## 1. INTRODUCCIÓN

### 1.1 Objetivo del Proyecto
Desarrollar un sistema completo de Red Bayesiana con un motor de inferencia por enumeración que permita:
- Modelar relaciones causales probabilísticas entre variables
- Realizar inferencia exacta para responder consultas bajo incertidumbre
- Proporcionar trazabilidad del proceso de razonamiento

### 1.2 Alcance
El sistema implementa:
- Estructura de datos para representar Redes Bayesianas
- Carga de estructura y probabilidades desde archivos
- Motor de inferencia por enumeración exacta
- Interfaz de usuario interactiva
- Validación y verificación automática

---

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Diseño Orientado a Objetos

El sistema está diseñado con cuatro clases principales que modelan las entidades fundamentales de una Red Bayesiana:

#### **Clase Nodo**
- **Responsabilidad**: Representar una variable aleatoria
- **Atributos principales**:
  - `nombre`: Identificador único
  - `padres`: Lista de nodos padres (causas)
  - `hijos`: Lista de nodos hijos (efectos)
  - `tabla_probabilidad`: CPT (Conditional Probability Table)
  - `valores_posibles`: Dominio de la variable

- **Métodos principales**:
  - `agregar_padre()`: Establece relación de dependencia
  - `agregar_hijo()`: Registra nodos dependientes
  - `establecer_probabilidad()`: Define valores de la CPT
  - `obtener_probabilidad()`: Consulta probabilidades condicionales
  - `mostrar_tabla_probabilidad()`: Visualización de la CPT

#### **Clase Arco**
- **Responsabilidad**: Representar dependencia causal entre variables
- **Atributos principales**:
  - `nodo_origen`: Nodo padre (causa)
  - `nodo_destino`: Nodo hijo (efecto)

- **Métodos principales**:
  - Constructor: Actualiza automáticamente relaciones bidireccionales
  - `es_valido()`: Verifica consistencia
  - `invertir()`: Permite cambiar dirección (con precaución)

#### **Clase RedBayesiana**
- **Responsabilidad**: Gestionar la red completa
- **Atributos principales**:
  - `nodos`: Diccionario de nodos indexados por nombre
  - `arcos`: Lista de todas las conexiones

- **Métodos principales**:
  - `cargar_estructura_desde_archivo()`: Parse de estructura
  - `cargar_probabilidades_desde_archivo()`: Parse de CPTs
  - `obtener_raices()`: Identifica nodos sin padres
  - `mostrar_estructura()`: Visualización en texto
  - `validar_red()`: Verifica integridad (ciclos, probabilidades)

#### **Clase MotorInferencia**
- **Responsabilidad**: Realizar inferencia probabilística
- **Atributos principales**:
  - `red`: Referencia a la RedBayesiana
  - `traza_activa`: Control de verbosidad
  - `nivel_traza`: Control de indentación en traza

- **Métodos principales**:
  - `inferir()`: Calcula P(consulta | evidencia)
  - `_enumerar_todas()`: Enumeración recursiva sobre variables ocultas
  - `_calcular_probabilidad_conjunta()`: Calcula P(X₁,...,Xₙ)

### 2.2 Diagrama de Clases

```
┌─────────────────┐
│     Nodo        │
├─────────────────┤
│ - nombre        │
│ - padres[]      │
│ - hijos[]       │
│ - tabla_prob{}  │
├─────────────────┤
│ + agregar_padre()│
│ + agregar_hijo() │
│ + establecer_p() │
└─────────────────┘
        △
        │ usa
        │
┌───────┴─────────┐
│      Arco       │
├─────────────────┤
│ - origen        │
│ - destino       │
├─────────────────┤
│ + es_valido()   │
└─────────────────┘
        △
        │ contiene
        │
┌───────┴─────────────┐
│  RedBayesiana       │
├─────────────────────┤
│ - nodos{}           │
│ - arcos[]           │
├─────────────────────┤
│ + cargar_estructura()│
│ + cargar_probs()    │
│ + validar_red()     │
└─────────────────────┘
        △
        │ usa
        │
┌───────┴──────────────┐
│  MotorInferencia     │
├──────────────────────┤
│ - red                │
│ - traza_activa       │
├──────────────────────┤
│ + inferir()          │
│ + _enumerar_todas()  │
└──────────────────────┘
```

---

## 3. ALGORITMO DE INFERENCIA

### 3.1 Fundamento Teórico

El motor implementa **inferencia por enumeración exacta**, basado en la regla de Bayes y la regla de la cadena:

**Fórmula de Inferencia:**
```
P(X | e) = α · P(X, e) = α · Σ_y P(X, e, y)
```

Donde:
- **X**: Variable de consulta
- **e**: Evidencia (variables observadas)
- **y**: Variables ocultas (no observadas)
- **α**: Constante de normalización = 1 / P(e)

**Regla de la Cadena:**
```
P(X₁,...,Xₙ) = ∏ᵢ P(Xᵢ | Parents(Xᵢ))
```

### 3.2 Pseudocódigo

```
INFERIR(consulta, evidencia):
    variables_ocultas ← NODOS - consulta - evidencia
    
    PARA CADA valor_consulta EN dominio(consulta):
        asignacion ← {consulta: valor_consulta} ∪ evidencia
        prob[valor_consulta] ← ENUMERAR_TODAS(variables_ocultas, asignacion)
    
    NORMALIZAR(prob)
    RETORNAR prob

ENUMERAR_TODAS(variables, asignacion):
    SI variables está vacío:
        RETORNAR PROB_CONJUNTA(asignacion)
    
    variable ← PRIMERA(variables)
    resto ← RESTO(variables)
    suma ← 0
    
    PARA CADA valor EN dominio(variable):
        nueva_asignacion ← asignacion ∪ {variable: valor}
        suma ← suma + ENUMERAR_TODAS(resto, nueva_asignacion)
    
    RETORNAR suma

PROB_CONJUNTA(asignacion):
    producto ← 1
    
    PARA CADA variable EN asignacion:
        valores_padres ← [asignacion[p] PARA p EN padres(variable)]
        prob ← P(variable=asignacion[variable] | valores_padres)
        producto ← producto × prob
    
    RETORNAR producto
```

### 3.3 Ejemplo de Ejecución

**Red**: Lluvia → Césped_Mojado ← Aspersor

**Consulta**: P(Lluvia=True | Césped_Mojado=True)

**Proceso**:
```
1. Variables ocultas: {Aspersor}

2. Enumerar para Lluvia=True:
   - Aspersor=True:
     P(Lluvia=T, Aspersor=T, Césped=T) = 
       P(Lluvia=T) × P(Aspersor=T) × P(Césped=T|Lluvia=T,Aspersor=T)
       = 0.2 × 0.1 × 0.99 = 0.0198
   
   - Aspersor=False:
     P(Lluvia=T, Aspersor=F, Césped=T) = 
       P(Lluvia=T) × P(Aspersor=F) × P(Césped=T|Lluvia=T,Aspersor=F)
       = 0.2 × 0.9 × 0.90 = 0.162
   
   Total Lluvia=True: 0.0198 + 0.162 = 0.1818

3. Enumerar para Lluvia=False:
   Similar proceso...
   Total Lluvia=False: 0.0738

4. Normalización:
   α = 1 / (0.1818 + 0.0738) = 3.914
   
   P(Lluvia=True | Césped=True) = 0.1818 × 3.914 = 0.711
   P(Lluvia=False | Césped=True) = 0.0738 × 3.914 = 0.289
```

### 3.4 Complejidad

- **Temporal**: O(d^n) donde:
  - d = tamaño del dominio de las variables
  - n = número de variables ocultas
  
- **Espacial**: O(n) para la pila de recursión

---

## 4. FORMATO DE ARCHIVOS

### 4.1 Archivo de Estructura

**Propósito**: Define la topología de la red (DAG)

**Formato**:
```
# Comentarios con #
nodo_padre nodo_hijo
```

**Ejemplo**:
```
# Red de clima
Lluvia Cesped_Mojado
Aspersor Cesped_Mojado
```

**Reglas**:
- Una línea por arco
- Nodos se crean automáticamente
- Las líneas vacías se ignoran
- Comentarios comienzan con #

### 4.2 Archivo de Probabilidades

**Propósito**: Define las CPTs (Tablas de Probabilidad Condicional)

**Formato**:
```
NODO: nombre_nodo
valor_padre1 valor_padre2 ... | valor_nodo | probabilidad
```

**Ejemplo para nodo raíz**:
```
NODO: Lluvia
| True | 0.2
| False | 0.8
```

**Ejemplo para nodo con padres**:
```
NODO: Cesped_Mojado
True True | True | 0.99
True False | True | 0.90
False True | True | 0.90
False False | True | 0.01
```

**Reglas**:
- Separador de campos: `|`
- Valores: True/False, números o strings
- Las probabilidades deben sumar 1 para cada configuración de padres

---

## 5. GUÍA DE USO

### 5.1 Instalación

```bash
# Clonar o descargar el proyecto
cd proyecto_red_bayesiana

# No requiere instalación de bibliotecas externas
# Solo Python 3.7+
```

### 5.2 Ejecución

```bash
# Programa principal
python main.py

# Suite de pruebas
python test_suite.py
```

### 5.3 Flujo de Trabajo

1. **Preparar archivos**:
   - Crear `estructura.txt` con la topología
   - Crear `probabilidades.txt` con las CPTs

2. **Cargar red**:
   ```
   Opción 1: Cargar Red Bayesiana
   ```

3. **Explorar red**:
   ```
   Opción 2: Mostrar estructura
   Opción 3: Mostrar probabilidades
   Opción 4: Validar red
   ```

4. **Realizar inferencias**:
   ```
   Opción 5: Inferencia personalizada
   Opción 6: Pruebas predefinidas
   ```

### 5.4 Ejemplo de Sesión

```
> Seleccione una opción: 1
Archivo de estructura: estructura.txt
Archivo de probabilidades: probabilidades.txt
✓ Red cargada exitosamente

> Seleccione una opción: 5
Variable de consulta: Lluvia
Valor de consulta: True
Variable de evidencia: Cesped_Mojado
Valor observado: True
Variable de evidencia: [Enter]
¿Mostrar traza detallada? (s/n): s

[Traza de ejecución...]

RESULTADO FINAL
P(Lluvia=True | Cesped_Mojado=True) = 0.7112 (71.12%)
P(Lluvia=False | Cesped_Mojado=True) = 0.2888 (28.88%)
```

---

## 6. VALIDACIÓN Y PRUEBAS

### 6.1 Pruebas Unitarias

El archivo `test_suite.py` incluye:
- Prueba de creación de nodos
- Prueba de creación de arcos
- Prueba de red simple
- Prueba de inferencia
- Prueba de probabilidad conjunta
- Prueba de detección de ciclos

### 6.2 Validación de Red

El sistema valida automáticamente:
- **Acíclicidad**: No debe haber ciclos en el DAG
- **Completitud**: Todos los nodos deben tener CPTs
- **Consistencia**: Las probabilidades deben sumar 1

### 6.3 Casos de Prueba

**Caso 1: Red Simple**
```
A → B → C
P(A) = 0.3
P(B|A) conocida
P(C|B) conocida
Consulta: P(C | A)
```

**Caso 2: Red con Convergencia**
```
  A   B
   \ /
    C
Consulta: P(A | C, B)
```

**Caso 3: Red Compleja**
```
Red médica de 5 nodos
Múltiples consultas
```

---

## 7. LIMITACIONES Y EXTENSIONES

### 7.1 Limitaciones Actuales

1. **Escalabilidad**: Complejidad exponencial con variables ocultas
2. **Dominios**: Solo valores discretos
3. **Interfaz**: Solo consola de texto
4. **Persistencia**: No guarda resultados

### 7.2 Extensiones Futuras

1. **Algoritmos**:
   - Eliminación de variables
   - Propagación de creencias
   - Muestreo de Monte Carlo
   - Algoritmo junction tree

2. **Funcionalidades**:
   - Aprendizaje de estructura
   - Aprendizaje de parámetros
   - Inferencia aproximada
   - Explicaciones causales

3. **Interfaz**:
   - GUI gráfica
   - Visualización de red
   - Editor interactivo
   - Exportación de resultados

4. **Optimizaciones**:
   - Caché de resultados
   - Ordenamiento óptimo de variables
   - Paralelización
   - Detección de independencias

---

## 8. REFERENCIAS

### 8.1 Fundamentos Teóricos
- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
- Pearl, J. (1988). *Probabilistic Reasoning in Intelligent Systems*
- Koller, D. & Friedman, N. (2009). *Probabilistic Graphical Models*

### 8.2 Recursos Adicionales
- Stanford CS228: Probabilistic Graphical Models
- MIT 6.438: Algorithms for Inference
- Coursera: Probabilistic Graphical Models Specialization

---

## 9. CONCLUSIONES

### 9.1 Logros del Proyecto

✓ Sistema completo de Red Bayesiana funcional
✓ Motor de inferencia por enumeración exacta
✓ Diseño orientado a objetos robusto
✓ Código bien documentado y modular
✓ Suite de pruebas automatizadas
✓ Interfaz de usuario intuitiva
✓ Ejemplos de uso incluidos

### 9.2 Aprendizajes

1. **Diseño OOP**: Importancia de la separación de responsabilidades
2. **Algoritmos probabilísticos**: Complejidad del razonamiento bajo incertidumbre
3. **Ingeniería de software**: Valor de la modularidad y testing
4. **Documentación**: Esencial para mantenibilidad

### 9.3 Aplicabilidad

El sistema es aplicable a:
- Diagnóstico médico
- Sistemas expertos
- Análisis de riesgos
- Predicción de fallas
- Toma de decisiones bajo incertidumbre

---

## ANEXOS

### A. Glosario

- **Red Bayesiana**: Modelo gráfico probabilístico que representa dependencias
- **CPT**: Conditional Probability Table (Tabla de Probabilidad Condicional)
- **DAG**: Directed Acyclic Graph (Grafo Dirigido Acíclico)
- **Inferencia**: Proceso de calcular probabilidades de consulta
- **Evidencia**: Variables observadas con valores conocidos
- **Variables ocultas**: Variables no observadas sobre las que se marginaliza

### B. Estructura de Archivos del Proyecto

```
proyecto/
│
├── nodo.py                 # Clase Nodo
├── arco.py                 # Clase Arco  
├── red_bayesiana.py        # Clase RedBayesiana
├── motor_inferencia.py     # Motor de Inferencia
├── main.py                 # Programa principal
├── test_suite.py           # Pruebas automatizadas
│
├── estructura.txt          # Ejemplo: estructura de red
├── probabilidades.txt      # Ejemplo: CPTs
│
├── estructura_medica.txt   # Ejemplo adicional
├── probabilidades_medica.txt
│
├── README.md               # Instrucciones de uso
└── DOCUMENTACION.md        # Este documento
```

### C. Contacto y Soporte

Para preguntas, reportar bugs o sugerencias:
- [Nombres de los estudiantes]
- [Información de contacto]
- [Repositorio del proyecto]

---

**Proyecto 3 - Sistemas Basados en Reglas**  
**Motor de Inferencia por Enumeración para Redes Bayesianas**  
**Fecha**: [Fecha de entrega]
