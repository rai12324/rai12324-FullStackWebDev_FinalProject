import random
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from flask import Flask, render_template, request, flash, redirect, url_for,session,redirect
from colored import fg, bg, attr
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

app = Flask("Basketball")
app.secret_key = 'wowsect'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///slam.db'
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    wins = db.Column(db.Integer, default=0)
    attempts = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', wins={self.wins}, attempts={self.attempts})>"

class PlayerInfo(db.Model):
    __tablename__ = 'players'
    player_id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.String(20), nullable=False)
    player_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    jersey = db.Column(db.Integer, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=True)

    def __repr__(self):
        return f"<PlayerInfo(player_id={self.player_id}, player_name='{self.player_name}', position='{self.position}', height='{self.height}', jersey={self.jersey}, team_id={self.team_id})>"
    
class TeamInfo(db.Model):
    __tablename__ = 'teams'
    team_id = db.Column(db.Integer, primary_key=True)
    conference = db.Column(db.String(10), nullable=False)
    division = db.Column(db.String(20), nullable=False)
    team_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<TeamInfo(team_id={self.team_id}, team_name='{self.team_name}', conference='{self.conference}', division='{self.division}')>"
    
##-----------------------------------------------------------------------------------------------------------------------------------------------------##

db.init_app(app)

tempTeamDict = {team: index for index, team in enumerate(["Nuggets", "Timberwolves", "Trail Blazers", "Thunder", "Jazz", "Warriors", "Clippers", "Lakers", "Suns", "Kings", "Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs", "Celtics", "Nets", "Knicks", "76ers", "Raptors", "Cavaliers", "Bulls", "Pistons", "Pacers", "Bucks", "Hawks", "Hornets", "Heat", "Magic", "Wizards"])}
player_dict = players.get_active_players()

attempts = 8
guess_history = []  # Move this outside the play function and make it global
guess_feedbacks = []
correct = False
random_player = None  # Define random_player globally

def updateDatabase():
    playerCounter = 0
    for x in player_dict:
        idIn = list(x.values())[0]
        playerNameIn = list(x.values())[1]
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=idIn)
        player_info = player_info.get_normalized_dict()
        heightIn = player_info['CommonPlayerInfo'][0]['HEIGHT']
        positionIn = player_info['CommonPlayerInfo'][0]['POSITION']
        jerseyIn = player_info['CommonPlayerInfo'][0]['JERSEY']
        team_name = player_info['CommonPlayerInfo'][0]['TEAM_NAME']
        if (team_name != ''):
            team_idIn = tempTeamDict[team_name]
        else:
            team_idIn = 300

        if (jerseyIn != ''):
            jerseyIn = int(jerseyIn)
        else:
            jerseyIn = None

        # Example check before adding a player
        with app.app_context():
            playerIn = PlayerInfo(player_id=idIn, height=heightIn, player_name=playerNameIn, position=positionIn, jersey=jerseyIn, team_id=team_idIn)
            existing_player = PlayerInfo.query.filter_by(player_id=idIn).first()
            if existing_player is None:
                playerCounter = playerCounter + 1
                print("PC: ", playerCounter, " | ID: ", idIn, " Name: ", playerNameIn, " Height: ", heightIn, " Position: ", positionIn, " Jersey: ", jerseyIn, " TeamName: ", team_name, " TeamID: ", team_idIn)
                db.session.add(playerIn)
            else:
                print("PC: ", playerCounter, " | Player already exists.")
                playerCounter = playerCounter + 1
            db.session.commit()

def validate_input(guess):
    print("Type of guess:", type(guess))
    guess = guess.upper()
    #playerList = players.get_players()
    #print(player_names)
    existing_player = PlayerInfo.query.filter(func.upper(PlayerInfo.player_name) == guess).first()
    if not existing_player:
        print("Invalid input. Please enter a NBA Player")
        return False
    return True


##### NEED TO FIX PROVIDE-FEEDBACK

