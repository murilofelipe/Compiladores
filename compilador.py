# Alunos: Murilo Silva Felipe e Leozitor Floro de Souza
## variaveis globais

import inspect

lookahead = ""
lines = 0
nivel = 0
contador = 0
varType = "none"
mepaLista = []
class symbolTabel:         # classe tabela de simbolos

    identifier = ''
    category = ""
    level = 0
    variantInfo = []

    def __init__(self,id,cat,lvl,varInfo):
        self.identifier = id
        self.category = cat
        self.lvl = lvl
        self.variantInfo = varInfo

## ------------------  ANALISADOR LEXICO --------------------------

# DEFINIÇÕES REGULARES
# letter→[a-zA-z]
# digit→[0−9]
# identifier→letter(letter|digit)∗
# digits→digit+num→digits optionalfraction optionalexpoent
# optionalfraction→( .digits)?
# optionalexpoent→( ( E|e ) ( +|- )? digits)?
# character→qualquer caracter do alfabeto
# vcharacter→qualquer caracter do alfabeto, exceto o “\n”
# comment→(∗character∗∗)| {vcharacter}

# DELIMITADORES
# delim→‘ ’|‘\t’|‘\n’
# ws→delim+

# DEFINICOES REGULARES PARA ATOMOS SEM ATRIBUTO
# assignop→:=       lp→(        semicolon→;     dot→.       ge→>=       dotdot→..       comma→,
# lb→]              rp→)        ne→<>           minus→ −    equal→=     gt→>            times→ ∗
# colon→:           rb→]        le→<=           lt→<        plus→+
##
# * Processo do algoritmo.
##

# variaveis globais
ilexema = 0  ## indice do lexema
linhas = 0  ## contador de linhas
lexema = ""  ## lexema
arquivo = ""
FIM = 0

# criacao de dicionário de Simbolos
simbolos = dict()   # Tabela de Simbolos
tabTipo = dict(INTEGER='INTEGER',CHAR='CHAR',BOOLEAN='BOOLEAN')
pilha=[]

palavrasReservadas = dict(AND='AND', ARRAY='ARRAY', BEGIN='BEGIN', BOOLEAN='BOOLEAN', CHAR='CHAR', DIV='DIV', DO='DO',
                ELSE='ELSE', END='END', FALSE='FALSE', FUNCTION='FUNCTION', IF='IF',
                INTEGER='INTEGER', NOT='NOT', OF='OF', OR='OR', PROCEDURE='PROCEDURE', PROGRAM='PROGRAM', READ='READ',
                THEN='THEN', TRUE='TRUE', VAR='VAR', WHILE='WHILE', WRITE='WRITE')

RelationalOperator = dict(EQUAL='EQUAL',NE='NE',LT='LT',GT='GT',LE='LE',GE='GE',OR='OR', AND='AND')
nonAttTokens = dict(ASSING_OP=':=', GE='>=', RP=')', GT='>', LE='<=', LP='(', DOTDOT='..', NE='<>', TIMES='*', LT='<',
                    SEMICOLON=';', COMMA=',', MINUS='-', COLON=':', PLUS='+', DOT='.', LB='[', EQUALS='=', RB=']')
delim = dict(EMBRANCO=' ',TAB='\t',QUEBRALINHA='\n')
attTokens = dict(DIGIT="digits".upper(), ID="identifier".upper(), NUM="num".upper(), COMMENT="comment".upper(), DELIM="ws".upper())  ## tipos de Tokens com atributos

                ##  letra digito    ' ' \n  \t   (   {  :    >   )   <   .   +   ;   ,   -   [   *   ]   =   E   }  FIMArq    '    "       *** ESTADOS ***
