from random import sample, seed
from string import digits
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class Card:
    BIN = '400000'  # Bank Identification Number

    def __init__(self):
        self.record_id = self.get_record_id()
        self.account_id = self.generate_account_id()
        self.checksum = self.get_checksum()
        self.card_number = self.BIN + self.account_id + self.checksum
        self.card_pin = self.generate_card_pin()
        self.balance = 0
        self.insert_into_database()

    @staticmethod
    def get_record_id():
        cur.execute('SELECT MAX(id) FROM card')
        max_id = cur.fetchone()
        return max_id[0] + 1 if max_id[0] is not None else 1

    @staticmethod
    def generate_account_id():
        seed()
        return ''.join(sample(digits, 9))

    @staticmethod
    def generate_card_pin():
        seed()
        return ''.join(sample(digits, 4))

    # gets the last number of the credit card
    def get_checksum(self):
        number = self.BIN + self.account_id
        return calc_checksum(number)

    def get_card_info(self):
        print(f'Your card number:\n{self.card_number}\n'
              f'Your card PIN:\n{self.card_pin}\n')

    def insert_into_database(self):
        cur.execute('INSERT INTO card VALUES(?, ?, ?, ?)',
                    (self.record_id, self.card_number, self.card_pin,
                     self.balance))
        conn.commit()


# the main menu of the banking system
def main_menu():
    while True:
        user_command = int(input('1. Create an account\n'
                                 '2. Log into account\n'
                                 '0. Exit\n'))
        if user_command == 1:
            create_new_card()
        elif user_command == 2:
            log_in()
        elif user_command == 0:
            print('\nBye!')
            exit()


# creates a new card (bank account) and prints basic information of it
def create_new_card():
    new_card = Card()
    print('\nYour card has been created')
    new_card.get_card_info()


# allows the user to login to their account using the card number and pin
def log_in():
    card_number = input('\nEnter your card number:\n')
    card_pin = input('Enter your PIN:\n')

    cur.execute('SELECT pin FROM card WHERE number=?', (card_number,))
    correct_pin = cur.fetchone()

    if correct_pin is not None and card_pin == correct_pin[0]:
        print('\nYou have successfully logged in!\n')
        log_in_menu(card_number)
    else:
        print('\nWrong card number or PIN!\n')
        main_menu()


# log in menu of the banking system
# (is only shown once successfully logged in)
def log_in_menu(card_number):
    while True:
        user_command = int(input('1. Balance\n'
                                 '2. Add income\n'
                                 '3. Do transfer\n'
                                 '4. Close account\n'
                                 '5. Log out\n'
                                 '0. Exit\n'))
        if user_command == 1:
            get_card_balance(card_number)
        elif user_command == 2:
            add_balance(card_number, input('\nEnter income:\n'))
            print('Income was added!\n')
        elif user_command == 3:
            transfer_money(card_number,
                           input('\nTransfer\nEnter card number:\n'))
        elif user_command == 4:
            close_account(card_number)
        elif user_command == 5:
            print('\nYou have successfully logged out\n')
            main_menu()
        elif user_command == 0:
            print('\nBye!')
            exit()


# gets and prints the current account's balance
def get_card_balance(card_number):
    cur.execute('SELECT balance FROM card WHERE number=?', (card_number,))
    print(f'\nBalance: {cur.fetchone()[0]}\n')


# adds the given amount of money to the given account
def add_balance(card_number, money):
    cur.execute('UPDATE card SET balance = balance+? WHERE number=?',
                (money, card_number))
    conn.commit()


# transfers the money from the current bank account
# to another existing in the database
def transfer_money(sender_card, receiver_card):
    # checks whether the receiver's card number passes Luhn algorithm
    if calc_checksum(receiver_card[:-1]) != receiver_card[-1]:
        print('Probably you made mistake in the card number. '
              'Please try again!\n')
    # checks whether the receiver's card exists in the database
    elif not check_card_exists(receiver_card):
        print('Such a card does not exist.\n')
    # checks whether the user tries to transfer money to the same account
    elif sender_card == receiver_card:
        print('You can\'t transfer money to the same account!\n')
    else:
        money = float(input('Enter how much money you want to transfer:\n'))

        cur.execute('SELECT balance FROM card WHERE number=?', (sender_card,))
        if cur.fetchone()[0] < money:
            print('Not enough money!\n')
        else:
            # adds money to the receiver's account
            add_balance(receiver_card, money)
            # takes away money from the sender's account
            add_balance(sender_card, -1 * money)
            print('Success!\n')


# uses Luhn algorithm to check whether the card number is valid
def calc_checksum(number):
    number = [int(x) * 2 if (i + 1) % 2 != 0 else int(x)
              for i, x in enumerate(number)]
    number = [x - 9 if x > 9 else x for x in number]
    control_number = sum(number)
    return '0' if control_number % 10 == 0 else str(10 - control_number % 10)


# checks whether the given card number exists in the database
def check_card_exists(card_number):
    cur.execute('SELECT number FROM card WHERE number=?', (card_number,))
    if cur.fetchone() is None:
        return False
    return True


# deletes the account with the given card number from the database
def close_account(card_number):
    cur.execute('DELETE FROM card WHERE number=?', (card_number,))
    conn.commit()
    print('\nThe account has been closed!\n')


# creates a table card in the database
def create_database():
    with conn:
        cur.execute('CREATE TABLE IF NOT EXISTS card '
                    '(id INTEGER, number TEXT, pin TEXT, '
                    'balance INTEGER DEFAULT  0, PRIMARY KEY (id));')


# optional function for deleting the card tables
def delete_table():
    cur.execute('DROP TABLE card')
    conn.commit()


# optional function for printing the card table
def print_table():
    for row in cur.execute('SELECT * FROM card'):
        print(row)


create_database()
main_menu()
