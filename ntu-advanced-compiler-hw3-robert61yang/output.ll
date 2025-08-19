declare i32 @atoi(i8*)
define void @main(i32 %argc, i8** %argv) {
entry:
  %i0 = add i32 0, 1
  br label %loop
loop:
  %i1 = phi i32 [ %i0, %entry ], [ %i2, %body ]
  %max = add i32 0, 10
  %cond = icmp slt i32 %i1, %max
  br i1 %cond, label %body, label %exit
body:
  %i2 = add i32 %i1, %i1
  br label %loop
exit:
  call i32 (ptr, ...) @printf(ptr @.str, i32 %i1)
  ret void
}
@.str = constant [4 x i8] c"%d\0A\00", align 1
@.str_true = constant [6 x i8] c"true\0A\00", align 1
@.str_false = constant [7 x i8] c"false\0A\00", align 1
declare i32 @printf(ptr, ...)