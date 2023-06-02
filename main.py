# This is a sample Python script.
from exp1_lex import lexer
from exp2_yacc import parser
from exp3_generate_code import *
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.




def read_text(text):
    lines=[]
    for line in text.split('\n'):
        line=line.strip()
        if len(line)>0 and not line.startswith('#'):
            lines.append(line)
    return ' '.join(lines)
def exp1_test(text):
    print("-"*20 + 'exp1 词法分析'+'-'*20)
    print(text)
    lexer.input(text)
    while True:
        tok = lexer.token()
        if not tok: break  # No more input
        print(tok.type, " ", tok.value)

def exp2_test(text):
    print("-"*20 + 'exp2 语法分析'+'-'*20)
    print(text)
    ast = parser.parse(text)
    ast.print_node(0)
    return ast

def exp3_test(ast,text):
    print("-"*20 + 'exp3 中间代码生成'+'-'*20)
    print(text)
    code = generate(ast)
    print(code)
    return code


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = read_text(open(r'tests/begin_end', 'r').read())
    exp1_test(text)
    root = exp2_test(text)
    code = exp3_test(root,text)
    # print(code)