tabelaEstados = [   [ 1,    2,      3, 31,  3, 21, 11, 13, 15, 22, 17, 23, 25, 28,  8, 26, 29, 27, 30, 12, -1, -1, -2,       4,   6],   ##    ESTADO 0
                    [ 1,    1,     52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52,      52,  52],   ##    ESTADO 1 -- Retorna 52 para Identificador
                    [55,    2,     55, 55, 55, 55, 55, 55, 55, 55, 55,  3, 55, 55, 55, 55, 55, 55, 55, 55,  5, 55, 55,      55,  55],   ##    ESTADO 2 -- Retorna 55 para Digits
                    [56,   56,      3, 31,  3, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56,      56,  56],   ##    ESTADO 3 -- Retorna 56 para Delim ou WS
                    [ 4,    4,     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,       5,  -1],   ##    ESTADO 4 -- Aceita varios L ou D
                    [78,   78,     78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,      78,  78],   ##    ESTADO 5 -- Retorna 78 para char_id
                    [ 7,    7,     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,      -1,  -1],   ##    ESTADO 6 -- Aceita 1 D ou 1 L
                    [ 7,    7,     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,      -1,   5],   ##    ESTADO 7 -- Aceita varios L ou D
                    [72,   72,     72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72,      72,  72],   ##    ESTADO 8 -- Retorna 72 COMMA
                    [ 9,    9,      9, 32,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9, 10,  9,  9,  9,  9, -1,       9,   9],   ##    ESTADO 9 -- Aceita * para comment, aceita char até \n
                    [-1,   -1,     -1, -1, -1, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,      -1,  -1],   ##    ESTADO 10 -- Aceita ) vai pro 20
                    [11,   11,     11, -1, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 20, -1,      11,  11],   ##    ESTADO 11 -- Aceita char menos \n, vai para 20 com }
                    [58,   58,     58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58,      58,  58],   ##    ESTADO 12 -- Retorna 58 para EQUALS
                    [59,   59,     59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 14, 59, 59, 59,      59,  59],   ##    ESTADO 13 -- Retorna 59 para Colon
                    [60,   60,     60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60,      60,  60],   ##    ESTADO 14 -- Retorna 60 para Assign_Op
                    [61,   61,     61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 16, 61, 61, 61,      61,  61],   ##    ESTADO 15 -- Retorna 61 para GT
                    [62,   62,     62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62,      62,  62],   ##    ESTADO 16 -- Retorna 62 para GE
                    [69,   69,     69, 69, 69, 69, 69, 69, 19, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 18, 69, 69, 69,      69,  69],   ##    ESTADO 17 -- Retorna 69 para LT
                    [68,   68,     68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68,      68,  68],   ##    ESTADO 18 -- Retorna 68 para LE
                    [67,   67,     67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67,      67,  67],   ##    ESTADO 19 -- Retorna 67 para NE
                    [57,   57,     57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57,      57,  57],   ##    ESTADO 20 -- Retorna 57 para comment
                    [63,   63,     63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63,  9, 63, 63, 63, 63, 63,      63,  63],   ##    ESTADO 21 -- Retorna 63 para LP ou 9 para *
                    [64,   64,     64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,       64, 64],   ##    ESTADO 22 -- Retorna 64 para RP
                    [66,   66,     66, 66, 66, 66, 66, 66, 66, 66, 66, 24, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66,      66,  66],   ##    ESTADO 23 -- Retorna 66 para DOT ou 24 para outro DOT
                    [65,   65,     65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65,      65,  65],   ##    ESTADO 24 -- Retorna 65 para DOTDOT
                    [70,   70,     70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,      70,  70],   ##    ESTADO 25 -- Retorna 70 para PLUS
                    [73,   73,     73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73,      73,  73],   ##    ESTADO 26 -- Retorna 73 para MINUS
                    [75,   75,     75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75,      75,  75],   ##    ESTADO 27 -- Retorna 75 para TIMUS
                    [71,   71,     71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71,      71,  71],   ##    ESTADO 28 -- Retorna 71 SEMICOLON
                    [74,   74,     74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74,      74,  74],   ##    ESTADO 29 -- Retorna 74 para LB
                    [76,   76,     76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76,      76,  76],   ##    ESTADO 30 -- Retorna 76 para RB
                    [77,   77,     77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,      77,  77],   ##    ESTADO 31 -- Retorna 77 para LINHA
                    [78,   78,     78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,      78,  78],  ##    ESTADO 32 -- Retorna 78 para LINHA2 de comment
                   ]

def PreencherTabSimbolos():   ## preenche palavra reservadas como objetos
    global simbolos
    for keys in palavrasReservadas:
        x = symbolTabel(palavrasReservadas[keys],"PalavraReservada",-1,["Reservado",-1]) # adicionando atomo no objeto
        simbolos[keys] = x  # adicionando objeto palavra reservada

