import random
import string


cards = []


class Card:
    MII = '4'  # Major Industry Identifier
    IIN = '400000'  # Issuer Identification Number
    cards = {}

    def __init__(self):
        self.account_number = ''.join(random.sample(string.digits, 9))
        self.checksum = str(random.choice(string.digits))
        self.card_number = self.IIN + self.account_number + self.checksum
        self.card_pin = ''.join(random.sample(string.digits, 4))
        self.cards[self.card_number] = self.card_pin
        self.balance = 0

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
            cards.append(create_new_card())
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

    if card_number in Card.cards and card_pin == Card.cards[card_number]:
        print('\nYou have successfully logged in!\n')
        current_card = get_current_card(card_number, card_pin)
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
