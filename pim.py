from colorama import init, Fore, Style
import os

init(autoreset=True)

usuarios = []
usuario_logado = None

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')  

def cadastrar_usuario():
    nome = input('Nome completo: ')
    cpf = input('CPF: ')
    if len(cpf) != 11 or not cpf.isdigit():
        print(Fore.RED + 'CPF invalido! deve conter 11 Numeros !')
        return
    cpf_forma = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    print(Fore.CYAN + f'Seu CPF foi formatado: {cpf_forma}')
      
    idade = int(input('Idade: '))
    email = input('E-mail: ')
    nivel = input('Nivel de conhecimento (Iniciante, Intermediário, Avançado): ')
    senha = input('Senha (mínimo 8 caracteres): ')
    
    while len(senha) < 8:
        senha = input(Fore.RED + 'Senha muito curta. Tente novamente: ')
    
    confirmar_senha = input(Fore.YELLOW + 'Confirme sua senha: ')
    while confirmar_senha != senha:
        confirmar_senha = input(Fore.YELLOW + 'As senhas devem ser iguais!: ')

    usuarios.append({
        'nome': nome,
        'cpf': cpf_forma,
        'idade': idade,
        'email': email,
        'nivel': nivel,
        'senha': senha,
        'livros_lidos': 0
    })

    limpar_tela()
    print(Fore.GREEN + 'Usuário cadastrado com sucesso, faça o login para utilizar nossos serviços!')

def criar_senha():
    email = input('E-mail: ')
    cpf = input('CPF: ')

    if len(cpf) != 11 or not cpf.isdigit():
        print(Fore.RED + 'CPF inválido! Deve conter 11 números.')
        return

    cpf_formatado = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

    for usuario in usuarios:
        if usuario['email'] == email and usuario['cpf'] == cpf_formatado:
            limpar_tela()
            print(Fore.GREEN + 'Credenciais válidas!')
            senha = input('Digite sua nova senha: ')

            while len(senha) < 8:
                limpar_tela()
                senha = input(Fore.RED + 'Senha muito curta, tente novamente: ')

            confirmar_senha = input(Fore.YELLOW + 'Confirme sua senha: ')
            while confirmar_senha != senha:
                limpar_tela()
                confirmar_senha = input(Fore.YELLOW + 'As senhas devem ser iguais: ')

            usuario['senha'] = senha
            limpar_tela()
            print(Fore.GREEN + 'Senha atualizada com sucesso!')
            return

    limpar_tela()
    print(Fore.RED + 'Usuário não encontrado com os dados fornecidos.')
            
def carregar_usuario():
    global usuario_logado

    
    email = input('E-mail: ')
    senha = input('Senha: ')
    
    for usuario in usuarios:
        if usuario['email'] == email and usuario['senha'] == senha:
                 usuario_logado = usuario
                 limpar_tela()
                 print(Fore.GREEN + f"Seja bem-vindo(a), {usuario['nome']}!")
                 menu_sec()
                 return

        
    limpar_tela()

    print(Fore.RED + 'Usuário ou senha inválidos, Tente Novamente ou Crie uma nova senha!')
    print('''
    [1] Criar nova senha
    [2] tentar novamente
            ''')
        
       
    opcao = input('Digite sua opcao: ')

    if opcao == '1':
        limpar_tela()
        criar_senha()

    elif opcao == '2':
        limpar_tela()
        carregar_usuario()

    else:
        limpar_tela()
        print(Fore.RED + 'Selecione uma opção válida.')
                 
def exibir_pagina(pagina, paginas, ultima):
    limpar_tela()
    print(f"Página {pagina + 1} de {len(paginas)}\n")
    for linha in paginas[pagina]:
        print(linha)
    print("\n[1] Voltar   [2] Avançar", end='')
    if ultima:
        print("   [3] Concluir Leitura", end='')
    print("   [0] Sair")

