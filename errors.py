# Exception créée lorsque la recherche vers l'API de la BNF ne renvoie pas de résultats.
class ResultError(Exception):

    def __init__(self, search, message="La recherche n'a pas renvoyé de résultat, essayez d'autres critères."):
        self.search = search
        self.message = message
        super().__init__(self.message)