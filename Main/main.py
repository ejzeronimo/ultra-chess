import pygame as pg
from pygame import freetype
import pieces
import sys

width,height,offsetX,offsetY = 900,600,25,25

#define 2 colors that can be used for the peices
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#chessboard colors
LIGHT = (252, 204, 116)
DARK = (87, 58, 46)
#other colors
GREY = (54, 57, 62)
SILVER = (192, 192, 192)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

turn_number = 0


def coords_to_notation(coords):
    return f'{chr(97 + coords[0])}{8 - coords[1]}'

def notation_to_coords(notation):
    return ord(notation[0]) - 97, 8 - int(notation[1])

#generates the peices and puts them in the appropriate position on the board array
def reset_board(with_pieces=True):
    def generate_pieces(colour):
        return [pieces.Rook(colour), pieces.Knight(colour), pieces.Bishop(colour), pieces.Angel(colour),pieces.Pawn(colour), pieces.Queen(colour), pieces.Cardinal(colour), pieces.Bishop(colour), pieces.Knight(colour), pieces.Rook(colour)]

    def generate_grunts(colour):
        return [pieces.Pawn(colour), pieces.Scout(colour), pieces.Pawn(colour), pieces.Pawn(colour),pieces.Pawn(colour), pieces.Pawn(colour), pieces.Pawn(colour), pieces.Pawn(colour), pieces.Scout(colour), pieces.Pawn(colour)]

    board = [[None for x in range(10)] for x in range(10)]
    if with_pieces:
        board[0] = generate_pieces("black")
        board[1] = generate_grunts("black")
        board[8] = generate_grunts("white")
        board[9] = generate_pieces("white")
        #now make kings
        board[0][4] = pieces.King("black")
        board[9][4] = pieces.King("white")
    return board

#this draws the board an labels dynamically
def draw_board(screen, font, board):
    #calc the height and width of each "square"
    squareUnit = int((screen.get_height() - 50) / 11)
    verticalLabel = ["10","9","8","7","6","5","4","3","2","1"]
    horizonatalLabel = ["A","B","C","D","E","F","G","H","I","J"]
    #draw the labels
    for row in verticalLabel:
        text_rect = font.get_rect(row, size = squareUnit)
        text_rect.center = [int(offsetX + (squareUnit/2)),offsetY + ((verticalLabel.index(row) + 1) * squareUnit) - (squareUnit / 2)]
        font.render_to(screen, text_rect, row, SILVER,size = squareUnit)
    for column in horizonatalLabel:
        text_rect = font.get_rect(column, size = squareUnit)
        text_rect.center = [offsetX + ((horizonatalLabel.index(column) + 2) * squareUnit) - (squareUnit / 2),int(offsetY + (squareUnit * 10) +(squareUnit/2))]
        font.render_to(screen, text_rect, column, SILVER,size = squareUnit)
    #draw the squares
    colour_dict = {True: LIGHT, False: DARK}
    current_colour = True
    for row in range(10):
        for square in range(10):
            pg.draw.rect(screen, colour_dict[current_colour], ((offsetX + squareUnit + (square * squareUnit)), offsetY + (row * squareUnit), squareUnit, squareUnit))
            current_colour = not current_colour
        current_colour = not current_colour

#this draws the peices dynamically
def draw_pieces(screen, font, board):
    #calc the height and width of each "square"
    squareUnit = int((screen.get_height() - 50) / 11)
    for row, pieces in enumerate(board[::(1)]):
        for square, piece in enumerate(pieces[::(1)]):
            if piece:
                text_rect = font.get_rect(piece.image, size = squareUnit)
                text_rect.center = [offsetX + ((square + 2) * squareUnit) - (squareUnit / 2),offsetY + ((row + 1) * squareUnit) - (squareUnit / 2)]
                font.render_to(screen, text_rect, piece.image, BLACK,size = squareUnit)

