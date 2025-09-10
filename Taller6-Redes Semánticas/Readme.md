# 📚 Taller 6 - Implementación de Redes Semánticas en Prolog

## 📋 Información del Proyecto

**Curso:** Inteligencia Artificial  
**Taller:** 6 - Redes Semánticas  
**Grupo:** 5  
**Integrantes:** 
- Santos Alejandro Arellano Olarte
- Alejandra Abaunza Suárez 
- Daniel Santiago Avila Medina
- Jeison Camilo Alfonso Moreno


## 📝 Descripción

Este proyecto desarrolla un sistema de **Redes Semánticas** en Prolog que modela el mundo del fútbol colombiano. Permite representar jugadores, equipos y sus características usando herencia de propiedades a través de jerarquías de clases, similar a como funciona la programación orientada a objetos.

## 🎯 Objetivos

1. **Crear** un sistema que permita heredar características entre clases relacionadas
2. **Implementar** el ejemplo básico de jugadores de fútbol con sus propiedades
3. **Expandir** el modelo incluyendo equipos del fútbol profesional colombiano
4. **Validar** que el sistema funcione correctamente con consultas prácticas

## 📁 Estructura del Proyecto

```
Taller6-Grup5/
│
├── README.md                       # Este archivo
├── redes_semanticas.pl            # Código principal en Prolog
├── red_semantica_ampliada.html    # Visualización de la red
├── presentacion_taller6.pptx      # Presentación con diagramas
│
├── capturas/
│   ├── primera_entrega/           # Pantallazos del caso base
│   │   ├── demo_basico.png
│   │   ├── consulta_altura.png
│   │   ├── consulta_pie_habil.png
│   │   └── consulta_patear.png
│   │
│   └── entrega_final/             # Pantallazos del caso ampliado
│       ├── demo_completo.png
│       ├── propiedades_equipo.png
│       ├── objetos_clase.png
│       └── companeros_equipo.png
│
└── documentacion/
    ├── diagrama_red_base.png
    └── diagrama_red_ampliada.png
```

## 🚀 Instalación y Requisitos

### Requisitos Previos
- **SWI-Prolog** versión 8.0 o superior
- Editor de texto (recomendado: VSCode con extensión Prolog)

### Instalación de SWI-Prolog

#### Windows
```bash
# Descargar desde https://www.swi-prolog.org/download/stable
# Ejecutar el instalador .exe
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install swi-prolog
```

#### macOS
```bash
brew install swi-prolog
```

## 💻 Uso del Sistema

### 1. Cargar el programa

```bash
# Iniciar SWI-Prolog
swipl

# Cargar el archivo
?- [redes_semanticas].
```

### 2. Ver el sistema en acción

```prolog
?- demo.
```

Esto mostrará todas las capacidades del sistema con ejemplos prácticos.

### 3. Consultas Básicas

#### Consultar características de los jugadores
```prolog
% ¿Cuál es la altura de Adith?
?- obtener_propiedad(adith, altura, X).
X = 1.85.

% ¿Con qué pie juega Miguel?
?- obtener_propiedad(miguel, pie_habil, X).
X = derecho.
```

#### Verificar habilidades
```prolog
% ¿Miguel puede patear el balón?
?- puede(miguel, patea, balon).
true.

% ¿Adith también puede hacerlo?
?- puede(adith, patea, balon).
true.
```

#### Información de equipos
```prolog
% Ver todo sobre Millonarios
?- listar_propiedades(millonarios).

% ¿Qué equipos están en primera división?
?- objetos_de_clase(equipo_primera_division, X).
X = millonarios ;
X = santa_fe ;
X = nacional.
```

#### Relaciones entre jugadores
```prolog
% ¿Dónde juega Miguel?
?- juega_en(miguel, X).
X = millonarios.

% ¿Miguel y Adith son compañeros de equipo?
?- companeros(miguel, adith).
true.
```

### 4. Consultas más avanzadas

```prolog
% ¿Quiénes son todos los jugadores?
?- objetos_de_clase(jugador_futbol, X).

% ¿Los defensas son un tipo de persona?
?- subclase_de(defensa, persona).

% ¿Qué jugadores son compañeros de equipo?
?- companeros(X, Y).
```

## 🏗️ Cómo funciona el sistema

### Estructura principal

