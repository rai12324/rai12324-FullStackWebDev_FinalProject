# import random
# import json
# from nba_api.stats.static import players
# from nba_api.stats.endpoints import commonplayerinfo
# from flask import Flask, render_template, request, flash
# from colored import fg, bg, attr

# app = Flask("Basketball")
# app.secret_key = 'wowsect'
# player_list = players.get_active_players()
# player_names = []
# player_names = [list(x.values())[1].lower() for x in player_list]

# # for x in player_list:
# #     player_names.append(list(x.values())[1].lower())

# # Your other functions go here...
# count = 0
# west = ["Nuggets","Timberwolves","Blazers","Thunder","Jazz","Warriors","Clippers","Lakers","Suns", "Kings", "Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs"]
# east = ["Celtics","Nets","Knicks","76ers","Raptors","Cavaliers","Bulls","Pistons","Pacers","Bucks","Hawks","Hornets","Heat","Magic","Wizards"]
# atlantic = ["Celtics","Nets","Knicks","76ers","Raptors"]
# central = ["Cavaliers","Bulls","Pistons","Pacers","Bucks"]
# southeast = ["Hawks","Hornets","Heat","Magic","Wizards"]
# northwest = ["Nuggets","Timberwolves","Blazers","Thunder","Jazz"]
# pacific = ["Warriors","Clippers","Lakers","Suns", "Kings"]
# southwest = ["Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs"]

# # Store the selected player's information in a variable
# current_player_info = {}
# guess_history = []

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
#                         height = val
#                     if(key == "DISPLAY_FIRST_LAST"):
#                         name = val
#                     if(key == "POSITION"):
#                         pos = val
#                     if(key == "JERSEY"):
#                         num = val
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

#     current_player_info = {"Name":name, "Team": team, "Conference": conference, "Division": div, "Position": pos, "Height" : height, "Jersey Number": num}
#     #guess_history.clear()
#     #return current_player_info
# initialize_game()
# def get_user_input():
#     return input("Enter your guess ").lower()

# def validate_input(guess):
#     #playerList = players.get_players()
#     #print(player_names)
#     if guess not in player_names:
#         print("Invalid input. Please enter a NBA Player")
#         return False
#     return True

# def provide_feedback(answer_dict, guess):
#     feedback = ""
#     feedback_parts = []
#     for x in player_list:
#         if((list(x.values())[1].lower()) == guess):
#             player_info = commonplayerinfo.CommonPlayerInfo(player_id=list(x.values())[0])
#             player_info = player_info.get_normalized_dict()
#             break
#     conference = "West"
#     for x in player_info:
#         if(x == "CommonPlayerInfo"):
#             value = player_info[x]
#             #print(value)
#             for dict in value:
#                 for key,val in dict.items():
#                     if(key == "HEIGHT"):
#                         height = val
#                     if(key == "DISPLAY_FIRST_LAST"):
#                         name = val
#                     if(key == "POSITION"):
#                         pos = val
#                     if(key == "JERSEY"):
#                         num = val
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
#     if answer_dict['Name'].lower() == guess.lower():
#         feedback_parts.append(("correct", name))
#     else:
#         feedback_parts.append(("incorrect", name))

#     if answer_dict['Team'] == team:
#         feedback_parts.append(("correct", team))
#         print(team)
#     else:
#         feedback_parts.append(("incorrect", team))
#         print(team)

#     if answer_dict['Conference'] == conference:
#         feedback_parts.append(("correct", conference))
#         print(conference)
#     else:
#         feedback_parts.append(("incorrect", conference))
#         print(conference)

#     if answer_dict['Division'] == div:
#         feedback_parts.append(("correct", div))
#     else:
#         feedback_parts.append(("incorrect", div))

#     if answer_dict['Position'] == pos:
#         feedback_parts.append(("correct", pos))
#     else:
#         feedback_parts.append(("incorrect", pos))

#     if answer_dict['Height'] == height:
#         feedback_parts.append(("correct", height))
#     elif((answer_dict['Height']) > (num)):
#         feedback_parts.append(("incorrect", height))
#     else:
#         feedback_parts.append(("incorrect", height))

#     if answer_dict['Jersey Number'] == num:
#         feedback_parts.append(("correct", num))
#         print(num)
#     elif((answer_dict['Jersey Number']) > (num)):
#         feedback_parts.append(("incorrect", num))
#         print(num)
#     else:
#         feedback_parts.append(("incorrect", num))
#         print(num)

#     #feedback = ' '.join(feedback_parts)
#     for part in feedback_parts:
#         status, value = part
#         feedback += f'<span class="{"correct-guess" if status == "correct" else "incorrect-guess"}">{value}</span> '

#     return feedback.strip(), feedback_parts

# def feedback_print(current_player_info,guess):
#     feedback = provide_feedback(current_player_info, guess)
#     print("Feedback:", feedback)

# @app.route('/')
# def home():
#     return "Welcome to Slamordle!"  # Replace this with your homepage content

