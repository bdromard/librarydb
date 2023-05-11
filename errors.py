# Exception créée lorsque la recherche vers l'API de la BNF ne renvoie pas de résultats.
class ResultError(Exception):

    def __init__(self, search, message="La recherche n'a pas renvoyé de résultat, essayez d'autres critères."):
        self.search = search
        self.message = message
        super().__init__(self.message)


# Exception créée lorsque le format de l'ISBN n'est pas correct.
class IncorrectISBNFormat(Exception):

    def __init__(self, message="Veuillez insérer un ISBN au bon format."):
        self.message = message
        super().__init__(self.message)

# Exception créée lorsque la référence existe déjà dans la collection de la base de données.
class ExistingReference(Exception):

    def __init__(self, message="Cette référence est déjà présente dans votre collection."):
        self.message = message
        super().__init__(self.message)

class ExistingCollection(Exception):

    def __init__(self, message="Cette collection existe déjà"):
        self.message = message
        super().__init__(self.message)