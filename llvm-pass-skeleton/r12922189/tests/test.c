#include <stdio.h>

// 1) add x, 0
int test_add0(int x) {
    return x + 0;
}

// 2) mul x, 1
int test_mul1(int x) {
    return x * 1;
}

// 3) sub x, 0
int test_sub0(int x) {
    return x - 0;
}

// 4) mul x, 2
int test_mul2(int x) {
    return x * 2;
}

// 5) div x, 1
int test_div1(int x) {
    return x / 1;  
}

// 6) xor x, 0
int test_xor0(int x) {
    return x ^ 0;
}

// 7) xor x, x
int test_xorx(int x) {
    return x ^ x;
}

// 8) and x, 0
int test_and0(int x) {
    return x & 0;
}

// 9) and x, x
int test_andx(int x) {
    return x & x;
}

// 10) or x, 0
int test_or0(int x) {
    return x | 0;
}

// 11) or x, x
int test_orx(int x) {
    return x | x;
}

// 12) sub x, x
int test_subx(int x) {
    return x - x;
}

int main() {
    int a = 42;
    printf("test_add0=%d\n",  test_add0(a));
    printf("test_mul1=%d\n", test_mul1(a));
    printf("test_sub0=%d\n", test_sub0(a));
    printf("test_mul2=%d\n", test_mul2(a));
    printf("test_div1=%d\n", test_div1(a));
    printf("test_xor0=%d\n", test_xor0(a));
    printf("test_xorx=%d\n", test_xorx(a));
    printf("test_and0=%d\n", test_and0(a));
    printf("test_andx=%d\n", test_andx(a));
    printf("test_or0=%d\n",  test_or0(a));
    printf("test_orx=%d\n",  test_orx(a));
    printf("test_subx=%d\n", test_subx(a));
    return 0;
}
