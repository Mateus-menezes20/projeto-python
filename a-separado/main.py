from datetime import datetime

#criando a classe eventos

class Evento:
    def __init__(self,nome,local,capacidade_maxima,categoria, preco):
        self.__nome = nome 
        self.__data = ""
        self.__local = local
        self.__capacidade_maxima = capacidade_maxima
        self.__categoria = categoria
        self.__preco = preco
        self.__inscritos = []
        self.__presenca = []
    
    def __str__(self):
        return f"{self.__nome}"
    
    def __repr__(self):
        return self.__str__()



    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self,valor):
        self.__nome = valor
    
    @property
    def data(self):
        return self.__data
   
    @property
    def local(self):
        return self.__local
    
    @local.setter
    def local(self,valor):
        self.__local = valor
    
    @property
    def capacidade_maxima(self):
        return self.__capacidade_maxima
    
    @capacidade_maxima.setter
    def capacidade_maxima(self,valor):
        self.__capacidade_maxima = valor

    @property
    def categoria(self):
        return self.__categoria
    
    @categoria.setter
    def categoria(self,valor):
        self.__categoria = valor 

    @property
    def preco(self):
        return self.__preco
    
    @preco.setter
    def preco(self,valor):
        self.__preco = valor

    @property
    def inscritos(self):
        return self.__inscritos
    
    @property
    def presenca(self):
        return self.__presenca

    def adicionar_data (self,data):
        data_evento = datetime.strptime(data,"%d/%m/%Y").date()
        data_atual = datetime.now().date()
        if data_atual <= data_evento:
            self.__data = data_evento
        else:
            print("A data atual não pode ser anterior a data do evento!")
    
    def adicionar_presenca (self,pessoa):
        if pessoa in self.__inscritos:
            self.__presenca.append(pessoa)

class Participante:
    def __init__(self,nome,email):
        self.__nome = nome 
        self.__email = email
        self.__evento_inscrito = []

    def __str__(self):
        return f"{self.__nome}"
    
    def __repr__(self):
        return self.__str__()


    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self,valor):
        self.__nome = valor

    @property
    def email(self):
        return self.__email
    
    @email.setter 
    def email(self,valor):
        self.__email = valor
    
    @property
    def evento_inscrito(self):
        return self.__evento_inscrito
    
    def add_evento (self,evento):
        if len(evento.inscritos) >= evento.capacidade_maxima:
            print("Erro! O evento está lotado.")
            return 
        for inscrito in evento.inscritos:
            if inscrito.email == self.__email:
                print("Email já registrado.")    
                return 
        self.__evento_inscrito.append(evento)
        evento.inscritos.append(self)
    
    def cancelar_inscricao (self,evento):
        if evento in self.__evento_inscrito:
            self.__evento_inscrito.remove(evento)
        evento.inscritos.remove(self)



class SistemaEventos:
    def __init__(self):
        self.__lista = []


    def __str__(self):
        return f"{self.__lista}"
    
    def __repr__(self):
        return self.__str__()


    @property
    def lista(self):
        return self.__lista

    def adicionar_evento(self,evento):
        self.__lista.append(evento)
    
    def eventos_categoria(self,categoria):
        lista2 = []

        for evento in self.lista:
            if evento.categoria == categoria:
                lista2.append(evento)
        return lista2 

    def eventos_data(self,data):
        lista2 = []
        data_evento = datetime.strptime(data,"%d/%m/%Y").date()

        for evento in self.lista:
            if evento.data == data_evento:
                lista2.append(evento)
        return lista2 

# Criando objetos

evento1=Evento("Artes Visuais","Rua bartolomeu",50,"artes",20)
print(evento1.adicionar_data("19/11/2025"))
print(evento1.data)

evento2=Evento("Artes cénicas","Rua eucalipto",60,"artes", 50)
evento2.adicionar_data("20/11/2025")


pessoa1=Participante("andrew","andrew19@gmail.com")
pessoa1.add_evento(evento1)
print(pessoa1.evento_inscrito)
print(evento1)

# pessoa1.cancelar_inscricao(evento1)
# print(pessoa1.evento_inscrito)

evento1.adicionar_presenca(pessoa1)
print(evento1.inscritos)
print(evento1.presenca)
print(pessoa1)

sistema=SistemaEventos()
sistema.adicionar_evento(evento1)
sistema.adicionar_evento(evento2)
print(sistema.eventos_categoria("artes"))
print(evento1)

print(sistema.eventos_data("20/11/2025"))
print(sistema.lista)








   
