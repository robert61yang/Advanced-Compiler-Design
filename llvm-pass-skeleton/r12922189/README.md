### Usage
1. build the skeleton
```shell
cd src/build
make
```
2. compile the test.c
```shell
cd src
clang -fpass-plugin=`echo build/skeleton/SkeletonPass.*` ../tests/test.c
```
It can be seen that the pass is correctly log on the screen, indicating that the pass has properly handled these patterns.
```
detect add x, 0 -> x
detect mul x, 1 -> x
detect sub x, 0 -> x
detect mul x, 2 -> shl x, 1
detect div x, 1 -> x
detect xor x, 0 -> x
detect and x, 0 -> 0
detect or x, 0 -> x
```

3. run the test.c
```shell
./a.out
```
It can be seen that the program is executed correctly.
```
test_add0=42
test_mul1=42
test_sub0=42
test_mul2=84
test_div1=42
test_xor0=42
test_xorx=0
test_and0=0
test_andx=42
test_or0=42
test_orx=42
test_subx=0
```