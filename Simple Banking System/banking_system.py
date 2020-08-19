import random
import string
import sqlite3


global conn, cur


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
        random.seed()
        return ''.join(random.sample(string.digits, 9))

    @staticmethod
    def generate_card_pin():
        random.seed()
        return ''.join(random.sample(string.digits, 4))

    def get_checksum(self):
        number = self.BIN + self.account_id
        return calc_checksum(number)

    def get_card_info(self):
        print(f'Your card number:\n{self.card_number}\n'
              f'Your card PIN:\n{self.card_pin}\n')

    def insert_into_database(self):
        cur.execute('INSERT INTO card VALUES(?, ?, ?, ?)',
                    (self.record_id, self.card_number, self.card_pin, self.balance))
        conn.commit()


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


def create_new_card():
    new_card = Card()
    print('\nYour card has been created')
    new_card.get_card_info()


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
            transfer_money(card_number, input('\nTransfer\nEnter card number:\n'))
        elif user_command == 4:
            close_account(card_number)
        elif user_command == 5:
            print('\nYou have successfully logged out\n')
            main_menu()
        elif user_command == 0:
            print('\nBye!')
            exit()


def get_card_balance(card_number):
    cur.execute('SELECT balance FROM card WHERE number=?', (card_number,))
    print(f'\nBalance: {cur.fetchone()[0]}\n')


def add_balance(card_number, money):
    cur.execute('UPDATE card SET balance = balance+? WHERE number=?',
                (money, card_number))
    conn.commit()


def transfer_money(sender_card, receiver_card):
    if calc_checksum(receiver_card[:-1]) != receiver_card[-1]:
        print('Probably you made mistake in the card number. Please try again!\n')
    elif not check_card_exists(receiver_card):
        print('Such a card does not exist.\n')
    elif check_card_same(sender_card, receiver_card):
        print('You can\'t transfer money to the same account!\n')
    else:
        money = float(input('Enter how much money you want to transfer:\n'))

        cur.execute('SELECT balance FROM card WHERE number=?', (sender_card,))
        if cur.fetchone()[0] < money:
            print('Not enough money!\n')
        else:
            add_balance(receiver_card, money)
            add_balance(sender_card, -1 * money)
            print('Success!\n')


def calc_checksum(number):
    number = [int(x) * 2 if (i + 1) % 2 != 0 else int(x)
              for i, x in enumerate(number)]
    number = [x - 9 if x > 9 else x for x in number]
    control_number = sum(number)
    return '0' if control_number % 10 == 0 else str(10 - control_number % 10)


def check_card_exists(card_number):
    cur.execute('SELECT number FROM card WHERE number=?', (card_number,))
    if cur.fetchone() is None:
        return False
    return True


def check_card_same(sender_card, receiver_card):
    if sender_card == receiver_card:
        return True
    return False


def close_account(card_number):
    cur.execute('DELETE FROM card WHERE number=?', (card_number,))
    conn.commit()
    print('\nThe account has been closed!\n')


def create_database():
    global cur, conn
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    with conn:
        cur.execute('CREATE TABLE IF NOT EXISTS card '
                    '(id INTEGER, number TEXT, pin TEXT, '
                    'balance INTEGER DEFAULT  0);')


def delete_table():
    cur.execute('DROP TABLE card')
    conn.commit()


def print_table():
    for row in cur.execute('SELECT * FROM card'):
        print(row)


create_database()
main_menu()
