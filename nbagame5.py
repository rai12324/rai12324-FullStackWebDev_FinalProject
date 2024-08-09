import random
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from flask import Flask, render_template, request, flash, redirect, url_for,session,redirect
from colored import fg, bg, attr
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash 

# from your_application_file import db
app = Flask("Basketball")
app.secret_key = 'wowsect'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///slam.db'
db = SQLAlchemy(app)

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
    jersey = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)

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
player_list = players.get_active_players()
player_names = []
for x in player_list:
    player_names.append(list(x.values())[1].lower())

# Your other functions go here...
count = 0
west = ["Nuggets","Timberwolves","Blazers","Thunder","Jazz","Warriors","Clippers","Lakers","Suns", "Kings", "Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs"]
east = ["Celtics","Nets","Knicks","76ers","Raptors","Cavaliers","Bulls","Pistons","Pacers","Bucks","Hawks","Hornets","Heat","Magic","Wizards"]
atlantic = ["Celtics","Nets","Knicks","76ers","Raptors"]
central = ["Cavaliers","Bulls","Pistons","Pacers","Bucks"]
southeast = ["Hawks","Hornets","Heat","Magic","Wizards"]
northwest = ["Nuggets","Timberwolves","Blazers","Thunder","Jazz"]
pacific = ["Warriors","Clippers","Lakers","Suns", "Kings"]
southwest = ["Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs"]

# Store the selected player's information in a variable
# #print(player_dict)
# # random.shuffle(player_dict)
# # player_dict = player_dict.pop()
# for x in player_dict:
#     # print(x['id'])
#     player_info = commonplayerinfo.CommonPlayerInfo(player_id=x['id'])
#     player_info = player_info.get_normalized_dict()
#     for x in player_info:
#         if(x == "CommonPlayerInfo"):
#             value = player_info[x]
#             for dict in value:
#                 for key,val in dict.items():
#                     if(key == "JERSEY"):
#                         num = "no"
#                         while(val):
#                             num = val
#                         print(val)
#                         jersey.append(num)
# print(jersey)
current_player_info = {}
guess_history = []
jersey = []
player_dict = players.get_active_players()
player_info = commonplayerinfo.CommonPlayerInfo(player_id='2544')
player_info = player_info.get_normalized_dict()
conference = "West"
# print(player_dict)
for x in player_info:
    if(x == "CommonPlayerInfo"):
        value = player_info[x]
        #print(value)
        for dict in value:
            for key,val in dict.items():
                if(key == "HEIGHT"):
                    height = (val)
                    feet = int(height[0])
                    for x in range(2,len(height)):
                        inches = int(height[x])
                    height = feet*12+inches
                if(key == "DISPLAY_FIRST_LAST"):
                    name = val
                if(key == "POSITION"):
                    pos = val
                if(key == "JERSEY"):
                    num = int(val)
                if(key == "TEAM_NAME"):
                    team = val
print(type(feet))
print(type(inches))
print(type(num))
print((height))
print(num)

def initialize_game():
    global current_player_info  # Use the global variable

    player_dict = players.get_active_players()
    #print(player_dict)
    random.shuffle(player_dict)
    player_dict = player_dict.pop()
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_dict['id'])
    player_info = player_info.get_normalized_dict()
    conference = "West"
    for x in player_info:
        if(x == "CommonPlayerInfo"):
            value = player_info[x]
            #print(value)
            for dict in value:
                for key,val in dict.items():
                    if(key == "HEIGHT"):
                        height = (val)
                        feet = int(height[0])
                        for x in range(2,len(height)):
                            inches = int(height[x])
                        print(feet)
                        print(inches)
                        compare = feet*12+inches
                    if(key == "DISPLAY_FIRST_LAST"):
                        name = val
                    if(key == "POSITION"):
                        pos = val
                    if(key == "JERSEY"):
                        num = int(val)
                        # if(len(num)>0):
                        #     num = int(val)
                    if(key == "TEAM_NAME"):
                        team = val
            if(team in east):
                conference = "East"
                if(team in atlantic):
                    div = "Atl."
                elif(team in central):
                    div = "Cen."
                else:
                    div = "SE"
            else:
                if(team in pacific):
                    div = "Pac."
                elif(team in northwest):
                    div = "NW"
                else:
                    div = "SW"

    current_player_info = {"Name":name, "Team": team, "Conference": conference, "Division": div, "Position": pos, "Height" : height, "CompareHeight" : compare, "Jersey Number": num}
    guess_history.clear()
    return current_player_info
initialize_game()
def get_user_input():
    return input("Enter your guess ").lower()

def validate_input(guess):
    #playerList = players.get_players()
    #print(player_names)
    if guess not in player_names:
        print("Invalid input. Please enter a NBA Player")
        return False
    return True