def sistema_so():

    global usuario_logado

    paginas = [
        [
            "Linux é um sistema operacional de código aberto.",
            "Windows é um sistema proprietário da Microsoft.",
            "Linux pode ser modificado por qualquer pessoa.",
            "Windows não permite acesso ao código-fonte.",
            "Ambos têm interfaces gráficas, mas com estilos diferentes."
        ],
        [
            "Linux é amplamente usado em servidores.",
            "Windows é mais comum em desktops e laptops.",
            "Linux tende a ser mais seguro por padrão.",
            "Windows é alvo mais frequente de vírus.",
            "Linux possui várias distribuições (Ubuntu, Fedora, etc)."
        ],
        [
            "A instalação de programas no Linux usa gerenciadores de pacotes.",
            "No Windows, o processo é geralmente feito por instaladores .exe.",
            "Linux tem forte integração com o terminal.",
            "Windows foca mais em interação por interface gráfica.",
            "Ambos suportam softwares populares como navegadores e IDEs."
        ],
        [
            "Linux costuma ser mais leve e roda em máquinas antigas.",
            "Windows exige mais recursos de hardware.",
            "Linux é usado em dispositivos embarcados, como roteadores.",
            "Windows domina o mercado de jogos, mas isso vem mudando.",
            "O suporte a drivers no Windows é mais direto para usuários comuns."
        ],
        [
            "Linux é gratuito para todos os usuários.",
            "Windows geralmente requer uma licença paga.",
            "Ambos têm comunidades grandes e documentação online.",
            "Linux favorece usuários avançados e personalização.",
            "Windows é ideal para quem busca praticidade sem mexer muito no sistema."
        ]
    ]

    pagina_atual = 0
    while True:
        ultima = pagina_atual == len(paginas) - 1
        exibir_pagina(pagina_atual, paginas, ultima)
        escolha = input("Escolha: ")

        if escolha == '1':
            if pagina_atual > 0:
                pagina_atual -= 1
        elif escolha == '2':
            if pagina_atual < len(paginas) - 1:
                pagina_atual += 1
        elif escolha == '3' and ultima:
            print(Fore.GREEN + "\nLeitura concluída! Parabéns :)")
            usuario_logado["livros_lidos"] += 1
            limpar_tela()
            break
        elif escolha == '0': 
            print("Saindo do livro...")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.")

def dicars():
    global usuario_logado

    paginas = [ 
        [
            "Utilize senhas complexas, com letras maiúsculas e minúsculas,"
            " números e símbolos, e diferentes para cada rede social. ",
            "utilize senhas fortes e únicas,",
            "ative a autenticação de dois fatores,",
            "revise as configurações de privacidade e compartilhe"
            " informações pessoais apenas com quem você confia."
            " Evite usar redes Wi-Fi públicas e tenha cuidado com links e conteúdos suspeitos. "
            
        ],
        [
            "Utilize senhas complexas, com letras maiúsculas e minúsculas,"
            " números e símbolos, e diferentes para cada rede social. ",
            "Revise as configurações de privacidade de cada rede social,"
            " limitando o acesso a informações pessoais e conteúdo compartilhado. .",
            "Seja cauteloso ao compartilhar informações pessoais, como endereço,"
            " data de nascimento e número de telefone. ",
            
        ],
        [
            "Evite usar redes Wi-Fi públicas para acessar suas redes sociais,"
            " pois elas podem não ser seguras. ",
            "Evite clicar em links ou baixar arquivos de fontes desconhecidas,"
            " pois eles podem conter malware. ",
            "Desative ou exclua contas antigas que você não usa mais."
            " para evitar que sejam utilizadas para fins maliciosos. .",
            
        ],
        [
            "Seja seletivo ao aceitar seguidores,"
            "Respeite a privacidade de outras pessoas ao compartilhar"
            " fotos ou informações sobre elas, pedindo permissão antes de postar. ",
            "Mantenha seus dispositivos e aplicativos atualizados para garantir que você tenha as últimas versões de segurança.",
            
        ],
        [
            "Parabens, por ler mais uma pagina de de curso, ela será acrescentada a sua conta!"
        ] ]


    pagina_atual = 0
    while True:
        ultima = pagina_atual == len(paginas) - 1
        exibir_pagina(pagina_atual, paginas, ultima)
        escolha = input("Escolha: ")

        if escolha == '1':
            if pagina_atual > 0:
                pagina_atual -= 1
        elif escolha == '2':
            if pagina_atual < len(paginas) - 1:
                pagina_atual += 1
        elif escolha == '3' and ultima:
            print(Fore.GREEN + "\nLeitura concluída! Parabéns :)")
            usuario_logado["livros_lidos"] += 1
            limpar_tela()
            break
        elif escolha == '0': 
            print("Saindo do livro...")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.")

