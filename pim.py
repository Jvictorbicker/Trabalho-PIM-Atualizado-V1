from colorama import init, Fore, Style
import os
import json
import hashlib

init(autoreset=True)

usuarios = []
usuario_logado = None

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def solicitar_consentimento():
    while True:
            print(Fore.BLUE + "---------------- Termo de Consentimento ---------------")
            print("Ao prosseguir, você concorda com o tratamento dos seus dados pessoais conforme descrito abaixo:")
            print("\n1. Dados coletados: nome completo, CPF, idade, e-mail, nível de conhecimento e senha.")
            print("2. Finalidade: cadastro no sistema, acesso a cursos, e geração de estatísticas de uso.")
            print("3. Armazenamento: os dados serão armazenados localmente em um arquivo JSON.")
            print("4. Compartilhamento: seus dados não serão compartilhados com terceiros.")
            print("5. Direitos do titular: você pode, a qualquer momento, solicitar acesso, correção ou exclusão dos seus dados, bem como revogar este consentimento.")
            print(Fore.BLUE + "---------------------------------------------------------")
            print("""[1]Estou de acordo, e aceito os termos acima !
[2]Não aceito os termos acima !""")
            print(Fore.BLUE + "---------------------------------------------------------")

            try:
                 opcao = int(input('Digite sua opção: '))
            except ValueError:
                limpar_tela()
                print(Fore.RED + 'Entrada inválida. Por favor, digite 1 ou 2.')
                continue

            if opcao == 1:
                limpar_tela()
                return True  
            elif opcao == 2:
                 limpar_tela()
                 print(Fore.YELLOW + 'Voltando ao menu principal')
                 return False  
            else:
                 limpar_tela()
                 print(Fore.RED + 'Selecione uma opção válida.')
 
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')  

def cadastrar_usuario():
    limpar_tela()
    print(Fore.BLUE + '====================cadastro de usuario=====================')
    if os.path.exists("dados.json"):
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            try:
                usuarios = json.load(arquivo)
            except json.JSONDecodeError:
                usuarios = []
    else:
        usuarios = []

    nome = input('Nome completo: ')
    cpf = input('CPF: ')
    if len(cpf) != 11 or not cpf.isdigit():
        limpar_tela()
        print(Fore.RED + 'CPF invalido! deve conter 11 Numeros !')
        return
    cpf_forma = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    idade = int(input('Idade: '))
    email = input('E-mail: ')
    nivel = input('Nivel de conhecimento (Iniciante, Intermediário, Avançado): ')
    senha = input('Senha (mínimo 8 caracteres): ')
    
    while len(senha) < 8:
        senha = input(Fore.RED + 'Senha muito curta. Tente novamente: ')
    
    confirmar_senha = input(Fore.YELLOW + 'Confirme sua senha: ')
    while confirmar_senha != senha:
        confirmar_senha = input(Fore.RED + 'As senhas devem ser iguais!: ')

    usuarios.append({
        'nome': nome,
        'cpf': cpf_forma,
        'idade': idade,
        'email': email,
        'nivel': nivel,
        'senha': criptografar_senha(senha),
        'login': email,
        'livros_lidos': 0
    })

    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)

    limpar_tela()
    print(Fore.GREEN + 'Usuário cadastrado com sucesso, faça o login para utilizar nossos serviços!')

def criar_senha():
    with open("dados.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo)

    email = input('E-mail: ')
    cpf = input('CPF: ')

    if len(cpf) != 11 or not cpf.isdigit():
        limpar_tela()
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

            confirmar_senha = input(Fore.BLUE + 'Confirme sua senha: ')
            while confirmar_senha != senha:
                limpar_tela()
                confirmar_senha = input(Fore.RED + 'As senhas devem ser iguais: ')

            usuario['senha'] = criptografar_senha(senha)
            with open("dados.json", "w", encoding="utf-8") as arquivo:
                json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)
            limpar_tela()
            print(Fore.GREEN + 'Senha atualizada com sucesso!')
            return
    
    limpar_tela()
    print(Fore.RED + 'Usuário não encontrado com os dados fornecidos.')
            