def provide_feedback(guess):
    guess_val =  PlayerInfo.query.filter_by(player_name=guess).first()
    random_val = PlayerInfo.query.filter_by(player_name = random_player.player_name).first()

    if guess_val is None:
        return "Player not found in the database", []

    feedback_parts = []
    guess_info = {}
    random_info = {}
    guess_info["NAME"] = guess_val.player_name
    guess_info['player_id'] = guess_val.player_id
    guess_info["HEIGHT"] = guess_val.height
    guess_info["POSITION"] = guess_val.position
    guess_info["JERSEY"] = guess_val.jersey
    guess_team = TeamInfo.query.filter_by(team_id = guess_val.team_id).first()
    guess_info["TEAM"] = guess_team.team_name
    guess_info["CONFERENCE"] = guess_team.conference
    guess_info["DIV"] = guess_team.division
    random_info["NAME"] = random_val.player_name
    random_info['player_id'] = random_val.player_id
    random_info["HEIGHT"] = random_val.height
    random_info["POSITION"] = random_val.position
    random_info["JERSEY"] = random_val.jersey
    random_team = TeamInfo.query.filter_by(team_id = random_val.team_id).first()
    random_info["TEAM"] = random_team.team_name
    random_info["CONFERENCE"] = random_team.conference
    random_info["DIV"] = random_team.division

    inches_guess = ""
    inches_rando = ""

    foot_rando = random_info["HEIGHT"][0]
    for x in range(2,len(random_info["HEIGHT"])):
        inches_rando += random_info["HEIGHT"][x]
    height_rando = int(foot_rando)*12+int(inches_rando)

    foot_guess = guess_info["HEIGHT"][0]
    for x in range(2,len(guess_info["HEIGHT"])):
        inches_guess += guess_info["HEIGHT"][x]
    height_guess = int(foot_guess)*12+int(inches_guess)

    # Append / reordering stuff
    # Name
    if random_info["NAME"].lower() == guess_info["NAME"].lower():
        feedback_parts.append(("correct", guess_info["NAME"]))
    else:
        feedback_parts.append(("incorrect", guess_info["NAME"]))

    # Team
    if random_info["TEAM"] == guess_info["TEAM"]:
        feedback_parts.append(("correct", guess_info["TEAM"]))
    else:
        feedback_parts.append(("incorrect", guess_info["TEAM"]))

    # Conference
    if random_info["CONFERENCE"] == guess_info["CONFERENCE"]:
        feedback_parts.append(("correct", guess_info["CONFERENCE"]))
    else:
        feedback_parts.append(("incorrect", guess_info["CONFERENCE"]))

    # Division
    if random_info["DIV"] == guess_info["DIV"]:
        feedback_parts.append(("correct", guess_info["DIV"]))
    else:
        feedback_parts.append(("incorrect", guess_info["DIV"]))

    # Position
    if random_info["POSITION"] == guess_info["POSITION"]:
        feedback_parts.append(("correct", guess_info["POSITION"]))
    elif random_info["POSITION"] in guess_info["POSITION"]:
        feedback_parts.append(("closeh", guess_info["POSITION"])) 
    else:
        feedback_parts.append(("incorrect", guess_info["POSITION"]))

    # Height
    if height_rando == height_guess:
        feedback_parts.append(("correct",guess_info["HEIGHT"] ))
    elif 0 < (height_rando - height_guess) <= 3:
        feedback_parts.append(("closeh", guess_info["HEIGHT"] + "↑"))
    elif -2 <= (height_rando - height_guess) < 0:
        feedback_parts.append(("closeh", guess_info["HEIGHT"] + "↓"))
    else:
        if(height_rando>height_guess):
            feedback_parts.append(("incorrect", guess_info["HEIGHT"] + "↑"))
        else:
            feedback_parts.append(("incorrect", guess_info["HEIGHT"]+ "↓"))

    # Jersey
    if random_info["JERSEY"] is not None and guess_info["JERSEY"] is not None:
        if random_info["JERSEY"] == guess_info["JERSEY"]:
            feedback_parts.append(("correct", f"{guess_info['JERSEY']}"))
        elif 0 < (random_info["JERSEY"] - guess_info["JERSEY"]) <= 3:
            feedback_parts.append(("closeh", f"{guess_info['JERSEY']}"+ "↑"))
        elif -2 <= (random_info["JERSEY"] - guess_info["JERSEY"]) < 0:
            feedback_parts.append(("closeh", f"{guess_info['JERSEY']}" + "↓"))
        else:
            if(random_info["JERSEY"] > guess_info["JERSEY"]):
                feedback_parts.append(("incorrect", f"{guess_info['JERSEY']}"+ "↑"))
            else:
                feedback_parts.append(("incorrect", f"{guess_info['JERSEY']}"+ "↓"))
    else:
        # Handle the case where one of the jersey numbers is None
        feedback_parts.append(("incorrect", "Jersey number is not available for comparison"))


    feedback = ""
    for part in feedback_parts:
        status, value = part
        feedback += f'<span class="{ "correct-guess" if status == "correct" else "closel-guess" if status == "closel" else "closeh-guess" if status == "closeh" else "incorrect-guess" }">{value}</span> '

    return feedback.strip(), feedback_parts

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username is already taken
        if User.query.filter_by(username=username).first():
            flash("Username is already taken. Please choose another.")
            return redirect(url_for('register'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password) # default hashing method is sha256

        # Create a new user
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global random_player
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        print(user)

        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            flash("Login successful!")
            attempts = 8
            random_player = PlayerInfo.query.order_by(func.random()).first()
            print(random_player)
            return redirect(url_for('play'))

        flash("Invalid username or password. Please try again.")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))

