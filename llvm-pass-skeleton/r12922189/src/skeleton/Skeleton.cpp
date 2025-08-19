#include "llvm/Pass.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

struct SkeletonPass : public PassInfoMixin<SkeletonPass> {
    PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM) {
        for (auto &F : M) {
            if (F.isDeclaration())
                continue;

            for (auto &B : F) {
                for (auto InstIt = B.begin(); InstIt != B.end(); ) {
                    Instruction *I = &*InstIt++;
                    if (auto *BinOp = dyn_cast<BinaryOperator>(I)) {
                        auto Opcode = BinOp->getOpcode();
                        Value *Op0 = BinOp->getOperand(0);
                        Value *Op1 = BinOp->getOperand(1);

                        //===------------------------------------------------------------------===//
                        // Pattern 1: add x, 0 -> x | add 0, x -> x
                        //===------------------------------------------------------------------===//
                        if (Opcode == Instruction::Add) {
                            if (auto *CInt = dyn_cast<ConstantInt>(Op1)) {
                                if (CInt->isZero()) {
                                    BinOp->replaceAllUsesWith(Op0);
                                    BinOp->eraseFromParent();
                                    errs() << "detect add x, 0 -> x \n";
                                    continue;
                                }
                            }
                            if (auto *CInt = dyn_cast<ConstantInt>(Op0)) {
                                if (CInt->isZero()) {
                                    BinOp->replaceAllUsesWith(Op1);
                                    BinOp->eraseFromParent();
                                     errs() << "detect add 0, x -> x \n";
                                    continue;
                                }
                            }
                        }

                        //===------------------------------------------------------------------===//
                        // Pattern 2: sub x, 0 -> x | sub x, x -> 0
                        //===------------------------------------------------------------------===//
                        if (Opcode == Instruction::Sub) {
                            // sub x, 0 -> x
                            if (auto *CInt = dyn_cast<ConstantInt>(Op1)) {
                                if (CInt->isZero()) {
                                    BinOp->replaceAllUsesWith(Op0);
                                    BinOp->eraseFromParent();
                                     errs() << "detect sub x, 0 -> x \n";
                                    continue;
                                }
                            }
                            // sub x, x -> 0
                            if (Op0 == Op1) {
                                IRBuilder<> Builder(BinOp);
                                Value *Zero = ConstantInt::get(BinOp->getType(), 0);
                                BinOp->replaceAllUsesWith(Zero);
                                BinOp->eraseFromParent();
                                 errs() << "detect sub x, x -> 0 \n";
                                continue;
                            }
                        }

                        //===------------------------------------------------------------------===//
                        // Pattern 3: mul x, 1 -> x | mul 1, x -> x | mul x, 2 -> shl x, 1
                        //===------------------------------------------------------------------===//
                        if (Opcode == Instruction::Mul) {
                            // mul x, 1 or mul 1, x -> x
                            if (auto *CInt = dyn_cast<ConstantInt>(Op1)) {
                                if (CInt->equalsInt(1)) {
                                    BinOp->replaceAllUsesWith(Op0);
                                    BinOp->eraseFromParent();
                                    errs() << "detect mul x, 1 -> x \n";
                                    continue;
                                }
                            }
                            if (auto *CInt = dyn_cast<ConstantInt>(Op0)) {
                                if (CInt->equalsInt(1)) {
                                    BinOp->replaceAllUsesWith(Op1);
                                    BinOp->eraseFromParent();
                                    errs() << "detect mul 1, x -> x \n";
                                    continue;
                                }
                            }
                            // mul x, 2 -> shl x, 1
                            if (auto *CInt = dyn_cast<ConstantInt>(Op1)) {
                                if (CInt->equalsInt(2)) {
                                    IRBuilder<> Builder(BinOp);
                                    Value *Shl = Builder.CreateShl(Op0, ConstantInt::get(BinOp->getType(), 1));
                                    BinOp->replaceAllUsesWith(Shl);
                                    BinOp->eraseFromParent();
                                    errs() << "detect mul x, 2 -> shl x, 1 \n";
                                    continue;
                                }
                            }
                        }

                        //===------------------------------------------------------------------===//
                        // Pattern 4: div x, 1 -> x
                        //===------------------------------------------------------------------===//
                        if (Opcode == Instruction::SDiv || Opcode == Instruction::UDiv) {
                            if (auto *CInt = dyn_cast<ConstantInt>(Op1)) {
                                if (CInt->equalsInt(1)) {
                                    BinOp->replaceAllUsesWith(Op0);
                                    BinOp->eraseFromParent();
                                    errs() << "detect div x, 1 -> x \n";
                                    continue;
                                }
                            }
                        }

                        //===------------------------------------------------------------------===//
                        // Pattern 5: xor x, 0 -> x | xor x, x -> 0
                        //===------------------------------------------------------------------===//
                        if (Opcode == Instruction::Xor) {
                            // xor x, 0 -> x
                            if (auto *CInt = dyn_cast<ConstantInt>(Op1)) {
                                if (CInt->isZero()) {
                                    BinOp->replaceAllUsesWith(Op0);
                                    BinOp->eraseFromParent();
                                    errs() << "detect xor x, 0 -> x \n";
                                    continue;
                                }
                            }
                            // xor x, x -> 0
                            if (Op0 == Op1) {
                                IRBuilder<> Builder(BinOp);
                                Value *Zero = ConstantInt::get(BinOp->getType(), 0);
                                BinOp->replaceAllUsesWith(Zero);
                                BinOp->eraseFromParent();
                                errs() << "detect xor x, x -> 0 \n";
                                continue;
                            }
                        }

                        //===------------------------------------------------------------------===//
                        // Pattern 6: and x, 0 -> 0 | and x, x -> x
                        //===------------------------------------------------------------------===//
                        if (Opcode == Instruction::And) {
                            // and x, 0 -> 0
                            if (auto *CInt = dyn_cast<ConstantInt>(Op1)) {
                                if (CInt->isZero()) {
                                    IRBuilder<> Builder(BinOp);
                                    Value *Zero = ConstantInt::get(BinOp->getType(), 0);
                                    BinOp->replaceAllUsesWith(Zero);
                                    BinOp->eraseFromParent();
                                    errs() << "detect and x, 0 -> 0 \n";
                                    continue;
                                }
                            }
                            // and x, x -> x
                            if (Op0 == Op1) {
                                BinOp->replaceAllUsesWith(Op0);
                                BinOp->eraseFromParent();
                                errs() << "detect and x, x -> x \n";
                                continue;
                            }
                        }

                        //===------------------------------------------------------------------===//
                        // Pattern 7: or x, 0 -> x | or x, x -> x
                        //===------------------------------------------------------------------===//
                        if (Opcode == Instruction::Or) {
                            // or x, 0 -> x
                            if (auto *CInt = dyn_cast<ConstantInt>(Op1)) {
                                if (CInt->isZero()) {
                                    BinOp->replaceAllUsesWith(Op0);
                                    BinOp->eraseFromParent();
                                    errs() << "detect or x, 0 -> x \n";
                                    continue;
                                }
                            }
                            // or x, x -> x
                            if (Op0 == Op1) {
                                BinOp->replaceAllUsesWith(Op0);
                                BinOp->eraseFromParent();
                                errs() << "detect or x, x -> x \n";
                                continue;
                            }
                        }
                    }
                }
            }
        }
        return PreservedAnalyses::all();
    };
};

}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
    return {
        .APIVersion = LLVM_PLUGIN_API_VERSION,
        .PluginName = "Skeleton pass",
        .PluginVersion = "v0.1",
        .RegisterPassBuilderCallbacks = [](PassBuilder &PB) {
            PB.registerPipelineStartEPCallback(
                [](ModulePassManager &MPM, OptimizationLevel Level) {
                    MPM.addPass(SkeletonPass());
                });
        }
    };
}