import flask
from flask import request, jsonify, json
from ShipBoard import Ship_Board
from game import Game

app = flask.Flask(__name__)
app.config["DEBUG"] = True

game = Game()
game.player1.board = Ship_Board()
game.player2.board = Ship_Board()
 

@app.route('/api/v1/battleship/shipboard/random/<str: name>', methods = ['GET'])
def get_random_board(name):
    
    if name == game.player1.name:
        return json.dumps({"player" :  name, "board" : game.player1.board.set_ships_random()})
    else:
        return json.dumps({"player" :  name, "board" : game.player2.board.set_ships_random()})


@app.route('/api/v1/battleship/shipboard/clear/<str: name>', methods = ['GET'])
def clear_board(name):

    if name == game.player1.name:
        return json.dumps({"player" : name, "board" : game.player1.board.deleting_board()})
    else:
        return json.dumps({"player" : name, "board" : game.player2.board.deleting_board()})


@app.route('/api/v1/battleship/shipboard/manual', methods = ['PUT'])
def set_board_menual():

    response = request.get_json()
    if ((response['row'] < 1) or (response['row'] > 10) or (response['column'] < 1) or (response['column'] > 10) or
       (response['direction'] < 1) or (response['direction'] > 4) or (response['ship_size'] < 1) or (response['ship_size'] > 4)):
        return "invalit parameters"

    else:
        row = response['row'] 
        column = response['column']
        direction = response['direction']
        ship_size = response['ship_size']
        if response['player'] == game.player1.name:
            return json.dumps({"player" : response['player'], "ships_count" : game.player1.board.ships_count, "board" : game.player1.board.set_ship_with_hand(row, column, direction, ship_size)})
        else:
            return json.dumps({"player" : response['player'], "ships_count" : game.player2.board.ships_count, "board" : game.player2.board.set_ship_with_hand(row, column, direction, ship_size)})


@app.route('/api/v1/battleship/player/registr', method = ['POST'])
def registr_player():

    response = request.get_json()
    if len(response['player1'].split()) == 0:
        return "Player1, Please enter Your name"
    elif len(response['player2'].split()) == 0:
        return "Player2, Please enter Your name"

    game.registration(response['player1'], response['player2'])
    return "Players are registred"

if __name__ == '__main__':
    app.run()