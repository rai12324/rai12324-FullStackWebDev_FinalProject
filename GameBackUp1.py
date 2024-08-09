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

guess_history = []

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

##################################################################################
# def initialize_game():
#     global current_player_info  # Use the global variable

#     player_dict = players.get_active_players()
#     #print(player_dict)
#     random.shuffle(player_dict)
#     player_dict = player_dict.pop()
#     player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_dict['id'])
#     player_info = player_info.get_normalized_dict()
#     conference = "West"
#     for x in player_info:
#         if(x == "CommonPlayerInfo"):
#             value = player_info[x]
#             #print(value)
#             for dict in value:
#                 for key,val in dict.items():
#                     if(key == "HEIGHT"):
#                         height = (val)
#                         feet = int(height[0])
#                         for x in range(2,len(height)):
#                             inches = int(height[x])
#                         print(feet)
#                         print(inches)
#                         compare = feet*12+inches
#                     if(key == "DISPLAY_FIRST_LAST"):
#                         name = val
#                     if(key == "POSITION"):
#                         pos = val
#                     if(key == "JERSEY"):
#                         num = int(val)
#                         # if(len(num)>0):
#                         #     num = int(val)
#                     if(key == "TEAM_NAME"):
#                         team = val
#             if(team in east):
#                 conference = "East"
#                 if(team in atlantic):
#                     div = "Atl."
#                 elif(team in central):
#                     div = "Cen."
#                 else:
#                     div = "SE"
#             else:
#                 if(team in pacific):
#                     div = "Pac."
#                 elif(team in northwest):
#                     div = "NW"
#                 else:
#                     div = "SW"

#     current_player_info = {"Name":name, "Team": team, "Conference": conference, "Division": div, "Position": pos, "Height" : height, "CompareHeight" : compare, "Jersey Number": num}
#     guess_history.clear()
#     return current_player_info
# initialize_game()
# def get_user_input():
#     return input("Enter your guess ").lower()

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

    if height_rando == height_guess:
        feedback_parts.append(("correct", f"{height_guess}"))
    elif 0 < (height_rando - height_guess) <= 2:
        feedback_parts.append(("closeh", f"{height_guess}"))
    elif -2 <= (height_rando - height_guess) < 0:
        feedback_parts.append(("closel", f"{height_guess}"))
    else:
        feedback_parts.append(("incorrect", f"{height_guess}"))

    if random_info["NAME"].lower() == guess_info["NAME"].lower():
        feedback_parts.append(("correct", guess_info["NAME"]))
    else:
        feedback_parts.append(("incorrect", guess_info["NAME"]))

    if random_info["JERSEY"] == guess_info["JERSEY"]:
        feedback_parts.append(("correct", f"{guess_info['JERSEY']}"))
    elif 0 < (random_info["JERSEY"] - guess_info["JERSEY"]) <= 2:
        feedback_parts.append(("closeh", f"{guess_info['JERSEY']}"))
    elif -2 <= (random_info["JERSEY"] - guess_info["JERSEY"]) < 0:
        feedback_parts.append(("closel", f"{guess_info['JERSEY']}"))
    else:
        feedback_parts.append(("incorrect", f"{guess_info['JERSEY']}"))

    if random_info["POSITION"] == guess_info["POSITION"]:
        feedback_parts.append(("correct", guess_info["POSITION"]))
    elif random_info["POSITION"] in guess_info["POSITION"]:
        feedback_parts.append(("closeh", guess_info["POSITION"])) 
    else:
        feedback_parts.append(("incorrect", guess_info["POSITION"]))

    if random_info["TEAM"] == guess_info["TEAM"]:
        feedback_parts.append(("correct", guess_info["TEAM"]))
    else:
        feedback_parts.append(("incorrect", guess_info["TEAM"]))

    if random_info["CONFERENCE"] == guess_info["CONFERENCE"]:
        feedback_parts.append(("correct", guess_info["CONFERENCE"]))
    else:
        feedback_parts.append(("incorrect", guess_info["CONFERENCE"]))

    if random_info["DIV"] == guess_info["DIV"]:
        feedback_parts.append(("correct", guess_info["DIV"]))
    else:
        feedback_parts.append(("incorrect", guess_info["DIV"]))

    feedback = ""
    for part in feedback_parts:
        status, value = part
        feedback += f'<span class="{ "correct-guess" if status == "correct" else "closel-guess" if status == "closel" else "closeh-guess" if status == "closeh" else "incorrect-guess" }">{value}</span> '

    return feedback.strip(), feedback_parts




