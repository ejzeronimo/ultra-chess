class Piece:
    images = ['white_king', 'white_queen', 'white_rook', 'white_bishop', 'white_knight', 'white_pawn', 'black_king','black_queen', 'black_rook', 'black_bishop', 'black_knight', 'black_pawn', 'black_cardinal', 'white_angel', None, 'black_scout', 'white_cardinal', 'black_angel', None, 'white_scout']

    #implement vector & displacement into moveset
    def __init__(self, colour, name):
        self.colour = colour
        self.name = name
        self.image = chr(int('98' + str(self.images.index(f'{colour}_{name}') + 12)))

    def find_moves(self, board, location, kings, check):
        x, y = location[0], location[1]
        legal_moves = []
        additional = set()
        #add the pawns en passant
        if self.name == 'pawn' or self.name == 'scout':
            additional.update(self.additional_moves(board, x, y))

        #for all peices movesets SLIGHT OVERHAUL
        for x2, y2, moveType in self.moveset.union(additional):
            #makes sure we cannot go off the negative side of the board
            if any(i < 0 for i in (x + x2, y + y2)):
                continue
            try:
                # #the destination
                # coords = x + x2, y + y2
                # square = board[coords[1]][coords[0]]
                # #if you are NOT a pawn and the square is captureable or empty you ARE a pawn and you can move two spaces
                # if self.name != 'pawn' and (square is None or square and square.colour != self.colour and square.name != 'king') or self.name == 'pawn' and ((x2 == 0 and square is None) or (x2, y2) in additional):
                #     #gets our king
                #     king = kings[int(self.colour == "black")]
                #     #castle logic
                #     king_pos = coords if king == (x, y) else king
                #     #if king is not in check when we move
                #     if not board[king[1]][king[0]].in_check(board, king_pos, moved_from=location, moved_to=coords):
                #         legal_moves.append(coords)
                #     #if the square is not ours, not yet in the moves, and not causing check and the square is not a king
                #     if square and square.colour != self.colour or coords not in legal_moves and not check and square.name != 'king':
                #         continue
                #     #if your not a knight/pawn or your a double moving pawn the you get to multiply out to make a line
                #     #if coords == vector \/
                #     while self.unbounded or self.name == 'pawn' and self.double_move:
                #         #multiply out the direction and get the square
                #         coords = coords[0] + x2, coords[1] + y2
                #         square = board[coords[1]][coords[0]]
                #         #if we are in check and the king would still be in check if we moved skip
                #         if check and board[king[1]][king[0]].in_check(board, king_pos, moved_from=location, moved_to=coords):
                #             continue
                #         #if we are not a pawn 
                #         if all(i >= 0 for i in coords) and self.name != 'pawn' and (square is None or square and square.colour != self.colour and square.name != 'king') or self.name == 'pawn' and (x2 == 0 and square is None):
                #             legal_moves.append(coords)
                #         #not in check leave
                #         elif not check:
                #             break
                #         #if we are a pawn and there is someone in that square that is not our color
                #         if self.name == 'pawn' or square and square.colour != self.colour:
                #             break

                #the destination
                coords = x + x2, y + y2
                square = board[coords[1]][coords[0]]

                if square is None or square and square.colour != self.colour and square.name != 'king':
                    #gets our king
                    king = kings[int(self.colour == "black")]
                    #castle logic
                    king_pos = coords if king == (x, y) else king
                    # #if king is not in check when we move
                    # if not board[king[1]][king[0]].in_check(board, king_pos, moved_from=location, moved_to=coords):
                    #     legal_moves.append(coords)
                    # #if the square is not ours, not yet in the moves, and not causing check and the square is not a king
                    # if square and square.colour != self.colour or coords not in legal_moves and not check:
                    #     continue
                    #if its a vector
                    if moveType == 'vector':
                        #if your not a knight/pawn or your a double moving pawn the you get to multiply out to make a line
                        while self.name != 'pawn' and self.name != 'scout' or (self.name == 'pawn' and self.double_move):
                            #if we are in check and the king would still be in check if we moved skip
                            if check and board[king[1]][king[0]].in_check(board, king_pos, moved_from=location, moved_to=coords):
                                continue
                            #if we are not a pawn 
                            if all(i >= 0 for i in coords) and self.name != 'pawn' and (square is None or square and square.colour != self.colour and square.name != 'king') or self.name == 'pawn' and (x2 == 0 and square is None):
                                legal_moves.append(coords)
                            #not in check leave
                            elif not check:
                                break
                            #if we are a pawn and there is someone in that square that is not our color
                            if self.name == 'pawn' or square and square.colour != self.colour:
                                break
                            #multiply out the direction and get the square
                            coords = coords[0] + x2, coords[1] + y2
                            square = board[coords[1]][coords[0]]
                        #scout special
                        while self.name == 'scout':
                            #if we are in check and the king would still be in check if we moved skip
                            if check and board[king[1]][king[0]].in_check(board, king_pos, moved_from=location, moved_to=coords):
                                continue
                            #if we are not a pawn 
                            if all(i >= 0 for i in coords) and (square is None):
                                legal_moves.append(coords)
                            #not in check leave
                            elif not check:
                                break
                            #multiply out the direction and get the square
                            coords = coords[0] + x2, coords[1] + y2
                            square = board[coords[1]][coords[0]]
                    #if its a displacement
                    else:
                        legal_moves.append(coords)
            except IndexError:
                continue
        #if the king is NOT in check and can still castle
        if self.name == 'king' and not check and self.castle_rights and self.castle(board, x, y):
            legal_moves.extend(self.castle(board, x, y))
        #return the list
        return legal_moves

