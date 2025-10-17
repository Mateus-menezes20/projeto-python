class SistemaLogin:
    def __init__(self):
        self.usuarios = {}

    def cadastrar(self, email, senha):
        if email in self.usuarios:
            print(f"Usuário '{email}' já cadastrado!")
        else:
            self.usuarios[email] = senha
            print(f"Usuário '{email}' cadastrado com sucesso!")

    def autenticar(self, email, senha):
        if self.usuarios.get(email) == senha:
            print(f"Login bem-sucedido para '{email}'!")
            return True
        print(f"Credenciais inválidas para '{email}'.")
        return False
