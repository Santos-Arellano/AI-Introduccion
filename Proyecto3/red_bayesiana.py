"""
Clase RedBayesiana - Gestiona la estructura completa de la red
"""

from typing import Dict, List, Tuple

from nodo import Nodo
from arco import Arco


class RedBayesiana:
    """
    Gestiona nodos y arcos de una Red Bayesiana, carga desde archivos,
    validación básica y visualización de estructura.
    """

    def __init__(self):
        self.nodos: Dict[str, Nodo] = {}
        self.arcos: List[Arco] = []

    # --- Gestión de nodos y arcos ---
    def agregar_nodo(self, nodo: Nodo):
        if nodo.nombre not in self.nodos:
            self.nodos[nodo.nombre] = nodo

    def obtener_o_crear_nodo(self, nombre: str) -> Nodo:
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)
        return self.nodos[nombre]

    def agregar_arco(self, nombre_origen: str, nombre_destino: str):
        origen = self.obtener_o_crear_nodo(nombre_origen)
        destino = self.obtener_o_crear_nodo(nombre_destino)
        arco = Arco(origen, destino)
        self.arcos.append(arco)
        return arco

    def obtener_raices(self) -> List[Nodo]:
        return [nodo for nodo in self.nodos.values() if nodo.es_raiz()]

    # --- Visualización ---
    def mostrar_estructura(self):
        print("\n" + "=" * 70)
        print("ESTRUCTURA DE LA RED BAYESIANA")
        print("=" * 70)
        if not self.nodos:
            print("(Red vacía)")
            return
        raices = self.obtener_raices()
        print(f"Nodos raíz: {[n.nombre for n in raices]}")
        for nombre, nodo in sorted(self.nodos.items()):
            padres = nodo.obtener_nombres_padres()
            hijos = nodo.obtener_nombres_hijos()
            print(f"- {nombre}: Padres={padres if padres else ['(ninguno)']} Hijos={hijos if hijos else ['(ninguno)']}")

    # --- Validación ---
    def _tiene_ciclos(self) -> bool:
        visitado = set()
        en_pila = set()

        def dfs(nodo: Nodo) -> bool:
            if nodo.nombre in en_pila:
                return True
            if nodo.nombre in visitado:
                return False
            visitado.add(nodo.nombre)
            en_pila.add(nodo.nombre)
            for hijo in nodo.hijos:
                if dfs(hijo):
                    return True
            en_pila.remove(nodo.nombre)
            return False

        for nodo in self.nodos.values():
            if dfs(nodo):
                return True
        return False

    def validar_red(self) -> bool:
        """
        Valida integridad básica: acíclicidad y presencia de CPTs.
        Returns:
            bool: True si pasa validaciones básicas.
        """
        if self._tiene_ciclos():
            print("✗ La red contiene ciclos")
            return False

        incompletos = [n.nombre for n in self.nodos.values() if not n.tabla_probabilidad]
        if incompletos:
            print(f"⚠ Nodos sin CPT definida: {incompletos}")
        else:
            print("✓ Todas las CPTs están definidas (básico)")
        return True

    # --- Carga desde archivos ---
    def cargar_estructura_desde_archivo(self, ruta: str):
        with open(ruta, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue
                partes = linea.split()
                if len(partes) != 2:
                    continue
                padre, hijo = partes
                self.agregar_arco(padre, hijo)

    def cargar_probabilidades_desde_archivo(self, ruta: str):
        """
        Formato:
            NODO: Nombre
            (para raíz) | valor_nodo | prob
            (con padres) val_padre1 val_padre2 ... | valor_nodo | prob
        """
        nodo_actual: Nodo = None
        with open(ruta, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue
                if linea.upper().startswith('NODO:'):
                    nombre = linea.split(':', 1)[1].strip()
                    nodo_actual = self.obtener_o_crear_nodo(nombre)
                    continue
                if nodo_actual is None:
                    continue

                # Esperamos algo como: "True False | True | 0.99" o "| True | 0.2"
                partes = [p.strip() for p in linea.split('|')]
                if len(partes) != 3:
                    continue
                padres_str, valor_nodo_str, prob_str = partes

                # Parse de valores de padres
                if padres_str == '' or padres_str == '':
                    valores_padres: Tuple = ()
                else:
                    tokens = [t for t in padres_str.split(' ') if t]
                    valores_padres = tuple(_parse_valor(t) for t in tokens)

                valor_nodo = _parse_valor(valor_nodo_str)
                prob = float(prob_str)

                nodo_actual.establecer_probabilidad((valores_padres, valor_nodo), prob)


def _parse_valor(token: str):
    """
    Convierte un token a tipo apropiado: True/False, número o string.
    """
    if token.lower() == 'true':
        return True
    if token.lower() == 'false':
        return False
    try:
        if '.' in token:
            return float(token)
        return int(token)
    except ValueError:
        return token