#REWORKING THE KING - COME BACK TO
class King(Piece):
    def __init__(self, colour):
        self.back_rank = 9 if colour == 'white' else 0
        self.moveset = {(-1,0,'displacement'),(1,0,'displacement'),(0,1,'displacement'),(0,-1,'displacement'),(-1,-1,'displacement'),(-1,1,'displacement'),(1,1,'displacement'),(1,-1,'displacement')}
        self.castle_rights = True
        super().__init__(colour, 'king')

    #NEEDS OVERHAUL JACKSON
    def in_check(self, board, location, moved_from=None, moved_to=None):
        for move in self.moveset:
            coords = location
            square = board[coords[1]][coords[0]]
            while (coords != moved_to or location == moved_to) and (coords == location or coords == moved_from or square is None):
                try:
                    if any(i < 0 or i > 9 for i in (coords[0] + move[0], coords[1] + move[1])):
                        break
                    coords = coords[0] + move[0], coords[1] + move[1]
                    square = board[coords[1]][coords[0]]
                except IndexError:
                    break
            if square is None or square.colour == self.colour or coords == moved_to:
                continue
            if 0 in move and (square.name == 'rook' or square.name == 'queen') or 0 not in move and (square.name == 'cardinal' or square.name == 'bishop' or square.name == 'queen' or (square.name == 'pawn' and location[1] - coords[1] == square.direction)):
                return True
            #subtract x and y from square square.additional_moves(board, coords[1], coords[0])
            #add the diagonal array to the kings pos then if this unit is at that point
            #{(-1,-1),(-1,1),(1,1),(1,-1)}

            if 0 not in move and ((square.name == 'scout' and abs(location[1] - coords[1]) == 1 )):
                return True

            if 0 not in move and  (square.name == 'scout'):
                print(location,({location[1] - coords[1],location[0] - coords[0]} in {(-1,-1),(-1,1),(1,1),(1,-1)}))
            
        for x, y in {(x, y) for x in range(-2, 3) for y in range(-2, 3) if x != 0 and y != 0 and abs(x) != abs(y)}:
            try:
                coords = location[0] + x, location[1] + y
                square = board[coords[1]][coords[0]]
                if any(i < 0 for i in (coords[0], coords[1])):
                    continue
                if square and square.colour != self.colour and square.name == 'knight' and coords != moved_to:
                    return True
            except IndexError:
                continue
        return False

    #used to castle the king
    def castle(self, board, x, y):
        moves = []
        if board[self.back_rank][0] and board[self.back_rank][0].name == 'rook' and board[self.back_rank][
            0].castle_rights:
            squares = [(i, self.back_rank) for i in range(1, 4)]
            if all(not piece for piece in board[self.back_rank][1:4]) and all(
                    not self.in_check(board, square) for square in squares):
                moves.append((2, self.back_rank))
        if board[self.back_rank][7] and board[self.back_rank][7].name == 'rook' and board[self.back_rank][
            7].castle_rights:
            squares = [(i, self.back_rank) for i in range(5, 7)]
            if all(not piece for piece in board[self.back_rank][5:7]) and all(
                    not self.in_check(board, square) for square in squares):
                moves.append((6, self.back_rank))
        return moves

