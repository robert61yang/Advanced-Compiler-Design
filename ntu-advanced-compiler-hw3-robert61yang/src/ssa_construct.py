from typing import Dict, List, Set
from bril import Function, Instruction, ValueOperation, Const, Label, EffectOperation
from cfg import CFG, BasicBlock
from dominance import DominatorTree

ENTRY_LABEL = "dummy_entry_label"
dummy = False

def construct_ssa(function: Function):
    """
    Transforms the function into SSA form.
    """
    cfg = CFG(function)
    # breakpoint()
    dom_tree = DominatorTree(cfg)

    # Step 1: Variable Definition Analysis
    def_blocks, Globals, var_type = collect_definitions(cfg)
    # breakpoint()
    
    # Step 2: Insert φ-Functions
    insert_phi_functions(cfg, dom_tree, def_blocks, Globals, var_type)
    # breakpoint()
    
    # Step 3: Rename Variables
    rename_variables(cfg, dom_tree, Globals)
    # breakpoint()
    
    # After transformation, update the function's instructions
    function.instrs = reconstruct_instructions(cfg)

def collect_definitions(cfg: CFG) -> Dict[str, Set[BasicBlock]]:
    """
    Collects the set of basic blocks in which each variable is defined.
    """
    Blocks = {}
    Globals = set()
    var_type = {}
    for b in cfg.blocks.values():
        varkill = set()
        for instr in b.instructions:
            try:
                var_type[instr.dest] = instr.type
            except:
                pass
            if instr.op != 'jmp' and instr.op != 'br':
                try:
                    for arg in instr.args:
                        if not arg in varkill:
                            # if arg == 'done':
                            #     breakpoint()
                            Globals = Globals.union({arg})
                except:
                    pass 
                try:
                    varkill = varkill.union({instr.dest})
                    if not instr.dest in Blocks:
                        Blocks[instr.dest] = set()    
                    Blocks[instr.dest] = Blocks[instr.dest].union({b})
                except:
                    pass
    return Blocks, Globals, var_type
            
                
            
    # TODO: Implement variable definition collection
    

def insert_phi_functions(cfg: CFG, dom_tree: DominatorTree, def_blocks: Dict[str, Set[BasicBlock]], Globals, var_type):
    """
    Inserts φ-functions into the basic blocks.
    """
    # breakpoint()
    # TODO: Implement φ-function insertion using dominance frontiers
    phi_function = {}
    for x in Globals:
        phi_function[x] = set()
    WorkList = set()
    for x in Globals:
        if not x in def_blocks:
            continue
        WorkList = WorkList.union(def_blocks[x])
        while WorkList:
            b = WorkList.pop()
            for d in dom_tree.dom_frontiers[b]:
                if not d in phi_function[x]:
                    # if b.label == 'b1':
                    #     breakpoint()
                    # if x == 'done':
                    #     breakpoint()
                    new_instr = {'op': 'phi', 'args': [], 'dest': x, 'labels': [], 'type': var_type[x]}
                    phi = ValueOperation(new_instr)
                    cfg.blocks[d.label].instructions = cfg.blocks[d.label].instructions[:1] + [phi] + cfg.blocks[d.label].instructions[1:]
                    phi_function[x] = phi_function[x].union({d})
                    WorkList = WorkList.union({d})
    
    # pass
def NewName(n, counter, stack):
    i = counter[n]
    counter[n] += 1 
    stack[n].append(f'{n}{i}')
    return f'{n}{i}'
    
