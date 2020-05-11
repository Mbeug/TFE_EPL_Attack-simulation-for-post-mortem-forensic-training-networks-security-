import os
import sys

from colorOutput import ColorOutput


class Utility:
    """
        This is an auxiliary class to help us to interact with a user and some other tools
    """

    @staticmethod
    def ask_user_boolean(message: str) -> bool:
        """
        This method ask to the user a question with a boolean answer
        :param message: The question to the user
        :return: The answer of the user
        :rtype: bool
        """
        flag = input(message + " (Y/N):").lower()
        while flag != 'y' and flag != 'n':
            flag = input("You enter a wrong value: " + str(flag) + " . Please try again with 'y' or 'n':").lower()
        return flag == 'y'

    @staticmethod
    def ask_user_choice(choices: list, message=None):
        """
        This method asks the user to make a choice based on a list *choices*.

        :param choices: The possible choices
        :param message: A question
        :return: The choice of user
        :rtype: Type of element in the choices list
        """
        if message is not None:
            print(message)
        for idx in range(0, len(choices)):
            print("[{0}]:{1}".format(idx, choices[idx]))

        user_in = input("Choose the number corresponding of your choice:")
        while not user_in.isdigit():
            user_in = input(
                "You enter a wrong value:" + str(user_in) + "\nPlease try again with a digit")
        user_idx = int(user_in)
        while user_idx < 0 or user_idx >= len(choices):
            try:
                user_idx = int(input("You enter a wrong value.\nPlease try again with a number between 0 and " + str(
                    len(choices) - 1)))
            except:
                print("You must enter a digit!")

        return choices[user_idx]

    @staticmethod
    def ask_user_number(message: str) -> int:
        """
        This method ask to the user a question with a response expected a number answer.

        :param message: The question
        :return: A number to answer to the question
        :rtype: int
        """
        value = input(message)
        while not value.isdigit():
            value = input(
                "You enter a wrong value: {}\nPlease try again with a digit".format(str(value)))

        value_int: int = int(value)
        return value_int

    @staticmethod
    def print_in_file(input: str, filename: str):
        """
        This method allows to print a specific input in a specific file.

        :param input: The message, input must be write in the file
        :param filename: The name of the file
        :return: Write the input in the specific file

        .. note:: The location of the file is in the out directory of this python project
        """
        if os.path.exists("out/" + filename):
            if Utility.ask_user_boolean("Do you want to delete the old file {}?".format(filename)):
                os.system("rm out/{}".format(filename))
                print(ColorOutput.INFO_TAG + ": {} deleted".format(filename))
        print(ColorOutput.INFO_TAG + ": writing in {} ...".format(filename))
        with open("out/" + filename, "w") as file:
            file.write(input)
        pass