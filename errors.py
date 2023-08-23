# Exception raised when BNF API request show no results.
class ResultError(Exception):
    def __init__(
        self,
        search,
        message="La recherche n'a pas renvoyé de résultat, essayez d'autres critères.",
    ):
        self.search = search
        self.message = message
        super().__init__(self.message)


# Exception raised when ISBN format is not correct.
class IncorrectISBNFormat(Exception):
    def __init__(self, message="Veuillez insérer un ISBN au bon format."):
        self.message = message
        super().__init__(self.message)


# Exception raised when reference already exists in collection.
class ExistingReference(Exception):
    def __init__(
        self, message="Cette référence est déjà présente dans votre collection."
    ):
        self.message = message
        super().__init__(self.message)


# Exception raised when collection already exists in database.
class ExistingCollection(Exception):
    def __init__(self, message="Cette collection existe déjà"):
        self.message = message
        super().__init__(self.message)