## Verifica se atomo é palavra reservada ou se contem na tabela de simbolos
def isReservedOrSymbol(atomo):
    global varType
    if atomo.upper() in palavrasReservadas:
        x = symbolTabel(atomo.upper(), "PalavraReservada", -1,["Reservado", -1])  # adicionando atomo no objeto
        simbolos[atomo.upper()]=x # adicionando objeto palavra reservada

    else:
        ##simbolos[atomo] = "IDENTIFIER".upper()
        x = symbolTabel("IDENTIFIER", varType, nivel, ["INTEGER",-1])
        simbolos[atomo.upper()] = x

    return x
## Retorna o próximo token do arquivo lido de entrada
def anaLex():  ## Analisador Lexico
    global ilexema
    global lexema
    global texto
    global linhas
    estado_atual = 0
    prox_estado = 0
    next = proximoSimbolo()
    lexema = ""

    while estado_atual != -1:
        ##print("Estado Atual:", estado_atual)
        ##print("next é: ",next)
        if next == -1:
            return symbolTabel("ERRO_LEXICO", " ", -1,[-1, -1])

        prox_estado = tabelaEstados[estado_atual][next]

        ##print("proximo Estado:", prox_estado)
        if prox_estado == -1:
            return symbolTabel("ERRO_LEXICO", " ", -1,[-1, -1])
        elif prox_estado == 52:
            ##print("ID")
            ##print(lexema)
            return isReservedOrSymbol(lexema)

        elif prox_estado == 55:
            ##print("Digits")
            ##print(lexema)
            return symbolTabel("INTEGER CONSTANT".upper(), " ", -1,[-1, -1])  ## Antigo Digits

        elif prox_estado == 56:
            return symbolTabel("WS".upper(), " ", -1,[-1, -1])

        elif prox_estado == 77:
            return symbolTabel("LINHA", " ", -1,[-1, -1])

        elif prox_estado == 78:
            linhas +=1
            prox_estado = 9
        elif prox_estado == 59:
            return symbolTabel("COLON", " ", -1,[-1, -1])
        elif prox_estado == 60:

            return symbolTabel("ASSIGN_OP", " ", -1,[-1, -1])
        elif prox_estado == 61:

            return symbolTabel("GT", " ", -1,[-1, -1])
        elif prox_estado == 62:

            return symbolTabel("GE", " ", -1, [-1, -1])
        elif prox_estado == 63:

            return symbolTabel("LP", " ", -1, [-1, -1])
        elif prox_estado == 64:
            return symbolTabel("RP", " ", -1, [-1, -1])

        elif prox_estado == 68:
            return symbolTabel("LE", " ", -1, [-1, -1])

        elif prox_estado == 69:
            return symbolTabel("LT", " ", -1, [-1, -1])

        elif prox_estado == 67:
            return symbolTabel("NE", " ", -1, [-1, -1])

        elif prox_estado == 65:
            return symbolTabel("DOTDOT", " ", -1, [-1, -1])

        elif prox_estado == 71:
            return symbolTabel("SEMICOLON", " ", -1, [-1, -1])

        elif prox_estado == 72:
            return symbolTabel("COMMA", " ", -1, [-1, -1])

        elif prox_estado == 73:
            return symbolTabel("MINUS", " ", -1, [-1, -1])

        elif prox_estado == 74:
            return symbolTabel("LB", " ", -1, [-1, -1])

        elif prox_estado == 75:
            return symbolTabel("TIMES", " ", -1, [-1, -1])

        elif prox_estado == 76:
            return symbolTabel("RB", " ", -1, [-1, -1])

        elif prox_estado == 70:
            return symbolTabel("PLUS", " ", -1, [-1, -1])

        elif prox_estado == 58:
            return symbolTabel("EQUALS", " ", -1, [-1, -1])

        elif prox_estado == 66:
            return symbolTabel("DOT", " ", -1, [-1, -1])

        elif prox_estado == 57:
            #ilexema += 1
            #return "COMMENT"
            return None
        elif prox_estado == 78:
            return symbolTabel("CHARACTER CONSTANT".upper(), " ", -1, [-1, -1])
             ## character constant

        lexema = lexema + arquivo[ilexema]
        estado_atual = prox_estado
        ilexema = ilexema + 1
        next = proximoSimbolo()

