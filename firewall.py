print("Firewall Simulator Started!")
rules = []

def add_rule():
    ip = input("Enter IP address: ")
    port = int(input("Enter port number: "))
    action = input("Enter action (ALLOW/BLOCK): ").upper()

    rules.append((ip, port, action))
    print("Rule added successfully!")


def check_connection():
    ip = input("Enter IP address: ")
    port = int(input("Enter port number: "))

    for rule_ip, rule_port, action in rules:
        if ip == rule_ip and port == rule_port:
            print("Result:", action)
            return

    print("Result: BLOCK")


def display_rules():
    print("\nFirewall Rules")
    print("-------------------------")

    if not rules:
        print("No rules found.")
        return

    for ip, port, action in rules:
        print(f"IP: {ip} | Port: {port} | Action: {action}")


while True:
    print("\n===== FIREWALL SIMULATOR =====")
    print("1. Add Rule")
    print("2. Check Connection")
    print("3. Display Rules")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_rule()

    elif choice == "2":
        check_connection()

    elif choice == "3":
        display_rules()

    elif choice == "4":
        print("Firewall Simulator closed.")
        break

    else:
        print("Invalid choice!")