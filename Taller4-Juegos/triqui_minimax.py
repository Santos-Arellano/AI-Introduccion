"""
Implementación del algoritmo MINIMAX para el juego de Triqui (Tic-Tac-Toe)
Taller 4 - Inteligencia Artificial - Juegos Multijugador
Pontificia Universidad Javeriana - Bogotá

Autores: [Nombre 1, Nombre 2, Nombre 3]
Grupo: [X]
"""

import math
import random
from typing import List, Tuple, Optional

class TriquiGame:
    """
    Clase principal para el juego de Triqui con implementación del algoritmo Minimax
    """
    
    def __init__(self):
        """Inicializa el estado del juego"""
        # Representación del estado: matriz 3x3
        # 0 = vacío, 1 = X (MAX/Humano), -1 = O (MIN/IA)
        self.board = [[0, 0, 0] for _ in range(3)]
        self.current_player = 1  # X empieza primero
        
    def print_board(self):
        """Imprime el tablero actual de forma visual"""
        print("\n  0   1   2")
        for i in range(3):
            print(f"{i} ", end="")
            for j in range(3):
                if self.board[i][j] == 1:
                    symbol = "X"
                elif self.board[i][j] == -1:
                    symbol = "O"
                else:
                    symbol = " "
                print(f"{symbol}", end="")
                if j < 2:
                    print(" | ", end="")
            print()
            if i < 2:
                print("  ---------")
    
    def get_valid_moves(self, state: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Genera los sucesores de un estado (movimientos válidos)
        
        Args:
            state: Estado actual del tablero
            
        Returns:
            Lista de tuplas (fila, columna) con los movimientos válidos
        """
        moves = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    moves.append((i, j))
        return moves
    
    def make_move(self, row: int, col: int, player: int, state: List[List[int]]) -> List[List[int]]:
        """
        Efectúa una jugada en una copia del estado
        
        Args:
            row: Fila donde colocar la ficha
            col: Columna donde colocar la ficha
            player: Jugador que realiza el movimiento (1 o -1)
            state: Estado actual del tablero
            
        Returns:
            Nuevo estado con el movimiento aplicado
        """
        new_state = [row[:] for row in state]  # Copia profunda del estado
        new_state[row][col] = player
        return new_state
    
    def check_winner(self, state: List[List[int]]) -> int:
        """
        Verifica si hay un ganador en el estado actual
        
        Args:
            state: Estado del tablero
            
        Returns:
            1 si gana X, -1 si gana O, 0 si no hay ganador
        """
        # Verificar filas
        for row in state:
            if row[0] == row[1] == row[2] != 0:
                return row[0]
        
        # Verificar columnas
        for col in range(3):
            if state[0][col] == state[1][col] == state[2][col] != 0:
                return state[0][col]
        
        # Verificar diagonales
        if state[0][0] == state[1][1] == state[2][2] != 0:
            return state[0][0]
        if state[0][2] == state[1][1] == state[2][0] != 0:
            return state[0][2]
        
        return 0
    
    def is_terminal_state(self, state: List[List[int]]) -> bool:
        """
        Verifica si el estado es terminal (hay ganador o empate)
        
        Args:
            state: Estado del tablero
            
        Returns:
            True si el juego terminó, False en caso contrario
        """
        # Hay ganador
        if self.check_winner(state) != 0:
            return True
        
        # Tablero lleno (empate)
        for row in state:
            if 0 in row:
                return False
        return True
    
    def evaluate_state(self, state: List[List[int]]) -> int:
        """
        Función heurística para valorar un estado
        
        Esta función evalúa el estado desde la perspectiva del jugador MAX (X)
        
        Args:
            state: Estado del tablero
            
        Returns:
            Valor heurístico del estado
        """
        winner = self.check_winner(state)
        
        # Si hay un ganador definitivo
        if winner == 1:  # Gana X (MAX)
            return 1000
        elif winner == -1:  # Gana O (MIN)
            return -1000
        
        # Si es empate
        if self.is_terminal_state(state):
            return 0
        
        # Evaluación heurística para estados no terminales
        score = 0
        
        # Indicadores para la función heurística
        # Ind1: Líneas potenciales de victoria para MAX
        # Ind2: Líneas potenciales de victoria para MIN
        # Ind3: Control del centro
        
        lines = []
        # Agregar todas las líneas (filas, columnas, diagonales)
        for i in range(3):
            lines.append([state[i][0], state[i][1], state[i][2]])  # Filas
            lines.append([state[0][i], state[1][i], state[2][i]])  # Columnas
        lines.append([state[0][0], state[1][1], state[2][2]])  # Diagonal principal
        lines.append([state[0][2], state[1][1], state[2][0]])  # Diagonal secundaria
        
        for line in lines:
            x_count = line.count(1)
            o_count = line.count(-1)
            
            # Líneas con potencial para X
            if o_count == 0:
                if x_count == 2:
                    score += 50  # Casi gana X
                elif x_count == 1:
                    score += 10  # Línea con potencial para X
            
            # Líneas con potencial para O
            if x_count == 0:
                if o_count == 2:
                    score -= 50  # Casi gana O (hay que bloquear)
                elif o_count == 1:
                    score -= 10  # Línea con potencial para O
        
        # Bonificación por control del centro
        if state[1][1] == 1:
            score += 30
        elif state[1][1] == -1:
            score -= 30
        
        # Bonificación por esquinas
        corners = [(0,0), (0,2), (2,0), (2,2)]
        for r, c in corners:
            if state[r][c] == 1:
                score += 15
            elif state[r][c] == -1:
                score -= 15
        
        return score
    
    def minimax(self, state: List[List[int]], depth: int, is_maximizing: bool, 
                alpha: float = -math.inf, beta: float = math.inf) -> Tuple[int, Optional[Tuple[int, int]]]:
        """
        Implementación del algoritmo Minimax con poda Alfa-Beta (BONUS)
        
        Args:
            state: Estado actual del tablero
            depth: Profundidad máxima de búsqueda
            is_maximizing: True si es el turno de MAX, False si es MIN
            alpha: Valor alfa para la poda
            beta: Valor beta para la poda
            
        Returns:
            Tupla (valor, mejor_movimiento)
        """
        # Caso base: estado terminal o profundidad máxima alcanzada
        if self.is_terminal_state(state) or depth == 0:
            return self.evaluate_state(state), None
        
        valid_moves = self.get_valid_moves(state)
        best_move = None
        
        if is_maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                new_state = self.make_move(move[0], move[1], 1, state)
                eval_score, _ = self.minimax(new_state, depth - 1, False, alpha, beta)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                # Poda Alfa-Beta
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Poda Beta
            
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in valid_moves:
                new_state = self.make_move(move[0], move[1], -1, state)
                eval_score, _ = self.minimax(new_state, depth - 1, True, alpha, beta)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                # Poda Alfa-Beta
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Poda Alfa
            
            return min_eval, best_move
    
    def get_ai_move(self) -> Tuple[int, int]:
        """
        Obtiene el mejor movimiento para la IA usando Minimax
        
        Returns:
            Tupla (fila, columna) con el mejor movimiento
        """
        # Usar profundidad 9 para explorar todo el árbol en Triqui
        _, best_move = self.minimax(self.board, 9, False)
        return best_move
    
    def play_human_move(self) -> bool:
        """
        Permite al jugador humano realizar su movimiento
        
        Returns:
            True si el movimiento fue válido, False en caso contrario
        """
        try:
            print("\nTu turno (X)")
            row = int(input("Ingresa la fila (0-2): "))
            col = int(input("Ingresa la columna (0-2): "))
            
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Coordenadas fuera del tablero!")
                return False
            
            if self.board[row][col] != 0:
                print("Esa casilla ya está ocupada!")
                return False
            
            self.board[row][col] = 1
            return True
        except ValueError:
            print("Entrada inválida! Ingresa números entre 0 y 2.")
            return False
    
    def play_game(self):
        """
        Loop principal del juego
        """
        print("=" * 50)
        print("BIENVENIDO AL JUEGO DE TRIQUI CON MINIMAX")
        print("=" * 50)
        print("\nTú juegas con X, la IA juega con O")
        print("Ingresa las coordenadas (fila, columna) para tu movimiento")
        print("Las coordenadas van de 0 a 2")
        
        # Preguntar quién empieza
        while True:
            starter = input("\n¿Quién empieza? (1: Humano, 2: IA): ")
            if starter in ['1', '2']:
                break
            print("Opción inválida. Ingresa 1 o 2.")
        
        if starter == '2':
            # La IA empieza con un movimiento aleatorio en el centro o esquina
            first_moves = [(1,1), (0,0), (0,2), (2,0), (2,2)]
            move = random.choice(first_moves)
            self.board[move[0]][move[1]] = -1
            print(f"\nLa IA juega en ({move[0]}, {move[1]})")
        
        # Loop del juego
        while not self.is_terminal_state(self.board):
            self.print_board()
            
            # Turno del humano
            while not self.play_human_move():
                pass
            
            # Verificar si el humano ganó
            if self.is_terminal_state(self.board):
                break
            
            # Turno de la IA
            print("\nTurno de la IA (O)...")
            ai_move = self.get_ai_move()
            if ai_move:
                self.board[ai_move[0]][ai_move[1]] = -1
                print(f"La IA juega en ({ai_move[0]}, {ai_move[1]})")
        
        # Mostrar resultado final
        self.print_board()
        print("\n" + "=" * 50)
        
        winner = self.check_winner(self.board)
        if winner == 1:
            print("¡FELICIDADES! ¡Has ganado! 🎉")
        elif winner == -1:
            print("La IA ha ganado. ¡Intenta de nuevo! 🤖")
        else:
            print("¡Es un empate! 🤝")
        print("=" * 50)


def main():
    """Función principal para ejecutar el juego"""
    game = TriquiGame()
    game.play_game()
    
    # Preguntar si quiere jugar de nuevo
    while True:
        play_again = input("\n¿Quieres jugar de nuevo? (s/n): ").lower()
        if play_again == 's':
            game = TriquiGame()
            game.play_game()
        elif play_again == 'n':
            print("¡Gracias por jugar! Hasta pronto.")
            break
        else:
            print("Opción inválida. Ingresa 's' o 'n'.")


if __name__ == "__main__":
    main()