#!/bin/bash

curl -fsSL https://deno.land/install.sh | sh
git clone https://github.com/sampsyo/bril.git
cd bril 
deno install brili.ts
pip install --user flit
cd bril-txt
flit install --symlink --user