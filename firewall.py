import datetime

rules = []


# Validate IPv4 address
def is_valid_ip(ip):
    parts = ip.split(".")

    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False

        if int(part) < 0 or int(part) > 255:
            return False

    return True


# Get a valid port number
def get_valid_port():
    while True:
        try:
            port = int(input("Enter port number: "))

            if 1 <= port <= 65535:
                return port

            print("Invalid port! Enter a number between 1 and 65535.")

        except ValueError:
            print("Invalid port! Please enter a number.")


# Get a valid protocol
def get_valid_protocol():
    while True:
        protocol = input("Enter protocol (TCP/UDP): ").upper()

        if protocol in ["TCP", "UDP"]:
            return protocol

        print("Invalid protocol! Enter TCP or UDP.")


# Get a valid action
def get_valid_action():
    while True:
        action = input("Enter action (ALLOW/BLOCK): ").upper()

        if action in ["ALLOW", "BLOCK"]:
            return action

        print("Invalid action! Enter ALLOW or BLOCK.")


# Add a firewall rule
def add_rule():
    ip = input("Enter IP address: ")

    if not is_valid_ip(ip):
        print("Invalid IP address!")
        return

    port = get_valid_port()
    protocol = get_valid_protocol()
    action = get_valid_action()

    rules.append((ip, port, protocol, action))

    print("Rule added successfully!")


# Write connection attempt to log file
def log_connection(ip, port, protocol, action):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("firewall.log", "a") as file:
        file.write(
            f"[{time}] {ip}:{port} {protocol} -> {action}\n"
        )


# Check a connection
def check_connection():
    ip = input("Enter IP address: ")

    if not is_valid_ip(ip):
        print("Invalid IP address!")
        return

    port = get_valid_port()
    protocol = get_valid_protocol()

    result = "BLOCK"

    for rule_ip, rule_port, rule_protocol, action in rules:
        if (ip == rule_ip and
            port == rule_port and
            protocol == rule_protocol):

            result = action
            break

    print("Result:", result)

    log_connection(ip, port, protocol, result)


# Display firewall rules
def display_rules():
    print("\nFirewall Rules")
    print("---------------------------------------------")

    if not rules:
        print("No rules found.")
        return

    for ip, port, protocol, action in rules:
        print(
            f"IP: {ip} | Port: {port} | "
            f"Protocol: {protocol} | Action: {action}"
        )


# Display connection logs
def view_logs():
    print("\nFirewall Activity Logs")
    print("---------------------------------------------")

    try:
        with open("firewall.log", "r") as file:
            logs = file.read()

            if logs:
                print(logs)
            else:
                print("No logs found.")

    except FileNotFoundError:
        print("No logs found.")


# Main program
while True:
    print("\n===== FIREWALL SIMULATOR =====")
    print("1. Add Rule")
    print("2. Check Connection")
    print("3. Display Rules")
    print("4. View Logs")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_rule()

    elif choice == "2":
        check_connection()

    elif choice == "3":
        display_rules()

    elif choice == "4":
        view_logs()

    elif choice == "5":
        print("Firewall Simulator closed.")
        break

    else:
        print("Invalid choice!")