import nltk

arquivo = open('Fonte.txt','r')
le = arquivo.read()
le = le.strip()
arquivo.close()
r = '\w+|\,|\:=|\:|\+|\;|.'
tokenizador = nltk.RegexpTokenizer(r)
ListaDeTermos = tokenizador.tokenize(le)
tokens = []
ReservedWords = ['var',':',',','integer','real','id',':=','+','if','then']

for i in ListaDeTermos:
    if(i.lower() != ' '):
        tokens.append(i.lower())
print tokens
l = list(map(chr,range(ord('a'), ord('z') + 1))) +\
                     list('_')
n = list(map(chr,range(ord('0'), ord('9') + 1)))
def identifier(s):
    if(s in ReservedWords):
        return False
    if(s[0] in l):
        for i in xrange(len(s[1:])):
            if(s[i] not in (n+l)):
                return False
        return True
    else:
        return False
temporario = 1
quad = 0
proximo = 0
quadrupla = []
def geraTemporario():
    global temporario
    temporario = temporario + 1
    return 't'+str(temporario-1)
def geraOuRemenda(p1, p2, p3, p4, p5):
    quadrupla.insert(p1,[p2,p3,p4,p5])
def nTermR(tokens,i,Resq):
    global proximo
    if(len(tokens) > i and tokens[i] == '+'):
        s = nTermT(tokens,i+1)
        if(s[1] == True):
            R1dir = s[2]
            s = nTermR(tokens,s[0],s[2])
            if(s[1] == True):
                Rdir = geraTemporario()
                geraOuRemenda(proximo,'+', Resq, R1dir, Rdir)
                proximo = proximo + 1
                return s[0], s[1], Rdir
            else:
                return s
        else:
            return s
    else:
        return i, True, Resq
def nTermT(tokens,i):
    if(len(tokens) > i and identifier(tokens[i])):
        return i+1, True, tokens[i] #tokens[i] = T.dir
    else:
        return i, False
def nTermE(tokens,i):
    s = nTermT(tokens,i)
    if(s[1] == True):
        Resq = s[2]
        return nTermR(tokens,s[0],Resq)
    else:
        return s[0], False
def nTermS(tokens,i):
    global proximo, quad
    if(len(tokens) > i and tokens[i] == 'if'):
        s = nTermE(tokens,i+1)
        if(s[1] == True):
            if(len(tokens) > s[0] and tokens[s[0]] == 'then'):
                S1quad = proximo
                proximo = proximo + 1
                Edir = s[2]
                s = nTermS(tokens,s[0]+1)
                if(s[1] == True):
                    geraOuRemenda(S1quad,'JF',Edir,proximo+1,'')
                    return s
                else:
                    return s[0], False
            else:
                return s[0], False
        else:
            return s
    elif(len(tokens) > i and identifier(tokens[i])):
        if(len(tokens) > i+1 and tokens[i+1] == ':='):
            s = nTermE(tokens,i+2)
            if(s[1] == True):
                Eesq = s[2]
                Edir = tokens[i]
                geraOuRemenda(proximo,':=',Edir,'',Eesq)
                proximo = proximo + 1
                return s
            else:
                return s[0], False
        else:
            return i+1, False
    else:
        return i, False
def nTermX(tokens,i):
    if(len(tokens) > i and tokens[i] == ','):
        return nTermL(tokens,i+1)
    else:
        return i, True
def nTermL(tokens,i):
    if(len(tokens) > i and identifier(tokens[i])):
        return nTermX(tokens,i+1)
    else:
        return i, False
def nTermK(tokens,i):
    if(len(tokens) > i and tokens[i] == 'integer' or tokens[i] == 'real'):
        return i+1, True
    else:
        return i, False
def nTermO(tokens,i):
    if(len(tokens) > i and tokens[i] == ';'):
        return nTermD(tokens,i+1)
    else:
        return nTermS(tokens,i)
def nTermD(tokens,i):
    i = nTermL(tokens,i)
    if(len(tokens) > i[0] and i[1] == True and tokens[i[0]] == ':'):
        i = nTermK(tokens,i[0]+1)
        if(i[1] == True):
            return nTermO(tokens,i[0])
        else:
            return i
    else:
        return i[0], False
def nTermI(tokens,i):
    if(len(tokens) > i and tokens[i] == 'var'):
        return nTermD(tokens,i+1)
    else:
        return i, False
erro = nTermI(tokens,0)
if(erro[0] < len(tokens)):
    print 'Erro antes de: ',tokens[erro[0]]
tabelaSimb = []
def tokenNaLista(token,lista):
    for subList in lista:
        if(token in subList):
            return True
def funcSeman(tokens):
    if(erro[1] == False):
        if(erro[0] < len(tokens)):
            return erro[0], False
        else:
            return erro[0]-1, False
    else:
        i = 0
        pos1 = 0
        pos2 = 0
        while tokens[i] != 'var':
            i = i + 1
        while(tokens[i] == ';' or tokens[i] == 'var'):
            i = i + 1
            while tokens[i] != ':':
                if(tokens[i] != ','):
                    if(tokenNaLista(tokens[i],tabelaSimb)):
                        return i, False
                    else:
                        tabelaSimb.append([tokens[i],'id','var'])
                        pos2 = pos2 + 1
                i = i + 1
            i = i + 1
            while pos1 < pos2:
                tabelaSimb[pos1].append(tokens[i])
                pos1 = pos1 + 1
            i = i + 1
            if(i >= len(tokens)):
                return i, False
        print 'Tabela de simbolos: ',tabelaSimb
        tabTipos = []
        pos1 = 0
        while(i < len(tokens)):
            if(tokens[i] == 'if' or tokens[i] == '+' or tokens[i] == 'then' or tokens[i] == ':='):
                if(tokens[i] == 'then'):
                    pos1 = pos1 + 1
                i = i + 1
            if(tokens[i] == 'if'):
                i = i + 1
            if(not tokenNaLista(tokens[i],tabelaSimb)):
                return i, False, 'Variavel nao declarada: '
            tabTipos.append([tokens[i],pos1,i])
            i = i + 1
        aux = 0
        pos2 = 0
        listAux = []
        def funcTiposIguais(lista):
            aux = lista[0][0]
            for i in xrange(len(lista)):
                if(aux != lista[i][0]):
                    return lista[i][1]
            return -1
        while aux < len(tabTipos):
            aux2 = 0
            if(tabTipos[aux][1] != pos2):
                aux3 = funcTiposIguais(listAux)
                if(aux3 != -1):
                    return aux3, False, 'Incompatible variable type: '
                pos2 = pos2 + 1
                listAux = []
            for j in xrange(len(tabelaSimb)):
                if(tabTipos[aux][0] in tabelaSimb[j]):
                    aux2 = j
            if(pos2 == tabTipos[aux][1]):
                listAux.append([tabelaSimb[aux2][3],tabTipos[aux][2]])
            aux = aux + 1
        aux3 = funcTiposIguais(listAux)
        if(aux3 != -1):
            return aux3, False, 'Tipo incompativel: '
        return i, True
erro = funcSeman(tokens)
if(erro[1] == False):
    if(len(erro) == 2):
        print 'Erro antes de:',tokens[erro[0]]
    else:
        print erro[2],tokens[erro[0]]
print 'Entrada:\n', le
print '\nSaida:'
for i in xrange(len(quadrupla)):
    print quadrupla[i]
