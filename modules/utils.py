# modules/utils.py

def obter_input_texto(prompt, permitir_espacos=True):
    """Pede um input de texto, garantindo que não seja vazio e que contenha apenas letras (e espaços, se permitido)."""
    while True:
        valor_str = input(prompt).strip()
        if not valor_str:
            print("Erro: Este campo não pode ser vazio.")
            continue

        string_para_verificar = valor_str.replace(' ', '')
        if not string_para_verificar.isalpha():
            print("Erro: Por favor, digite apenas letras." if not permitir_espacos else "Erro: Por favor, digite apenas letras e espaços.")
            continue
        
        if not permitir_espacos and ' ' in valor_str:
            print("Erro: Espaços não são permitidos neste campo.")
            continue

        return valor_str

def obter_input_numerico(prompt, tipo_dado=int, valor_minimo=None, permitir_zero=False):
    """Pede um input numérico e o valida (tipo, valor mínimo, permissão de zero)."""
    while True:
        try:
            valor_str = input(prompt)
            valor = tipo_dado(valor_str)

            if permitir_zero and valor < 0:
                print("Erro: O valor não pode ser negativo.")
                continue

            if not permitir_zero and valor <= 0:
                print("Erro: O valor deve ser maior que zero.")
                continue

            if valor_minimo is not None and valor < valor_minimo:
                print(f"Erro: O valor precisa ser no mínimo {valor_minimo}.")
                continue
            
            return valor
        except ValueError:
            print("Erro: Entrada inválida. Por favor, digite um número válido.")

def obter_input_numerico_opcional(prompt, tipo_dado=float):
    """Pede um input numérico que pode ser deixado em branco."""
    while True:
        valor_str = input(prompt).strip()
        if not valor_str: # Se o usuário apertar Enter, retorna None
            return None
        try:
            valor = tipo_dado(valor_str)
            if valor <= 0:
                print("Erro: Se for preencher, o valor deve ser positivo.")
                continue
            return valor
        except ValueError:
            print("Erro: Entrada inválida. Por favor, digite um número válido.")