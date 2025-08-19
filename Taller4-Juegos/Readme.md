# Taller 4 - Implementación del Algoritmo MINIMAX para Triqui
**Inteligencia Artificial - Juegos Multijugador**  
**Pontificia Universidad Javeriana - Bogotá**  
**Departamento de Ingeniería de Sistemas**

---

## 📚 Información del Proyecto

- **Curso**: Inteligencia Artificial
- **Profesor**: Ing. Laura Juliana Mora Páez Msc
- **Tema**: Juegos Multijugador - Algoritmo MINIMAX
- **Grupo**: [5]
- **Integrantes**: 
- Alejandra Abaunza Suárez 
- Daniel Santiago Avila Medina
- Santos Alejandro Arellano Olarte
- Jeison Camilo Alfonso Moreno


---

## 🎯 Objetivo del Taller

Implementar el algoritmo MINIMAX para el juego de Triqui (Tic-Tac-Toe) en un tablero 3x3, donde dos jugadores se alternan para colocar símbolos 'X' y 'O', ganando quien logre poner tres en línea.

---

## 📋 Requisitos Implementados

### 1. **Representación del Estado** ✅

El estado del juego se representa mediante una **matriz 3x3** donde:

```python
# Estado inicial (tablero vacío)
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# Valores posibles:
# 0 = Casilla vacía
# 1 = X (Jugador MAX - Humano)
# -1 = O (Jugador MIN - IA)
```

**Justificación de la representación:**
- Uso de valores numéricos (1, -1, 0) facilita el cálculo de la función heurística
- La representación matricial permite acceso directo O(1) a cualquier posición
- Los valores 1 y -1 simplifican la alternancia de turnos y evaluación de estados

### 2. **Función Heurística** ✅

La función `evaluate_state()` implementa una evaluación sofisticada basada en múltiples indicadores:

#### **Indicadores utilizados:**

1. **Ind1 - Estados Terminales**:
   - Victoria de X (MAX): **+1000 puntos**
   - Victoria de O (MIN): **-1000 puntos**
   - Empate: **0 puntos**

2. **Ind2 - Líneas Potenciales**:
   - Línea con 2X y sin O: **+50 puntos** (casi victoria para MAX)
   - Línea con 1X y sin O: **+10 puntos** (potencial para MAX)
   - Línea con 2O y sin X: **-50 puntos** (peligro, debe bloquearse)
   - Línea con 1O y sin X: **-10 puntos** (potencial para MIN)

3. **Ind3 - Control Posicional**:
   - Control del centro (1,1): **±30 puntos**
   - Control de esquinas: **±15 puntos** cada una

#### **Fórmula de la Función Heurística:**

```
H(estado) = w1×(Victoria) + w2×(Líneas_Potenciales) + w3×(Control_Posicional)

Donde:
- w1 = 1000 (peso máximo para estados terminales)
- w2 = Variable según el tipo de línea (50, 10)
- w3 = Variable según la posición (30 centro, 15 esquinas)
```

### 3. **Generación de Sucesores** ✅

La función `get_valid_moves()` genera todos los movimientos válidos (sucesores) de un estado:

```python
def get_valid_moves(state):
    # Retorna lista de tuplas (fila, columna) 
    # donde hay casillas vacías (valor = 0)
    moves = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                moves.append((i, j))
    return moves
```

**Características:**
- Exploración completa del espacio de estados
- Generación dinámica según el estado actual
- Complejidad O(9) en el peor caso

### 4. **Efectuar Jugadas y Dar Turno** ✅

El sistema implementa:

- **Alternancia automática de turnos** entre humano y IA
- **Validación de movimientos** (casilla vacía, dentro del tablero)
- **Interfaz interactiva** para entrada del usuario
- **Retroalimentación visual** del estado del tablero

### 5. **BONUS: Poda Alfa-Beta** ⭐ ✅

Implementación completa de la optimización Alfa-Beta:

```python
def minimax(state, depth, is_maximizing, alpha=-∞, beta=+∞):
    # Poda cuando beta <= alpha
    # Reduce el espacio de búsqueda significativamente
```

**Mejoras de la Poda Alfa-Beta:**
- Reduce el número de nodos evaluados de O(b^d) a O(b^(d/2)) en el mejor caso
- Mantiene la optimalidad del resultado
- Mejora significativa en tiempo de respuesta

---

## 🎮 Funcionamiento del Algoritmo MINIMAX

### Árbol de Juego

