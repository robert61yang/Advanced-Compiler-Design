from bril import Program, Label, Const, ValueOperation, EffectOperation
from bril import serialize_bril

var_type = {}

def type_change(var_type):
    if var_type == 'int':
        return 'i32'
    elif var_type == None:
        return 'void'
    elif var_type == 'bool':
        return 'i1'
    
def phi_function(instr):
    # breakpoint()
    ins = f'%{instr.dest}'
    ins += ' = phi '
    ins += type_change(instr.type)
    ins += ' '
    for i in range(len(instr.args)):
        if i != 0:
            ins += ', '
        ins += f'[ %{instr.args[i]}, %{instr.labels[i]} ]'
    # breakpoint()
    return ins

def lt_operation(instr):
    # breakpoint()
    ins = f'%{instr.dest}'
    ins += ' = icmp slt '
    ins += 'i32'
    # ins += type_change(instr.type)
    ins +=  ' '
    for idx, arg in enumerate(instr.args):
        if idx != 0:
            ins += ', '
        ins += f'%{arg}'
    # breakpoint()
    return ins

def eq_operation(instr):
        # breakpoint()
    ins = f'%{instr.dest}'
    ins += ' = icmp eq '
    ins += 'i32'
    # ins += type_change(instr.type)
    ins +=  ' '
    for idx, arg in enumerate(instr.args):
        if idx != 0:
            ins += ', '
        ins += f'%{arg}'
    # breakpoint()
    return ins

def op_check(op):
    if op == 'div':
        return 'sdiv'
    else:
        return op

def gt_operation(instr):
    ins = f'%{instr.dest}'
    ins += ' = icmp sgt '
    ins += 'i32'
    # ins += type_change(instr.type)
    ins +=  ' '
    for idx, arg in enumerate(instr.args):
        if idx != 0:
            ins += ', '
        ins += f'%{arg}'
    # breakpoint()
    return ins

def id_instr(instr):
    #{"op": "id", "dest": "tmp0", "type": "int", "args": ["input"]}
    ins = f'%{instr.dest} = add {type_change(instr.type)} 0, %{instr.args[0].lower()}'
    # breakpoint()
    return ins
    
def binary_instr(instr):
    # breakpoint()
    if instr.op == 'phi':
        return phi_function(instr)
    elif instr.op == 'lt':
        return lt_operation(instr)
    elif instr.op == 'eq':
        return eq_operation(instr)
    elif instr.op == "gt":
        return gt_operation(instr)
    elif instr.op == "id":
        return id_instr(instr)
    else:
        ins = f'%{instr.dest}'
        ins += ' = '
        ins += op_check(instr.op)
        ins += ' '
        ins += type_change(instr.type)
        ins += ' %'
        ins += instr.args[0]
        ins += ', %'
        ins += instr.args[1]
        return ins

def function_instr(function):
    # breakpoint()
    ret_ins = 'define '
    name = function.name
    ret_type = type_change(function.type)
    ret_ins += ret_type
    ret_ins += f' @{name}('
    for idx, arg in enumerate(function.args):
        # breakpoint()
        if idx != 0:
            ret_ins += ', '
        var_type = type_change(arg['type'])
        var_name = f'%{arg["name"]}'
        ret_ins += f'{var_type} {var_name}'
    ret_ins += ')'
    # ret_ins += ' #0 '
    ret_ins += '{'
    # breakpoint()
    return ret_ins

def label_instr(instr):
    # breakpoint()
    ins = instr.label
    ins += ':'
    return ins

def const_opration(instr):
    # breakpoint()
    ins = f'%{instr.dest}'
    ins += ' = add '
    ins += type_change(instr.type)
    ins += ' 0, '
    ins += str(instr.value).lower()
    return ins

def br_instr(instr):
    ins = 'br i1 %'
    ins += instr.args[0]
    ins += ', label %'
    ins += instr.labels[0]
    ins += ', label %'
    ins += instr.labels[1]
    return ins

def jmp_instr(instr):
    ins = 'br label %'
    ins += instr.labels[0]
    return ins

def effect_operation(instr):
    # breakpoint()
    if instr.op == 'br':
        return br_instr(instr)
    elif instr.op == 'jmp':
        # breakpoint()
        return jmp_instr(instr)
    elif instr.op == "call":
        par = ""
        for idx, arg in enumerate(instr.args):
            if idx != 0:
                par += ', '
            par += f'{var_type[arg]} %{arg}' 
        ins = f'call void @{instr.funcs[0]} ( {par} )'
        return ins
   
def define_print():
    ins = 'declare i32 @printf(ptr, ...)'
    return ins
def print_instr(instr):
    # breakpoint()
    ins_list = []
    if var_type[instr.args[0]] == "i32":
        ins_list.append(f'  call i32 (ptr, ...) @printf(ptr @.str, {var_type[instr.args[0]]} %{instr.args[0]})')
    elif var_type[instr.args[0]] == "i1":
        ins_list.append(f"  %print_value = select i1 %{instr.args[0]}, ptr @.str_true, ptr @.str_false")
        ins_list.append(f"  call i32 (ptr, ...) @printf(ptr %print_value)")
    return ins_list