def rename(b: BasicBlock, counter, stack, Globals, dom_tree, visited, cfg):
    visited = visited.union({b})
    # breakpoint()
    pop_list = []
    local = set()
    for instr in b.instructions:
        if instr.op == 'phi':
            pop_list.append(instr.dest)
            instr.dest = NewName(instr.dest, counter, stack)
        elif isinstance(instr, Const):
            if instr.dest in Globals:
                pop_list.append(instr.dest)
                instr.dest = NewName(instr.dest, counter, stack)
            elif instr.dest in local:
                pop_list.append(instr.dest)
                instr.dest = NewName(instr.dest, counter, stack)
            else:
                local.add(instr.dest)
                counter[instr.dest] = 0
                stack[instr.dest] = []
                
        elif isinstance(instr, ValueOperation):
            a = [] 
            for arg in instr.args:
                if arg in Globals:
                    try:
                        arg = stack[arg][-1]
                    except:
                        pass
                elif arg in local:
                    try:
                        arg = stack[arg][-1]
                    except:
                        pass
                a.append(arg)
            instr.args = a
            if instr.dest in Globals:
                pop_list.append(instr.dest)
                instr.dest = NewName(instr.dest, counter, stack)
            elif instr.dest in local:
                pop_list.append(instr.dest)
                instr.dest = NewName(instr.dest, counter, stack)
            else:
                local.add(instr.dest)
                counter[instr.dest] = 0
                stack[instr.dest] = []
        # elif instr.op == "print" or instr.op == 'call':
        elif not isinstance(instr, Label):
            a = [] 
            for arg in instr.args:
                if arg in Globals:
                    arg = stack[arg][-1]
                elif arg in local:
                    try:
                        arg = stack[arg][-1]
                    except:
                        pass
                a.append(arg)
            instr.args = a
    # breakpoint()
    for succ in b.successors:
        for instr in succ.instructions:
            if instr.op == 'phi':
                arg = instr.phi_var
                if len(stack[arg]) > 0:
                    # instr.args[0] = instr.args[1]
                    # instr.args[1] = stack[arg][-1]
                    instr.args.append(stack[arg][-1])
                    instr.labels.append(b.label)
                else:
                    instr.args.append(NewName(arg, counter, stack))
                    instr.labels.append(b.label)
                if succ == cfg.entry_block:
                    length = len(succ.predecessors) + 1
                else:
                    length = len(succ.predecessors)
                if len(instr.args) > length:
                    instr.args = instr.args[-1 * len(succ.predecessors):]
                    instr.labels = instr.labels[-1 * len(succ.predecessors):]
    for x, pred in dom_tree.idom.items():
        if (b == pred) and (x not in visited):
            rename(x, counter, stack, Globals, dom_tree, visited, cfg)
    for x in pop_list:
        stack[x].pop()

def rename_variables(cfg: CFG, dom_tree: DominatorTree, Globals):
    """
    Renames variables to ensure each assignment is unique.
    """
    # TODO: Implement variable renaming
    counter = {}
    stack = {}
    visited = set()
    # breakpoint()
    for i in Globals:
        counter[i] = 0
        stack[i] = []
    for arg in cfg.function.args:
        stack[arg['name']].append(arg['name'])
    for instr in cfg.entry_block.instructions:
        if instr.op == 'phi':
            global dummy
            dummy = True
            arg = instr.phi_var
            if len(stack[arg]) > 0:
                instr.args.append(stack[arg][-1])
                instr.labels.append(ENTRY_LABEL)
    rename(cfg.entry_block, counter, stack, Globals, dom_tree, visited, cfg)

def instr_of_block(b:BasicBlock):
    l = []
    for instr in b.instructions:
         l.append(instr)   
    return l

def reconstruct_instructions(cfg: CFG) -> List[Instruction]:
    """
    Reconstructs the instruction list from the CFG after SSA transformation.
    """
    # TODO: Implement instruction reconstruction
    block_count = 0
    cur_block = None
    instr_list = []
    if dummy:
        instr_list += [Label({"label": ENTRY_LABEL})]
    # breakpoint()
    for idx, instr in enumerate(cfg.function.instrs):
        if cur_block == None:
            if isinstance(instr, Label):
                cur_block = instr.label
                instr_list += instr_of_block(cfg.blocks[cur_block])
                # breakpoint()
            else:
                cur_block = f'B{block_count}'
                instr_list += instr_of_block(cfg.blocks[cur_block])
                block_count += 1
        else:
            if isinstance(instr, Label):
                cur_block = instr.label
                instr_list += instr_of_block(cfg.blocks[cur_block])
                # breakpoint()
            elif isinstance(instr, EffectOperation) and instr.op != "print":
                cur_block = None
    # breakpoint()
    return instr_list
    # pass