.LFB0:
        movl    %edi, -20(%rsp)
        movq    $0, -8(%rsp)
        movl    $0, -12(%rsp)
        jmp     .L2
.L3:
        movl    -12(%rsp), %eax
        cltq
        addq    %rax, -8(%rsp)
        addl    $1, -12(%rsp)
.L2:
        movl    -12(%rsp), %eax
        cmpl    -20(%rsp), %eax
        jl      .L3
        movq    -8(%rsp), %rax
        ret