#### 1. **Jerarquías de clases**
- **Jugadores:** `persona → hombre_adulto → jugador_futbol → {defensa, delantero}`
- **Equipos:** `organizacion → equipo_futbol → equipo_profesional → equipo_primera_division`

#### 2. **Herencia de características**
Cuando buscas una propiedad, el sistema:
1. Primero mira si el objeto la tiene directamente
2. Si no, busca en su clase padre
3. Sigue subiendo por la jerarquía hasta encontrarla

#### 3. **Tipos de relaciones**
- `es_un/2`: Define jerarquías (ej: defensa es_un jugador_futbol)
- `instancia_de/2`: Conecta objetos con clases (ej: miguel instancia_de delantero)
- `propiedad/3`: Asigna características (ej: miguel tiene equipo millonarios)
- `juega_en/2`: Relaciona jugadores con equipos
- `companeros/2`: Encuentra jugadores del mismo equipo

## 📊 Ejemplo de cómo se organiza la información

```prolog
% Definir jerarquías
es_un(jugador_futbol, hombre_adulto).
es_un(hombre_adulto, persona).

% Crear jugadores específicos
instancia_de(miguel, delantero).
instancia_de(adith, defensa).

% Asignar características
propiedad(persona, pie_habil, derecho).        % Todos heredan esto
propiedad(jugador_futbol, altura, 1.85).       % Solo los jugadores
propiedad(miguel, equipo, millonarios).        % Solo Miguel
```

## 🧪 Ejemplos de funcionamiento

### Herencia básica
```prolog
% Adith obtiene su altura de la clase jugador_futbol
?- obtener_propiedad(adith, altura, 1.85).
true.
```

### Herencia de varios niveles
```prolog
% Miguel hereda el pie hábil desde la clase persona (3 niveles arriba)
?- obtener_propiedad(miguel, pie_habil, derecho).
true.
```

### Propiedades específicas por posición
```prolog
% Los defensas tienen menos goles que los delanteros
?- obtener_propiedad(defensa, numero_goles, 1).
true.
```

### Relaciones entre jugadores y equipos
```prolog
% Miguel y Adith son compañeros porque ambos juegan en Millonarios
?- companeros(miguel, adith).
true.
```

## 📈 Características implementadas

### 1. **Equipos de fútbol colombiano** ✅
- Jerarquía completa desde organizaciones hasta equipos de primera división
- Incluye los tres grandes: Millonarios, Santa Fe y Nacional
- Cada equipo tiene su ciudad, año de fundación y colores

### 2. **Conexiones entre jugadores y equipos** ✅
- Los jugadores pueden pertenecer a equipos específicos
- Sistema para encontrar compañeros de equipo automáticamente

### 3. **Consultas útiles** ✅
- Ver todas las propiedades de cualquier objeto
- Listar todos los miembros de una clase
- Demostración interactiva del sistema completo

## 🐛 Problemas comunes y soluciones

### "undefined procedure" al hacer consultas
```prolog
% Primero carga el archivo
?- [redes_semanticas].
```

### Las consultas devuelven "false"
```prolog
% Revisa que los nombres estén escritos exactamente igual
% Prolog distingue entre mayúsculas y minúsculas
?- instancia_de(Miguel, delantero).  % ❌ INCORRECTO
?- instancia_de(miguel, delantero).  % ✅ CORRECTO
```

### Ver todas las respuestas posibles
```prolog
% Presiona ; (punto y coma) para ver más resultados
?- objetos_de_clase(equipo_primera_division, X).
X = millonarios ;  % Presiona ; aquí
X = santa_fe ;
X = nacional.
```

## 📚 Referencias

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*
- E. Rich, *Inteligencia Artificial*, 1994
- Jorge Baier, *Redes Semánticas y PLN en Prolog*, PUC de Chile
- Documentación SWI-Prolog: https://www.swi-prolog.org/

## 🤝 Desarrollo del proyecto

Este proyecto fue desarrollado colaborativamente para el Taller 6 de Inteligencia Artificial:

- **Implementación base**: Sistema de herencia y jugadores de fútbol
- **Expansión**: Jerarquía de equipos del fútbol colombiano
- **Documentación**: Guías de uso y ejemplos prácticos
- **Pruebas**: Validación completa del funcionamiento

## 📄 Licencia

Este proyecto es de uso académico para el curso de Inteligencia Artificial.

## ✉️ Contacto

Para preguntas o sugerencias sobre este proyecto:
- **Email:** [arellanosantoso6@gmail.com]



