from datetime import datetime

habits = []

def add_habit():
    name = input("Enter habit name (e.g., 'Read 30 mins'): ")
    habits.append({
        "name": name,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "streak": 0,
        "log": []
    })
    print(f"Added habit: '{name}'")

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
        else:
            print("Invalid habit number.")
    except ValueError:
        print("Please enter a number.")

if __name__ == "__main__":
    add_habit()
    mark_habit_completed()