# def provide_feedback(guess):
#     guess_val =  PlayerInfo.query.filter_by(player_name=guess).first()
#     random_val = PlayerInfo.query.filter_by(player_name = random_player.player_name).first()

#     if guess_val is None:
#         return "Player not found in the database", []
    
#     feedback = ""
#     feedback_parts = []
#     guess_info = {}
#     random_info = {}
#     guess_info["NAME"] = guess_val.player_name
#     guess_info['player_id'] = guess_val.player_id
#     guess_info["HEIGHT"] = guess_val.height
#     guess_info["POSITION"] = guess_val.position
#     guess_info["JERSEY"] = guess_val.jersey
#     guess_team = TeamInfo.query.filter_by(team_id = guess_val.team_id).first()
#     guess_info["TEAM"] = guess_team.team_name
#     guess_info["CONFERENCE"] = guess_team.conference
#     guess_info["DIV"] = guess_team.division
#     random_info["NAME"] = random_val.player_name
#     random_info['player_id'] = random_val.player_id
#     random_info["HEIGHT"] = random_val.height
#     random_info["POSITION"] = random_val.position
#     random_info["JERSEY"] = random_val.jersey
#     random_team = TeamInfo.query.filter_by(team_id = random_val.team_id).first()
#     random_info["TEAM"] = random_team.team_name
#     random_info["CONFERENCE"] = random_team.conference
#     random_info["DIV"] = random_team.division
#     print(random_info)
#     print(guess_info)
#     # for x in player_list:
#     #     if((list(x.values())[1].lower()) == guess):
#     #         player_info = commonplayerinfo.CommonPlayerInfo(player_id=list(x.values())[0])
#     #         player_info = player_info.get_normalized_dict()
#     #         break
#     # conference = "West"
#     inches_guess = ""
#     # for key in guess_info:
#     #     if(key == "HEIGHT"):
#     #         height = ()
#     inches_rando = ""

#     foot_rando = random_info["HEIGHT"][0]
#     for x in range(2,len( random_info["HEIGHT"])):
#         inches_rando +=  random_info["HEIGHT"][x]
#     height_rando = int(foot_rando)*12+int(inches_rando)
#     print("rando h" + str(height_rando))
#     foot_guess = guess_info["HEIGHT"][0]
#     for x in range(2,len( guess_info["HEIGHT"])):
#         inches_guess +=  guess_info["HEIGHT"][x]
#     height_guess = int(foot_guess)*12+int(inches_guess)
#     print("guess h" + str(height_guess))
#     if height_rando == height_guess:
#         feedback_parts.append(("correct", height_guess))
#     elif(0 < (height_rando - height_guess) <= 2):
#         feedback_parts.append(("closeh", height_guess))
#         print(height_rando - height_guess)
#     elif(-2 <= (height_rando - height_guess) < 0):
#         feedback_parts.append(("closel", height_guess))
#         print(height_rando - height_guess)
#     else:
#         feedback_parts.append(("incorrect", height_guess))
#         print("too big")
#     if random_info["NAME"].lower() == guess_info["NAME"].lower():
#         feedback_parts.append(("correct", guess_info["NAME"]))
#     else:
#         feedback_parts.append(("incorrect", guess_info["NAME"]))

