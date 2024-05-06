from flask import Flask, request, render_template, redirect, make_response, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
boggle_game = Boggle()
app.debug = False

app.config['SECRET_KEY'] = 'key_value_random_somewhere'

toolbar = DebugToolbarExtension(app)


@app.route("/")
def start_page():
    """Game Board Page"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    
    return render_template("game.html", board=board, highscore=highscore)

@app.route("/submit-guess")
def check_guess():
    guess= request.args["guess"]
    print(guess)
    board = session["board"]
    response = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': response})

@app.route("/score-submit", methods=["POST"])
def score_logic():
    """Handle submitting score logic"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    session['highscore'] = max(score, highscore)

    return jsonify(newRecord = score > highscore)
    