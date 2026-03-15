

def start_training_program(weeks_ahead, player_name):
    print("Starting the training program...")
    
    if weeks_ahead == 1:
        text = f"# Træningsprogram for {player_name} for den næste uge:\n\n"
    else:

        text = f"# Træningsprogram for {player_name} for de næste {weeks_ahead} uger:\n\n"
    return text  # Return the generated content

def write_markdown_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:  # Added encoding='utf-8'
        f.write(content)

