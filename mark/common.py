
class Prerequisites:

    counter = 0

    def __init__(self, gmail, password, text):

        self.text = text
        self.gmail = gmail
        self.password = password
        self.images = []

        self.__class__.counter += 1

    def __repr__(self):

        return f"Post_{self.__class__.counter}"


class Public:

    def __init__(self, link, name):

        self.link = link
        self.name = name