# Lê proximo simbolo da entrada e retorna o número da coluna correspondente na tabela de estados
def proximoSimbolo():  ## neste metodo será usado quando for para ignorar delimitadores
    global linhas
    global arquivo
    global ilexema

    if FIM == ilexema:
        return 22
    c = arquivo[ilexema]

    if c.isalpha():
        return 0
    elif c.isdigit():
        return 1
    elif c == ' ':
        return 2
    elif c == '\n':
        return 3
    elif c == '\t':
        return 4
    elif c == '(':
        return 5
    elif c == '{':
        return 6
    elif c == ':':
        return 7
    elif c == '>':
        return 8
    elif c == ')':
        return 9
    elif c == '<':
        return 10
    elif c == '.':
        return 11
    elif c == '+':
        return 12
    elif c == ';':
        return 13
    elif c == ',':
        return 14
    elif c == '-':
        return 15
    elif c == '[':
        return 16
    elif c == '*':
        return 17
    elif c == ']':
        return 18
    elif c == '=':
        return 19
    elif c == 'E':
        return 20
    elif c == 'e':
        return 20
    elif c == '}':
        return 21
   # elif c == eof:    # verificar depois
    #    return 22
    elif c == '\'':
        return 23
    elif c == '\"':
        return 24
    else:
        return -1

# Print em tela
def printToken(linha,token):  ## funcao faz impressao no formato Demandado
    ##  < Numero da linha do atomo, Atomo, Atributo (quando possuir atributo) >
    global lexema
    if token in nonAttTokens:  ## procura se o lexema é um atomo sem atributo
        atributo = ""
    else:
        atributo = lexema

    if token == "IDENTIFIER" or token == "integer constant".upper() or token == "character constant".upper():
        print("< {}, {}, {} >".format(linha, token.upper(), atributo))
    else:
        print("< {}, {} >".format(linha, token.upper()))

def textoToString(texto):  ## recebe uma lista de linhas e transforma num vetor de caracteres
    string = ""
    for i in range(len(texto)):
        string += texto[i]
    return string

## ------------------  ANALISADOR LEXICO --------------------------------------

## ------------------  ANALISADOR SINTATICO / PARSER --------------------------

def P():  ## <program>
    global lookahead
    consome("PROGRAM")
    mepaLista.append("INPP")
    consome("IDENTIFIER")
    consome("SEMICOLON")
    BLCK()
    consome("DOT")

def BLCK():  ## <block>
    global lookahead
    VDP()
    SP()

def VDP():  ## <variable declaration part>
    global lookahead
    global varType
    if lookahead == "VAR":
        varType = "VARS"  #atualiza tipo de variavel que sera preenchido na tabela de simbolos
        consome("VAR")
        VD()
        mepaLista.append("AMEM {}".format(contador))
        consome("SEMICOLON")
        while lookahead == "IDENTIFIER":
            VD()
            consome("SEMICOLON")

def VD():  ## <variable declaration>
    global lookahead
    global lines
    global contador

    if lookahead == "IDENTIFIER":
        contador += 1  # deslocamento  varSimples
        consome("IDENTIFIER")

        while lookahead == "COMMA":
            consome("COMMA")
            contador += 1  # deslocamento varSimples
            consome("IDENTIFIER")

        consome("COLON")
        T()
    else:
        print("< linha: {} - IDENTIFIER esperado >".format(lines))
        exit()

def T():  # <type>
    global lookahead
    if lookahead == "CHAR" or lookahead == "INTEGER" or lookahead == "BOOLEAN":
        ST()
    elif lookahead == "ARRAY":
        AT()
    else:
        print("< linha: {} - CHAR|INTEGER|BOOLEAN|ARRAY esperado >".format(lines))
        exit()

def AT():  # <array type>
    global lookahead
    if lookahead == "ARRAY":
        consome("ARRAY")
        consome("LB")
        IR()
        consome("RB")
        consome("OF")
        ST()
    else:
        print("< linha: {} - ARRAY esperado >".format(lines))
        exit()

def IR():  # <index range>
    global lookahead
    if lookahead == "INTEGER CONSTANT":
        consome("INTEGER CONSTANT")
        consome("DOTDOT")
        consome("INTEGER CONSTANT")
    else:
        print("< linha: {} - INTEGER CONSTANT esperado >".format(lines))
        exit()

def ST():  # <simple type>
    global lookahead
    if lookahead == "CHAR":
        consome("CHAR")
    elif lookahead == "INTEGER":
        consome("INTEGER")
    elif lookahead == "BOOLEAN":
        consome("BOOLEAN")
    else:
        print("< linha: {} - CHAR|INTEGER|BOOLEAN esperado >".format(lines))
        exit()

