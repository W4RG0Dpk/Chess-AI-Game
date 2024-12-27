import pygame as p
import ChessEngine
import os
import AI_Algo
import sys
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
player_white = True
player_black = False

folderpath = r"C:\amrita_uni\s3\Fundamentals of AI\Chess Project"

def loadImages():
    pieces = ['bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR', 'bB', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(folderpath + "\\images1\\" + piece + ".PNG"), (SQUARE_SIZE, SQUARE_SIZE)
        )


p.mixer.init()
# Load sound files
move_sound = p.mixer.Sound(folderpath+ "\\sounds\\"+"sounds\\move-sound.mp3")
capture_sound = p.mixer.Sound(folderpath+ "\\sounds\\"+"sounds\\capture.mp3")
promote_sound = p.mixer.Sound(folderpath+ "\\sounds\\"+"sounds\\promote.mp3")



# Initialize pygame
p.init()

# Function to draw text with shadow effect
def draw_text(screen, text, font, color, x, y):
    """Helper function to draw centered text without shadow."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    screen.blit(text_obj, text_rect)

    
# Function to load and draw the pawns
def draw_pawn(screen, color, x, y):
    """Draw a simple pawn on the specified button."""
    # Load pawn images
    white_pawn = p.image.load(folderpath+ "\\images1\\wp.png")  
    black_pawn = p.image.load(folderpath+ "\\images1\\bp.png")  

    if color == "white":
        screen.blit(white_pawn, (x - 0, y - 40))  
    elif color == "black":
        screen.blit(black_pawn, (x - 0, y - 40))  

def menu_screen():
    global AI_Algo, player_black, player_white
    screen = p.display.set_mode((800, 600)) 
    p.display.set_caption("Chess AI - Menu")
    font = p.font.Font(None, 40)
    button_font = p.font.Font(None, 50)

    clock = p.time.Clock()

    # Button coordinates and sizes
    easy_button = p.Rect(50, 150, 200, 80)
    medium_button = p.Rect(300, 150, 200, 80)
    difficult_button = p.Rect(550, 150, 200, 80)
    white_button = p.Rect(150, 300, 200, 80)
    black_button = p.Rect(450, 300, 200, 80)
    start_button = p.Rect(300, 450, 200, 80)

    difficulty_selected = False
    color_selected = False

    while True:
        screen.fill(p.Color(135, 206, 250))  # Sky blue background

        # Draw gradient background
        gradient = p.Surface((800, 600))
        for y in range(600):
            p.draw.line(gradient, p.Color(135 + y//10, 206 - y//20, 250), (0, y), (800, y))
        screen.blit(gradient, (0, 0))

        # Draw buttons with hover effects and rounded corners
        for button in [easy_button, medium_button, difficult_button]:
            if button.collidepoint(p.mouse.get_pos()):
                p.draw.rect(screen, p.Color("white"), button, border_radius=10)
            else:
                p.draw.rect(screen, p.Color("lightgray"), button, border_radius=10)
            p.draw.rect(screen, p.Color("darkgray"), button.inflate(10, 10), 5, border_radius=10)

        # Special color scheme for the "White" and "Black" buttons
        if white_button.collidepoint(p.mouse.get_pos()):
            p.draw.rect(screen, p.Color("lightgray"), white_button, border_radius=10)
        else:
            p.draw.rect(screen, p.Color("white"), white_button, border_radius=10)

        if black_button.collidepoint(p.mouse.get_pos()):
            p.draw.rect(screen, p.Color("lightgray"), black_button, border_radius=10)
        else:
            p.draw.rect(screen, p.Color("black"), black_button, border_radius=10)

        # Draw start button
        p.draw.rect(screen, p.Color("black"), start_button, border_radius=10)

        # Add text with shadow effect
        draw_text(screen, "Easy", button_font, p.Color("black"), easy_button.centerx, easy_button.centery)
        draw_text(screen, "Medium", button_font, p.Color("black"), medium_button.centerx, medium_button.centery)
        draw_text(screen, "Difficult", button_font, p.Color("black"), difficult_button.centerx, difficult_button.centery)
        draw_text(screen, "White", button_font, p.Color("black"), white_button.centerx, white_button.centery)
        draw_text(screen, "Black", button_font, p.Color("white"), black_button.centerx, black_button.centery)
        draw_text(screen, "Start", button_font, p.Color("white"), start_button.centerx, start_button.centery)

        # Draw pawns on the buttons beside them
        draw_pawn(screen, "white", white_button.centerx, white_button.centery)
        draw_pawn(screen, "black", black_button.centerx, black_button.centery)

        # Instructions
        draw_text(screen, "Select Difficulty and Color", font, p.Color("black"), 400, 50)

        # Handle events
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()

            if e.type == p.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(e.pos):
                    difficulty_selected = True
                    AI_Algo.DEPTH = 2
                elif medium_button.collidepoint(e.pos):
                    difficulty_selected = True
                    AI_Algo.DEPTH = 4
                elif difficult_button.collidepoint(e.pos):
                    difficulty_selected = True
                    AI_Algo.DEPTH = 6
                elif white_button.collidepoint(e.pos):
                    color_selected = True
                    player_white = True
                    player_black = False
                elif black_button.collidepoint(e.pos):
                    color_selected = True
                    player_white = False
                    player_black = True
                elif start_button.collidepoint(e.pos) and difficulty_selected and color_selected:
                    return  

        # Highlight selected buttons
        if difficulty_selected:
            p.draw.rect(screen, p.Color("black"), easy_button if AI_Algo.DEPTH == 2 else (medium_button if AI_Algo.DEPTH == 3 else difficult_button), 5)
        if color_selected:
            p.draw.rect(screen, p.Color("darkgray"), white_button if player_white else black_button, 5)

        p.display.flip()
        clock.tick(60)


def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False
    animate = False
    loadImages()
    running = True
    square_selected = ()
    player_clicks = []
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
   

    while running:
        human_turn = (game_state.white_to_move and player_white) or (not game_state.white_to_move and player_black)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2 and human_turn:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected] #doubt
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()
                move_finder_process = Process(target=AI_Algo.findBestMove, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = AI_Algo.findRandomMove(valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            last_move = game_state.move_log[-1]
            if last_move.piece_captured != "--":
                capture_sound.play()
            elif last_move.piece_moved.lower() == 'wp' and last_move.end_row in [0, 7]:
                promote_sound.play()
            else:
                move_sound.play()
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if not game_over:
            drawMoveLog(screen, game_state, move_log_font)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, game_state, valid_moves, square_selected):
    drawBoard(screen)
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquares(screen, game_state, valid_moves, square_selected):
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100) #transaerency
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ('w' if game_state.white_to_move else 'b'):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawMoveLog(screen, game_state, font):
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH / 2 - text_object.get_width() / 2,
        BOARD_HEIGHT / 2 - text_object.get_height() / 2
    )
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))

def animateMove(move, screen, board, clock):
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 15
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    menu_screen()
    print(player_white,player_black)

    main()