#this find the x y of the square chosen
def find_square(screen, x, y):
    #calc the height and width of each "square"
    squareUnit = int((screen.get_height() - 50) / 11)
    #look for the square at the xy position (pos - offset) /unit
    target_square = int((x - offsetX) / squareUnit) - 1, int((y - offsetY) / squareUnit)
    return target_square

#draws tiny circles for each legal move
def draw_legal_moves(screen, color, moves, board):
    #calc the height and width of each "square"
    squareUnit = int((screen.get_height() - 50) / 11)
    for move in moves:
        pg.draw.circle(screen, color, (offsetX - (squareUnit / 2) + (move[0] + 2 ) * squareUnit, offsetY + (squareUnit / 2) + (move[1] * squareUnit)), squareUnit / 6)

#draw a small red.orange rectangle on the king
def draw_check(screen, board, kings, turn, checkmate):
    if checkmate:
        king = kings[1 if turn == 'white' else 0]
    else:
        king = kings[0 if turn == 'white' else 1]
    #calc the height and width of each "square"
    squareUnit = int((screen.get_height() - 50) / 11)
    #use the unit to draw a rectangle there
    pg.draw.rect(screen, RED if checkmate else ORANGE, (offsetX + ((king[0] + 1 ) * squareUnit), offsetY + (king[1] * squareUnit), squareUnit, squareUnit), width= int(squareUnit / 10))

#check for checkmate
def checkmate(board, turn, kings):
    for y, row in enumerate(board):
        for x, square in enumerate(row):
            if square and square.colour != turn:
                moves = square.find_moves(board, (x, y), kings, True)
                if moves:
                    return False
    return True

#renders the text and the three background boxes to the side
def draw_text(screen, font, turn, colour, check, playing, promotion):
    #calc the height and width of each "square"
    squareUnit = int((screen.get_height() - 50) / 11)
    counter_colour = BLACK if turn == 'white' else WHITE
    #draw the three rectangles to the side
    pg.draw.rect(screen, SILVER, (2*offsetX + (squareUnit * 11), offsetY + (squareUnit * 4), squareUnit * 5, squareUnit * 2))
    pg.draw.rect(screen, BLACK, (2*offsetX + (squareUnit * 11), offsetY, squareUnit * 5, squareUnit * 4), width=3)
    pg.draw.rect(screen, WHITE, (2*offsetX + (squareUnit * 11), offsetY + (squareUnit * 6), squareUnit * 5, squareUnit * 4), width=3)
    #draw the turn text
    if playing:
        text_rect = font.get_rect(f'{turn} to move'.capitalize(), size = int(squareUnit/3))
        text_rect.center = [2*offsetX + int(squareUnit * 12),offsetY + int(squareUnit * 4.5)]
        font.render_to(screen, text_rect, f'{turn} to move'.capitalize(), counter_colour,size = int(squareUnit/3))
    else:
        text_rect = font.get_rect(f'{turn} wins!'.capitalize(), size = int(squareUnit/3))
        text_rect.center = [2*offsetX + int(squareUnit * 12),offsetY + int(squareUnit * 4.5)]
        font.render_to(screen, text_rect, f'{turn} wins!'.capitalize(), counter_colour,size = int(squareUnit/3))
    #promotion chooser text
    promote_dict = {'queen': 9813, 'rook': 9814, 'bishop': 9815, 'knight': 9816}
    text_rect = font.get_rect(f'Promote: {chr(promote_dict[promotion])}', size = int(squareUnit/3))
    text_rect.center = [2*offsetX + int(squareUnit * 15),offsetY + int(squareUnit * 4.5)]
    font.render_to(screen, text_rect, f'Promote: {chr(promote_dict[promotion])}', counter_colour,size = int(squareUnit/3))
    #check text lol
    if check:
        text_rect = font.get_rect(('Check' if playing else 'Checkmate'), size = int(squareUnit))
        text_rect.center = [2*offsetX + int(squareUnit * 13.5),offsetY + int(squareUnit * 5.5)]
        font.render_to(screen, text_rect, ('Check!' if playing else 'Checkmate'), ORANGE if playing else RED,size = int(squareUnit))

