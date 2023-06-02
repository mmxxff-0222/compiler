from ply import lex
# List of token names.   This is always required
# 标记的列表
tokens = (
    'IDN','DEC','OCT','HEX','ASSIGN','FLOAT',
    'ADD', 'SUB', 'MUL', 'DIV', 'GT', 'LT', 'EQ', 'GE', 'LE', 'NEQ',
    'SLP', 'SRP', 'SEMI', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'BEGIN', 'END',
    'ILOCT','ILHEX'
)

# Regular expression rules for simple tokens
# 标记的规则定义
'''
顺序很重要！！！
1 所有由方法定义的标记规则，按照他们的出现顺序依次加入
2 由字符串变量定义的标记规则按照其正则式长度倒序后，依次加入（长的先入）
'''
def t_OCT(t):
    r'0(0|1|2|3|4|5|6|7)(0|1|2|3|4|5|6|7)*[ ]'
    t.value = int(t.value,8)
    return t
def t_ILOCT(t):
    r'0(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*[ ]'
    # t.value = t
    return t
def t_HEX(t):
    r'0(x|X)(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|A|B|C|D|E|F)*[ ]'
    t.value = int(t.value,16)
    return t
def t_ILHEX(t):
    r'0(x|X)([a-z]|[0-9]|[A-Z])([a-z]|[0-9]|[A-Z])+[ ]'
    # t.value = ''
    return t
def t_FLOAT(t):
    r'([1-9]\d*\.\d+|0\.\d+)'
    t.value = float(t.value)
    return t

def t_DEC(t):
    r'0|(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*([ ]|)'
    t.value = int(t.value)
    return t

def t_ADD(t):
    r'\+'
    t.value = '+'
    return t
def t_SUB(t):
    r'-'
    t.value = '-'
    return t
def t_MUL(t):
    r'\*'
    t.value = '*'
    return t
def t_DIV(t):
    r'/'
    t.value = '/'
    return t
def t_GE(t):
    r'>='
    t.value = '>='
    return t
def t_LE(t):
    r'<='
    t.value = '<='
    return t
def t_NEQ(t):
    r'<>'
    t.value = '<>'
    return t
def t_GT(t):
    r'>'
    t.value = '>'
    return t
def t_LT(t):
    r'<'
    t.value = '<'
    return t
def t_EQ(t):
    r'=='
    t.value = '=='
    return t
def t_ASSIGN(t):
    r'='
    t.value = '='
    return t
def t_SLP(t):
    r'\('
    t.value = '('
    return t
def t_SRP(t):
    r'\)'
    t.value = ')'
    return t
def t_SEMI(t):
    r';'
    t.value = ';'
    return t
def t_IF(t):
    r'if'
    t.value = 'if'
    return t
def t_THEN(t):
    r'then'
    t.value = 'then'
    return t
def t_ELSE(t):
    r'else'
    t.value = 'else'
    return t
def t_WHILE(t):
    r'while'
    t.value = 'while'
    return t
def t_DO(t):
    r'do'
    t.value = 'do'
    return t
def t_BEGIN(t):
    r'begin'
    t.value = 'begin'
    return t
def t_END(t):
    r'end'
    t.value = 'end'
    return t

def t_IDN(t):
    r'([a-z]|[A-Z])([0-9]|[a-z]|[A-Z]|_|)*'
    return t
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 忽略空格、tab
t_ignore  = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character {}" .format(t.value))
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()