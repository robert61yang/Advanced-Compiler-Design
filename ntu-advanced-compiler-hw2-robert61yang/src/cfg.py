from typing import Dict, List, Set
from bril import Function, Instruction, Label, Const, ValueOperation, EffectOperation

class BasicBlock:
    def __init__(self, label: str):
        self.label = label
        self.instructions: List[Instruction] = []
        self.predecessors: Set['BasicBlock'] = set()
        self.successors: Set['BasicBlock'] = set()

    def __repr__(self):
        return f'BasicBlock({self.label})'

class CFG:
    def __init__(self, function: Function):
        self.function = function
        self.blocks: Dict[str, BasicBlock] = {}
        self.entry_block: BasicBlock = self.construct_cfg()

    def construct_cfg(self) -> BasicBlock:
        """
        Constructs the CFG for the function and returns the entry block.
        """
        cur_block = None
        # last_block = None
        block_count = 0
        for idx, instr in enumerate(self.function.instrs):
            if cur_block == None:
                if isinstance(instr, Label):
                    cur_block = BasicBlock(instr.label)
                    cur_block.instructions.append(instr)
                else:
                    cur_block = BasicBlock(f'B{block_count}')
                    label_ins = {"label": f'B{block_count}'}
                    cur_block.instructions.append(Label(label_ins))
                    block_count += 1
                    cur_block.instructions.append(instr)
                if idx == 0:
                    EntryBlock = cur_block
                self.blocks[cur_block.label] = cur_block
                # else:
                #     last_block.successors.add(cur_block)
                #     cur_block.predecessors.add(last_block)
            else:
                if isinstance(instr, Label):
                    last_block = cur_block
                    self.blocks[cur_block.label] = cur_block
                    cur_block = BasicBlock(instr.label)
                    self.blocks[cur_block.label] = cur_block
                    cur_block.instructions.append(instr)
                    last_block.successors.add(cur_block)
                    cur_block.predecessors.add(last_block)
                elif isinstance(instr, EffectOperation):
                    if instr.op == "print":
                        cur_block.instructions.append(instr)
                    else:
                        cur_block.instructions.append(instr)
                        # self.blocks[cur_block.label] = cur_block
                        # last_block = cur_block
                        cur_block = None
                else:
                    cur_block.instructions.append(instr)
        # breakpoint()
                
        for block in self.blocks.values():
            if isinstance(block.instructions[-1], EffectOperation): 
                for label in block.instructions[-1].labels:
                    block.successors.add(self.blocks[label])
                    self.blocks[label].predecessors.add(block)
        # breakpoint()
               
        # TODO: Implement CFG construction logic
        # Steps:
        # 1. Divide instructions into basic blocks.
        # 2. Establish successor and predecessor relationships.
        # 3. Handle labels and control flow instructions.
        return EntryBlock

    def get_blocks(self) -> List[BasicBlock]:
        return list(self.blocks.values())