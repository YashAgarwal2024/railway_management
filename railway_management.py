import sqlite3

class RailwayManagementSystem:
    def __init__(self):
        self.connection = sqlite3.connect("railway_management.db")
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    mobile TEXT NOT NULL,
                    email TEXT NOT NULL,
                    date TEXT NOT NULL,
                    from_station TEXT NOT NULL,
                    to_station TEXT NOT NULL
                )
            """)

    def admin_login(self):
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        return username == "admin" and password == "password"

    def create_ticket(self):
        name = input("Enter traveler's name: ")
        mobile = input("Enter traveler's mobile number: ")
        email = input("Enter traveler's email: ")
        date = input("Enter travel date (YYYY-MM-DD): ")
        from_station = input("Enter departure station: ")
        to_station = input("Enter destination station: ")
        
        with self.connection:
            self.connection.execute("""
                INSERT INTO tickets (name, mobile, email, date, from_station, to_station)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, mobile, email, date, from_station, to_station))
        
        print("Ticket created successfully!")

    def cancel_ticket(self):
        self.view_tickets()
        ticket_id = int(input("Enter the ticket ID to cancel: "))
        
        with self.connection:
            cursor = self.connection.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
            if cursor.rowcount > 0:
                print(f"Ticket with ID {ticket_id} canceled successfully!")
            else:
                print("Invalid ticket ID.")

    def view_tickets(self):
        cursor = self.connection.execute("SELECT * FROM tickets")
        tickets = cursor.fetchall()
        
        if tickets:
            print("\nTickets available:")
            for ticket in tickets:
                print(f"ID: {ticket[0]}, Name: {ticket[1]}, Mobile: {ticket[2]}, Email: {ticket[3]}, Date: {ticket[4]}, From: {ticket[5]}, To: {ticket[6]}")
        else:
            print("No tickets available.")

    def run(self):
        if not self.admin_login():
            print("Invalid login credentials.")
            return

        while True:
            print("\nWelcome to the Railway Management System")
            print("1. Create Ticket")
            print("2. Cancel Ticket")
            print("3. View Tickets")
            print("4. Exit")
            choice = input("What would you like to do? (1/2/3/4): ")

            if choice == '1':
                self.create_ticket()
            elif choice == '2':
                self.cancel_ticket()
            elif choice == '3':
                self.view_tickets()
            elif choice == '4':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    rms = RailwayManagementSystem()
    rms.run()