def python():
    global usuario_logado

    paginas = [
        [
            "Python é uma linguagem de programação de alto nível, versátil e de fácil leitura.",
            "É amplamente usada em várias áreas, desde scripts simples até sistemas complexos."
        ],
        [
            "Python é usada em diversas áreas, como:",
            "- Desenvolvimento Web: Criação de sites e aplicações.",
            "- Ciência de Dados: Análise e visualização de dados."
        ],
        [
            "- Inteligência Artificial: Algoritmos de aprendizado de máquina.",
            "- Automação: Tarefas repetitivas automatizadas com scripts.",
            "- Desenvolvimento de jogos, aplicativos e muito mais."
        ],
        [
            "Python possui sintaxe simples, próxima da linguagem humana.",
            "Isso a torna ideal para iniciantes e fácil de manter em grandes projetos."
        ],
        [
            "Funciona em diversos sistemas operacionais (Windows, macOS, Linux).",
            "Possui uma grande comunidade e muitas bibliotecas disponíveis.",
            "Parabéns! Você concluiu a leitura deste conteúdo :)"
        ]
    ]

    pagina_atual = 0
    while True:
        ultima = pagina_atual == len(paginas) - 1
        exibir_pagina(pagina_atual, paginas, ultima)
        escolha = input("Escolha: ")

        if escolha == '1':
            if pagina_atual > 0:
                pagina_atual -= 1
        elif escolha == '2':
            if pagina_atual < len(paginas) - 1:
                pagina_atual += 1
        elif escolha == '3' and ultima:
            print(Fore.GREEN + "\nLeitura concluída! Parabéns :)")
            usuario_logado["livros_lidos"] += 1
            limpar_tela()
            break
        elif escolha == '0': 
            print("Saindo do livro...")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.")

def ver_perfil():
    if usuario_logado:
        limpar_tela()
        print(Fore.CYAN + "===== PERFIL DO USUÁRIO =====")
        print(f"Nome: {usuario_logado['nome']}")
        print(f"CPF: {usuario_logado['cpf']}")
        print(f"Idade: {usuario_logado['idade']}")
        print(f"E-mail: {usuario_logado['email']}")
        print(f"Nível de conhecimento: {usuario_logado['nivel']}")
        print(f"Livros lidos: {usuario_logado['livros_lidos']}")
        print("=" * 30)
        input("\nPressione Enter para voltar...")
        limpar_tela()

    else:
        print(Fore.RED + "Nenhum usuário logado.")

def deslogar():
    global usuario_logado
    usuario_logado = None
    limpar_tela()
    print(Fore.YELLOW + "Você foi deslogado com sucesso!")

def estatistica():
    print('em reforma!')
#preciso terminar

def menu_sec():
    while True:
        print('''\n============ Menu do Usuário ============ 
[1] Ler sobre Sistemas Operacionais
[2] Dica de segurança para redes sociais
[3] O que é python e para que serve?
[4] Ver Perfil
[5] Deslogar
''')
        
        opcao = input('Digite sua opção: ')
        
        if opcao == '1':
            sistema_so()

        elif opcao =='2':
            dicars()

        elif opcao == '3':
            python()

        elif opcao == '4':
            ver_perfil()

        elif opcao == '5':
            deslogar()
            break

        else:
            print(Fore.RED + 'Opção não existente, tente novamente!')

def menu_principal():
    while True:
        print('''=========== Seja bem-vindo! ===========
[1] Cadastrar-se
[2] Login
[3] Ver estatísticas
[4] Sair
''')
        opcao = input('Escolha sua opção: ')

        if opcao == '1':
            limpar_tela()
            cadastrar_usuario()
        elif opcao == '2':
            limpar_tela()
            carregar_usuario()
        elif opcao == '3':
            limpar_tela()
            estatistica()
        elif opcao == '4':
            limpar_tela()
            print('Saindo...')
            break
        else:
            limpar_tela()
            print(Fore.RED + 'Selecione uma opção válida.')


menu_principal()
