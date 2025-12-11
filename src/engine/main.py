import chess

from minmax import best_move

if __name__ == '__main__':
    table = chess.Board()
    mov = best_move(table, 3)
    print(mov)