#queen OK
class Queen(Piece):
    def __init__(self, colour):
        self.moveset = {(-1,0,'vector'),(1,0,'vector'),(0,1,'vector'),(0,-1,'vector'),(-1,-1,'vector'),(-1,1,'vector'),(1,1,'vector'),(1,-1,'vector')}
        super().__init__(colour, 'queen')

#rook OK
class Rook(Piece):
    def __init__(self, colour):
        self.moveset = {(-1,0,'vector'),(1,0,'vector'),(0,1,'vector'),(0,-1,'vector')}
        self.castle_rights = True
        super().__init__(colour, 'rook')

#bishop OK
class Bishop(Piece):
    def __init__(self, colour):
        self.moveset = {(-1,-1,'vector'),(-1,1,'vector'),(1,1,'vector'),(1,-1,'vector')}
        super().__init__(colour, 'bishop')

#knight OK
class Knight(Piece):
    def __init__(self, colour):
        self.moveset = {(2,-1,'displacement'),(1,2,'displacement'),(-1,-2, 'displacement'),(-2,-1,'displacement'),(2,1,'displacement'),(-2,1,'displacement'),(1,-2,'displacement'),(-1,2,'displacement')}
        super().__init__(colour, 'knight')


class Pawn(Piece):
    def __init__(self, colour):
        self.direction = -1 if colour == 'white' else 1
        self.moveset = {(0, y * self.direction, 'displacement') for y in range(1, 2)}
        self.en_passant = False
        self.double_move = True
        super().__init__(colour, 'pawn')

    def additional_moves(self, board, x, y):
        valid_attacks = set()
        for n in range(-1, 2, 2):
            try:
                square = board[y + self.direction][x + n]
                if square and square.colour != self.colour:
                    valid_attacks.add((n, self.direction, 'displacement'))
                else:
                    square = board[y][x + n]
                    if square and square.name == 'pawn' and square.en_passant:
                        valid_attacks.add((n, self.direction, 'displacement'))
            except IndexError:
                pass
        return valid_attacks

#scout OK
class Scout(Piece):
    def __init__(self, colour):
        self.moveset = {(0,-1,'vector'),(0,1,'vector')}
        super().__init__(colour, 'scout')

    def additional_moves(self, board, x, y):
        valid_attacks = set()
        for x2 in range(-1, 2, 2):
            try:
                for y2 in range(-1, 2, 2):
                    try:
                        square = board[y + y2][x + x2]
                        if square and square.colour != self.colour:
                            valid_attacks.add((x2, y2, 'displacement'))
                    except IndexError:
                        pass
            except IndexError:
                pass
        return valid_attacks

#cardinal OK
class Cardinal(Piece):
    def __init__(self, colour):
        #add in horizontal and vertical displacement ones
        self.moveset = {(-1,-1,'vector'),(-1,1,'vector'),(1,1,'vector'),(1,-1,'vector'),(1,0,'displacement'),(0,1,'displacement'),(-1,0,'displacement'),(0,-1,'displacement')}
        super().__init__(colour, 'cardinal')


class Angel(Piece):
    def __init__(self, colour):
        self.moveset = {(-1,0,'displacement'),(1,0,'displacement'),(0,1,'displacement'),(0,-1,'displacement'),(-1,-1,'displacement'),(-1,1,'displacement'),(1,1,'displacement'),(1,-1,'displacement')}
        super().__init__(colour, 'angel')