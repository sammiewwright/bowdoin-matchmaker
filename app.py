from flask import Flask, render_template, request
from user_profile import Profile
from matcher import Matcher
import random
import time

app = Flask(__name__)

fun_fact = random.choice([
    "Opposites attract!",
    "Shared interests matter most!",
    "Music taste says a lot about compatibility!"
])
current_time = time.ctime()

def load_profiles():
    profiles_list = []

    try:
        with open("profiles.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")

                if len(data) == 10:
                    profile = Profile(
                        data[0], data[1], int(data[2]),
                        data[3], data[4], data[5],
                        data[6], data[7], data[8], data[9]
                    )
                    profiles_list.append(profile)

    except FileNotFoundError:
        pass

    return profiles_list


profiles = load_profiles()


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    global profiles

    try:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        age = int(request.form["age"])
        gender = request.form["gender"]
        preferred_gender = request.form["preferred_gender"]
        interest1 = request.form["interest1"]
        interest2 = request.form["interest2"]
        music_type = request.form["music_type"]
        hometown = request.form["hometown"]
        goal = request.form["goal"]

    except ValueError:
        return "Age must be a number!"

    except KeyError:
        return "Missing form data!"

    if interest1 == interest2:
        return "Choose two different interests!"

    profile = Profile(first_name, last_name, age, gender, preferred_gender, interest1, interest2, music_type, hometown, goal)

    # loads existing profiles before matching
    profiles = load_profiles()
    matcher = Matcher(profiles)
    matches = matcher.find_matches(profile)

    # save new profile
    with open("profiles.txt", "a") as file:
        file.write(f"{first_name},{last_name},{age},{gender},{preferred_gender},"
                   f"{interest1},{interest2},{music_type},{hometown},{goal}\n")

    # save match results
    with open("matches.txt", "a") as file:
        if matches:
            for p, score in matches:
                file.write(f"{profile.first_name} matched with {p.first_name} ({score})\n")
        else:
            file.write(f"{profile.first_name} had no good matches yet\n")

    # reload profiles so app has updated list
    profiles = load_profiles()

    return render_template("matches.html", matches=matches, user=profile)


@app.route("/profiles")
def show_profiles():
    global profiles
    profiles = load_profiles()

    return {
        "profiles": [
            {
                "name": f"{p.first_name} {p.last_name}",
                "age": p.age,
                "gender": p.gender,
                "preferred_gender": p.preferred_gender,
                "interests": list(p.get_interests()),
                "music_type": p.music_type,
                "hometown": p.hometown,
                "goal": p.goal
            }
            for p in profiles
        ]
    }


@app.route("/match/<int:index>")
def match(index):
    global profiles
    profiles = load_profiles()

    if index < 0 or index >= len(profiles):
        return {"error": "Invalid profile index"}, 404

    target = profiles[index]

    matcher = Matcher(profiles)
    matches = matcher.find_matches(target)

    total = matcher.count_matches(matches)

    return {
        "total_matches": total,
        "matches": [
            {"name": f"{p.first_name} {p.last_name}", "score": score}
            for p, score in matches
        ]
    }

@app.route("/check")
def check():
    return render_template("check.html")


@app.route("/check_matches", methods=["POST"])
def check_matches():
    profiles = load_profiles()

    first_name = request.form["first_name"].strip()
    last_name = request.form["last_name"].strip()
    hometown = request.form["hometown"].strip()

    user = None
    for profile in profiles:
        if (
            profile.first_name.lower() == first_name.lower()
            and profile.last_name.lower() == last_name.lower()
            and profile.hometown.lower() == hometown.lower()
        ):
            user = profile
            break

    if not user:
        return "Profile not found. Please sign up first."

    matcher = Matcher(profiles)
    matches = matcher.find_matches(user)

    return render_template("matches.html", matches=matches, user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
    
