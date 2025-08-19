from typing import Dict, Set
from cfg import CFG, BasicBlock
from collections import deque

def reverse_postorder(cfg: CFG):
    stack1 = [cfg.entry_block]
    stack2 = []
    
    while stack1:
        node = stack1.pop()
        stack2.append(node)
        
        for child in node.successors:
            if (not child in stack1) and (not child in stack2):
                stack1.append(child)
    
    return stack2

class DominatorTree:
    def __init__(self, cfg: CFG):
        self.cfg = cfg
        self.dom: Dict[BasicBlock, Set[BasicBlock]] = {}
        self.idom: Dict[BasicBlock, BasicBlock] = {}
        self.dom_frontiers: Dict[BasicBlock, Set[BasicBlock]] = {}
        self.compute_dominators()
        self.compute_idom()
        self.compute_dominance_frontiers()

    def compute_dominators(self):
        """
        Computes the dominators for each basic block.
        """
        # TODO: Implement the iterative algorithm to compute dominators.
        cfg = self.cfg
        block_list = reverse_postorder(cfg)
        dom = {}
        N = set(cfg.blocks.values())
        n = len(N) - 1
        for block in cfg.blocks.values():
            dom[block.label] = N
        changed = True
        while(changed):
            changed = False
            for block in block_list:
                joint_dom = set()
                f = True
                for pred in block.predecessors:
                    if f:
                        f = False
                        joint_dom = dom[pred.label]
                    else:
                        joint_dom = dom[pred.label].intersection(joint_dom)
                temp = {block}.union(joint_dom)
                
                if temp != dom[block.label]:
                    dom[block.label] = temp
                    changed = True
        # breakpoint()
        self.dom = dom

    def compute_idom(self):
        """
        Computes the immediate dominator for each basic block.
        """
        # TODO: Compute immediate dominators based on the dominator sets.
        cfg = self.cfg
        idom = {}
        for label, dom in self.dom.items():
            queue = deque([label])
            while queue:
                n = queue.popleft()
                if n != label and cfg.blocks[n] in dom:
                    idom[cfg.blocks[label]] = cfg.blocks[n]
                    break
                for parent in cfg.blocks[n].predecessors:
                    if not parent.label in queue:
                        queue.append(parent.label)
        idom[cfg.entry_block] = cfg.entry_block
        self.idom = idom

    def compute_dominance_frontiers(self):
        """
        Computes the dominance frontiers for each basic block.
        """
        # TODO: Implement dominance frontier computation.
        cfg = self.cfg
        idom = self.idom
        df = {}
        for n in cfg.blocks.values():
            df[n] = set()
        for n in cfg.blocks.values():
            if n == cfg.entry_block:
                if len(n.predecessors) > 0:
                    for p in n.predecessors:
                        runner = p
                        while runner != idom[n]:
                            df[runner] = df[runner].union({n})
                            runner = idom[runner]
                continue
            if len(n.predecessors) > 1:
                for p in n.predecessors:
                    runner = p
                    while runner != idom[n]:
                        df[runner] = df[runner].union({n})
                        runner = idom[runner]
        # breakpoint()
        # df[cfg.entry_block] = set()
        self.dom_frontiers = df