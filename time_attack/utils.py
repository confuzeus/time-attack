def yes_or_no(msg: str) -> bool:
    acceptable = False

    while not acceptable:
        answer = input(msg + " (y/n) ")
        if answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        else:
            print(f"You typed {answer}. Please type only y or n.")
    return False
