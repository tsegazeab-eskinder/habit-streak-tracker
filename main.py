from datetime import datetime, timedelta
import json
import os

DATA_FILE = "habit_data.json"

def load_habits():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_habits():
    with open(DATA_FILE, "w") as f:
        json.dump(habits, f, indent=4)

habits = load_habits()

def add_habit():
    name = input("Enter habit name (e.g., 'Read 30 mins'): ")
    habits.append({
        "name": name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "streak": 0,
        "log": []
    })
    print(f"Added habit: '{name}'")
    save_habits()

def mark_habit_completed():
    if not habits:
        print("No habits found.")
        return

    print("\nYour habits:")
    for idx, habit in enumerate(habits, 1):
        print(f"{idx}. {habit['name']} (Streak: {habit['streak']})")

    try:
        choice = int(input("Enter the number of the habit you completed today: "))
        if 1 <= choice <= len(habits):
            selected = habits[choice - 1]
            today = datetime.now().strftime("%Y-%m-%d")

            if selected["log"] and selected["log"][-1] == today:
                print("You've already marked this habit as completed today.")
            else:
                selected["log"].append(today)
                selected["streak"] += 1
                print(f"'{selected['name']}' marked as completed. Current streak: {selected['streak']}")
                save_habits()
        else:
            print("Invalid habit number.")
    except ValueError:
        print("Please enter a number.")

def edit_or_remove_habit():
    if not habits:
        print("No habits found.")
        return

    print("\nYour habits:")
    for idx, habit in enumerate(habits, 1):
        print(f"{idx}. {habit['name']} (Streak: {habit['streak']})")

    try:
        choice = int(input("Enter the number of the habit you want to edit or remove: "))
        if 1 <= choice <= len(habits):
            selected = habits[choice - 1]
            print(f"Selected: {selected['name']}")
            print("1. Rename habit")
            print("2. Delete habit")
            action = input("Choose an option (1 or 2): ")

            if action == "1":
                new_name = input("Enter the new name for the habit: ")
                selected["name"] = new_name
                print(f"Habit renamed to '{new_name}'")
                save_habits()
            elif action == "2":
                confirm = input(f"Are you sure you want to delete '{selected['name']}'? (y/n): ")
                if confirm.lower() == "y":
                    habits.pop(choice - 1)
                    print("Habit deleted.")
                    save_habits()
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid option.")
        else:
            print("Invalid habit number.")
    except ValueError:
        print("Please enter a valid number.")
def view_history(habit_name, days=7):
    habit = next((h for h in habits if h["name"] == habit_name), None)
    if not habit:
        print(f"No history found for '{habit_name}'.")
        return
    today = datetime.today()
    start_date = today - timedelta(days=days)
    completed_days = [date for date in habit["log"] if datetime.strptime(date, "%Y-%m-%d") >= start_date]

    print(f"\n📅 Habit history for '{habit_name}' in the last {days} days:")
    print("✔️ Completed Days:", ", ".join(completed_days) if completed_days else "None")

    missed_days = [
        str((start_date + timedelta(days=i)).date()) 
        for i in range(days) 
        if str((start_date + timedelta(days=i)).date()) not in completed_days
    ]
    print("❌ Missed Days:", ", ".join(missed_days) if missed_days else "None")
if __name__ == "__main__":
    add_habit()
    mark_habit_completed()
    edit_or_remove_habit()
    habit_name = input("Enter the habit name to view history: ")
    view_history(habit_name,days=7)
