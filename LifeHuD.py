import os
from datetime import datetime
import json
import time


data_store = "HUD_data.json"

def load_data():
    template = {
        "profile": {"name": "User" , "age": 0 , "role": "Student"},
        "finance": {"balance": 0.0, "history": []},
        "health": {"score": 0 , "last_log": "Never", "history": []},
        "tasks": [],
        "goals": {"title": "Setup HUD", "progress": 0}
    }
    if not os.path.exists(data_store):
        return template
    else:
        try:
            with open(data_store, 'r') as f:
                return json.load(f)
        except:
            return template

def save_data(data):
    try:
        with open(data_store, 'w') as f:
            json.dump(data, f, indent=4)
        print("System State Saved")
        time.sleep(0.5)
    except IOError:
        print("Could not sasve data.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_dashboard(data):
    clear_screen()
    p = data['profile']
    f = data['finance']
    h = data['health']
    g = data['goals']

    print("--- DASHBOARD ---")
    print("Name:", p['name'])
    print("Wallet Balance:", f['balance'])
    print("Health Score:", h['score'])
    print("Goal:", g['title'])
    print("Pending Tasks:", len(data['tasks']))
    print("-----------------")

def update_finance(data):
    print("==== FINANCE MANAGER ===")
    print("1. Add Spending(-)")
    print("2. Add Income (+)")

    choice = input("Select Action >> ")
    try:
        amount = float(input("Enter Amount: ")) 
        note = input("Description: ")
        if choice == '1':
            data['finance']['balance'] -= amount
            log_type = "EXPENSE"
        elif choice == '2':
            data['finance']['balance'] += amount
            log_type = "INCOME"
        else:
            return
        
        data['finance']['history'].append({
            "type": log_type, "amount": amount, "note": note
        })
        print("TRANSACTION LOGGED.")
    except:
        print("Invalid amount.")

def calculate_health(data):
    print("Health Algorithm")
    print("Rate parameters 1-10:")
    try:
        sleep = int(input("Sleep quality last night : "))
        diet = int(input("Quality of diet :"))
        mental = int(input("Mental Stress : "))
        activity = int(input('Physical Activity : '))
        
        score = 50 + (sleep*2.5) + (diet*1.5) +(activity*1)-(mental*2)
        score = max(0,min(100,int(score)))
        
        data['health']['score'] = score
        print("Health Updated: ", score)
    except:
        print("Enter numbers only.")

def main():
    data = load_data()
    
    if data['profile']['name'] == "User":
        clear_screen()
        print("Welcome to LifeHUD")
        new_name = input("Please enter your name: ")
        data['profile']['name'] = new_name
        save_data(data)
    
    while True:
        show_dashboard(data)
        print("1. Update Finance")
        print("2. Update Health")
        print("3. Save & Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            update_finance(data)
        elif choice == '2':
            calculate_health(data)
        elif choice == '3':
            save_data(data)
            break
        else:
            print("Invalid choice")
            time.sleep(1)

if __name__ == "__main__":
    main()
