import random
import string


cards = []


class Card:
    BIN = '400000'  # Bank Identification Number

    def __init__(self):
        self.account_id = self.generate_account_id()
        self.checksum = self.calc_checksum()
        self.card_number = self.BIN + self.account_id + self.checksum
        self.card_pin = self.generate_card_pin()
        self.balance = 0
        cards.append(self)

    @staticmethod
    def generate_account_id():
        return ''.join(random.sample(string.digits, 9))

    @staticmethod
    def generate_card_pin():
        return ''.join(random.sample(string.digits, 4))

    def calc_checksum(self):
        control_number = self.calc_control_number()
        return '0' if control_number % 10 == 0 else str(10 - control_number % 10)

    # uses Luhn algorithm to calculate control number for finding checksum
    def calc_control_number(self):
        number = self.BIN + self.account_id
        number = [int(x) * 2 if (i + 1) % 2 != 0 else int(x)
                  for i, x in enumerate(number)]
        number = [x - 9 if x > 9 else x for x in number]
        control_number = sum(number)
        return control_number

    def get_card_number(self):
        return self.card_number

    def get_card_pin(self):
        return self.card_pin

    def get_card_info(self):
        print(f'Your card number:\n{self.card_number}\n'
              f'Your card PIN:\n{self.card_pin}\n')

    def get_card_balance(self):
        print(f'\nBalance: {self.balance}\n')


def main_menu():
    global cards
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
    return new_card


def log_in():
    card_number = input('\nEnter your card number:\n')
    card_pin = input('Enter your PIN:\n')
    current_card = get_current_card(card_number, card_pin)

    if current_card is not None:
        print('\nYou have successfully logged in!\n')
        log_in_menu(current_card)

    print('\nWrong card number or PIN!\n')
    main_menu()


def log_in_menu(current_card):
    while True:
        user_command = int(input('1. Balance\n'
                                 '2. Log out\n'
                                 '0. Exit\n'))
        if user_command == 1:
            get_card_balance(current_card)
        elif user_command == 2:
            print('\nYou have successfully logged out\n')
            main_menu()
        elif user_command == 0:
            print('\nBye!')
            exit()


def get_current_card(card_number, card_pin):
    for card in cards:
        if card_number == card.get_card_number() \
                and card_pin == card.get_card_pin():
            return card
    return None


def get_card_balance(current_card):
    current_card.get_card_balance()


main_menu()
