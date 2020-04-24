class Utility:

    @staticmethod
    def ask_user_boolean(message: str):
        flag = input(message + " (Y/N):").lower()
        while flag != 'y' and flag != 'n':
            flag = input("You enter a wrong value: " + str(flag) + " . Please try again with 'y' or 'n'.").lower()
        return flag == 'y'

    @staticmethod
    def ask_user_number(choices:list):
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
                print("You must enter a digit")

        return choices[user_idx]