#draws all the captured peices
def draw_captures(screen, font, captures):
    #calc the height and width of each "square"
    squareUnit = int((screen.get_height() - 50) / 11)
    #if the peices were captured by white
    for e, piece in enumerate([i for i in captures if i.colour == 'black']):
        offsetSudoY,offsetSudoX = 0,0
        if e < 5:
            offsetSudoY = 0
            offsetSudoX = 0
        elif e < 10:
            offsetSudoY = squareUnit
            offsetSudoX = 5
        elif e < 15:
            offsetSudoY = 2*squareUnit
            offsetSudoX = 10
        else:
            offsetSudoY = 3*squareUnit
            offsetSudoX = 15
        #now render the image
        text_rect = font.get_rect(piece.image, size = squareUnit)
        text_rect.center = [2*offsetX + int(squareUnit * 11.5) + (squareUnit * (e - offsetSudoX)),offsetY + offsetSudoY + int(.5 * squareUnit)]
        font.render_to(screen, text_rect, piece.image, BLACK,size = squareUnit)
    #if the peices were captured by black
    for e, piece in enumerate([i for i in captures if i.colour == 'white']):
        offsetSudoY,offsetSudoX = 0,0
        if e < 5:
            offsetSudoY = 0
            offsetSudoX = 0
        elif e < 10:
            offsetSudoY = squareUnit
            offsetSudoX = 5
        elif e < 15:
            offsetSudoY = 2*squareUnit
            offsetSudoX = 10
        else:
            offsetSudoY = 3*squareUnit
            offsetSudoX = 15
        #now render the image
        text_rect = font.get_rect(piece.image, size = squareUnit)
        text_rect.center = [2*offsetX + int(squareUnit * 11.5) + (squareUnit * (e - offsetSudoX)),offsetY + offsetSudoY + int(6.5 * squareUnit)]
        font.render_to(screen, text_rect, piece.image, WHITE,size = squareUnit)



#FIX THIS
def move_piece(board, target, kings, origin, destination, captures, promotion):
    global turn_number
    if target.colour == 'white':
        turn_number += 1

    #piece move conditions
    for row in board:
        for piece in row:
            if piece and piece.name == 'pawn' and piece.en_passant:
                piece.en_passant = False


    promoting = False

    #all the rules for moving pawns
    if target.name == 'pawn':
        if target.double_move:
            target.double_move = False
        if abs(origin[1] - destination[1]) == 2:
            target.en_passant = True
        if origin[0] != destination[0] and not board[destination[1]][destination[0]]:
            captures.append(board[destination[1] - target.direction][destination[0]])
            board[destination[1] - target.direction][destination[0]] = None
        if destination[1] == (0 if target.colour == 'white' else 7):
            promoting = True
            piece_dict = {'queen': pieces.Queen(target.colour), 'knight': pieces.Knight(target.colour),
                          'rook': pieces.Rook(target.colour), 'bishop': pieces.Bishop(target.colour)}


    #all the rules for moving kings
    if target.name == 'king':
        kings[int(target.colour == "black")] = destination
        if target.castle_rights:
            target.castle_rights = False
        if destination[0] - origin[0] == 2:
            board[target.back_rank][5] = board[target.back_rank][7]
            board[target.back_rank][7] = None
        if origin[0] - destination[0] == 2:
            board[target.back_rank][3] = board[target.back_rank][0]
            board[target.back_rank][0] = None

    #castling
    if target.name == 'rook' and target.castle_rights:
        target.castle_rights = False

    # add any existing piece to captures list
    if board[destination[1]][destination[0]]:
        captures.append(board[destination[1]][destination[0]])

    #move piece
    if not promoting:
        board[destination[1]][destination[0]] = target
    else:
        board[destination[1]][destination[0]] = piece_dict[promotion]
    board[origin[1]][origin[0]] = None

    # any checks with new board status
    enemy_king = kings[int(target.colour == "white")]
    check = board[enemy_king[1]][enemy_king[0]].in_check(board, enemy_king)
    return board, captures, kings, check