```
                    Estado_Inicial
                    (Tablero vacío)
                         |
            ┌────────────┼────────────┐
            |            |            |
         MAX(X)       MAX(X)       MAX(X)    ... (9 opciones)
            |            |            |
       ┌────┼────┐  ┌────┼────┐  ┌────┼────┐
       |    |    |  |    |    |  |    |    |
    MIN(O) MIN  MIN MIN  MIN MIN MIN  MIN MIN  ... (8 opciones c/u)
       |                                    
    (recursión hasta estado terminal)
```

### Proceso de Decisión

1. **MAX (Jugador X)** busca maximizar la evaluación
2. **MIN (Jugador O)** busca minimizar la evaluación
3. Se evalúan recursivamente todos los estados posibles
4. Se propaga el mejor valor hacia arriba en el árbol
5. La raíz selecciona el movimiento con mejor evaluación

---

## 💻 Instrucciones de Uso

### Requisitos del Sistema
- Python 3.6 o superior
- No requiere librerías externas

### Instalación y Ejecución

1. **Guardar el código** en un archivo `triqui_minimax.py`

2. **Ejecutar desde la terminal:**
```bash
python triqui_minimax.py
```

3. **Interacción con el juego:**
   - Elegir quién empieza (1: Humano, 2: IA)
   - Ingresar coordenadas para tu movimiento (fila y columna de 0 a 2)
   - La IA calculará automáticamente su mejor jugada

### Ejemplo de Partida

```
BIENVENIDO AL JUEGO DE TRIQUI CON MINIMAX
==========================================

¿Quién empieza? (1: Humano, 2: IA): 1

  0   1   2
0   |   |  
  ---------
1   |   |  
  ---------
2   |   |  

Tu turno (X)
Ingresa la fila (0-2): 1
Ingresa la columna (0-2): 1

  0   1   2
0   |   |  
  ---------
1   | X |  
  ---------
2   |   |  

Turno de la IA (O)...
La IA juega en (0, 0)

  0   1   2
0 O |   |  
  ---------
1   | X |  
  ---------
2   |   |  
```

---

## 🔍 Análisis de Complejidad

### Complejidad Temporal

- **Sin poda**: O(b^d) donde b = factor de ramificación, d = profundidad
  - Peor caso Triqui: O(9!) = O(362,880) nodos
  
- **Con poda Alfa-Beta**: O(b^(d/2)) en el mejor caso
  - Mejor caso Triqui: O(√(9!)) ≈ O(602) nodos

### Complejidad Espacial

- O(d) para la pila de recursión
- En Triqui: O(9) máximo

---

## 📊 Validación y Pruebas

### Casos de Prueba Implementados

1. **Victoria del Jugador X (Horizontal)**
```
X | X | X
---------
O | O |  
---------
  |   |  
```

2. **Victoria del Jugador O (Vertical)**
```
X | O | X
---------
  | O | X
---------
  | O |  
```

3. **Victoria Diagonal**
```
X | O | O
---------
  | X |  
---------
O |   | X
```

4. **Empate**
```
X | O | X
---------
X | X | O
---------
O | X | O
```

### Garantías del Algoritmo

- ✅ La IA **nunca pierde** contra un jugador humano
- ✅ Encuentra la **jugada óptima** en cada turno
- ✅ **Bloquea** amenazas del oponente
- ✅ **Aprovecha** oportunidades de victoria

---

## 📈 Posibles Mejoras Futuras

1. **Interfaz Gráfica**: Implementar GUI con tkinter o pygame
2. **Diferentes Niveles de Dificultad**: Limitar profundidad de búsqueda
3. **Aprendizaje por Refuerzo**: Implementar Q-Learning
4. **Tableros Más Grandes**: Extender a 4x4 o 5x5
5. **Base de Datos de Aperturas**: Memorizar jugadas iniciales óptimas

---

## 📝 Conclusiones

Esta implementación del algoritmo MINIMAX para Triqui demuestra:

1. **Correcta representación del espacio de estados** mediante estructura de datos eficiente
2. **Función heurística robusta** que evalúa correctamente las posiciones
3. **Generación completa de sucesores** para exploración exhaustiva
4. **Sistema de turnos funcional** con validación de entradas
5. **Optimización mediante poda Alfa-Beta** reduciendo el espacio de búsqueda

El algoritmo garantiza juego óptimo por parte de la IA, siendo imposible ganarle si juega correctamente, demostrando así la efectividad del enfoque MINIMAX en juegos de suma cero con información perfecta.

---

## 📚 Referencias

- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
- Algoritmo Minimax - Stanford CS221
- Alpha-Beta Pruning - MIT OpenCourseWare

---

**Fecha de Entrega**: [Próxima clase]  
**Versión**: 1.0