#     if random_info["JERSEY"] == guess_info["JERSEY"]:
#         feedback_parts.append(("correct", guess_info["JERSEY"]))
#         print(guess_info["JERSEY"])
#     elif(0 < (random_info["JERSEY"] - guess_info["JERSEY"]) <= 2):
#         print((random_info["JERSEY"] - guess_info["JERSEY"]))
#         feedback_parts.append(("closeh", guess_info["JERSEY"]))
#         print(guess_info["JERSEY"])
#     elif(-2 <= (random_info["JERSEY"] - guess_info["JERSEY"]) < 0):
#         print(random_info["JERSEY"] - guess_info["JERSEY"])
#         feedback_parts.append(("closel", guess_info["JERSEY"]))
#         print(guess_info["JERSEY"])
#     else:
#         feedback_parts.append(("incorrect", guess_info["JERSEY"]))
#         print(guess_info["JERSEY"])
#     if random_info["POSITION"] == guess_info["POSITION"]:
#         feedback_parts.append(("correct", guess_info["POSITION"]))
#     elif random_info["POSITION"] in guess_info["POSITION"]:
#         feedback_parts.append(("closeh", guess_info["POSITION"])) 
#     else:
#         feedback_parts.append(("incorrect", guess_info["POSITION"]))
#     if random_info["TEAM"] == guess_info["TEAM"]:
#         feedback_parts.append(("correct", guess_info["TEAM"]))
#         print(guess_info["TEAM"])
#     else:
#         feedback_parts.append(("incorrect", guess_info["TEAM"]))
#         print(guess_info["TEAM"])

#     if random_info["CONFERENCE"] == guess_info["CONFERENCE"]:
#         feedback_parts.append(("correct", guess_info["CONFERENCE"]))
#         print(guess_info["CONFERENCE"])
#     else:
#         feedback_parts.append(("incorrect", guess_info["CONFERENCE"]))
#         print(guess_info["CONFERENCE"])

#     if random_info["DIV"] == guess_info["DIV"]:
#         feedback_parts.append(("correct", guess_info["DIV"]))
#         print(guess_info["DIV"])

#     else:
#         feedback_parts.append(("incorrect", guess_info["DIV"]))
#         print(guess_info["DIV"])


#     # if answer_dict['CompareHeight'] == compare:
#     #     feedback_parts.append(("correct", height))
#     # elif(0 < ((answer_dict['CompareHeight']) - compare) <= 2):
#     #     feedback_parts.append(("closeh", height))
#     #     print((answer_dict['CompareHeight']) - compare)
#     # elif(-2 <= ((answer_dict['CompareHeight']) - compare) < 0):
#     #     feedback_parts.append(("closel", height))
#     #     print((answer_dict['CompareHeight']) - compare)
#     # else:
#     #     feedback_parts.append(("incorrect", height))
#     #     print("too big")
# #  if answer_dict['Position'] == pos:
# #         feedback_parts.append(("correct", pos))
# #     elif answer_dict['Position'] in pos :
# #         feedback_parts.append(("closeh", pos)) 
# #     else:
# #         feedback_parts.append(("incorrect", pos))
# #     if answer_dict['Jersey Number'] == num:
# #         feedback_parts.append(("correct", num))
# #         print(num)
# #     elif(0 < (answer_dict['Jersey Number'] - num) <= 2):
# #         print((answer_dict['Jersey Number'] - num))
# #         feedback_parts.append(("closeh", num))
# #         print(num)
# #     elif(-2 <= (answer_dict['Jersey Number'] - num) < 0):
# #         print((answer_dict['Jersey Number'] - num))
# #         feedback_parts.append(("closel", num))
# #         print(num)
# #     else:
# #         feedback_parts.append(("incorrect", num))
# #         print(num)
            
#     #         for dict in value:
#     #             for key,val in dict.items():
#     #                 if(key == "HEIGHT"):
#     #                     height = (val)
#     #                     feet_guess = int(height[0])
#     #                     for x in range(2,len(height)):
#     #                         inches_guess += str(height[x])
#     #                     print(feet_guess)
#     #                     print(inches_guess)
#     #                     compare = feet_guess*12+int(inches_guess)
#     #                 if(key == "DISPLAY_FIRST_LAST"):
#     #                     name = val
#     #                 if(key == "POSITION"):
#     #                     pos = val
#     #                 if(key == "JERSEY"):
#     #                     num = int(val)
#     #                 if(key == "TEAM_NAME"):
#     #                     team = val
#     #         if(team in east):
#     #             conference = "East"
#     #             if(team in atlantic):
#     #                 div = "Atl."
#     #             elif(team in central):
#     #                 div = "Cen."
#     #             else:
#     #                 div = "SE"
#     #         else:
#     #             if(team in pacific):
#     #                 div = "Pac."
#     #             elif(team in northwest):
#     #                 div = "NW"
#     #             else:
#     #                 div = "SW"
#     # if answer_dict['Name'].lower() == guess.lower():
#     #     feedback_parts.append(("correct", name))
#     # else:
#     #     feedback_parts.append(("incorrect", name))

