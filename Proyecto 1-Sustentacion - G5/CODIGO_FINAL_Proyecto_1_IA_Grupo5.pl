% Definimos nuestro estado inicial y final
estado_inicial(estado(i,i,i,i)).
estado_final(estado(d,d,d,d)).

% Declaramos Lados opuestos
opuesto(i,d).
opuesto(d,i).

% Estados inseguros
inseguro(estado(G,L,C,_)) :- L = C, G \= L.   % lobo se come cabra
inseguro(estado(G,_,C,H)) :- C = H, G \= C.  % Cabra se come al heno
seguro(S) :- \+ inseguro(S).

% Movimientos que podemos hacer:
% Granjero cruza solo (m1)
mover(estado(G,L,C,H), estado(G2,L,C,H), m1_solo) :-
    opuesto(G,G2),
    seguro(estado(G2,L,C,H)).

% Granjero cruza con el lobo (m2)
mover(estado(G,L,C,H), estado(G2,G2,C,H), m2_lobo) :-
    G = L, opuesto(G,G2),
    seguro(estado(G2,G2,C,H)).

% Granjero cruza con la cabra (m3)
mover(estado(G,L,C,H), estado(G2,L,G2,H), m3_cabra) :-
    G = C, opuesto(G,G2),
    seguro(estado(G2,L,G2,H)).

% Granjero cruza con el heno (m4)
mover(estado(G,L,C,H), estado(G2,L,C,G2), m4_heno) :-
    G = H, opuesto(G,G2),
    seguro(estado(G2,L,C,G2)).

% Costo del estado == cuántos objetos siguen en la orilla izquierda
costo_estado(estado(_,L,C,H), Costo) :- contar_i([L,C,H], Costo).
contar_i([],0).
contar_i([i|T],N) :- !, contar_i(T,N1), N is N1+1.
contar_i([_|T],N) :- contar_i(T,N).

% Cola para el BFS 
cola_vacia([]).
encolar(E,Q,Q2) :- append(Q,[E],Q2).
encolar_lista(Q,[],Q).
encolar_lista(Q,[H|T],Qf) :- encolar(H,Q,Q1), encolar_lista(Q1,T,Qf).

en_cola(E,[nodo(E,_,_,_)|_]).
en_cola(E,[_|R]) :- en_cola(E,R).

% -Hacemos BFS con costo
resolver_bfs_costo(CaminoEstados,CaminoMovs,Expandidos) :-
    estado_inicial(E0),
    cola_vacia(Q0),
    encolar(nodo(E0,[E0],[],0),Q0,Q1),
    bfs_costo(Q1,[],NodoSol,ExpandidosRev),
    NodoSol = nodo(_,CERev,CMRev,_),
    reverse(CERev,CaminoEstados),
    reverse(CMRev,CaminoMovs),
    reverse(ExpandidosRev,Expandidos).

% Caso meta que queremos
bfs_costo([nodo(E,CE,CM,D)|_],_,nodo(E,CE,CM,D),[E]) :-
    estado_final(E), !.

% Paso recursivo
bfs_costo([Nodo|Resto],Cerrados,NodoSol,[E|ExpTail]) :-
    Nodo = nodo(E,_,_,_),
    \+ member(E,Cerrados),
    expandir_hijos(Nodo,Resto,Cerrados,Hijos),
    encolar_lista(Resto,Hijos,NuevaCola),
    bfs_costo(NuevaCola,[E|Cerrados],NodoSol,ExpTail),
    E = E.

% Si ya estaba cerrado
bfs_costo([nodo(E,_,_,_)|Resto],Cerrados,NodoSol,Exp) :-
    member(E,Cerrados), !,
    bfs_costo(Resto,Cerrados,NodoSol,Exp).

% Expandimos y ordenamos hijos por costo
expandir_hijos(nodo(E,CE,CM,D),Cola,Cerrados,Hijos) :-
    findall(K-Hijo,
        ( mover(E,E2,Acc),
          \+ member(E2,Cerrados),
          \+ en_cola(E2,Cola),
          costo_estado(E2,K),
          Hijo=nodo(E2,[E2|CE],[Acc|CM],D+1)
        ),
        Pares),
    keysort(Pares,Ordenados),
    pares_valores(Ordenados,Hijos).

pares_valores([],[]).
pares_valores([_-V|T],[V|R]) :- pares_valores(T,R).

% Sustentación de la implementación de DFS

% Resolver el camino con dfs
resolver_dfs(CaminoEstados, CaminoMovs) :-
    estado_inicial(E0),
    dfs(E0, [E0], [], CamEstRev, CamMovRev),
    reverse(CamEstRev, CaminoEstados),
    reverse(CamMovRev, CaminoMovs).

% si Estado ya es final, devolvemos el camino que armamos (en reversa)
dfs(E, Visitados, MovsRev, Visitados, MovsRev) :-
    estado_final(E), !.

% Paso recursivo: tomamos un sucesor E2 mediante un movimiento "Accion"
dfs(E, Visitados, MovsRev, CamEstRev, CamMovRev) :-
    mover(E, E2, Accion),
    \+ member(E2, Visitados), % Hacemos esto para evitar ciclos.
    dfs(E2, [E2|Visitados], [Accion|MovsRev], CamEstRev, CamMovRev).

imprimir_solucion(Estados,Movs) :-
    writeln('Estados'),
    forall(member(E,Estados),(write('  '),writeln(E))),
    writeln('Movimientos'),
    forall(member(M,Movs),(write('  '),writeln(M))).

% Prueba 1
prueba :- resolver_bfs_costo(Estados,Movs,_), imprimir_solucion(Estados,Movs).

% Prueba para DFS
prueba_dfs :-resolver_dfs(Estados, Movs), imprimir_solucion(Estados, Movs).