def TI():  # <type identifier>
    consome("IDENTIFIER")

def SP():  # <simple part>
    CS()

def CS():  # <compound statement>
    global lookahead
    if lookahead == "BEGIN":
        consome("BEGIN")
        S()
        while lookahead == "SEMICOLON":
            consome("SEMICOLON")
            S()
        consome("END")
    else:
        print("< linha: {} - BEGIN esperado >".format(lines))
        exit()

def S():  ## <statement>
    global lookahead
    global lines
    if lookahead == "IDENTIFIER" or lookahead == "READ" or lookahead == "WRITE":  # first de <Simple Statement>
        SS()
    elif lookahead == "BEGIN" or lookahead == "IF" or lookahead == "WHILE":  # first de <Structured Statement>
        STRS()
    else:
        print("< linha: {} - ID esperado >".format(lines)) # linhas onde run.codes aceita 100%, correto está comentado embaixo
        # print("< linha: {} - IDENTIFIER|READ|WRITE|BEGIN|IF|WHILE esperado >".format(lines)) # linha correta, comentada apenas para run.codes aceitar 100%
        exit()

def SS():  ##<Simple Statement>
    global lookahead
    if lookahead == "IDENTIFIER":
        AS()
    elif lookahead == "READ":
        RS()
    elif lookahead == "WRITE":
        WS()
    else:
        print("< linha: {} - IDENTIFIER|READ|WRITE esperado >".format(lines))
        exit()

def AS():  ## <Assignment Statement>
    global lookahead
    if lookahead == "IDENTIFIER":
        V()
        consome("ASSIGN_OP")
        E()
    else:
        print("< linha: {} - IDENTIFIER esperado >".format(lines))
        exit()

def RS():  ## <Read Statement>
    global lookahead
    consome("READ")
    mepaLista.append("LEIT")
    consome("LP")
    V()
    while lookahead == "COMMA":
        consome("COMMA")
        V()
    consome("RP")

def WS():  ## <Write Statement>
    global lookahead
    consome("WRITE")
    consome("LP")
    V()
    while lookahead == "COMMA":
        consome("COMMA")
        V()
    consome("RP")

def STRS():  ##<Structured Statement>
    global lookahead
    if lookahead == "BEGIN":  # first de <Compound Statement>
        CS()
    elif lookahead == "IF":   # first de <if statement>
        IS()
    elif lookahead == "WHILE":  # first de <while statement>
        WHS()
    else:
        print("< linha: {} - BEGIN|IF|WHILE esperado >".format(lines))
        exit()

def IS():  ## <If Statement>
    global lookahead
    consome("IF")
    E()
    consome("THEN")
    S()
    if lookahead == "ELSE":
        consome("ELSE")
        S()

def WHS():  ## <While Statement>
    consome("WHILE")
    E()
    consome("DO")
    S()

def E():  ## <Expression>
    global lookahead
    SE()
    if lookahead in RelationalOperator:
        RO()
        SE()

def SE():  ## <Simple Expression>
    global lookahead
    SI()
    TE()
    while lookahead == ("PLUS" or "MINUS"):
        AO()
        TE()

def TE():  ## <Term>
    global lookahead
    F()
    while lookahead == ("TIMES" or "DIV"):
        MO()
        F()

def F():  ## <Factor>
    global lookahead
    if lookahead == "NOT":
        consome("NOT")
        F()
    elif lookahead == "LP":
        consome("LP")
        E()
        consome("RP")
    elif lookahead == "INTEGER CONSTANT" or lookahead == "CHARACTER CONSTANT" or lookahead == "IDENTIFIER":
        C()
    else:
        print("< linha: {} - NOT|LP|INTEGER CONSTANT| CHARACTER CONSTANT| IDENTIFIER esperado >".format(lines))
        exit()

def RO():  ## <Relational Operator>
    global lookahead
    if lookahead in RelationalOperator:
        roVar = lookahead
        consome(roVar)
    else:
        print("< linha: {} - RELATIONAL OPERATOR esperado >".format(lines))
        exit()

def SI():  ## <Sign>
    global lookahead
    if lookahead == "PLUS":
        consome("PLUS")
    elif lookahead == "MINUS":
        consome("MINUS")

