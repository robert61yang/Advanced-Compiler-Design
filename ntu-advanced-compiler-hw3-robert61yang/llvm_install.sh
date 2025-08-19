#!/bin/bash

# 確保 Homebrew 已安裝
if ! command -v brew &> /dev/null; then
    echo "Homebrew 未安裝，請先安裝 Homebrew。"
    exit 1
fi

# 安裝 LLVM
LLVM_VERSION=17
echo "正在使用 Homebrew 安裝 LLVM $LLVM_VERSION..."
brew install llvm@$LLVM_VERSION || { echo "安裝 LLVM 失敗"; exit 1; }

# 配置 PATH 環境變數
echo "配置 PATH 環境變數..."
echo 'export PATH="/usr/local/opt/llvm@17/bin:$PATH"' >> ~/.zshrc
echo 'export LDFLAGS="-L/usr/local/opt/llvm@17/lib"' >> ~/.zshrc
echo 'export CPPFLAGS="-I/usr/local/opt/llvm@17/include"' >> ~/.zshrc
source ~/.zshrc

echo "LLVM $LLVM_VERSION 安裝完成！"