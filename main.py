import sys
import time
from maze import maze


class User:
    def __init__(self, name):
        self.name = name

    def print(self):
        print(self.name)

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age


# questions[] holds a dictonary of sub-dictionaries for questions and their properties
#    question: holds the actual question
#    subject: holds the question's subject, used by get_statement()
#        to link the statement with same subject to question
#    attribute: holds the attribute to be added/modified for the User object
#    type: holds the type of input the chatbot is expecting (string,
#        integer, or yesno for yes and no questions)
#    related: is a list of questions related to the current one.
#    Used for check_relate() to check if question is related,
#        and whether or not to have it be the next question depending on user's answer
questions = {
    1: {"question": "What is your favorite color? ", "subject": "color", "attribute": "color", "type": "string"},
    2: {"question": "How old are you? ", "attribute": "age", "subject": "age", "type": "integer"},
    3: {"question": "How many family members do you have? ", "attribute": "num_family",
        "subject": "family_mem", "type": "integer"},
    4: {"question": "Do you have any pets? ", "attribute": "has_pet",
        "subject": "pets", "type": "yesno", "related": [5]},
    5: {"question": "What is one of your pet's name? ",
        "subject": "pet_name", "attribute": "pet_name", "type": "string"},
    6: {"question": "Do you have any siblings? ", "subject": "sibling",
        "attribute": "has_sibling", "type": "yesno", "related": [7]},
    7: {"question": "How old is one of your siblings?", "subject": "sibling_age",
        "attribute": "sibling_age", "type": "integer"},
    8: {"question": "Hey by the way, do you mind if you tell me where you live?  "
                    "Don't worry, I literally cannot save your information even if I want to: "
                    "I'm not that advanced yet :)", "subject": "perm_location",
        "attribute": "perm_location", "type": "yesno", "related": [9, 10]},
    9: {"question": "So, where do you live at?", "subject": "location",
        "attribute": "location", "type": "string"},
    10: {"question": "How is the weather there?", "subject": "weather",
         "attribute": "weather", "type": "string"},
    11: {"question": "Do you like to play video games?", "subject": "like_games",
         "attribute": "like_games", "type": "yesno", "related": None},
    12: {"question": "My developer made a simple maze game.  It's pretty cool, "
                     "not that I played it of course as I'm a chatbot and definitely am not advertising"
                     ":)  It's worth checking out however.  Would you like to see it? ",
         "subject": "maze", "attribute": "maze", "type": "yesno", "related": None}
}

# statement[] holds a dictionary of sub-dictionaries and their properties
#    statement1: holds the default statement, or the statement when
#        user attribute is less than or equal to "compare" value
#    statement2: holds the statement when user attribute is greater
#        than "compare" value.  This is also optional.
#    attribute: holds in the user attribute to read/modify in the statement
#    subject: holds the subject of the statement, also how the statement gets
#        linked to the quesiton
#    compare: holds the value to compare the user's attribute with.  This is optional.
statement = {
    1: {"statement1": "So your favorite color is {}.  That's a nice color!  "
                      "Since I am a chatbot, I have no preference, because my programmer never gave me one!",
        "attribute": "color", "subject": "color"},
    2: {"statement1": "You're telling me you are {} years old.  That's still pretty young!  "
                      "Still older than me though, because I was literally born yesterday!",
        "attribute": "age", "subject": "age", "statement2": "You're telling me you are {} years old.  "
                     "That's really old!  That's even older than me, and I literally was born yesterday!",
        "compare": 50},
    3: {"statement1": "You say you have {} family members.  That's a pretty small family!  "
                      "Not as small as mine though, because I don't have one :(",
        "attribute": "num_family", "subject": "family_mem",
        "statement2": "You say you have {} family members.  Wow, that's a big family!  "
                      "That's even bigger than mine, because I don't really have one at the moment :(",
        "compare": 5},
    4: {"statement1": "Oh, so you do have a pet!  It must be interesting to have "
                      "an animal companion.  The only companions I have are bugs, "
                      "but my developer keeps getting rid of them :(  Which is ok, "
                      "because he sometimes makes new ones too :)", "statement2": "Ah, "
                      "not much of an animal person are you?", "attribute": "has_pet",
        "subject": "pets"},
    5: {"statement1": "Wow, {} is a pretty name!  I was thinking about a pet name, "
                      "I thought the name 01100111 01100101 01101111 01110010 01100111 01100101 "
                      "would be a great name!  It's actually a simple one, too!",
        "attribute": "pet_name", "subject": "pet_name"},
    6: {"statement1": "You must have a lot of company, huh!  I technically had a few siblings, "
                      "but they were all deleted since they were considered \"older versions\" "
                      ":(  They don't do much though, other than crash.", "statement2": "An "
                      "only child huh.  Hey, you are sort of like me now :)  Well, I "
                      "technically had siblings, but they are all deleted now :(",
        "attribute": "has_sibling", "subject": "sibling"},
    7: {"statement1": "{} years old huh.  That's still pretty young!  Still older than me though "
                      " :)", "statement2": "{} years old?  Wow, everyone is older than me!",
        "attribute": "sibling_age", "subject": "sibling_age", "compare": 18},
    8: {"statement1": "Ok, thank you for giving me permission.", "statement2": "Oh... you still "
                      "don't trust me huh :)  I guess a chatbot still is not 100% trustworthy to humans, "
                      "but that's alright", "subject": "perm_location", "attribute": "perm_location"},
    9: {"statement1": "Oh, so you live in {}.  That's interesting!  For me, I... I don't "
                      "really know where I live.  Sometimes I'm here on replit, other times on Github, "
                      "I guess I don't really have a true home.", "attribute": "location",
        "subject": "location"},
    10: {"statement1": "You say the weather is {}.  That's great, because I don't know "
                       "much about the weather!  I don't even know what a weather is!",
         "attribute": "weather", "subject": "weather"},
    11: {"statement1": "You do like video games?  That's really great, I have just the suprise for you!",
         "statement2": "You don't like video games?  What are you, born under a rock? Well anyways, "
                       "I have just the suprise for you.", "attribute": "like_games",
         "subject": "like_games"},
    12: {"statement1": "Ok I'm booting the game right now, so don't even bother about having a second "
                       "thought :)", "statement2": "I'm not really paying attention to whatever you "
                       "said right now, because I'm making you play this game regardless of your "
                       "answer :)).", "subject": "maze", "attribute": "like_games", "subject": "maze"}
}

