import os
import sys

from colorOutput import ColorOutput


class Utility:

    @staticmethod
    def ask_user_boolean(message: str) -> bool:
        flag = input(message + " (Y/N):").lower()
        while flag != 'y' and flag != 'n':
            flag = input("You enter a wrong value: " + str(flag) + " . Please try again with 'y' or 'n':").lower()
        return flag == 'y'

    @staticmethod
    def ask_user_choice(choices:list,message=None):
        if message != None:
            print(message)
        for idx in range(0, len(choices)):
            print("[{0}]:{1}".format(idx, choices[idx]))

        user_in = input("Choose the number corresponding of your choice:")
        while not user_in.isdigit():
           user_in = input(
                "You enter a wrong value:" + str(user_in) + "\nPlease try again with a digit")
        user_idx = int(user_in)
        while user_idx < 0 or user_idx >= len(choices):
            try :
                user_idx = int(input("You enter a wrong value.\nPlease try again with a number between 0 and " + str(
                    len(choices)-1)))
            except:
                print("You must enter a digit!")

        return choices[user_idx]
    @staticmethod
    def ask_user_number(message:str) -> int:
        value = input(message)
        while not value.isdigit():
            value = input(
                "You enter a wrong value: {}\nPlease try again with a digit".format(str(value)))

        value_int : int = int(value)
        return value_int

    @staticmethod
    def print_in_file(input:str, filename:str):
        if os.path.exists("out/"+filename):
            if Utility.ask_user_boolean("Do you want to delete the old file {}?".format(filename)):
                os.system("rm out/{}".format(filename))
                print(ColorOutput.INFO_TAG+": {} deleted".format(filename))
        print(ColorOutput.INFO_TAG+": writning in {} ...".format(filename))
        with open("out/"+filename, "w") as file:
            file.write(input)