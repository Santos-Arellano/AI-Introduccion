"""
Clase Arco - Representa una relación causal dirigida entre dos nodos
"""

from nodo import Nodo


class Arco:
    """
    Representa la dependencia causal entre un nodo origen (padre)
    y un nodo destino (hijo).
    """

    def __init__(self, nodo_origen: Nodo, nodo_destino: Nodo):
        self.nodo_origen = nodo_origen
        self.nodo_destino = nodo_destino

        # Actualizar relaciones bidireccionales en los nodos
        self.nodo_destino.agregar_padre(self.nodo_origen)
        self.nodo_origen.agregar_hijo(self.nodo_destino)

    def es_valido(self) -> bool:
        """
        Verifica consistencia básica del arco.
        Returns:
            bool: True si el arco es válido.
        """
        # Un arco no puede ir de un nodo hacia sí mismo
        if self.nodo_origen is self.nodo_destino:
            return False
        # Deben ser instancias de Nodo
        return isinstance(self.nodo_origen, Nodo) and isinstance(self.nodo_destino, Nodo)

    def __str__(self):
        return f"Arco({self.nodo_origen.nombre} -> {self.nodo_destino.nombre})"

    def __repr__(self):
        return f"Arco({self.nodo_origen!r} -> {self.nodo_destino!r})"