# attempts = 8
# guess_history = []  # Move this outside the play function and make it global
# guess_feedbacks = []
# correct = False
# # def is_guess_repeated(guess, guess_history):
# #     return any(entry['guess'] == guess for entry in guess_history)
# @app.route('/reset_game', methods=['POST'])
# def reset_game():
#     global guess_history,correct,attempts,guess_feedbacks,current_player_info
#     attempts = 8
#     guess_feedbacks.clear()
#     guess_history.clear() # Clear the guess_history list
#     initialize_game()
#     correct = False
#     return 'Game reset', 200
# @app.route('/play', methods=['GET', 'POST'])
# def play():
#     global current_player_info, guess_history, guess_feedbacks, correct, attempts
#     guess_feedbacks = []
#     filtered_player_names = []
#     secret_word = current_player_info.get('Name', '')
#     print(current_player_info)

#     if request.method == 'POST':
#         if 'reset' in request.form:
#             correct = False
#             filtered_player_names = [name for name in player_names if name is not Undefined]
#             return render_template('play.html', feedback="", attempts=8, secret_word=current_player_info.get('Name', ''),
#                                guess="", guess_history=guess_history,player_names = json.dump(filtered_player_names))
#         guess = request.form.get('guess').lower()
#         if not validate_input(guess):
#             flash("Invalid input. Please enter an NBA Player.")
#             return render_template('play.html', feedback="", attempts=8, secret_word=secret_word, guess="", guess_history=guess_history)
#         feedback, feedback_parts = provide_feedback(current_player_info, guess)
#         print(feedback_parts)
#         print(feedback)
#         guess_feedbacks.append({"guess": guess, "feedback_parts": feedback_parts})
#         guess_history.append({"guess": guess, "feedback": feedback_parts})  # Store the feedback as a list of tuples

#         attempts = int(request.form.get('attempts'))
#         attempts -= 1
#         if guess.lower() == secret_word.lower():
#             if attempts == 0:
#                 flash("Congratulations! You guessed the player correctly: {}".format(secret_word))
#                 correct = True  # Set correct to True
#                 return render_template('play.html', feedback_parts=feedback_parts, attempts=0, secret_word=secret_word,
#                                     correct=True, game_over=True, guess_history=guess_history, guess_feedbacks=guess_feedbacks)  # Pass the feedback to the template
#             else:
#                 flash("Congratulations! You guessed the player correctly: {}".format(secret_word))
#                 correct = True  # Set correct to True
#                 return render_template('play.html', feedback_parts=feedback_parts, attempts=0, secret_word=secret_word,
#                                     correct=True, guess_history=guess_history, guess_feedbacks=guess_feedbacks)  # Pass the feedback to the template

#         elif attempts == 0:
#             guess_history.append({"guess": guess, "feedback": feedback_parts})  # Append the current guess on game over
#             flash("Sorry, you've run out of attempts. The correct player was: {}".format(secret_word))
#             correct = False  # Reset correct to False after processing the guess
#             return render_template('play.html', feedback_parts=feedback_parts, attempts=0, secret_word=secret_word,
#                                 correct=False, game_over=True, guess_history=guess_history, guess_feedbacks=guess_feedbacks)  # Pass the feedback to the template

#         else:
#             correct = False  # Reset correct to False after processing the guess
#             return render_template('play.html', feedback_parts=feedback_parts, attempts=attempts, secret_word=secret_word,
#                                 correct=False, guess_history=guess_history, guess_feedbacks=guess_feedbacks)  # Pass the feedback to the template

#     # If it's a GET request (initial load), set the attempts to 8
#     return render_template('play.html', feedback="", attempts=8, secret_word=secret_word, guess="", guess_history=guess_history)


# if __name__ == "__main__":
#     app.run(debug=True)

import random
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from flask import Flask, render_template, request
from colored import fg,bg,attr

app = Flask("Basketball")
player_list = players.get_active_players()
player_names = []
for x in player_list:
    player_names.append(list(x.values())[1].lower())
