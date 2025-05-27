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

if __name__ == "__main__":
    add_habit()