#CLEANUP????????
def main():
    #this will store the turns taken
    global turn_number
    # window init
    pg.init()
    clock = pg.time.Clock()
    window_logo = pg.image.load('chess_piece_king.png')
    pg.display.set_caption('Ultra Chess')
    pg.display.set_icon(window_logo)
    screen = pg.display.set_mode((width, height),pg.RESIZABLE)
    # font/pieces init: the piece icons come from the unicode of this font
    freetype.init()
    font = freetype.Font('FreeSerif-4aeK.ttf', 50)
    # board init
    board = reset_board()
    # declare vars
    playing = True
    turn = 'white'
    check = False
    kings = [(4, 9), (4, 0)]
    promotion = 'queen'
    target_square = None
    target = None
    captures = []
    legal_moves = []

    while True:
        #set the colors to be used
        screen.fill(GREY)
        COLOR = WHITE if turn == 'white' else BLACK
        #draw the static baord and its labels
        draw_board(screen, font, board)
        #draw the peices
        draw_pieces(screen, font, board)
        #draw the test to the side
        draw_text(screen,font, turn, COLOR, check, playing, promotion)

        #check for all user inputs
        for event in pg.event.get():
            #resize the window
            if event.type == pg.VIDEORESIZE:
                surface = pg.display.set_mode((int((event.h - 50) / 11)*16 + offsetX*3, event.h), pg.RESIZABLE)
            #mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                #calc the height and width of each "square"
                squareUnit = int((screen.get_height() - 50) / 11)
                if playing and (11*squareUnit + offsetX) > event.pos[0] > (squareUnit + offsetX) and (10*squareUnit + offsetX) > event.pos[1] > offsetY:
                    #left click shows moves only if turn color and peice color are the same and in zone
                    if event.button != 3:
                        target_square = find_square(screen, event.pos[0], event.pos[1])
                        target = board[target_square[1]][target_square[0]]
                        if target and turn == target.colour:
                            legal_moves = target.find_moves(board, target_square, kings, check)
                    #EDIT THIS
                    elif target_square and target:
                        #right click?
                        destination = find_square(screen, event.pos[0], event.pos[1])
                        if destination in legal_moves:
                            board, captures, kings, check = move_piece(board, target, kings, target_square, destination,captures, promotion)
                            if check and checkmate(board, turn, kings):
                                playing = False
                                target_square = None
                            else:
                                turn = 'black' if turn == 'white' else 'white'
                            legal_moves = []
                        else:
                            target_square = None
                    else:
                        target_square = None
                else:
                    target_square = None
            if event.type == pg.KEYDOWN:
                #button press
                if event.key == pg.K_r:
                    #game reset
                    board = reset_board()
                    kings = [(4, 7), (4, 0)]
                    turn = 'white'
                    check = False
                    target_square = None
                    captures = []
                    playing = True
                    turn_number = 0
                #choose what to promote to, should be in a menu
                if event.key == pg.K_1:
                    promotion = 'queen'
                if event.key == pg.K_2:
                    promotion = 'knight'
                if event.key == pg.K_3:
                    promotion = 'rook'
                if event.key == pg.K_4:
                    promotion = 'bishop'
            #of the user clicks the close button
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        #draw all legal moves of the selecte peice
        if target_square and target and turn == target.colour and legal_moves:
            draw_legal_moves(screen, COLOR, legal_moves, board)
        if captures:
            draw_captures(screen, font, captures)
        #if anyone is in check draw a phat square
        if check:
            draw_check(screen, board, kings, turn, not playing)
        #if you have a target draw a rectangle there
        if target_square:
            #calc the height and width of each "square"
            squareUnit = int((screen.get_height() - 50) / 11)
            #use the unit to draw a rectangle there
            pg.draw.rect(screen, COLOR, (offsetX + ((target_square[0] + 1 ) * squareUnit), offsetY + (target_square[1] * squareUnit), squareUnit, squareUnit), width= int(squareUnit / 20))

        #update cycle code
        pg.display.update()
        clock.tick(60)

#starts the main loop
if __name__ == '__main__':
    main()