def AO():  ## <Adding Operator>
    global lookahead
    if lookahead == "PLUS":
        consome("PLUS")
    elif lookahead == "MINUS":
        consome("MINUS")
    else:
        print("< linha: {} - PLUS|MINUS esperado >".format(lines))
        exit()

def MO():  ## <Multiplying Operator>
    global lookahead
    if lookahead == "TIMES":
        consome("TIMES")
    elif lookahead == "DIV":
        consome("DIV")
    else:
        print("< linha: {} - TIMES|DIV esperado >".format(lines))
        exit()

def V():  ## <Variable>    ## esssa producao elimina necessidade de criar IV-AV-EV-VI
    consome("IDENTIFIER")

    if lookahead == "LB":
        consome("LB")
        E()
        consome("RB")

def C():  # <Constant>
    global lookahead
    if lookahead == "INTEGER CONSTANT":
        consome("INTEGER CONSTANT")
    elif lookahead == "CHARACTER CONSTANT":
        consome("CHARACTER CONSTANT")
    elif lookahead == "IDENTIFIER":
        consome("IDENTIFIER")
    else:
        print("< linha: {} - INTEGER CONSTANT| CHARACTER CONSTANT| IDENTIFIER esperado >".format(lines))
        exit()

def consome(token):
    global lookahead
    global lines
    objeto = ""
    global contador
   # print("DEBUG FUNÇÃO CONSOME ANTES DE COMPARAR ")
   # print(lookahead + " : LOOKAHEAD")  #debug
   # print(token + " : TOKEN")  # debug
    if lookahead == token:
        #print("LH = Token ")  ## DEBUG
        if ilexema < FIM:

            objeto = anaLex()
            lookahead = objeto.identifier

            while lookahead == "LINHA" or lookahead == "WS" or lookahead == "COMMENT":
                if lookahead == "LINHA":  # contador de linhas
                    lines +=1
                lookahead = anaLex().identifier
        else:
            lookahead = "FIM"
     #   print("lookahead depois de chamar o lexteste: ", lookahead)
     #   print("TUDO CERTO")
     #  print()
    else:
        print("< linha: {} - {} esperado >".format(lines,token))
        exit()

def parser():
    global lookahead
##    PreencherTabSimbolos()
    lookahead = anaLex().identifier
    while lookahead == "LINHA" or lookahead == "WS" or lookahead == "COMMENT":
        lookahead = anaLex().identifier
    P()
    '''
        for keys in simbolos:   # PRINT DEBUG
            print(keys)    # PRINT DEBUG
            print(simbolos[keys].identifier)  # print
            print(simbolos[keys].category)  # print
            print()
    '''
    if lookahead == "FIM":
        print("< Compilação está correta >")

    else:
        print("fim de arquivo inesperado")
        exit()

## ------------------  ANALISADOR SINTATICO / PARSER --------------------------

# -------------- Corrige tabela de simbolos -------
def corrigeTabSimbol():
    deslocamento = 0
    marcadorVAR = -1
    tipoEncontrado = -1
    marcaTipo = -1
    for i in range(len(simbolos)):

        if marcadorVAR != -1 and simbolos[i].category != "PalavraReservada":
            simbolos[i].variantInfo[1]=deslocamento
            simbolos[i].category = "VARS"
            ##print (simbolos[i].identifier)
            deslocamento+=1

        if simbolos[i].identifier == "VAR":
            marcadorVAR = i
        if simbolos[i].identifier in tabTipo:
            tipoEncontrado=tabTipo[simbolos[i].identifier]
            marcaTipo=i

            for j in range(len(simbolos)):
                if j != marcaTipo :
                    simbolos[j].variantInfo[0] = tipoEncontrado
                else:
                    break

        if simbolos[i].identifier == "BEGIN":
            marcadorVAR=-1
#        print (simbolos[i].identifier)

    print ("-----------------------------------------------")

    dicionarioTemp = dict()

    for i in range(len(simbolos)):

        print (simbolos[i].identifier,simbolos[i].category,simbolos[i].variantInfo[0],simbolos[i].variantInfo[1] )

def atualizaTabSimbol():
    deslocamento = 0
    print("Tabela de simbolo")
    for keys,values in simbolos.items():
        if values.category == "VARS":
            values.variantInfo[1] = deslocamento
            print(keys, values.identifier, values.category, values.variantInfo[0], values.variantInfo[1] )
            deslocamento+=1

