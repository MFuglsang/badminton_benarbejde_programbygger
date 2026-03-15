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
            for days in week_dates:
                content += f"### {week_dates[days]['danish']} d. {week_dates[days]['date']}\n"
                content += f"**Gentagelser : {player_info['repetitions']}**\n\n"
                exercises_for_day = get_n_exercises(trainings, player_info['exercises'])


                for count, exercise in enumerate(exercises_for_day):
                    content += f"#### Øvelse {count + 1}: {training_setup[exercise]['name']}\n"
                    training_info = training_setup[exercise]
                    content += f"<font size = \"1\">{training_info['description']}</font>\n\n"
                    content += f"**Varighed: {training_info['duration']} sekunder**\n\n"
    


        if start == end:
            filename = f"week_programs/{player_name}_{start}.md"
        else:
            filename = f"week_programs/{player_name}_{start}-{end}.md"
        md.write_markdown_file(content, filename)




    #for week_number in weeks_to_plan:
    #    week_dates = wd.get_week_dates(week_number)

    
    



if __name__ == "__main__":
    build_program()