from py_compile import main
import sqlite3
from datetime import datetime

DATABASE_NAME = "mystery_mission.db"

class DetectiveGame:
    def __init__(self, player_name):
        self.player_name = player_name
        self.score = 0
        self.clues_found = []

    def show_welcome(self):
        print("\n" + "="*48)
        print("      MYSTERY MISSION: THE DETECTIVE CHALLENGE   ")
        print("=" * 48)
        print(f"Welcome, {self.player_name}! Let's solve the mystery.")
        print("Study the clues, interrogate suspects, and uncover the truth.")

    def choose_case(self):
        print("\nChoose a case to investigate:")
        print("1. \033[3mThe Missing Diamond Necklace\033[0m")
        print("2. \033[3mThe Missing Laptop\033[0m")
        
        while True:
            choice = input("Enter the number of your choice:").strip()
            if choice == "1":
                return "Diamond Necklace"
            
            elif choice == "2":
                return "Laptop"

            else:
                print("Invalid choice. please enter 1 or 2.")

    def get_case_details(self, case_title):
        cases = {
            "Diamond Necklace": {
                "Title": "The Missing Diamond Necklace",
                "Story": ( 
                    "A priceless diamond necklace has gone missing from the City Museum betwween 6:00PM to 7:00PM during a special exhibition. "
                    ),

                    "Suspects":{
                        "1":{
                            "Name": "Anaya - The Museum Curator",
                            "Statement": "I was checking the visitor registration list at front desk and ensuring the security cameras were functioning properly. I didn't see anything suspicious around 6:00PM."
                        },
                        "2":{
                            "Name": "Ravi - The Security Guard",
                            "Statement": "I was patrolling the museum floor and noticed a suspicious figure near the necklace display around 6:30PM."
                        },
                        "3":{
                            "Name": "Priya - The cleaning staff",
                            "Statement": "I was cleaning the museum floor and didn't notice anything unusual. I was focused on my work and didn't see anyone near the necklace display." 
                        }
                    },            

                    "Clues": [
                        "A muddy footprint was found near the staff only exit door.",
                        "The security access log shows Ravi opened the staff only exit door at 6:15PM.",
                        "A visitors photograph shows Anaya at front desk at 6:18PM.",
                        "The cleaning schedule places Priya in the museum lobby .",
                        "A witness saw someone in security uniform carrying a bag ."
                    ],

                    "Culprit": "Ravi - The Security Guard",

                    "explanation": (
                         "Ravi, the guard, was the culprit. He used his access to the staff only exit door to steal the necklace and tried to cover his tracks by claiming he was patrolling the musuem floor.",
                         "The witness also confirmed that someone in security uniform was seen carrying a bag which was likely used to tranport the stolen necklace."
                    )
                },

            "Laptop": {
                "Title": "The Missing Laptop",
                "Story": (
                    "A Laptop vanished from the computer lab at the University between 2:00PM to 3:00PM during a busy lecture."
                ),
                "Suspects":{
                    "1": {
                        "Name" : "Riya - The Lab Assistant",
                        "Statement" : "I was assisting students with their assignments and didn't notice anything unusual."
                    },
                    "2": {
                        "Name" : "Amit - The Professor",
                        "Statement" : "I was giving a lecture and didn't see anyone near the lab during that time."
                    },
                    "3": {
                        "Name": "Neel - The Student",
                        "Statement" : "I was in the lab working on my project and didn't see anyone take the laptop."
                    }
                },
                "Clues": [
                    "The lab entry log shows Riya entered the lab at 2:05PM.",
                    " A witness saw Amit leaving the lab with a laptop bag at 2:30PM.",
                    "The lab security camera footage shows Neel entering the lab at 2:10PM and leaving at 2:50PM.",
                    "The laptop was last seen on the lab desk at 2:15PM.",
                    "A witness saw someone in a lab coat carrying a laptop bag."
                ],
                "Culprit": "Amit - The Professor",
                "explanation": (
                    "Amit, the professor took advantage of the busy lecture time to steal the laptop. He was seen leaving the lab with a laptop bag, and the witness confirmed that someone in a lab coat was carrying a laptop bag."

                )
                }
            }
        return cases[case_title]

    def investigate(self, case_details):
        print("\nCase Title:", case_details["Title"])
        print("\nStory:", case_details["Story"])
        print("\nSuspects:")
        for key, suspect in case_details["Suspects"].items():
            print(f"  {key}. {suspect['Name']}: {suspect['Statement']}")
        print("\nClues:")
        for clue in case_details["Clues"]:
            print(f"  - {clue}")
        print(f"\nCulprit: {case_details['Culprit']}")
        print(f"Explanation: {case_details['explanation'][0]}")

    def question_suspect(self, case_details):
        print("\n---- QUESTION A SUSPECT ----")
        for number, suspect in case_details["Suspects"].items():
            print(f"{number}. {suspect['Name']}")

        while True:
            choice = input("choose a suspect to question (1-3):").strip()
            if choice in case_details["Suspects"]:
                suspect = case_details["Suspects"][choice]
                print(f"\nYou questioned" , suspect["Name"])
                print("Their Response:", suspect["Statement"])
                break
            print("Invalid choice. Please choose a valid suspect.")

    def make_accusation(self, case_details):
        print("\n---- MAKE AN ACCUSATION ----")
        print("Who do you think is the culprit?")
        for number, suspect in case_details["Suspects"].items():
            print(f"{number}. {suspect['Name']}")

        while True:
            choice = input("Enter the number of your accusation (1-3):").strip()
            if choice in case_details["Suspects"]:
                accused = case_details["Suspects"][choice]["Name"]
                if accused == case_details["Culprit"]:
                    print(f"\nCongratulations! You correctly identified {accused} as the culprit.")
                    self.score += 10
                else:
                    print(f"\nSorry, {accused} is not the culprit. The correct answer was {case_details['Culprit']}.")
                break
            print("Invalid choice. Please choose a valid suspect.")

        if choice ==case_details["Culprit"]:
            print("\nCorrect! Excellent detective work.")
            self.score += 10
            result ="Solved"
        else:
            correct_culprit = case_details["Culprit"]
            print(f"\nIncorrect. The correct culprit was {correct_culprit}.")
            result = "Not Solved"
        print("\nCase EXplanation:", case_details["explanation"])
        return result

    def play_again(self):
        while True:
            choice = input("\nDo you want to play again? (yes/no):").strip().lower()
            if choice in ["yes", "y"]:
                return True
            elif choice in ["no", "n"]:
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")


    def create_database(self):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                case_title TEXT NOT NULL,
                result TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def save_game_result(self, case_title, result):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO game_results (player_name, case_title, result, score)
            VALUES (?, ?, ?, ?)
        ''', (self.player_name, case_title, result, self.score))
        conn.commit()
        conn.close()


    def show_previous_results(self):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT player_name, case_title, result, score, timestamp
            FROM game_results
            ORDER BY timestamp DESC
        ''')
        results = cursor.fetchall()
        conn.close()

        if results:
            print("\n---- Previous Game Results ----")
            for row in results:
                player_name, case_title, result, score, timestamp = row
                print(f"Player: {player_name}, Case: {case_title}, Result: {result}, Score: {score}, Time: {timestamp}")
        elif not results:
            print("\nNo previous game results found.")

        else:
            for record in results:
                print(f"Player: {record[0]} | Case: {record[1]} | Result: {record[2]} | Score: {record[3]} | Timestamp: {record[4]}")


def main():
    print("Welcome to the Mystery Mission: The Detective Challenge!")
    player_name = input("Enter your name:").strip()
    if not player_name:
        player_name = "Detective"

    game = DetectiveGame(player_name)
    game.create_database()
    game.show_welcome()

    game.show_previous_results()

    while True:
        case_title = game.choose_case()
        case_details = game.get_case_details(case_title)
        game.investigate(case_details)
        game.question_suspect(case_details)
        result = game.make_accusation(case_details)
        game.save_game_result(case_title, result)

        if not game.play_again():
            print("\nThank you for playing! Goodbye.")
            break

        print("\n" + "="*48)
        print("Thank you for playing MYSTERY MISSION: THE DETECTIVE CHALLENGE!")
        print(f"Your final score: {game.score}")
        print("="*48 )

    if __name__ == "__main__":
            try:
                main()
            except sqlite3.Error as e:
                print("Database error:", e)
            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")