def provide_feedback(answer_dict, guess):
    feedback = ""
    feedback_parts = []
    for x in player_list:
        if((list(x.values())[1].lower()) == guess):
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=list(x.values())[0])
            player_info = player_info.get_normalized_dict()
            break
    conference = "West"
    for x in player_info:
        if(x == "CommonPlayerInfo"):
            value = player_info[x]
            inches_guess = ""
            #print(value)
            for dict in value:
                for key,val in dict.items():
                    if(key == "HEIGHT"):
                        height = (val)
                        feet_guess = int(height[0])
                        for x in range(2,len(height)):
                            inches_guess += str(height[x])
                        print(feet_guess)
                        print(inches_guess)
                        compare = feet_guess*12+int(inches_guess)
                    if(key == "DISPLAY_FIRST_LAST"):
                        name = val
                    if(key == "POSITION"):
                        pos = val
                    if(key == "JERSEY"):
                        num = int(val)
                    if(key == "TEAM_NAME"):
                        team = val
            if(team in east):
                conference = "East"
                if(team in atlantic):
                    div = "Atl."
                elif(team in central):
                    div = "Cen."
                else:
                    div = "SE"
            else:
                if(team in pacific):
                    div = "Pac."
                elif(team in northwest):
                    div = "NW"
                else:
                    div = "SW"
    if answer_dict['Name'].lower() == guess.lower():
        feedback_parts.append(("correct", name))
    else:
        feedback_parts.append(("incorrect", name))

    if answer_dict['Team'] == team:
        feedback_parts.append(("correct", team))
        # print(team)
    else:
        feedback_parts.append(("incorrect", team))
        # print(team)

    if answer_dict['Conference'] == conference:
        feedback_parts.append(("correct", conference))
        # print(conference)
    else:
        feedback_parts.append(("incorrect", conference))
        # print(conference)

    if answer_dict['Division'] == div:
        feedback_parts.append(("correct", div))
    else:
        feedback_parts.append(("incorrect", div))

    if answer_dict['Position'] == pos:
        feedback_parts.append(("correct", pos))
    elif answer_dict['Position'] in pos :
        feedback_parts.append(("closeh", pos)) 
    else:
        feedback_parts.append(("incorrect", pos))

    if answer_dict['CompareHeight'] == compare:
        feedback_parts.append(("correct", height))
    elif(0 < ((answer_dict['CompareHeight']) - compare) <= 2):
        feedback_parts.append(("closeh", height))
        print((answer_dict['CompareHeight']) - compare)
    elif(-2 <= ((answer_dict['CompareHeight']) - compare) < 0):
        feedback_parts.append(("closel", height))
        print((answer_dict['CompareHeight']) - compare)
    else:
        feedback_parts.append(("incorrect", height))
        print("too big")
    if answer_dict['Jersey Number'] == num:
        feedback_parts.append(("correct", num))
        print(num)
    elif(0 < (answer_dict['Jersey Number'] - num) <= 2):
        print((answer_dict['Jersey Number'] - num))
        feedback_parts.append(("closeh", num))
        print(num)
    elif(-2 <= (answer_dict['Jersey Number'] - num) < 0):
        print((answer_dict['Jersey Number'] - num))
        feedback_parts.append(("closel", num))
        print(num)
    else:
        feedback_parts.append(("incorrect", num))
        print(num)

    #feedback = ' '.join(feedback_parts)
    for part in feedback_parts:
        status, value = part
        feedback += f'<span class="{ "correct-guess" if status == "correct" else "closel-guess" if status == "closel" else "closeh-guess" if status == "closeh" else "incorrect-guess" }">{value}</span> '

    return feedback.strip(), feedback_parts

def feedback_print(current_player_info,guess):
    feedback = provide_feedback(current_player_info, guess)
    print("Feedback:", feedback)
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
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            flash("Login successful!")
            return redirect(url_for('play'))

        flash("Invalid username or password. Please try again.")
        return redirect(url_for('login'))

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))

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

@app.route('/')
def home():
    return "Welcome to Slamordle!"  # Replace this with your homepage content

attempts = 8
guess_history = []  # Move this outside the play function and make it global
guess_feedbacks = []
correct = False
# def is_guess_repeated(guess, guess_history):
#     return any(entry['guess'] == guess for entry in guess_history)
@app.route('/reset_game', methods=['POST'])
@app.route('/reset_game', methods=['POST'])
def reset_game():
    global guess_history, correct, attempts, guess_feedbacks, current_player_info
    attempts = 8
    guess_feedbacks.clear()
    guess_history.clear()  # Clear the guess_history list
    initialize_game()
    correct = False
    return redirect(url_for('play'))  # Redirect to the '/play' route
@app.route('/play', methods=['GET', 'POST'])
def play():
    global current_player_info, guess_history, guess_feedbacks, correct, attempts
    guess_feedbacks = []
    secret_word = current_player_info.get('Name', '')
    print(current_player_info)
    if 'username' not in session:
        flash("Please log in to play.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'reset' in request.form:
            correct = False
            return redirect(url_for('reset_game'))
        guess = request.form.get('guess').lower()
        if not validate_input(guess):
            flash("Invalid input. Please enter an NBA Player.")
            return render_template('play.html', feedback="", attempts=8, secret_word=secret_word, guess="", guess_history=guess_history)
        feedback, feedback_parts = provide_feedback(current_player_info, guess)
        print(feedback_parts)
        print(feedback)
        guess_feedbacks.append({"guess": guess, "feedback_parts": feedback_parts})
        guess_history.append({"guess": guess, "feedback": feedback_parts})  # Store the feedback as a list of tuples

        attempts = int(request.form.get('attempts'))
        attempts -= 1
        if guess.lower() == secret_word.lower():
            if attempts == 0:
                correct = True
                username = session.get('username')
                user = User.query.filter_by(username=username).first()
                if user:
                    user.wins += 1
                    db.session.commit()
                return render_template('play_again.html', correct=True, secret_word=secret_word)

            elif attempts == 0:
                correct = True
                username = session.get('username')
                user = User.query.filter_by(username=username).first()
                if user:
                    user.attempts += 1
                    db.session.commit()
                return render_template('play_again.html', correct=False, secret_word=secret_word)

        else:
            correct = False  # Reset correct to False after processing the guess
            return render_template('play.html', feedback_parts=feedback_parts, attempts=attempts, secret_word=secret_word,
                                correct=False, guess_history=guess_history, guess_feedbacks=guess_feedbacks)  # Pass the feedback to the template

    # If it's a GET request (initial load), set the attempts to 8
    return render_template('play.html', feedback="", attempts=8, secret_word=secret_word, guess="", guess_history=guess_history)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)