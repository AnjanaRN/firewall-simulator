import json
import os
from datetime import datetime
import ipaddress

RULES_FILE = "rules.json"
LOG_FILE = "firewall.log"
MAX_LOGS = 20

rules = []

# Statistics
total_connections = 0
allowed_connections = 0
blocked_connections = 0
tcp_connections = 0
udp_connections = 0


# -------------------------------
# LOAD AND SAVE RULES
# -------------------------------

def load_rules():
    global rules

    if os.path.exists(RULES_FILE):
        try:
            with open(RULES_FILE, "r") as file:
                rules = json.load(file)
        except:
            rules = []


def save_rules():
    with open(RULES_FILE, "w") as file:
        json.dump(rules, file, indent=4)


# -------------------------------
# INPUT VALIDATION
# -------------------------------

def get_ip():
    while True:
        ip = input("Enter IP address: ")

        try:
            ipaddress.IPv4Address(ip)
            return ip
        except ValueError:
            print("Invalid IP address. Try again.")


def get_port():
    while True:
        try:
            port = int(input("Enter port number: "))

            if 1 <= port <= 65535:
                return port

            print("Port must be between 1 and 65535.")

        except ValueError:
            print("Invalid port. Enter a number.")


def get_protocol():
    while True:
        protocol = input("Enter protocol (TCP/UDP): ").upper()

        if protocol == "TCP" or protocol == "UDP":
            return protocol

        print("Enter only TCP or UDP.")


def get_action():
    while True:
        action = input("Enter action (ALLOW/BLOCK): ").upper()

        if action == "ALLOW" or action == "BLOCK":
            return action

        print("Enter only ALLOW or BLOCK.")


# -------------------------------
# ADD RULE
# -------------------------------

def add_rule():

    print("\n===== ADD FIREWALL RULE =====")

    ip = get_ip()
    port = get_port()
    protocol = get_protocol()
    action = get_action()

    rule = {
        "ip": ip,
        "port": port,
        "protocol": protocol,
        "action": action
    }

    rules.append(rule)

    save_rules()

    print("\nRule added successfully!")


# -------------------------------
# DISPLAY RULES
# -------------------------------

def display_rules():

    print("\n===== FIREWALL RULES =====")

    if len(rules) == 0:
        print("No firewall rules found.")
        return

    for i, rule in enumerate(rules):

        print(
            f"{i + 1}. "
            f"IP: {rule['ip']} | "
            f"Port: {rule['port']} | "
            f"Protocol: {rule['protocol']} | "
            f"Action: {rule['action']}"
        )


# -------------------------------
# CHECK CONNECTION
# -------------------------------

def check_connection():

    global total_connections
    global allowed_connections
    global blocked_connections
    global tcp_connections
    global udp_connections

    print("\n===== CHECK CONNECTION =====")

    ip = get_ip()
    port = get_port()
    protocol = get_protocol()

    total_connections += 1

    if protocol == "TCP":
        tcp_connections += 1
    else:
        udp_connections += 1

    # Default policy
    result = "BLOCK"

    # Check rules in order
    for rule in rules:

        if (
            rule["ip"] == ip
            and rule["port"] == port
            and rule["protocol"] == protocol
        ):
            result = rule["action"]
            break

    if result == "ALLOW":
        allowed_connections += 1
    else:
        blocked_connections += 1

    print("\nConnection Result:", result)

    add_log(ip, port, protocol, result)


# -------------------------------
# LOGGING
# -------------------------------

def add_log(ip, port, protocol, result):

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_log = (
        f"[{time}] "
        f"{ip}:{port} "
        f"{protocol} -> {result}\n"
    )

    logs = []

    if os.path.exists(LOG_FILE):

        try:
            with open(LOG_FILE, "r") as file:
                logs = file.readlines()

        except:
            logs = []

    logs.append(new_log)

    # Keep only latest 20 logs
    logs = logs[-MAX_LOGS:]

    with open(LOG_FILE, "w") as file:
        file.writelines(logs)