count = 0
west = ["Nuggets","Timberwolves","Blazers","Thunder","Jazz","Warriors","Clippers","Lakers","Suns", "Kings", "Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs"]
east = ["Celtics","Nets","Knicks","76ers","Raptors","Cavaliers","Bulls","Pistons","Pacers","Bucks","Hawks","Hornets","Heat","Magic","Wizards"]
atlantic = ["Celtics","Nets","Knicks","76ers","Raptors"]
central = ["Cavaliers","Bulls","Pistons","Pacers","Bucks"]
southeast = ["Hawks","Hornets","Heat","Magic","Wizards"]
northwest = ["Nuggets","Timberwolves","Blazers","Thunder","Jazz"]
pacific = ["Warriors","Clippers","Lakers","Suns", "Kings"]
southwest = ["Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs"]
def initialize_game():
    
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
                        height = val
                    if(key == "DISPLAY_FIRST_LAST"):
                        name = val
                    if(key == "POSITION"):
                        pos = val
                    if(key == "JERSEY"):
                        num = val
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
            # print(height)
            # print(name)
            # print(pos)
            # print(num)
            # print(team)
            # print(conference)
    answer_dict = {"Name":name, "Team": team, "Conference": conference, "Division": div, "Position": pos, "Height" : height, "Jersey Number": num}
    return answer_dict
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
    for x in player_list:
        if((list(x.values())[1].lower()) == guess):
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=list(x.values())[0])
            player_info = player_info.get_normalized_dict()
    conference = "West"
    for x in player_info:
        if(x == "CommonPlayerInfo"):
            value = player_info[x]
            #print(value)
            for dict in value:
                for key,val in dict.items():
                    if(key == "HEIGHT"):
                        height = val
                    if(key == "DISPLAY_FIRST_LAST"):
                        name = val
                    if(key == "POSITION"):
                        pos = val
                    if(key == "JERSEY"):
                        num = val
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

    if(answer_dict['Name'] == name):
        feedback += bg("green") + fg("black") + name + " " + attr(0)
    else:
        feedback += bg("red") + fg("black") + name + " " + attr(0)
    if(answer_dict['Team'] == team):
        feedback += bg("green") + fg("black") + team + " " + attr(0)
    else:
        feedback += bg("red") + fg("black") + team + " " + attr(0)
    if(answer_dict['Conference'] == conference):
        feedback += bg("green") + fg("black") + conference + " " + attr(0)
    else:
        feedback += bg("red") + fg("black") + conference + " " + attr(0)
    if(answer_dict['Division'] == div):
        feedback += bg("green") + fg("black") + div + " " + attr(0)
    else:
        feedback += bg("red") + fg("black") + div + " " + attr(0)
    if(answer_dict['Position'] == pos):
        feedback += bg("green") + fg("black") + pos + " " + attr(0)
    else:
        feedback += bg("red") + fg("black") + pos + " " + attr(0)
    if(answer_dict['Height'] == height):
        feedback += bg("green") + fg("black") + height + " " + attr(0)
    elif(answer_dict['Height'] > height):
        feedback += bg("red") + fg("black") + height + " higher " + attr(0)
    elif(answer_dict['Height'] < height):
        feedback += bg("red") + fg("black") + height + " lower " + attr(0)
    if(int(answer_dict['Jersey Number']) == int(num)):
        print(answer_dict['Jersey Number'])
        feedback += bg("green") + fg("black") + num + " " + attr(0)
    elif(int(answer_dict['Jersey Number']) > int(num)):
        print(answer_dict['Jersey Number'])
        feedback += bg("red") + fg("black") + num + " higher " + attr(0)
    elif(int(answer_dict['Jersey Number']) < int(num)):
        print(answer_dict['Jersey Number'])
        feedback += bg("red") + fg("black") + num + " lower " + attr(0)
    return feedback
def feedback_print(secret_dict,guess):
    feedback = provide_feedback(secret_dict, guess)
    print("Feedback:", feedback)
def wrong_print(secret_dict):
    feedback = ""
    feedback+= bg("red") + fg("black") + secret_dict["Name"] + " " + attr(0)
    feedback+= bg("red") + fg("black") + secret_dict["Team"] + " " + attr(0)
    feedback+= bg("red") + fg("black") + secret_dict["Conference"] + " " + attr(0)
    feedback+= bg("red") + fg("black") + secret_dict["Position"] + " " + attr(0)
    feedback+= bg("red") + fg("black") + secret_dict["Height"] + " " + attr(0)
    feedback+= bg("red") + fg("black") + secret_dict["Jersey Number"] + " " + attr(0)
    print("Feedback:" , feedback)

def main():
    #print("Welcome to Slamordle!")
    secret_dict = initialize_game()
    secret_word = secret_dict['Name']
    print(secret_word)
    attempts = 8

    while attempts > 0:
        guess = get_user_input().lower()

        if not validate_input(guess):
            continue

        if guess.lower() == secret_word.lower():
            feedback_print(secret_dict,guess)
            print("Congratulations! You guessed the word!")
            break
        else:
            attempts -= 1
            feedback_print(secret_dict,guess)
            print(f"Attempts remaining: {attempts}")

    if attempts == 0:
        wrong_print(secret_dict)
        print("Game over! The secret word was:", secret_word)
@app.route('/')
def home():
    return "Welcome to Slamordle!"  # Replace this with your homepage content

@app.route('/play', methods=['GET', 'POST'])
def play():
    secret_dict = initialize_game()
    secret_word = secret_dict['Name']

    if request.method == 'POST':
        guess = request.form.get('guess').lower()
        if not validate_input(guess):
            return render_template('play.html', feedback="Invalid input. Please enter a NBA Player.", attempts=8, secret_word=secret_word, guess="")
        
        if guess.lower() == secret_word.lower():
            feedback = provide_feedback(secret_dict, guess)
            return render_template('play.html', feedback=feedback, attempts=0, secret_word=secret_word, guess=guess, correct=True)
        else:
            attempts = int(request.form.get('attempts'))
            attempts -= 1
            feedback = provide_feedback(secret_dict, guess)
            return render_template('play.html', feedback=feedback, attempts=attempts, secret_word=secret_word, guess=guess, correct=False)

    return render_template('play.html', feedback="", attempts=8, secret_word="", guess="")

if __name__ == "__main__":
    app.run(debug=True)