def assign_print_format():
    # ins = '@.str = private unnamed_addr constant [4 x i8] c"%d\\0A\\00", align 1'
    ins_list = []
    ins_list.append(f'@.str = constant [4 x i8] c"%d\\0A\\00", align 1')
    ins_list.append(f'@.str_true = constant [6 x i8] c"true\\0A\\00", align 1')
    ins_list.append(f'@.str_false = constant [7 x i8] c"false\\0A\\00", align 1')
    return ins_list

def return_instr(instr):
    ins = "ret"
    for arg in instr.args:
        ins += f' {var_type[arg]} %{arg}'
    return ins
    # breakpoint()

def call_instr(instr):
    #{"op": "call", "dest": "digits0", "type": "int", "args": ["input"], "funcs": ["getDigits"]}
    # breakpoint()
    par = ""
    for idx, arg in enumerate(instr.args):
        if idx != 0:
            par += ', '
        par += f'{var_type[arg]} %{arg}' 
    ins = f'%{instr.dest} = call {type_change(instr.type)} @{instr.funcs[0]} ( {par} )'
    return ins
   

def bril_to_llvm(program: Program) -> str:
    """
    Translate a Bril program in SSA form to LLVM IR.

    Args:
        program (Program): The Bril program represented as a Program object.

    Returns:
        str: The generated LLVM IR code as a string.
    """
    llvm_ir_lines = []
    llvm_ir_lines.append('declare i32 @atoi(i8*)')
    has_print = False
    dummy = False
    for function in program.functions:
        for arg in function.args:
            global var_type
            if arg['type'] == "int":
                var_type[arg['name']] = "i32"
            elif arg['type'] == "bool":
                var_type[arg['name']] = "i1"
        # breakpoint()
        if function.name == 'main':
            llvm_ir_lines.append(f'define i32 @main(i32 %argc, i8** %argv)' + ' {')
            if len(function.args) > 0:
                llvm_ir_lines.append('Argb:')
                llvm_ir_lines.append(f'  %arg1_ptr = getelementptr inbounds i8*, i8** %argv, i32 1')
                llvm_ir_lines.append(f'  %arg1 = load i8*, i8** %arg1_ptr')
                llvm_ir_lines.append(f'  %{function.args[0]["name"]} = call i32 @atoi(i8* %arg1)')
                assert isinstance(function.instrs[0], Label)
                llvm_ir_lines.append(f'  br label %{function.instrs[0].label}')
        else:
            ins = function_instr(function)
            llvm_ir_lines.append(ins)
        for instr in function.instrs:
            try:
                if instr.dest != None:
                    # global var_type
                    if instr.type == "bool":
                        var_type[instr.dest] = "i1"
                    elif instr.type == "int":
                         var_type[instr.dest] = "i32"
            except:
                pass
            if isinstance(instr, ValueOperation):
                # breakpoint()
                ins = "  "
                if instr.op == "call":
                    ins += call_instr(instr)
                    llvm_ir_lines.append(ins)
                else:    
                    ins += binary_instr(instr)
                    llvm_ir_lines.append(ins)
            elif isinstance(instr, Label):
                if dummy:
                    dummy = False
                    llvm_ir_lines.append(f"  br label %{instr.label}")
                ins = label_instr(instr)
                llvm_ir_lines.append(ins)
                if instr.label == "dummy_entry_label":
                    dummy = True
            elif isinstance(instr, Const):
                ins = "  "
                ins += const_opration(instr)
                llvm_ir_lines.append(ins)
                # breakpoint()
            elif isinstance(instr, EffectOperation):
                ins = "  "
                if instr.op == 'print':
                    has_print = True
                    ins_list = print_instr(instr)
                    for i in ins_list:
                        llvm_ir_lines.append(i)
                    # continue
                elif instr.op == "ret":
                    # breakpoint()
                    if function.type == None:
                        continue
                    else:
                        ins += return_instr(instr)
                        llvm_ir_lines.append(ins)
                else:
                    ins += effect_operation(instr)
                    llvm_ir_lines.append(ins)
                # breakpoint()
        # breakpoint()
        if function.type == None:
            if function.name == "main":
                ins = '  ret i32 0'
            else:
                ins = '  ret void'
            llvm_ir_lines.append(ins)
        ins = '}'
        llvm_ir_lines.append(ins)
    # Join all lines into a single LLVM IR string
    # breakpoint()
    # json_output = serialize_bril(program)
    # breakpoint()
    if has_print:
        print_list = assign_print_format()
        for p in print_list:
            llvm_ir_lines.append(p)
        llvm_ir_lines.append(define_print())
    llvm_ir = '\n'.join(llvm_ir_lines)
    # breakpoint()
    return llvm_ir