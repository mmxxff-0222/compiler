from ply import lex
from ply import yacc
from exp1_lex import *
from node import node,num_node,float_node

# 定义语法规则
# 第一个定义的必须是 开始的非终结符
def p_program(p):
    '''
    program : line
            | line program
    '''
    if len(p) == 2:
        # p[0] = ('[PROGRAM]', p[1])
        p[0] = node('[PROGRAM_L]')
        p[0].add(p[1])
    else:
        # p[0] = ('program', p[1], p[2])
        p[0] = node('[PROGRAM_LP]')
        p[0].add(p[1])
        p[0].add(p[2])

def p_line(p):
    '''
    line : statement SEMI
    '''
    p[0] = node('[LINE]')
    p[0].add(p[1])
    p[0].add(node(p[2]))

def p_statement(p):
    '''
    statement : IDN ASSIGN expression
              | IF condition THEN statement
              | IF condition THEN statement ELSE statement
              | WHILE condition DO statement
              | BEGIN program END
    '''
    if len(p) == 4:
        if p.slice[1].type == 'IDN':
            # p[0] = ('ASSIGN_statement', p[1], p[3])
            p[0] = node("[ASSIGN_statement]")
            p[0].add(node(p[1]))
            p[0].add(node(p[2]))
            p[0].add(p[3])
        else :
            p[0] = node("[BEGIN_END_statement]")
            p[0].add(node(p[1]))
            p[0].add(p[2])
            p[0].add(node(p[3]))
    elif len(p) == 5:
        if p.slice[1].type == 'WHILE':
            p[0] = node("[WHILE_DO_statement]")
            p[0].add(node(p[1]))
            p[0].add(p[2])
            p[0].add(node(p[3]))
            p[0].add(p[4])
        else:
            p[0] = node("[IF_THEN_statement]")
            p[0].add(node(p[1]))
            p[0].add(p[2])
            p[0].add(node(p[3]))
            p[0].add(p[4])
    else:
        p[0] = node("[IF_ELSE_statement]")
        p[0].add(node(p[1]))
        p[0].add(p[2])
        p[0].add(node(p[3]))
        p[0].add(p[4])
        p[0].add(node(p[5]))
        p[0].add(p[6])

def p_condition(p):
    '''
    condition : expression GT expression
              | expression LT expression
              | expression EQ expression
              | expression GE expression
              | expression LE expression
              | expression NEQ expression
    '''
    p[0] = node("[CONDITION]")
    p[0].add(p[1])
    p[0].add(node(p[2]))
    p[0].add(p[3])



def p_expression(p):
    """
    expression : term
               | expression ADD term
               | expression SUB term
    """
    if len(p) == 2:
        p[0] = node('[EXPRESSION_term]')
        p[0].add(p[1])
    else:
        if p.slice[2].type == 'ADD':
            p[0] = node('[EXPRESSION_ADD]')
        else:
            p[0] = node('[EXPRESSION_SUB]')
        p[0].add(p[1])
        p[0].add(node(p[2]))
        p[0].add(p[3])


def p_term(p):
    """
    term : factor
         | term MUL factor
         | term DIV factor
    """
    if len(p) == 2:
        p[0] = node('[TERM_F]')
        p[0].add(p[1])
    else:
        if p.slice[2].type == 'MUL':
            p[0] = node('[TERM_MUL]')
        else:
            p[0] = node('[TERM_DIV]')
        p[0].add(p[1])
        p[0].add(node(p[2]))
        p[0].add(p[3])




def p_factor(p):
    """
    factor : IDN
           | DEC
           | FLOAT
           | OCT
           | HEX
           | ADD factor
           | SUB factor
           | SLP expression SRP
    """
    if len(p) == 2:
        p[0] = node("[FACTOR]")
        if(p.slice[1].type == 'DEC'):
            t = node("[DEC]")
            t.add(num_node(p[1]))
            p[0].add(t)
        elif (p.slice[1].type == 'FLOAT'):
            t = node("[FLOAT]")
            t.add(float_node(p[1]))
            p[0].add(t)
        elif (p.slice[1].type == 'OCT'):
            t = node("[OCT]")
            t.add(num_node(p[1]))
            p[0].add(t)
        elif (p.slice[1].type == 'HEX'):
            t = node("[HEX]")
            t.add(num_node(p[1]))
            p[0].add(t)
        else:
            t = node("[IDN]")
            t.add(node(p[1]))
            p[0].add(t)
    elif len(p) == 3:
        p[0] = node("unary")
        p[0].add(node(p[1]))
        p[0].add(p[2])
    else:
        p[0]=node("[FACTOR_()]")
        p[0].add(node(p[1]))
        p[0].add(p[2])
        p[0].add(node(p[3]))


def p_error(p):
    print(f'Syntax error at {p}')

parser = yacc.yacc()