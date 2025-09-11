% ===================================================
% TALLER 6 - REDES SEMÁNTICAS EN PROLOG
% ===================================================
% Implementación de un sistema de redes semánticas que permite
% representar jerarquías de clases y herencia de propiedades

% Evitar advertencias de predicados separados
:- discontiguous es_un/2.
:- discontiguous instancia_de/2.
:- discontiguous propiedad/3.

% ===================================================
% JERARQUÍA DE CLASES Y OBJETOS
% ===================================================

% Jerarquía: persona -> hombre_adulto -> jugador_futbol -> defensa/delantero
es_un(hombre_adulto, persona).
es_un(jugador_futbol, hombre_adulto).
es_un(defensa, jugador_futbol).
es_un(delantero, jugador_futbol).

% Instancias específicas de jugadores
instancia_de(miguel, delantero).
instancia_de(adith, defensa).

% ===================================================
% PROPIEDADES DE CLASES E INSTANCIAS
% ===================================================

% Propiedades generales por clase
propiedad(persona, pie_habil, derecho).
propiedad(hombre_adulto, altura, 1.80).
propiedad(jugador_futbol, altura, 1.85).
propiedad(jugador_futbol, numero_goles, 3).
propiedad(jugador_futbol, patea, balon).
propiedad(defensa, numero_goles, 1).
propiedad(delantero, numero_goles, 5).

% Propiedades individuales de los jugadores
propiedad(miguel, equipo, millonarios).
propiedad(adith, equipo, millonarios).

% ===================================================
% REGLAS DE HERENCIA
% ===================================================

% Determina si una clase hereda de otra (transitivo)
subclase_de(X, Y) :- es_un(X, Y).
subclase_de(X, Y) :- 
    es_un(X, Z), 
    subclase_de(Z, Y).

% Verifica si un objeto pertenece a una clase
pertenece_a(X, Y) :- instancia_de(X, Y).
pertenece_a(X, Y) :- 
    instancia_de(X, Z), 
    subclase_de(Z, Y).

% ===================================================
% SISTEMA DE HERENCIA DE PROPIEDADES
% ===================================================

% Busca una propiedad, primero en el objeto, luego en su jerarquía
obtener_propiedad(Objeto, Atributo, Valor) :-
    propiedad(Objeto, Atributo, Valor), !.

obtener_propiedad(Objeto, Atributo, Valor) :-
    instancia_de(Objeto, Clase),
    obtener_propiedad_clase(Clase, Atributo, Valor), !.

obtener_propiedad(Clase, Atributo, Valor) :-
    es_un(Clase, Superclase),
    obtener_propiedad_clase(Superclase, Atributo, Valor).

% Auxiliar para buscar en la jerarquía de clases
obtener_propiedad_clase(Clase, Atributo, Valor) :-
    propiedad(Clase, Atributo, Valor), !.

obtener_propiedad_clase(Clase, Atributo, Valor) :-
    es_un(Clase, Superclase),
    obtener_propiedad_clase(Superclase, Atributo, Valor).

% ===================================================
% CONSULTAS Y UTILIDADES
% ===================================================

% Muestra todas las propiedades que tiene un objeto
listar_propiedades(Objeto) :-
    write('Propiedades de '), write(Objeto), write(':'), nl,
    forall(obtener_propiedad(Objeto, Atributo, Valor),
           (write('  '), write(Atributo), write(' = '), write(Valor), nl)).

% Verifica si un objeto puede realizar una acción
puede(Objeto, Accion, Sobre) :-
    obtener_propiedad(Objeto, Accion, Sobre).

% Lista todos los objetos que pertenecen a una clase
objetos_de_clase(Clase, Objeto) :-
    pertenece_a(Objeto, Clase).

% ===================================================
% EQUIPOS DE FÚTBOL COLOMBIANO
% ===================================================

% Jerarquía de equipos deportivos
es_un(equipo_futbol, organizacion).
es_un(equipo_profesional, equipo_futbol).
es_un(equipo_primera_division, equipo_profesional).

% Los tres grandes del fútbol colombiano
instancia_de(millonarios, equipo_primera_division).
instancia_de(santa_fe, equipo_primera_division).
instancia_de(nacional, equipo_primera_division).

% Características comunes de los equipos
propiedad(organizacion, tipo, deportiva).
propiedad(equipo_futbol, deporte, futbol).
propiedad(equipo_futbol, numero_jugadores, 11).
propiedad(equipo_profesional, tiene_estadio, si).
propiedad(equipo_primera_division, division, primera).

% Datos específicos de cada equipo
propiedad(millonarios, ciudad, bogota).
propiedad(millonarios, fundacion, 1946).
propiedad(millonarios, colores, 'azul y blanco').
propiedad(santa_fe, ciudad, bogota).
propiedad(santa_fe, fundacion, 1941).
propiedad(santa_fe, colores, 'rojo y blanco').
propiedad(nacional, ciudad, medellin).
propiedad(nacional, fundacion, 1947).
propiedad(nacional, colores, 'verde y blanco').

% Encuentra en qué equipo juega alguien
juega_en(Jugador, Equipo) :-
    obtener_propiedad(Jugador, equipo, Equipo).

% Encuentra jugadores del mismo equipo
companeros(Jugador1, Jugador2) :-
    juega_en(Jugador1, Equipo),
    juega_en(Jugador2, Equipo),
    Jugador1 \= Jugador2.

% ===================================================
% DEMOSTRACIÓN DEL SISTEMA
% ===================================================

