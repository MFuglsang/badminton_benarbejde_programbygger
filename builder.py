import json
import random
from src import weeks_days as wd
from src import markdown as md

def read_configuration():
    with open('configuration.json', 'r') as f:
        config = json.load(f)
    return config

def read_trainings():
    with open('training.json', 'r', encoding='utf-8') as f:  # Added encoding='utf-8'
        config = json.load(f)
    return config

def read_players():
    with open('players.json', 'r') as f:
        config = json.load(f)
    return config

def get_n_exercises(training_list, count):
    selected = []
    while len(selected) < count:
        random_index = random.randint(0,len(training_list) - 1)
        elm = training_list[random_index]
        if elm not in selected:
            selected.append(elm)
    return selected

def select_unique_exercises_by_type(training_setup):
    """
    Select one exercise from each type (isometrisk, plyometrisk, kardiovaskulær, styrke).
    """
    types = {"isometrisk": [], "plyometrisk": [], "kardiovaskulær": [], "styrke": []}

    # Group exercises by type
    for exercise in training_setup.values():
        if isinstance(exercise, dict) and "type" in exercise:
            types[exercise["type"].lower()].append(exercise)

    # Select one random exercise from each type
    selected_exercises = []
    for exercise_type, exercises in types.items():
        if exercises:  # Ensure there are exercises of this type
            selected_exercises.append(random.choice(exercises))

    return selected_exercises

def select_three_exercises_by_type(training_setup):
    """
    Select three exercises by randomly excluding one type and picking one exercise from each of the remaining three types.
    """
    types = {"isometrisk": [], "plyometrisk": [], "kardiovaskulær": [], "styrke": []}

    # Group exercises by type
    for exercise in training_setup.values():
        if isinstance(exercise, dict) and "type" in exercise:
            types[exercise["type"].lower()].append(exercise)

    # Randomly exclude one type
    excluded_type = random.choice(list(types.keys()))
    types.pop(excluded_type)

    # Select one random exercise from each of the remaining types
    selected_exercises = []
    for exercises in types.values():
        if exercises:  # Ensure there are exercises of this type
            selected_exercises.append(random.choice(exercises))

    return selected_exercises

def build_program():
    config = read_configuration()
    training_setup = read_trainings()
    players = read_players()
    trainings = list(training_setup.keys()) 
    trainings.remove("template")  # Use remove() to delete 'template' from the list

    weeks_to_plan = wd.next_n_week_numbers(config["config"]["weeks-ahed"])
    print(f"Planning for weeks: {weeks_to_plan}")

    for player_name, player_info in players.items():
        print(f"Building program for {player_name} with repetitions {player_info['repetitions']} and scale {player_info['scale']}")

        content = md.start_training_program(config["config"]["weeks-ahed"], player_name)
        start, end = weeks_to_plan[0], weeks_to_plan[-1]

        for week_number in weeks_to_plan:
            week_dates = wd.get_week_dates(week_number)
            content += f"## Uge {week_number} ({week_dates['Monday']['date']} - {week_dates['Sunday']['date']})\n\n"
            for day in week_dates:
                content += f"### {week_dates[day]['danish']} d. {week_dates[day]['date']}\n"

                # Select three exercises for the day
                daily_exercises = select_three_exercises_by_type(training_setup)
                for exercise in daily_exercises:
                    content += f"#### {exercise['name']}\n\n"
                    content += f"Gentagelser: {player_info['repetitions']}\n\n"  # Use repetitions from player info
                    content += f"Tid: {exercise['duration']} sekunder\n\n"
                    content += f"Type: {exercise['type']}\n\n"
                    content += f"Beskrivelse: {exercise['description']}\n\n"
                content += "---\n\n"

        if start == end:
            filename = f"week_programs/{player_name}_{start}.md"
        else:
            filename = f"week_programs/{player_name}_{start}-{end}.md"
        md.write_markdown_file(content, filename)




if __name__ == "__main__":
    build_program()