def carregar_usuario():
    global usuario_logado

    print(Fore.BLUE + '==================== Login de usuario =====================')
    email = input('E-mail: ')
    senha = input('Senha: ')
    
    with open("dados.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo) 
    print(usuarios)
    for usuario in usuarios:
        if usuario['email'] == email and usuario['senha'] == criptografar_senha(senha):
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

def SO_escolher():

    global usuario_logado
    with open("dados.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo) 
    for usuario in usuarios:
        if "login" not in usuario:
            usuario["login"] = usuario.get("email", "")
    for usuario in usuarios:
        if usuario.get("login") == usuario_logado.get("login"):
            usuario["livros_lidos"] = usuario_logado.get("livros_lidos", 0)
            break

    paginas = [
        [
            "A escolha entre Linux e Windows depende da necessidade do usuário.",
            "O Windows é mais fácil de usar e possui suporte a hardware mais amplo,",
            "enquanto o Linux é mais seguro, gratuito e altamente personalizável.",
            "O Windows tem uma interface mais amigável,",
            "mas o Linux oferece mais liberdade e personalização."
        ],
        [
            "Diferenças e semelhanças:",
            "O Windows tem uma interface gráfica única e consistente,\n"
            "enquanto o Linux oferece uma variedade de interfaces,"
            "\nmuitas com grande capacidade de personalização. ",
            "Linux tende a ser mais seguro por padrão.",
            "Windows é alvo mais frequente de vírus.",
        ],
        [
            "Custo:",
            "O Windows é um sistema operacional proprietário,"
            "\ncom versões que exigem compra, enquanto a maioria das distribuições"
            "\nLinux são gratuitas. ",
            "Segurança:",
            "O Linux é conhecido por ser mais seguro, com uma taxa mais"
            "\nbaixa de infecção por vírus e malware. ",
        ],
        [
            "Compatibilidade de software e hardware:",
            "O Windows tem um suporte mais amplo de software e hardware,"
            "\nenquanto o Linux pode ter menos suporte, dependendo da distribuição. ",
            "Personalização:",
            "O Linux oferece um alto grau de personalização, permitindo que o"
            "\nusuário modifique o sistema para atender às suas necessidades. ",
        ],
        [
            "Qual escolher?",
            "Windows: É a melhor opção para usuários que buscam facilidade de uso,"
            "\ncompatibilidade com a maioria dos softwares e jogos,"
            "\ne um sistema que não exige conhecimento técnico. ",
            "Linux:",
            "É a melhor opção para usuários que buscam segurança, personalização,"
            "\nliberdade de escolha, e uma experiência mais flexível e poderosa. "
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
            limpar_tela()
            print(Fore.GREEN + "\nLeitura concluída! Parabéns :)")
            usuario_logado["livros_lidos"] = usuario_logado.get("livros_lidos", 0) + 1
            for usuario in usuarios:
               if usuario.get("login") == usuario_logado.get("login"):
                   usuario["livros_lidos"] = usuario_logado["livros_lidos"]
                   break
            with open("dados.json", "w", encoding="utf-8") as arquivo:
                json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)
            break
        elif escolha == '0': 
            print("Saindo do livro...")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.")

def curso_python():
    global usuario_logado
    with open("dados.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo) 
    for usuario in usuarios:
     if usuario.get("login") == usuario_logado.get("login"):
        usuario["livros_lidos"] = usuario_logado.get("livros_lidos", 0)
        break
     
    paginas = [ 
        [
            "Sintaxe do python:\n"
            "A sintaxe em Python refere-se às regras que definem como o código"
            "\né escrito e interpretado. É a gramática da linguagem,"
            "\nque garante que o código seja estruturado e compreensível tanto"
            "\npelo interpretador Python quanto pelos humanos."
            "\nA sintaxe em Python é conhecida por ser simples e legível,"
            "\nusando palavras inglesas em vez de símbolos complexos, como em outras linguagens. "
            
        ],
        [
            "Elementos da sintaxe básica em Python:\n"
            "Variáveis:",
            "São contêineres que armazenam dados (números, textos, etc.)."
            "\nSão criadas atribuindo um valor a um nome, por exemplo, nome = João.\n"
            "Tipos de dados:",
            "Definem o tipo de valor que uma variável pode armazenar"
            "\n(inteiros, ponto flutuante, strings, booleanos, etc.)."
            "\nExemplo: idade = 30, altura = 1.75, nome = Ana. "     
        ],
        [
            "Operadores:\n"
            " Símbolos que realizam operações"
            "\n(matemáticas, lógicas, de comparação, etc.)."
            "\nExemplo: + (adição), - (subtração), == (igual), and (e), or (ou).",
            "Estruturas de controle:\n"
            "Permitem controlar a execução do código com base em condições"
            "\nou repetições. Incluem if, else, elif (para condições) e for,"
            "\nwhile (para repetições). ",
        ],
        [
            "Funções:\n"
            "Blocos de código reutilizáveis que realizam tarefas específicas."
            "\nSão definidas usando a palavra-chave def."
            "\nExemplo: def saudacao(nome): print(f Olá, nome!."
            "\nfotos ou informações sobre elas, pedindo"
            "\npermissão antes de postar. ",
            "Mantenha seus dispositivos e aplicativos atualizados"
            "\npara garantir que você tenha as últimas versões de segurança.",
            
        ],
        [
            "Listas, tuplas e dicionários:\n"
            "São estruturas de dados que permitem armazenar coleções de dados."
            "\nListas são mutáveis, tuplas são imutáveis e dicionários são usados"
            "\nPara armazenar pares chave-valor. "
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
            limpar_tela()
            print(Fore.GREEN + "\nLeitura concluída! Parabéns :)")
            usuario_logado["livros_lidos"] = usuario_logado.get("livros_lidos", 0) + 1
            for usuario in usuarios:
                 if usuario.get("login") == usuario_logado.get("login"):
                    usuario["livros_lidos"] = usuario_logado["livros_lidos"]
                    break
            with open("dados.json", "w", encoding="utf-8") as arquivo:
                json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)
            break
            
        elif escolha == '0': 
            print("Saindo do livro...")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.")

def editar_perfil():
    global usuario_logado
    if usuario_logado:
        print(Fore.CYAN + "============ EDITAR PERFIL ===========")
        print("Aperte enter para manter os dados atuais.\n")

        nome = input(f"Nome completo [{usuario_logado['nome']}]: ")
        if nome:
            usuario_logado['nome'] = nome

        idade_input = input(f"Idade [{usuario_logado['idade']}]: ")
        if idade_input:
            usuario_logado['idade'] = idade_input
                

        email = input(f"E-mail [{usuario_logado['email']}]: ")
        if email:
            usuario_logado['email'] = email
        nivel = input(f'Nivel de conhecimento [{usuario_logado['nivel']}]: ')
        if nivel:
            usuario_logado['nivel'] = nivel

        with open("dados.json", "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)

        for usuario in usuarios:
            if usuario['cpf'] == usuario_logado['cpf']:
                usuario.update(usuario_logado)
                break

        with open("dados.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)

        print(Fore.GREEN + "Perfil atualizado com sucesso!")
    else:
        print(Fore.RED + "Nenhum usuário logado.")
   
def excluir_conta_logada():
    global usuario_logado, usuarios

    if usuario_logado is None:
        print(Fore.RED + "Nenhum usuário está logado.")
        return

    with open("dados.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo)

    
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario['cpf'] == usuario_logado['cpf']:
            usuario_encontrado = usuario
            break

    if usuario_encontrado:
        usuarios.remove(usuario_encontrado)
        
        with open("dados.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)
        usuario_logado = None
        limpar_tela()
        print(Fore.GREEN + "Conta excluída com sucesso.")
        input("Pressione Enter para continuar...")
        menu_principal()
        
    else:
        print(Fore.RED + "Usuário não encontrado.")

def excluir():
    global usuario_logado
    while True:
         print(Fore.YELLOW + 'Deseja realmente excluir sua conta? *ESSA ACAO NAO SERA REVERTIDA')
         print(''''
[1] Excluir conta
[2] Voltar
''')
         opcao = int(input('Digite sua opcao: '))

         if opcao == 1:
             limpar_tela()
             excluir_conta_logada()
             
             
         elif opcao == 2:
             limpar_tela()
             print(Fore.YELLOW + 'Voltando...')
             break

         else:
             print('Selecione uma opcao existente!')
                     
def historia_python():
    global usuario_logado
    with open("dados.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo)
    for usuario in usuarios:
     if "login" not in usuario:
        usuario["login"] = usuario.get("email", "")
    for usuario in usuarios:
     if usuario.get("login") == usuario_logado.get("login"):
        usuario["livros_lidos"] = usuario_logado.get("livros_lidos", 0)
        break

    paginas = [
        [
            "A linguagem Python foi criada por Guido van Rossum no"
            "\nfinal dos anos 1980, no Centrum Wiskunde & Informatica (CWI)"
            "\nna Holanda, e lançada pela primeira vez em 1991. Inicialmente,"
            "\no projeto era um hobby para ocupar o tempo durante o Natal,"
            "\nmas evoluiu para se tornar uma linguagem de programação de uso geral, popular e versátil. ",
        ],
        [
            "Origens e Inspirações:",
            "Guido van Rossum pretendia criar uma linguagem que\n"
            "fosse mais fácil de aprender e usar do que a linguagem ABC. "
            "\nNome:"
            "\nO nome Python foi inspirado no grupo de comédia britânico"
            "\nMonty Python, de que Guido van Rossum era fã. ",
        ],
        [
            "Hobby:",
            "A criação do Python começou como um projeto de hobby"
            "Amoeba:",
            "A necessidade de uma linguagem para gerenciar o sistema"
            "\noperacional distribuído Amoeba também contribuiu para o"
            "\ndesenvolvimento do Python, conforme explicita Guido van Rossum na"
            "\ndocumentação oficial. "
        ],
        [
            "Versão 3.0:",
            "Em 2008, foi lançada a versão 3.0 do Python,"
            "\nque trouxe mudanças significativas na linguagem,"
            "\nquebrando a compatibilidade com versões anteriores. "
            "\nPython Software Foundation (PSF):"
            "\nEm 2001, foi criada a Python Software Foundation,"
            "\numa organização sem fins lucrativos que apoia o desenvolvimento da linguagem. "
        ],
        [
            "Popularidade:",
            "O Python tornou-se uma das linguagens de programação"
            "\nmais populares do mundo, utilizada em diversas áreas"
            "\nincluindo desenvolvimento web, análise de dados,"
            "\ninteligência artificial e muito mais. ",
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
            limpar_tela()
            print(Fore.GREEN + "\nLeitura concluída! Parabéns :)")
            usuario_logado["livros_lidos"] = usuario_logado.get("livros_lidos", 0) + 1
            for usuario in usuarios:
               if usuario.get("login") == usuario_logado.get("login"):
                   usuario["livros_lidos"] = usuario_logado["livros_lidos"]
                   break
            with open("dados.json", "w", encoding="utf-8") as arquivo:
                json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)
            break
        elif escolha == '0': 
            print("Saindo do livro...")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.")

def ver_perfil():
    while True:
        if usuario_logado:
            limpar_tela()
            print(Fore.CYAN + "===== PERFIL DO USUÁRIO =====")
            print(f"Nome: {usuario_logado['nome']}")
            print(f"CPF: {usuario_logado['cpf']}")
            print(f"Idade: {usuario_logado['idade']}")
            print(f"E-mail: {usuario_logado['email']}")
            print(f"Nível de conhecimento: {usuario_logado['nivel']}")
            print(f"Livros lidos: {usuario_logado['livros_lidos']}")
            print(Fore.CYAN + "=" * 30)
            
            print('''[1] Editar Perfil
[2] Voltar''')
            print(Fore.RED + '[3] Excluir sua conta')

            opcao = int(input('digite sua opcao: '))

            if opcao == 1:
                limpar_tela()
                editar_perfil()

            elif opcao == 2:
                limpar_tela()
                print(Fore.YELLOW + 'Voltando...')
                break
            if opcao == 3:
                limpar_tela()
                excluir()

            else:
                print(Fore.YELLOW + 'Por favor selecione uma opcao existente!')

        else:
             print(Fore.RED + "Nenhum usuário logado.")

def deslogar():
    global usuario_logado
    usuario_logado = None
    limpar_tela()
    print(Fore.YELLOW + "Você foi deslogado com sucesso!")

def estatistica():
    while True:
        print(Fore.BLUE + '=========== Estatisticas dos Usuarios ===========')
        print('''[1] Media de Idades entre usuarios
[2] Mediana de livros lidos entre usuarios
[3] Moda de idade entre usuarios
[4] Voltar''')
        
        opcao = int(input('Digite sua opcao: ')) 

        if opcao == 1:
            limpar_tela()
            calcular_media()

        elif opcao == 2:
            limpar_tela()
            exibir_mediana_livros()
            

        elif opcao == 3:
            limpar_tela()
            calcular_moda()

        elif opcao == 4:
            limpar_tela()
            print(Fore.YELLOW + 'Voltando...')
            break
        
def calcular_mediana():
    with open("dados.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo)

   
        livros_lidos = [int(u['livros_lidos']) for u in usuarios if 'livros_lidos' in u]
        livros_lidos.sort()

        n = len(livros_lidos)
        if n == 0:
          return None 
        if n % 2 == 1:
          return livros_lidos[n // 2]
        else:
           primeiro = livros_lidos[n // 2 - 1]
           segundo = livros_lidos[n // 2]
           return (primeiro + segundo) // 2  
    
def exibir_mediana_livros():
    limpar_tela()
    mediana = calcular_mediana()
    if mediana is not None:
        print(Fore.BLUE + f'A mediana de livros lidos é: {mediana}')
    else:
        print(Fore.RED + 'Não há dados suficientes para calcular a mediana.')
    input('Aperte Enter para voltar...')
    limpar_tela()

def calcular_moda():
    if not os.path.exists("dados.json"):
        print("Arquivo de dados não encontrado.")
        return

    with open("dados.json", "r", encoding="utf-8") as arquivo:
        try:
            usuarios = json.load(arquivo)
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo de dados.")
            return

    idades = [int(u['idade']) for u in usuarios if 'idade' in u]

    if not idades:
        print("Nenhuma idade registrada.")
        return

    frequencias = {}
    for idade in idades:
        if idade in frequencias:
            frequencias[idade] += 1
        else:
            frequencias[idade] = 1

    
    moda_idade = None
    maior_frequencia = 0

    for idade, frequencia in frequencias.items():
        if frequencia > maior_frequencia:
            maior_frequencia = frequencia
            moda_idade = idade

    print(Fore.BLUE + f"A moda das idades é {moda_idade} anos (ocorreu {maior_frequencia} vezes).")
    input('Aperte enter para voltar...')
    limpar_tela()

def calcular_media():
    with open("dados.json", "r", encoding="utf-8") as arquivo:
         usuarios = json.load(arquivo)

    idade_usuarios = [u for u in usuarios if 'idade' in u]
    qntd_user = len(idade_usuarios)
    soma_idades = sum(int(u['idade']) for u in idade_usuarios)
    media = soma_idades // qntd_user
    print(Fore.BLUE + f'A media de idades dos usuarios cadastrados são de {media}')
    input('Aperte enter para voltar....')
    limpar_tela()

def menu_sec():
    while True:
        print(Fore.BLUE + '\n============ Menu do Usuário ============')
        print('''[1] Ler Nossos livros
[2] Estatisticas
[3] Ver Perfil
[4] Deslogar
''')
        
        opcao = input('Digite sua opção: ')
        
        if opcao == '1':
            limpar_tela()
            menu_livro()

        elif opcao =='2':
            limpar_tela()
            estatistica()

        elif opcao == '3':
            limpar_tela()
            ver_perfil()

        elif opcao == '4':
            deslogar()
            break

        else:
            limpar_tela()
            print(Fore.RED + 'Opção não existente, tente novamente!')

def menu_livro():
    while True:
        print(Fore.BLUE + '''=========== Livros/Minicursos Disponíveis ===========''')
        print('''[1] Curso de programacao em python (Nivel iniciante)
[2] Historia do PYTHON
[3] Qual sistema operacional escolher?
[4] Voltar''')
        print(Fore.BLUE + '======================================================')

        opcao = input('Escolha sua opção: ')

        if opcao == '1':
            limpar_tela()
            curso_python()

            
        elif opcao == '2':
            limpar_tela()
            historia_python()
            

        elif opcao == '3':
            limpar_tela()
            SO_escolher()
            
        elif opcao == '4':
            limpar_tela()
            print(Fore.YELLOW + 'Voltando ao menu principal...')
            break
        else:
            limpar_tela()
            print(Fore.RED + 'Selecione uma opção válida.')

def menu_principal():
    limpar_tela()
    while True:
        print(Fore.BLUE + '''=========== Seja bem-vindo! ===========''')
        print('''[1] Cadastrar-se
[2] Login
[3] Sair
[4] Créditos ''')
        print(Fore.BLUE + '=======================================')

        opcao = input('Escolha sua opção: ')

        if opcao == '1':
            limpar_tela()
            if solicitar_consentimento():
                 cadastrar_usuario()
                 for usuario in usuarios:
                    if "login" not in usuario:
                        usuario["login"] = usuario["email"]
        elif opcao == '2':
            limpar_tela()
            carregar_usuario()
        elif opcao == '3':
            limpar_tela()
            print(Fore.YELLOW + 'Saindo...')
            break
        elif opcao == '4':
            limpar_tela()
            print('''Este foi um projeto que foi iniciado dia 29/04/2025 e foi ser terminado dia 11/05/2025, com intuito 
de ser apresentado como trabalho semestral da UNIP(Universidade Paulista)

Aplicação em modo console desenvolvida por:
                  
João Victor Oliveira Bicker(H76IJC0) 
Ryan Victor Anoni Ferreira (T170796) 
Carlos Eduardo Marques Gomes (H689066) 
Renan Lucas Maia (H76ABC1)
''')
            input(Fore.CYAN + 'Pressione Enter para continuar...')
            limpar_tela()
        else:
            limpar_tela()
            print(Fore.RED + 'Selecione uma opção válida.')

menu_principal()