#     # if answer_dict['Team'] == team:
#     #     feedback_parts.append(("correct", team))
#     #     # print(team)
#     # else:
#     #     feedback_parts.append(("incorrect", team))
#     #     # print(team)

#     # if answer_dict['Conference'] == conference:
#     #     feedback_parts.append(("correct", conference))
#     #     # print(conference)
#     # else:
#     #     feedback_parts.append(("incorrect", conference))
#     #     # print(conference)

#     # if answer_dict['Division'] == div:
#     #     feedback_parts.append(("correct", div))
#     # else:
#     #     feedback_parts.append(("incorrect", div))

#     # if answer_dict['Position'] == pos:
#     #     feedback_parts.append(("correct", pos))
#     # elif answer_dict['Position'] in pos :
#     #     feedback_parts.append(("closeh", pos)) 
#     # else:
#     #     feedback_parts.append(("incorrect", pos))

#     # if answer_dict['CompareHeight'] == compare:
#     #     feedback_parts.append(("correct", height))
#     # elif(0 < ((answer_dict['CompareHeight']) - compare) <= 2):
#     #     feedback_parts.append(("closeh", height))
#     #     print((answer_dict['CompareHeight']) - compare)
#     # elif(-2 <= ((answer_dict['CompareHeight']) - compare) < 0):
#     #     feedback_parts.append(("closel", height))
#     #     print((answer_dict['CompareHeight']) - compare)
#     # else:
#     #     feedback_parts.append(("incorrect", height))
#     #     print("too big")
#     # if answer_dict['Jersey Number'] == num:
#     #     feedback_parts.append(("correct", num))
#     #     print(num)
#     # elif(0 < (answer_dict['Jersey Number'] - num) <= 2):
#     #     print((answer_dict['Jersey Number'] - num))
#     #     feedback_parts.append(("closeh", num))
#     #     print(num)
#     # elif(-2 <= (answer_dict['Jersey Number'] - num) < 0):
#     #     print((answer_dict['Jersey Number'] - num))
#     #     feedback_parts.append(("closel", num))
#     #     print(num)
#     # else:
#     #     feedback_parts.append(("incorrect", num))
#     #     print(num)
#     print(feedback_parts)
#     feedback = " ".join(feedback_parts)
#     for part in feedback_parts:
#         status, value = part
#         feedback += f'<span class="{ "correct-guess" if status == "correct" else "closel-guess" if status == "closel" else "closeh-guess" if status == "closeh" else "incorrect-guess" }">{value}</span> '

#     return feedback.strip(), feedback_parts

# def feedback_print(current_player_info,guess):
#     feedback = provide_feedback(current_player_info, guess)
#     print("Feedback:", feedback)
##################################################################################

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

        flash("Registration successful. Please log in.")
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

random_player = None  # Define random_player globally
guess_feedbacks = []  # Define guess_feedbacks globally

@app.route('/play', methods=['GET', 'POST'])
def play():
    global random_player, guess_feedbacks  # Add guess_feedbacks to the global scope

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
            return render_template('play.html', feedback="", attempts=8, secret_word=random_player.player_name, guess="", guess_history=guess_history)
        else:
            print("Guess: ", guess)
            feedback, feedback_parts = provide_feedback(guess)
            print("Temp", feedback_parts)
            guess_feedbacks.append({"guess": guess, "feedback_parts": feedback_parts})
            guess_history.append({"guess": guess, "feedback": feedback_parts})  # Store the feedback as a list of tuples

    return render_template('play.html')



if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)