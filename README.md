#Implementação de um compilador simples
Implementação de um analisador sintático descendente recursivo para analisar cadeias pertencentes à linguagem por ela gerada (utilizando funções para cada não-terminal), junto com sua representação através de grafos sintáticos.
G = ( {I,D,L,X,K,O,S,E,R,T}, {var, : , , , integer, real, id, :=, +, id, if, then}, P, I)
P:
I → var D
D → L : K O
L → id X
X → , L
X → ε
K → integer
K → real
O → ; D
O →ε
S → id := E
S → if E then S
E → T R
R → + T R
R → ε
T → id

Os grafos sintáticos, descrevem as ações semânticas de inserção dos identificadores na tabela de símbolos e de verificação de tipos. 

A implementação inclui a geração de código intermediário, com regras tais como previstas abaixo:
S → id := {E.esq = id.lexval} E {gera(‘:=‘, E.dir, , E.esq)}
E → T {R.esq = T.dir} R {E.dir = R.dir}
R → + T {R 1.esq = T.dir } R1{R.dir := geratemp; gera(‘+’, R.esq, R1.dir, R.dir)}
R → ε {R.dir = R.esq}
T → id {T.dir = id.lexval}
S → if E then {S1.quad := prox; prox := prox+1} S1{remenda(S 1 .quad, JF, E.dir, prox, ‘ ‘)}
Ps: O índice (1) serve apenas para diferenciar qual não terminal está sendo referido nas regras das ações semânticas. Na sintaxe, são os mesmos elementos. Exemplo: Na regra: R → + T R1 a, os dois Rs são o mesmo.