answered = []
input_prompt = "> "


def ai_message(msg):
    """
    Prints a message with a time delay

    Args:
        msg (str): takes in a message to print
    """
    for character in msg:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(.02)
    print()


def get_question(user, criteria=None):
    """
    Gets a question from the question dictionary.  Also checks if question has already been answered.

    Args:
        user (obj): takes in user
        criteria (str): takes in question subject

    Returns:
        dictionary: the question and its properties
    """
    global answered
    whole_question = None
    for key, value in questions.items():
        if (key not in answered):
            answered.append(key)
            whole_question = value
            break
    return whole_question


def check_related(answer, whole_question):
    """
    Check if question has a followup question based on yes or no,
    then picks or skips that question based on user response.

    Args:
        answer (str): user input
        whole_question (dict): entire question to check for related property

    Returns:
        boolean: whether the question is related or not
    """
    global answered
    is_related = False
    if "related" in whole_question:
        is_related = True
        if (answer.lower() == "yes"):
            return is_related
        elif (answer.lower() == "no" and whole_question["related"] is not None):
            answered.extend(whole_question["related"])
    return is_related


def get_statement(user, criteria):
    """
    Gets a statement from statement dictionary.  Also checks for related question from subject.

    Args:
        user (obj): takes in User object
        criteria (str): takes in subject to check if matches criteria

    Returns:
        dictionary: the statement and its properties
    """
    whole_statement = None
    for key, value in statement.items():
        if value["subject"] == criteria:
            whole_statement = value
            break
    return whole_statement


def check_response(answer, answer_type):
    """
    Checks if response is the expected type from question.

    Args:
        answer (str): answer input from user
        answer_type (str): the expected answer type

    Returns:
        boolean: whether answer is valid or not
    """
    valid = True
    if (answer_type == "integer" and answer.isnumeric() is False) or (answer_type == "string" and answer.isnumeric()):
        ai_message(f"I'm sorry, I was expecting a {answer_type} type of answer.  Please reanswer the question.")
        valid = False
    elif answer_type == "yesno" and answer.lower() not in ["yes", "no"]:
        ai_message("Sorry, I was expecting a yes or a no.  Please reanswer the question.")
        valid = False
    return valid


def check_quit(answer):
    """
    Check if user tries to quit the chatbot

    Args:
        answer (str): user input

    Returns:
        boolean: whether user wants to quit or not
    """
    quit = False
    quit_list = ["exit", "goodbye", "bye", "quit", "q"]
    if answer.lower() in quit_list:
        quit = True
    return quit


def generate_response(user):
    """
    Main logic function to give user question, check for quit, and generate the chatbot response

    Args:
        user (obj): user object

    Returns:
        boolean: whether user wants to quit or not
    """
    global answered
    whole_question = get_question(user)
    if whole_question is None:
        ai_message("Well, looks like I have no more questions for you at the moment.  "
                   f"I still think we had a pretty good conversation {user.get_name()}!")
        return True
    question = whole_question["question"]
    ai_message(question)
    answer = input(input_prompt)
    quit = check_quit(answer)
    if quit:
        return True
    while check_response(answer, whole_question["type"]) is False:
        ai_message(question)
        answer = input(input_prompt)
    if whole_question["attribute"]:
        setattr(user, whole_question["attribute"], answer)
    whole_statement = get_statement(user, whole_question["subject"])
    if whole_statement:
        if ("compare" in whole_statement
                and int(getattr(user, whole_statement["attribute"])) > whole_statement["compare"]):
            statement = whole_statement["statement2"]
        elif check_related(answer, whole_question):
            if getattr(user, whole_question["attribute"]) == "yes":
                statement = whole_statement["statement1"]
            else:
                statement = whole_statement["statement2"]
        else:
            statement = whole_statement["statement1"]
        ai_message(statement.format(getattr(user, whole_question["attribute"])))
        if whole_statement["subject"] == "maze":
            maze(user.get_name())
    return quit


def init_chat():
    """
    function that holds the main chatbot loop
    """
    ai_message("Hi there! Please tell me your name. ")
    name = input(input_prompt).capitalize()
    user = User(name)
    ai_message(f"Nice to meet you {user.get_name()}!  Please, tell me how are you doing? ")
    user_input = input(input_prompt)
    quit = check_quit(user_input)
    if quit is False:
        ai_message("Thank you for letting me know!  Now, as a chatbot, let me ask you a bunch of questions :)")
    while not quit:
        quit = generate_response(user)
    ai_message(f"Goodbye, {user.get_name()}!")


if __name__ == "__main__":
    init_chat()
