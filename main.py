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

def show_all_streaks():
    if not habits:
        print("No habits found.")
        return

    print("\nYour habits and current streaks:")
    for idx, habit in enumerate(habits, 1):
        print(f"{idx}. {habit['name']} - Streak: {habit['streak']}")

def add_habit():
    name = input("Enter habit name (e.g., 'Read 30 mins'): ").strip()
    
    if any(h['name'].lower() == name.lower() for h in habits):
        print("Habit already exists.")
        return

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

    choice = input("Enter the number of the habit you completed today: ").strip()

    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    choice = int(choice)
    if 1 <= choice <= len(habits):
        selected = habits[choice - 1]
        today = datetime.now().strftime("%Y-%m-%d")

        if selected["log"] and selected["log"][-1] == today:
            print("You've already marked this habit as completed today.")
        else:
            if selected["log"]:
                last_date = datetime.strptime(selected["log"][-1], "%Y-%m-%d")
                yesterday = datetime.now() - timedelta(days=1)
                if last_date.date() == yesterday.date():
                    selected["streak"] += 1
                else:
                    selected["streak"] = 1
            else:
                selected["streak"] = 1

            selected["log"].append(today)
            print(f"'{selected['name']}' marked as completed. Current streak: {selected['streak']}")
            save_habits()
    else:
        print("Invalid habit number.")

def edit_or_remove_habit():
    if not habits:
        print("No habits found.")
        return

    print("\nYour habits:")
    for idx, habit in enumerate(habits, 1):
        print(f"{idx}. {habit['name']} (Streak: {habit['streak']})")

    choice = input("Enter the number of the habit you want to edit or remove: ").strip()

    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    choice = int(choice)
    if 1 <= choice <= len(habits):
        selected = habits[choice - 1]
        print(f"Selected: {selected['name']}")
        print("1. Rename habit")
        print("2. Delete habit")
        action = input("Choose an option (1 or 2): ").strip()

        if action == "1":
            new_name = input("Enter the new name for the habit: ").strip()
            selected["name"] = new_name
            print(f"Habit renamed to '{new_name}'")
            save_habits()
        elif action == "2":
            confirm = input(f"Are you sure you want to delete '{selected['name']}'? (y/n): ").strip()
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

def view_history(habit_name, days=7):
    habit = next((h for h in habits if h["name"].lower() == habit_name.lower()), None)
    if not habit:
        print(f"No history found for '{habit_name}'.")
        return

    today = datetime.today()
    start_date = today - timedelta(days=days)
    completed_days = [date for date in habit["log"] if datetime.strptime(date, "%Y-%m-%d") >= start_date]

    print(f"\n Habit history for '{habit_name}' in the last {days} days:")
    print(" Completed Days:", ", ".join(completed_days) if completed_days else "None")

    missed_days = [
        str((start_date + timedelta(days=i)).date()) 
        for i in range(days) 
        if str((start_date + timedelta(days=i)).date()) not in completed_days
    ]
    print(" Missed Days:", ", ".join(missed_days) if missed_days else "None")

habits = load_habits()

if __name__ == "__main__":
    while True:
        print("\nHabit Tracker Menu:")
        print("1. Show all habits and streaks")
        print("2. Add new habit")
        print("3. Mark habit as completed")
        print("4. Edit or remove habit")
        print("5. View habit history")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            show_all_streaks()
        elif choice == "2":
            add_habit()
        elif choice == "3":
            mark_habit_completed()
        elif choice == "4":
            edit_or_remove_habit()
        elif choice == "5":
            habit_name = input("Enter the habit name to view history: ")
            view_history(habit_name, days=7)
        elif choice == "6":
            print("Goodbye! Stay consistent ")
            break
        else:
            print("Invalid option. Please try again.")