# -------------------------------
# VIEW LOGS
# -------------------------------

def view_logs():

    print("\n===== FIREWALL LOGS =====")

    if not os.path.exists(LOG_FILE):
        print("No logs found.")
        return

    with open(LOG_FILE, "r") as file:
        logs = file.readlines()

    if len(logs) == 0:
        print("No logs found.")
        return

    for log in logs:
        print(log, end="")


# -------------------------------
# CLEAR LOGS
# -------------------------------

def clear_logs():

    if not os.path.exists(LOG_FILE):
        print("\nNo logs found.")
        return

    confirm = input(
        "\nClear all logs? (Y/N): "
    ).upper()

    if confirm == "Y":

        open(LOG_FILE, "w").close()

        print("Logs cleared successfully.")

    else:
        print("Operation cancelled.")


# -------------------------------
# EDIT RULE
# -------------------------------

def edit_rule():

    if len(rules) == 0:
        print("\nNo rules available.")
        return

    display_rules()

    try:
        number = int(
            input("\nEnter rule number to edit: ")
        )

        if number < 1 or number > len(rules):
            print("Invalid rule number.")
            return

    except ValueError:
        print("Invalid input.")
        return

    index = number - 1

    print("\nEnter new rule details:")

    rules[index] = {
        "ip": get_ip(),
        "port": get_port(),
        "protocol": get_protocol(),
        "action": get_action()
    }

    save_rules()

    print("\nRule updated successfully!")


# -------------------------------
# DELETE RULE
# -------------------------------

def delete_rule():

    if len(rules) == 0:
        print("\nNo rules available.")
        return

    display_rules()

    try:
        number = int(
            input("\nEnter rule number to delete: ")
        )

        if number < 1 or number > len(rules):
            print("Invalid rule number.")
            return

    except ValueError:
        print("Invalid input.")
        return

    confirm = input(
        "Delete this rule? (Y/N): "
    ).upper()

    if confirm == "Y":

        rules.pop(number - 1)

        save_rules()

        print("Rule deleted successfully.")

    else:
        print("Operation cancelled.")


# -------------------------------
# STATISTICS
# -------------------------------

def statistics():

    print("\n===== FIREWALL STATISTICS =====")

    print(
        "Total Connections :",
        total_connections
    )

    print(
        "Allowed           :",
        allowed_connections
    )

    print(
        "Blocked           :",
        blocked_connections
    )

    print(
        "TCP Connections   :",
        tcp_connections
    )

    print(
        "UDP Connections   :",
        udp_connections
    )

    if total_connections > 0:

        allowed_percent = (
            allowed_connections
            / total_connections
        ) * 100

        blocked_percent = (
            blocked_connections
            / total_connections
        ) * 100

        print(
            f"Allowed Percentage : "
            f"{allowed_percent:.2f}%"
        )

        print(
            f"Blocked Percentage : "
            f"{blocked_percent:.2f}%"
        )


# -------------------------------
# MAIN PROGRAM
# -------------------------------

load_rules()

print("\n================================")
print("       FIREWALL SIMULATOR")
print("================================")

print(
    f"{len(rules)} rule(s) loaded."
)


while True:

    print("\n===== MENU =====")
    print("1. Add Firewall Rule")
    print("2. Check Connection")
    print("3. Display Rules")
    print("4. Edit Rule")
    print("5. Delete Rule")
    print("6. View Logs")
    print("7. Clear Logs")
    print("8. View Statistics")
    print("9. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_rule()

    elif choice == "2":
        check_connection()

    elif choice == "3":
        display_rules()

    elif choice == "4":
        edit_rule()

    elif choice == "5":
        delete_rule()

    elif choice == "6":
        view_logs()

    elif choice == "7":
        clear_logs()

    elif choice == "8":
        statistics()

    elif choice == "9":
        print("\nFirewall Simulator closed.")
        break

    else:
        print("\nInvalid choice. Enter 1-9.")