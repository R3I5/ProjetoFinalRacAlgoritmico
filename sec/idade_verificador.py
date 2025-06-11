import datetime

def verificar_idade(maioridade):
    ano_nascimento = int(input("Digite o ano de nascimento do usuário: "))
    ano_atual = datetime.datetime.now().year
    idade = ano_atual - ano_nascimento
    print(f"Sua idade é {idade}")
    if idade>18:
        return True
    else:
        return False