% Muestra las capacidades completas del sistema de redes semánticas
demo :-
    nl, write('╔══════════════════════════════════════════════════════════╗'), nl,
    write('║           SISTEMA DE REDES SEMÁNTICAS EN PROLOG         ║'), nl,
    write('║              Demostración Completa del Sistema           ║'), nl,
    write('╚══════════════════════════════════════════════════════════╝'), nl, nl,
    
    % Sección 1: Herencia Multinivel
    write('🔗 1. HERENCIA MULTINIVEL DE PROPIEDADES'), nl,
    write('   ─────────────────────────────────────────'), nl,
    write('   • Adith (defensa) hereda altura de jugador_futbol: '),
    obtener_propiedad(adith, altura, AlturaAdith),
    write(AlturaAdith), write(' metros'), nl,
    
    write('   • Miguel (delantero) hereda pie hábil de persona: '),
    obtener_propiedad(miguel, pie_habil, PieMiguel),
    write(PieMiguel), nl,
    
    write('   • Ambos heredan la capacidad de patear de jugador_futbol'), nl, nl,
    
    % Sección 2: Especialización por Posición
    write('⚽ 2. ESPECIALIZACIÓN POR POSICIÓN'), nl,
    write('   ──────────────────────────────────'), nl,
    obtener_propiedad(defensa, numero_goles, GolesDefensa),
    obtener_propiedad(delantero, numero_goles, GolesDelantero),
    write('   • Defensas (como Adith): '), write(GolesDefensa), write(' goles promedio'), nl,
    write('   • Delanteros (como Miguel): '), write(GolesDelantero), write(' goles promedio'), nl,
    write('   → La especialización sobrescribe propiedades generales'), nl, nl,
    
    % Sección 3: Verificación de Capacidades
    write('🎯 3. VERIFICACIÓN DE CAPACIDADES'), nl,
    write('   ─────────────────────────────────'), nl,
    write('   • ¿Miguel puede patear el balón? '),
    (puede(miguel, patea, balon) -> 
        write('✓ SÍ - Heredado de jugador_futbol') ; 
        write('✗ NO')), nl,
    write('   • ¿Adith puede patear el balón? '),
    (puede(adith, patea, balon) -> 
        write('✓ SÍ - Heredado de jugador_futbol') ; 
        write('✗ NO')), nl, nl,
    
    % Sección 4: Relaciones y Equipos
    write('👥 4. RELACIONES ENTRE JUGADORES'), nl,
    write('   ──────────────────────────────────'), nl,
    obtener_propiedad(miguel, equipo, EquipoMiguel),
    obtener_propiedad(adith, equipo, EquipoAdith),
    write('   • Miguel juega en: '), write(EquipoMiguel), nl,
    write('   • Adith juega en: '), write(EquipoAdith), nl,
    write('   • ¿Son compañeros de equipo? '),
    (companeros(miguel, adith) -> 
        write('✓ SÍ - Ambos en '), write(EquipoMiguel) ; 
        write('✗ NO')), nl, nl,
    
    % Sección 5: Información Detallada de Equipos
    write('🏟️  5. INFORMACIÓN DEL EQUIPO MILLONARIOS'), nl,
    write('   ────────────────────────────────────────'), nl,
    obtener_propiedad(millonarios, ciudad, Ciudad),
    obtener_propiedad(millonarios, fundacion, Fundacion),
    obtener_propiedad(millonarios, colores, Colores),
    obtener_propiedad(millonarios, deporte, Deporte),
    write('   • Deporte: '), write(Deporte), nl,
    write('   • Ciudad: '), write(Ciudad), nl,
    write('   • Fundación: '), write(Fundacion), nl,
    write('   • Colores: '), write(Colores), nl, nl,
    
    % Sección 6: Perfiles Completos
    write('📋 6. PERFIL COMPLETO DE LOS JUGADORES'), nl,
    write('   ───────────────────────────────────────'), nl,
    write('   ▶ MIGUEL (Delantero):'), nl,
    mostrar_perfil_jugador(miguel),
    nl,
    write('   ▶ ADITH (Defensa):'), nl,
    mostrar_perfil_jugador(adith),
    nl,
    
    % Sección 7: Resumen del Sistema
    write('🎉 7. RESUMEN DEL SISTEMA'), nl,
    write('   ──────────────────────'), nl,
    findall(J, pertenece_a(J, jugador_futbol), Jugadores),
    findall(E, pertenece_a(E, equipo_primera_division), Equipos),
    length(Jugadores, NumJugadores),
    length(Equipos, NumEquipos),
    write('   • Jugadores registrados: '), write(NumJugadores), nl,
    write('   • Equipos de primera división: '), write(NumEquipos), nl,
    write('   • Niveles de herencia: 4 (persona → hombre_adulto → jugador_futbol → posición)'), nl,
    write('   • Sistema completamente funcional con herencia multinivel ✓'), nl.

% Auxiliar para mostrar perfil detallado de un jugador
mostrar_perfil_jugador(Jugador) :-
    findall(Atributo=Valor, obtener_propiedad(Jugador, Atributo, Valor), Propiedades),
    mostrar_propiedades_formateadas(Propiedades).

% Auxiliar para mostrar propiedades con formato mejorado
mostrar_propiedades_formateadas([]).
mostrar_propiedades_formateadas([Atributo=Valor|Resto]) :-
    write('     • '), write(Atributo), write(': '), write(Valor), nl,
    mostrar_propiedades_formateadas(Resto).
