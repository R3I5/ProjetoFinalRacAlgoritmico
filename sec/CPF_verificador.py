def validar_cpf(cpf: str) -> bool:
    # Remove pontos e traços
    cpf = cpf.replace(".", "").replace("-", "")
    
    # Verifica se o CPF tem 11 dígitos e não é uma sequência repetida
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10

    # Verifica se os dígitos calculados conferem com os do CPF
    return cpf[-2:] == f"{digito1}{digito2}"


# Exemplo de uso:
cpf_teste = input("Digite um CPF para validar (somente números ou com pontuação): ")

if validar_cpf(cpf_teste):
    print("CPF VÁLIDO!")
else:
    print("CPF INVÁLIDO!")
