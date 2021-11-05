class Curso:
    def __init__(self, nome, categoria, duracao, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.duracao = duracao


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
