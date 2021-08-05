def get_response(prompt):
    response = input(prompt).lower()
    if response == "y" or response == "yes":
        return True
    return False