# random_player = None  # Define random_player globally
# guess_feedbacks = []  # Define guess_feedbacks globally

@app.route('/play', methods=['GET', 'POST'])
def play():
    # global random_player, guess_feedbacks  # Add guess_feedbacks to the global scope

    if 'username' not in session:
        flash("Please log in to play.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        guess = request.form.get('guess')
        print(guess)
        
        if guess == None:
            print("It IS NONE")
        if not validate_input(guess):
            flash("Invalid input. Please enter an NBA Player.")
            # Don't redirect, render the template directly
            attempts = int(request.form.get('attempts'))
            return render_template('play.html', feedback="", attempts=attempts, secret_word=random_player.player_name, guess="", guess_history=guess_history)
        else:
            print("Guess: ", guess)
            feedback, feedback_parts = provide_feedback(guess)
            # print("Temp", feedback_parts)
            guess_feedbacks.append({"guess": guess, "feedback_parts": feedback_parts})
            guess_history.append({"guess": guess, "feedback": feedback_parts})  # Store the feedback as a list of tuples

            attempts = int(request.form.get('attempts'))
            attempts -= 1

        if guess.lower() == random_player.player_name.lower():
            print("I am in the wins checker")
            correct = True
            username = session.get('username')
            user = User.query.filter_by(username=username).first()
            if user:
                user.wins += 1
                db.session.commit()
            return render_template('play_again.html', correct=True, secret_word=random_player.player_name)
        elif attempts == 0:
            print("You lost")
            return render_template('play_again.html', correct=False, secret_word=random_player.player_name)
        else:
            correct = False  # Reset correct to False after processing the guess
            return render_template('play.html', feedback_parts=feedback_parts, attempts=attempts, secret_word=random_player.player_name,
                                correct=False, guess_history=guess_history, guess_feedbacks=guess_feedbacks)

    # return render_template('play.html')
    # attempts = int(request.form.get('attempts'))
    return render_template('play.html', feedback="", attempts=8, secret_word=random_player.player_name, guess="", guess_history=guess_history)

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global guess_history, correct, attempts, guess_feedbacks, random_player
    attempts = 8
    guess_feedbacks.clear()
    guess_history.clear()  # Clear the guess_history list
    correct = False
    random_player = PlayerInfo.query.order_by(func.random()).first()
    print(random_player)
    flash("Game reset successfully!")
    return redirect(url_for('play'))

@app.route('/leaderboard')
def leaderboard():
    if 'username' not in session:
        flash("Please log in to view the leaderboard.")
        return redirect(url_for('login'))
    # Get global leaderboard data
    global_leaderboard = User.query.order_by(User.wins.desc()).limit(10).all()

    # Get local leaderboard for the current user (you may use authentication for this)
    # Assuming the current user's username is available in the session
    username = session.get('username')
    local_leaderboard = User.query.filter_by(username=username).first()

    return render_template('leaderboard.html', global_leaderboard=global_leaderboard, local_leaderboard=local_leaderboard)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)