import pygame
import sys

WIDTH = 500
HEIGHT = 500
SIZETILE = 500 // 3

pygame.init()
sc = pygame.display.set_mode(size=(500, 500))
clock = pygame.time.Clock()

class Tile:
    def __init__(self, x, y, value=None):
        self.value = value
        self.x = x
        self.y = y
        self.hovered = False

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def check_hover(self, mouse_pos):
        rect = pygame.Rect(self.x * SIZETILE, self.y * SIZETILE, SIZETILE, SIZETILE)
        self.hovered = rect.collidepoint(mouse_pos)

grid = []
for i in range(3):
    for j in range(3):
        e = Tile(i, j)
        grid.append(e)

TILE = 3
current_player = 'X'

def draw_x(x, y):
    x, y = x * SIZETILE + SIZETILE // 2, y * SIZETILE + SIZETILE // 2
    pygame.draw.line(sc, "black", (x - 20, y - 20), (x + 20, y + 20), 5)
    pygame.draw.line(sc, "black", (x - 20, y + 20), (x + 20, y - 20), 5)

def draw_o(x, y):
    x, y = x * SIZETILE + SIZETILE // 2, y * SIZETILE + SIZETILE // 2
    pygame.draw.circle(sc, "black", (x, y), 20, 5)

def check_winner():
    for i in range(3):
        if grid[i*3].value == grid[i*3+1].value == grid[i*3+2].value and grid[i*3].value is not None:
            return grid[i*3].value
        if grid[i].value == grid[i+3].value == grid[i+6].value and grid[i].value is not None:
            return grid[i].value
    if grid[0].value == grid[4].value == grid[8].value and grid[0].value is not None:
        return grid[0].value
    if grid[2].value == grid[4].value == grid[6].value and grid[2].value is not None:
        return grid[2].value
    return None

def is_moves_left():
    for tile in grid:
        if tile.value is None:
            return True
    return False

def evaluate():
    winner = check_winner()
    if winner == 'X':
        return 10
    elif winner == 'O':
        return -10
    return 0

def minimax(depth, is_max):
    score = evaluate()

    if score == 10 or score == -10:
        return score

    if not is_moves_left():
        return 0

    if is_max:
        best = -1000
        for tile in grid:
            if tile.value is None:
                tile.set_value('X')
                best = max(best, minimax(depth + 1, not is_max))
                tile.set_value(None)
        return best
    else:
        best = 1000
        for tile in grid:
            if tile.value is None:
                tile.set_value('O')
                best = min(best, minimax(depth + 1, not is_max))
                tile.set_value(None)
        return best

def find_best_move():
    best_val = -1000
    best_move = None
    for tile in grid:
        if tile.value is None:
            tile.set_value('X')
            move_val = minimax(0, False)
            tile.set_value(None)
            if move_val > best_val:
                best_move = tile
                best_val = move_val
    return best_move

while True:
    sc.fill(pygame.Color(245, 215, 215))

    pygame.draw.line(sc, "black", (HEIGHT // 3, 0), (HEIGHT // 3, HEIGHT), 5)
    pygame.draw.line(sc, "black", (HEIGHT * 2 / 3, 0), (HEIGHT * 2 / 3, HEIGHT), 5)
    pygame.draw.line(sc, "black", (0, HEIGHT // 3), (HEIGHT, HEIGHT // 3), 5)
    pygame.draw.line(sc, "black", (0, HEIGHT * 2 / 3), (HEIGHT, HEIGHT * 2 / 3), 5)

    mouse_pos = pygame.mouse.get_pos()
    for tile in grid:
        tile.check_hover(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'O':
            for row in range(TILE):
                for col in range(TILE):
                    tile = grid[row * 3 + col]
                    rect = pygame.Rect(row * SIZETILE, col * SIZETILE, SIZETILE, SIZETILE)
                    if rect.collidepoint(mouse_pos) and tile.value is None:
                        tile.set_value(current_player)
                        current_player = 'X'

    if current_player == 'X':
        best_move = find_best_move()
        if best_move:
            best_move.set_value('X')
            current_player = 'O'

    for row in range(TILE):
        for col in range(TILE):
            tile = grid[row * 3 + col]
            rect = pygame.Rect(row * SIZETILE, col * SIZETILE, SIZETILE - 5, SIZETILE - 5)
            color = (200, 200, 200) if tile.hovered else (245, 215, 215)
            pygame.draw.rect(sc, color, rect)
            if tile.value == 'X':
                draw_x(row, col)
            elif tile.value == 'O':
                draw_o(row, col)

    winner = check_winner()
    if winner:
        print(f"{winner} wins!")
        

    pygame.display.update()
    clock.tick(60)