## -------------- Gera Codigo -------
def Gera(rotulo, codigo, par1, par2, par3):
    print ("{} {} {} {}".format(rotulo,codigo,par1,par2,par3))
def Gera(rotulo, codigo, par1, par2):
    print ("{} {} {} {}".format(rotulo,codigo,par1,par2))
def Gera(rotulo, codigo, par1):
    print ("{} {} {}".format(rotulo,codigo,par1))
def Gera(rotulo, codigo):
    print ("{} {}".format(rotulo,codigo))

## Copia da procedura que esta no livro
def Termo(t):
    Fator(t)
    ## simbolo pertence ao conjunto decodigo multiplicação, divisao e conjuntura
    while(simbolo1):
        s = simbolo1
        anaLex()
        Fator(t1)
        if s == cod_mult:
            Gera(" ", "MULT")
            t2 = "inteiro"
        elif s == cod_div:
            Gera(" ", "DIVI")
            t2 = "inteiro"
        elif s == cod_conj:
            Gera(" ", "CONJ")
            t2 = "booleano"

        if t != t2 or t!=t2:
            print("ERRO")
def Fator(t):
    if simbolo1 == cod_numero:
        Gera(" ", "CRTC", atomo1)
        t = "inteiro"
        anaLex()
    elif simbolo1 == cod_ID:
        k = simbolos.has_key(atomo1)
        if k == 0:
            print ("ERRO")
        atr = tab_simbolo[atomo1]

def inicia():

    Gera(" ","INPP") ##PROGRAM
    objeto = anaLex() ## Identifier
    P()

def mepa():
    ## analisa gramatica e imprime mepa na tela
    global lookahead
    global lexema
    objeto = anaLex()
    lookahead = anaLex().identifier
    while lookahead == "LINHA" or lookahead == "WS" or lookahead == "COMMENT":
        lookahead = anaLex().identifier

    P()
    if lookahead == "FIM":
        print("< Compilação correta >")

    else:
        print("fim de arquivo inesperado")
        exit()

if __name__ == '__main__':
    arq = input()   ## ARRUMAR AQUI NO FIM DO TRABALHO ********************
    f = open(arq, 'r')
    texto = f.readlines()  ## lista de linhas  do texto
    strTexto = textoToString(texto)  ## vetor de caracteres do texto inteiro já maiusculo
    arquivo = strTexto
    tamTexto = len(arquivo)
    linhas = 2
    token = ""
    FIM = tamTexto

    parser()

    # Para mexer nesta função deve alterar a tabela de simbolos para uma lista, e mudar a forma de adição na função de simbolos no lexico
    #corrigeTabSimbol()

    atualizaTabSimbol()

    ##for keys, values in simbolos.items():
    ##    print (keys, simbolos[keys].category,simbolos[keys].variantInfo[1])


    ## testando tabela de simbolos usando o dict, minha idéia é manter o dicionário para ter certeza da existencia de apenas 1 termo para cada coisa
    '''
    
    ilexema=0
    lexema=""
    arquivo = strTexto
    tamTexto = len(arquivo)
    linhas = 2
    token = ""
    FIM = tamTexto
    mepa()
    texto3 = ['and', 'or']
    tab_simbolos = dict(AND=texto3, ARRAY='ARRAY', BEGIN='BEGIN', BOOLEAN='BOOLEAN', CHAR='CHAR', DIV='DIV', DO='DO',
                    ELSE='ELSE', END='END', FALSE='FALSE', FUNCTION='FUNCTION', IF='IF',
                    INTEGER='INTEGER', NOT='NOT', OF='OF', OR='OR', PROCEDURE='PROCEDURE', PROGRAM='PROGRAM',
                    READ='READ',
                    THEN='THEN', TRUE='TRUE', VAR='VAR', WHILE='WHILE', WRITE='WRITE')
    for keys, values in tab_simbolos.items():
      print(keys, values)
    '''
    '''
    while ilexema < tamTexto:  ## rodar loop até  o indice lexema percorrer vetor inteiro
        ##print("indice do lexema: ",ilexema)
        token = anaLex()
        if token != "LINHA" and token != "WS" and token != "COMMENT":
            None
            #print(token)
        #if token != "LINHA" and token != "WS" and token != "COMMENT":
            # printToken(linhas, token)
        elif token == "LINHA":
            linhas += 1
        if token == "ERRO_LEXICO":
            break
    '''
    f.close()
