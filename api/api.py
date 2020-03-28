import flask
from flask import request, jsonify, json
from ShipBoard import Ship_Board
from game import Game

app = flask.Flask(__name__)
app.config["DEBUG"] = True

game = Game()

 
@app.route('/api/v1/battleship/player/registr', methods = ['POST'])
def registr_player():
    
    response = request.get_json()
    if len(response['player1'].split()) == 0:
        return "Player1, Please enter Your name"
    elif len(response['player2'].split()) == 0:
        return "Player2, Please enter Your name"

    game.registration(response['player1'], response['player2'])
    game.player1.board = Ship_Board()
    game.player2.board = Ship_Board()
    return "Players are registred!!! Game are playing {} and {}".format(game.player1.name, game.player2.name)


@app.route('/api/v1/battleship/shipboard/random/<name>', methods = ['GET'])
def get_random_board(name):
    
    if name == game.player1.name:
        return json.dumps({"player" :  name, "board" : game.player1.board.set_ships_random()})
    elif name == game.player2.name:
        return json.dumps({"player" :  name, "board" : game.player2.board.set_ships_random()})
    else:
        return "Oops!!! That was no valid name. Please enter again."


@app.route('/api/v1/battleship/shipboard/clear/<name>', methods = ['GET'])
def clear_board(name):

    if name == game.player1.name:
        return json.dumps({"player" : game.player1.name, "result" : game.player1.board.deleting_board()})
    elif name == game.player2.name:
        return json.dumps({"player" : game.player2.name, "result" : game.player2.board.deleting_board()})
    else:
        return "Oops!!! That was no valid name. Please enter again."


@app.route('/api/v1/battleship/shipboard/manual', methods = ['PUT'])
def set_board_menual():

    response = request.get_json()
    if ((response['row'] in range(1, 11)) and (response['column'] in range(1, 11))  and (response['direction'] in [1, 2])
       and (response['ship_size'] in range(1, 5))):
        row = response['row'] 
        column = response['column']
        direction = response['direction']
        ship_size = response['ship_size']
        if response['player'] == game.player1.name:
            return json.dumps({"player" : response['player'], "ships_count" : game.player1.board.ships_count, "board" : game.player1.board.set_ship_with_hand(row, column, direction, ship_size)})
        elif response['player'] == game.player2.name:
            return json.dumps({"player" : response['player'], "ships_count" : game.player2.board.ships_count, "board" : game.player2.board.set_ship_with_hand(row, column, direction, ship_size)})
        else:
            return "Oops!!! No player by this name."
    else:
          return "invalit parameters"


@app.route('/api/v1/battleship/player/begginer', methods = ["GET"])
def who_is_starter():

    return json.dumps({"player" : game.starting()})


@app.route('/api/v1/battleship/player/fight', methods = ['PUT'])
def fight_players():
    
    response = request.get_json()
    if ((response['row'] in range(1, 11)) and (response['column'] in range(1, 11))):    
        row = response['row'] 
        column = response['column']
        if response['player'] == game.player1.name:
            return json.dumps({"player" : response['player'], "result" : game.player2.board.checking_ships_fight(row, column)})
        elif response['player'] == game.player2.name:
            return json.dumps({"player" : response['player'], "result" : game.player1.board.checking_ships_fight(row, column)})
        else:
            return "No player by this name"
    else:
        return "invalit parameters"


if __name__ == '__main__':
    app.run()