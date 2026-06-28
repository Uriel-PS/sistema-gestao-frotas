class Oficina:
    _proximo_id = 1

    def __init__(self, nome: str, cnpj: str,
                 telefone: str, endereco: str) -> None:
        if not nome or not nome.strip():
            raise ValueError("O nome da oficina não pode ser vazio.")

        self.__id = Oficina._proximo_id
        Oficina._proximo_id += 1
        self.__nome = nome
        self.__cnpj = cnpj
        self.__telefone = telefone
        self.__endereco = endereco

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def cnpj(self):
        return self.__cnpj

    @staticmethod #metodo pertence à classe em si, e não o objeto, é um factory method praticamente
    def cadastrarOficina(nome: str, cnpj: str,
                         telefone: str, endereco: str) -> "Oficina":
        return Oficina(nome=nome, cnpj=cnpj,
                       telefone=telefone, endereco=endereco)

    def __repr__(self):
        return f"Oficina(id={self.id}, nome={self.nome!r})"