# login.py
import json
import os

class Login:
    def email_exists(self, email_to_check, user_list):
        return any(user["email"] == email_to_check for user in user_list)

    def sign_up(self):
        from main import Book_Management  # ✅ Move import here
        users = self.load_users()
        user = dict()
        name = input(" Enter full name: ")

        email = input("Enter your email address(should be more than 4 characters): ").strip()
        if self.email_exists(email, users):
            print("\nEmail already exist!")
            input("\nPress enter to continue")
            Book_Management().Login()
            return  

        while True:
            password = input("Enter password: ")
            if len(password) > 4:
                break
            print("Password should be more than 4 characters\n")

        while True:
            cpassword = input("Confirm password: ")
            if cpassword != password:
                print("Password does not match\n")
            else:
                break

        while True:
            Admin_check = input("Are you an admin? (yes/no): ").strip().lower()
            if Admin_check in ['yes', 'no']:
                if Admin_check == 'yes':
                    admin_code = input("Enter admin code: ")
                    if admin_code == "admin123":
                        print("Admin code recognised")
                        user["admin"] = True
                        break
                    else:
                        print("Admin code not recognised\n")
                else:
                    user["admin"] = False
                    break
            else:
                print("Please enter 'yes' or 'no'")

        user["name"] = name
        user["email"] = email
        user["password"] = password
        users.append(user)
        self.save_login(users)
        print("Account created successfully")
        self.sign_in()

    def sign_in(self):
        from main import Book_Management  
        users = self.load_users()
        email = input("Enter email: ").strip()
        matched_user = next((u for u in users if u["email"] == email), None)

        if not matched_user:
            print("Email not found, try again!\n")
            return Book_Management().Login()

        for attempt in range(5):
            password = input("Enter password: ").strip()
            if matched_user["password"] == password:
                print(f"Welcome, {matched_user['name']}!\n")
                bm = Book_Management()
                bm.current_user_email = matched_user["email"]
                bm.log_activity(matched_user["email"], "Logged in")
                if matched_user.get("admin", False):
                    bm.adminMenu()
                else:
                    bm.userMenu()
                return
            else:
                print("Incorrect password.")
        print("Too many failed attempts. Try again later.")

    def save_login(self, users):
        with open('user.json', 'w') as file:
            return json.dump(users, file, indent=4)

    def load_users(self):
        if os.path.exists("user.json"):
            with open("user.json", "r") as file:
                content = file.read().strip()
                return json.loads(content) if content else []
        return []
