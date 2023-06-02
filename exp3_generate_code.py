from node import node,num_node
tmp_count = 1  # 用于生成临时变量的计数器
def newTemp():
    global tmp_count
    temp = 't'+str(tmp_count)
    tmp_count += 1
    return temp


label_count = 0  # 用于生成临时变量的计数器
def newLabel():
    global label_count
    label = 'L'+str(label_count)
    label_count += 1
    return label

# 生成三地址代码
def generate_code(node):
    '''
    通过 if elif 语句实现不同文法对应的制导规则
    :param node: AST中的结点
    :return: 该结点对应的三地址代码
    '''
    if node.getdata() == '[PROGRAM_L]':
        ''' P → L '''
        code_L = generate_code(node.getchild(0))
        if node._flag == 1:
            node.getchild(0)._flag = 1
            node.getchild(0).setbegin(node.getbegin())
            node.getchild(0).setnext(node.getnext())
            code_L += node.getbegin()+node.getnext()+'\n'
        return code_L
    elif node.getdata() == '[PROGRAM_LP]':
        ''' P → L P1 '''
        code_L = generate_code(node.getchild(0))
        code_P1 = generate_code(node.getchild(1))
        if node._flag == 1:
            node.getchild(0)._flag = 1
            node.getchild(0).setbegin(node.getbegin())
            node.getchild(0).setnext(node.getnext())
            node.getchild(1)._flag = 1
            node.getchild(1).setbegin(node.getbegin())
            node.getchild(1).setnext(node.getnext())

        return code_L + '\n' + code_P1
    elif node.getdata() == '[LINE]':
        ''' L → S ; '''
        code_S = generate_code(node.getchild(0))
        if node._flag == 1:
            node.getchild(0)._flag = 1
            node.getchild(0).setbegin(node.getbegin())
            node.getchild(0).setnext(node.getnext())
        return code_S
    elif node.getdata() == '[BEGIN_END_statement]':
        ''' S → BEGIN P END '''
        # node.getchild(1)._flag = 1
        # node.getchild(1).setbegin(node.getbegin())
        # node.getchild(1).setnext(node.getnext())
        return generate_code(node.getchild(1))

    elif node.getdata() == '[ASSIGN_statement]':
        ''' S → id = E '''
        code_IDN = generate_code(node.getchild(0))
        code_E = generate_code(node.getchild(2))
        code_gen = node.getchild(0).getdata()+' := '+node.getchild(2).getplace()
        return code_E + '\n' + code_gen
    elif node.getdata() == '[IF_THEN_statement]':
        ''' S → if C then S1 '''
        if node.getnext() is None:
            node.setnext(newLabel())
            end_label = node.getnext() + ":"
        else:
            end_label = 'none'
        node.getchild(1).settrue(newLabel())    # C.true = newlabel
        node.getchild(1).setfalse(node.getnext())  # C.false = S.next;
        node.getchild(3).setnext(node.getnext())  # S1.next = S.next;
        node.getchild(3).setbegin(node.getchild(1).gettrue()) # s1.begin = c.true
        code_C = generate_code(node.getchild(1))
        code_gen = node.getchild(1).gettrue()+":"   # gen(C.true ‘:’)
        code_S1 = generate_code(node.getchild(3))

        # S.code = C.code || gen(C.true ‘:’) || S1.code || gen(S.next ':)
        return code_C + '\n' + code_gen + '\n' + code_S1 + '\n' + end_label
        # return code_C + '\n' + code_gen + '\n' + code_S1
    elif node.getdata() == '[IF_ELSE_statement]':
        ''' S → if C then S1 else S2 '''
        if node.getnext() is None:
            node.setnext(newLabel())
            end_label = node.getnext() + ":"
        else:
            end_label = 'none'
        node.getchild(1).settrue(newLabel())    # C.true = newlabel
        node.getchild(1).setfalse(newLabel())    # C.false = newlabel;
        node.getchild(3).setnext(node.getnext())  # S1.next = S.next;
        node.getchild(3).setbegin(node.getchild(1).gettrue()) # s1.begin = c.true
        node.getchild(5).setnext(node.getnext())  # S2.next = S.next;
        code_C = generate_code(node.getchild(1))
        true_label = node.getchild(1).gettrue()+":"   # gen(C.true ‘:’)
        code_S1 = generate_code(node.getchild(3))
        code_goto = 'goto ' + node.getnext()        #gen(‘goto’ S.next)
        false_label = node.getchild(1).getfalse()+":" # gen(C.false:’)
        code_S2 =generate_code(node.getchild(5))
        # C.code || gen(C.true ‘:’) || S1.code|| gen(‘goto’ S.next) || gen(C.false‘:’) || S2.code;
        return code_C + '\n' + true_label + '\n' + code_S1 + '\n' + code_goto + '\n' + false_label + '\n' + code_S2 + '\n' + end_label
    elif node.getdata() == '[WHILE_DO_statement]':
        ''' S → while C do S1 '''
        if node.getnext() is None:
            node.setnext(newLabel())
            end_label = node.getnext() + ":"
        else:
            end_label = 'none'
        if node.getbegin() is None:
            node.setbegin(newLabel())  # S.begin = newlabel;
            begin_label = node.getbegin() + ":"
        else:
            begin_label = 'none'
        # if node.getchild(3).getdata() == '[BEGIN_END_statement]':
        #     node.getchild(3).setbegin(node.getbegin())
        #     node.getchild(3).setnext(node.getnext())
        node.getchild(1).settrue(newLabel())    # C.true = newlabel;
        node.getchild(1).setfalse(node.getnext())   # C.false = S.next;
        node.getchild(3).setnext(node.getbegin())   # S1.next = S.begin;
        node.getchild(3).setbegin(node.getnext())  # S1.begin = S.next
        code_C = generate_code(node.getchild(1))
        true_label = node.getchild(1).gettrue()+":"
        cdoe_S1 = generate_code(node.getchild(3))
        code_go = 'goto '+node.getbegin()

        # S.code = gen(S.begin ‘:’) || C.code || gen(C.true ‘:’) || S1.code || gen(‘goto’ S.begin);
        # return begin_label + '\n' + code_C + '\n' + true_label + '\n' + cdoe_S1 + '\n' + code_go + '\n' + end_label
        return begin_label + '\n' + code_C + '\n' + true_label + '\n' + cdoe_S1 + '\n' + code_go + '\n' + end_label
    elif node.getdata() == '[CONDITION]':
        ''' C → E1 == E2 '''
        code_E1 = generate_code(node.getchild(0))
        code_E2 = generate_code(node.getchild(2))
        # C.code = E1.code || E2.code || gen(‘if ’ E1.place ‘ <|>|== ’ E2.place ‘goto’C.true) || gen(‘goto’ C.false)
        code_gen1 = 'if '+ node.getchild(0).getplace() + node.getchild(1).getdata() + node.getchild(2).getplace() + ' goto '+ node.gettrue()
        code_gen2 = 'goto ' + node.getfalse()
        return code_E1 + '\n' + code_E2 + '\n' + code_gen1 + '\n' + code_gen2
    elif node.getdata() == '[EXPRESSION_ADD]':
        ''' E → E1 + T'''
        node.setplace(newTemp())
        code_E1 = generate_code(node.getchild(0))
        code_T = generate_code(node.getchild(2))
        code_gen = node.getplace()+' := '+node.getchild(0).getplace()+' + '+node.getchild(2).getplace()
        return code_E1+'\n'+code_T + '\n' + code_gen
    elif node.getdata() == '[EXPRESSION_SUB]':
        ''' E → E1 - T'''
        node.setplace(newTemp())
        code_E1 = generate_code(node.getchild(0))
        code_T = generate_code(node.getchild(2))
        code_gen = node.getplace()+' := '+node.getchild(0).getplace()+' - '+node.getchild(2).getplace()
        return code_E1+'\n'+code_T+'\n'+code_gen
    elif node.getdata() == '[EXPRESSION_term]':
        ''' E → T '''
        code_T = generate_code(node.getchild(0))
        node.setplace(node.getchild(0).getplace())
        return  code_T
    elif node.getdata() == '[TERM_F]':
        ''' T → F '''
        code_F = generate_code(node.getchild(0))
        node.setplace(node.getchild(0).getplace())
        return  code_F
    elif node.getdata() == '[TERM_MUL]':
        ''' T → T1 * F '''
        node.setplace(newTemp())
        code_T1 = generate_code(node.getchild(0))
        code_F = generate_code(node.getchild(2))
        code_gen = node.getplace() + ' := ' + node.getchild(0).getplace() + ' * ' + node.getchild(2).getplace()
        return code_T1+'\n'+code_F+'\n'+code_gen
    elif node.getdata() == '[TERM_DIV]':
        ''' T → T1 / F '''
        node.setplace(newTemp())
        code_T1 = generate_code(node.getchild(0))
        code_F = generate_code(node.getchild(2))
        code_gen = node.getplace() + ' := ' + node.getchild(0).getplace() + ' / ' + node.getchild(2).getplace()
        return code_T1+'\n'+code_F + '\n' + code_gen
    elif node.getdata() == '[FACTOR]':
        ''' F → DEC | OCT | HEX | IDN | FLOAT'''
        code_t = generate_code(node.getchild(0))
        node.setplace(node.getchild(0).getplace())
        return  code_t
    elif node.getdata() == '[FACTOR_()]':
        ''' F → ( E ) '''
        code =generate_code(node.getchild(1))
        node.setplace(node.getchild(1).getplace())
        return code
    elif node.getdata() == '[DEC]' or node.getdata() == '[OCT]' or node.getdata() == '[HEX]' or node.getdata() == '[FLOAT]' :
        node.setplace(str(node.getchild(0).getvalue()))
        return 'none'
    elif node.getdata() == '[IDN]':
        node.setplace(str(node.getchild(0).getdata()))
        return 'none'

def generate(root):
    code = ' '*4 + generate_code(root)
    code = code.replace("none\n", "")  # 删除多余内容
    code = code.replace('\n','\n'+' '*4)
    code = code.replace('    L','L')
    code = code.replace(':\n    ',':'+' ')
    return code