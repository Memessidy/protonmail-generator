import os
import settings
from common.get_choice import get_user_input, check_num
from common.save_in_file import add_to_file, create_new_file
from pom_objects.protonmail_creation_pages import create_accounts


def text_menu():
    hello_string = ("Hello! This script will help you to create ProtonMail accounts."
                    " Would you like to create new accounts?")
    print(hello_string)
    choice = get_user_input()
    match choice:
        case 'y':
            save_in_file_string = "Would you like to save your ProtonMail accounts in file?"
            print(save_in_file_string)
            save_in_file = get_user_input() == 'y'

            if save_in_file:
                if not os.path.isfile(settings.filename):
                    print(f"Creating {settings.filename} for saving ProtonMail accounts...")
                    create_new_file(settings.filename,
                                    first_row=['protonmail address', 'protonmail password', 'date and time'])

            print(f"How many accounts would you like to create? (min=1, max={settings.max_accounts_count})")
            ui = input('>> ')
            if check_num(ui):
                accounts = create_accounts(count=int(ui))
                for account in accounts:
                    print(f"Created account! Login: {account[0]} Password: {account[1]}")
                    if save_in_file:
                        add_to_file(data=[account], filename=settings.filename)
                        print(f"Data saved to {settings.filename}")
        case 'n':
            print('Thanks for using this script!')


def main():
    try:
        text_menu()
    except Exception as exc:
        print(exc)
    finally:
        input('Press enter to continue...')


if __name__ == '__main__':
    main()
