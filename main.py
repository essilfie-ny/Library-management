# main.py
import json
import os
import random
import sys
import datetime
from login import Login  



class Book_Management:
    def __init__(self):
        self.current_user_email = "Unknown"

    def log_activity(self, user_email, action):
        with open("activity_log.txt", "a") as log:
            log.write(f"{datetime.datetime.now()} | {user_email} | {action}\n")

    def save_book(self, book):
        with open('BookList.json', 'w') as file:
            return json.dump(book, file, indent=4)
    
    def load_books(self):
        if os.path.exists("BookList.json"):
            with open("BookList.json", "r") as file:
                content = file.read().strip()
                if content:
                    return json.loads(content)
                else:
                    return []
        else:
            return []
               
    def add_book(self):
        serial_numbers = 0 
        book = dict()
        title = input("\nInput title of book: ").capitalize()
        author = input("Input author's name: ").capitalize()
        
        if len(title) < 2 or len(author) < 1:
            print("Title must be at least 2 characters and author at least 1 character.")
            return
        serial = random.randint(11111, 99999)
        while True:
            price = input("How much will the book be selling for: Ghc ")
            try:
                price = float(price)
                break
            except ValueError:
                print('Enter a proper amount')
                continue
        input("\nPress enter to continue\n") 

        book['title'] = title
        book['author'] = author
        book['serial'] = title[0] + title[-1].upper() + author[0] + str(serial)
        book['price'] = price
        book["borrow"] = 'NO'
        books = self.load_books()
        books.append(book)
        self.save_book(books)
        print("\nBook added successfully\n")
        self.log_activity(self.current_user_email, f"Added book: {title}")

    def view_all_books(self):
        books = self.load_books()
        num = 0
        for book in books:
            num += 1
            print(f"""
{num}. Book title: {book['title']}
   Author: {book['author']}
   Serial Number: {book['serial']}
   Borrrow Price(per month): GHc {book['price']}
""")
        self.log_activity(self.current_user_email, "Viewed all books")
        input("\nPress enter to continue\n") 

    def search_by_title(self):
        search_t = input("\nEnter book title: ")
        found = False
        books = self.load_books()
        num = 0
        for book in books:
            if book['title'].lower() == search_t.lower():
                print(f"""
Book title: {book['title']}
Author: {book['author']}
Serial Number: {book['serial']}
Borrrow Price(per month): GHc {book['price']}
""")
                found = True
        
        if not found:
            print('Book was not found')
        self.log_activity(self.current_user_email, f"Searched for book title: {search_t}")
        input("\nPress enter to continue\n") 

    def borrow_book(self):
        bookb = dict()
        search_t = input("\nEnter title of book you would like to borrow: ")
    
        found = False
        books = self.load_books()
        num = 0
        books_found = []
        for book in books:
            if book['title'].lower() == search_t.lower():
                print(f"""
Book title: {book['title']}
Author: {book['author']}
Serial Number: {book['serial']}
Borrrow Price(per month): GHc {book['price']}
Borrowed: {book["borrow"]}
""")
                books_found.append(book)
                found = True
        
        if found:
            found = False

            while(True):
                borrow = input("Enter serial number of book you want to borrow: ")
                try:
                    month = int(input("How many months would you like to borrow book for (1-24): "))
                    if month < 1 or month > 24:
                        print("Select a month within the range given")
                    else:
                        break

                except ValueError:
                    print("Enter a valid number of months")

            for book in books:
                if borrow.lower() == book['serial'].lower() and book['borrow'] == "NO":
                    pay = book['price'] * month
                    print(f"Amount to borrow {book['title']} for {month} month(s) is GHC {pay} ")
                    bookb['title'] = book['title']
                    bookb['author'] = book['author']
                    bookb['serial'] = book['serial']
                    bookb['price'] = book['price']
                    bookb["borrow"] = 'YES'
                    books.remove(book)
                    while True:
                        payment  = input("""\nSelect 
1. To pay online 
2. To pay at the front desk
3. To cancel
Option: """)
                        if payment in ['1', '2', '3']:
                            break
                        else:
                            print("\nPlease select option available")
                    if payment == "3":
                        print("Payment cancelled")
                        books.append(book)
                        self.save_book(books)
                        self.log_activity(self.current_user_email, f"Cancelled borrowing book: {book['title']}")
                    else:
                        input("Press enter if done with payment")
                        print("""Head to library to pick up your book.
Please note additional charges will be added if book is not returned before due date in a readable condition""")
                        books.append(bookb)
                        self.save_book(books)
                        self.log_activity(self.current_user_email, f"Borrowed book: {book['title']} for {month} month(s)")
                    found = True
                elif borrow.lower() == book['serial'].lower() and book['borrow'] == "YES":
                    print ('''This book has been borrowed.
Please select another book in book list that is available for borrowing''')
                    found = True
            if not found:
                print("Book with this serial number was not found")

        else:
            print('\nBook was not found\n')
        input("\nPress enter to continue\n") 
        
    def display_pending_returns(self):
        books = self.load_books()
        num = 0
        for book in books:
            if book['borrow'] == 'YES':
                num += 1
            
                print(f"""
{num}. Book title: {book['title']}
   Author: {book['author']}
   Serial Number: {book['serial']}
   Borrrow Price(per month): GHc {book['price']}
""")
        self.log_activity(self.current_user_email, "Viewed pending returns")
        input("\nPress enter to continue\n") 
    
    def return_borrowed_book(self):
        bookb = dict()
        while True:
            serial = input("Enter serial number on book (or 0 to return to main menu): ")
            if serial == "0":
                break
            found = False
            books = self.load_books()
            for book in books:
                if book['serial'].lower() == serial.lower():
                    bookb['title'] = book['title']
                    bookb['author'] = book['author']
                    bookb['serial'] = book['serial']
                    bookb['price'] = book['price']
                    bookb["borrow"] = 'NO'
                    books.remove(book)
                    books.append(bookb)
                    self.save_book(books)
                    found = True
                    print("Book returned successfully.")
                    self.log_activity(self.current_user_email, f"Returned book: {book['title']}")
                    break
            if found:
                break
            else:
                print("Serial number not recognized")
                print("Please try again or enter 0 to return to main menu")
        input("\nPress enter to continue\n") 

    def delete_book(self):
        serial = input("Enter the serial number of the book to be deleted: ")
        found = False
        books = self.load_books()
        for book in books:
            if book['serial'] == serial:
                books.remove(book)
                self.save_book(books)
                found = True
                print (f"Book with serial number: {serial} has been removed from library")
                self.log_activity(self.current_user_email, f"Deleted book: {book['title']}")
        
        if not found:
            print('Book was not found')
        input("\nPress enter to continue\n") 

    def sort_book(self):
        num = 0
        books = self.load_books()
        sorted_books = sorted(books, key=lambda x: x['title'])
        for book in sorted_books:
            num += 1
            print(f"""
{num}. Book title: {book['title']}
   Author: {book['author']}
   Serial Number: {book['serial']}
   Borrrow Price(per month): GHc {book['price']}""")
        self.log_activity(self.current_user_email, "Sorted books alphabetically")
    
    def Welcome(self):
        print("""
    \n--------WELCOME-------
         TO
    ESSILFIE LIBRARY\n""")
    def Login(self):
        print("""1. Sign In
2. Sign up
""")    
        while True:
            option = input("Select an option to get access to the library: ").strip()
            if option == "1":
                Login().sign_in()
            elif option == "2":
                Login().sign_up()
            else:
                print("Invalid input, Try again")

    def adminMenu(self):
        print("""
    \n--------WELCOME-------
         TO
    ESSILFIE LIBRARY\n""")
        while True:
            while True:
                print("""1. Add a book
2. View all books
3. Search by title
4. Borrow book
5. Display pending returns
6. Return borrowed book
7. Delete a book
8. Sort book in alphabetical order
9. Exit
                    """)
                options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                try:
                    choice = int(input('What would you like to do: '))
                    if choice not in options:
                        print ("\nPlease select a number from the options provided!")
                    else:
                        break
                except ValueError:
                    print("\nPlease select a number from the provided options!")
                    continue

            if choice == 1:
                self.add_book()
            elif choice == 2:
                self.view_all_books()
            elif choice == 3:
                self.search_by_title()
            elif choice == 4:
                self.borrow_book()
            elif choice == 5:
                self.display_pending_returns()
            elif choice == 7:
                self.delete_book()
            elif choice == 6:
                self.return_borrowed_book()
            elif choice == 8:
                self.sort_book()
            else:
                self.log_activity(self.current_user_email, "Logged out (admin)")
                print("Goodbye.....")
                sys.exit()
                
    def userMenu(self):
        print("""
    \n--------WELCOME-------
         TO
    ESSILFIE LIBRARY\n""")
        while True:
            while True:
                print("""
1. View all books
2. Search by title
3. Borrow book
4. Return borrowed book
5. Sort book in alphabetical order
6. Exit
                    """)
                options = [1, 2, 3, 4, 5, 6] 
                try:
                    choice = int(input('What would you like to do: '))
                    if choice not in options:
                        print ("\nPlease select a number from the options provided!")
                    else:
                        break
                except ValueError:
                    print("\nPlease select a number from the provided options!")
                    continue

            
            if choice == 1:
                self.view_all_books()
            elif choice == 2:
                self.search_by_title()
            elif choice == 3:
                self.borrow_book()
            elif choice == 4:
                self.return_borrowed_book()
            elif choice == 5:
                self.sort_book()
            else:
                self.log_activity(self.current_user_email, "Logged out (user)")
                print("Goodbye.....")
                sys.exit()
            

if __name__ == "__main__":
    Book_Management().Welcome()
    Book_Management().Login()
    
