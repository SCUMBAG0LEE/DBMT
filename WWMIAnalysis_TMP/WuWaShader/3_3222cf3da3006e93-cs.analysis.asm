cs_5_0
dcl_globalFlags refactoringAllowed
dcl_immediateConstantBuffer { { 1.000000, 0, 0, 0},
                              { 0, 1.000000, 0, 0},
                              { 0, 0, 1.000000, 0},
                              { 0, 0, 0, 1.000000} }
dcl_constantbuffer CB0[66], dynamicIndexed //这次读取了完整的cb0，读取到第66行
dcl_resource_buffer (uint,uint,uint,uint) t0
dcl_resource_buffer (float,float,float,float) t1
dcl_uav_typed_buffer (uint,uint,uint,uint) u0
dcl_uav_typed_buffer (sint,sint,sint,sint) u1
dcl_input vThreadIDInGroupFlattened
dcl_input vThreadIDInGroup.x
dcl_input vThreadID.y
dcl_temps 4
dcl_tgsm_structured g0, 4, 128
//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dcl-tgsm-structured--sm5---asm-
//声明共享内存,ComputeShader中独有的机制
dcl_tgsm_structured g1, 4, 128
dcl_thread_group 2, 32, 1
ult r0.x, vThreadIDInGroupFlattened.x, l(32)
if_nz r0.x //处理前64个内容
  ishl r0.x, vThreadIDInGroupFlattened.x, l(2) 
  //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ishl--sm5---asm-
  //r0.x = vThreadIDInGroupFlattened.x * 4 (左移相当于乘以2的2次方)
  mov r0.y, l(0)
  loop
  //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/loop--sm4---asm-
  //循环一直等到遇到break语句
    ige r0.w, r0.y, l(4)
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ige--sm4---asm-
    //如果r0.y大于等于4，r0.w = 1 否则r0.w = 0
    breakc_nz r0.w
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/breakc--sm4---asm-
    //r0.w如果不为0就break结束循环
    //组合起来看就是如果r0.y > 4那就结束循环

    iadd r0.w, r0.y, r0.x
    //r0.w = r0.y + r0.x(vThreadIDInGroupFlattened.x * 4)

    mov r1.x, vThreadIDInGroupFlattened.x
    dp4 r1.y, cb0[r1.x + 32].xyzw, icb[r0.y + 0].xyzw
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dp4--sm4---asm-
    //dp4是点积 
    // icb是什么？？转为 integer constant buffer? 还不确定不能乱猜

    //icb[r0.y + 0].xyzw 这里r0.y只能是0,1,2,3   但是由于不知道icb是干啥的，暂时不知道结果，所以icb是干啥的？
    //cb0[r1.x + 32].xyzw 这里指从ConstantBuffer的32行开始，每行16字节，

    //icb在网上搜不到，github搜到是有关于GLSL
    //经过不断的摸索，终于知道了，icb是immediate constant buffer的意思，也就是开头定义的dcl_immediateConstantBuffer

    store_structured g0.x, r0.w, l(0), r1.y
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/store-structured--sm5---asm-
    //Nico:真要命啊，这么大一长串ASM一点一点看！
    //Item	Description
    ///dest
    //[in] The address of the results of the operation.
    //dstAddress
    //[in] The address at which to write.
    //dstByteOffset
    //[in] The index of the structure to write.
    //src0
    //[in] The components to write.
    //写出r1.y的内容，写入g0.x中，写入地址为r0.w，偏移量为立即数0
    //g0是共享内存，应该是这里写好之后，在后面的地方要用到。

    ineg r1.y, r0.y
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ineg--sm4---asm-
    //ineg指令是按位取反，官方文档说的是求2的补码，对任何数执行2的补码运算，相当于乘以-1
    //也就是之前的点积结果，在这里取反后放到r1.y里

    ult r2.xyz, r0.yyyy, l(1, 2, 3, 0)
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ult--sm4---asm-
    //如果r0.yyyy < l(1,2,3,0)，则r2.xyz = 1

    and r3.y, r1.y, r2.y
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/and--sm4---asm-
    //bitwise and result put in r3.y

    iadd r0.yz, r0.yyyy, l(0, 1, -3, 0)
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/iadd--sm4---asm-
    //整数加法

    movc r3.z, r2.y, l(0), r0.z
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/movc--sm4---asm-
    //如果r2.y == 1 则r3.z = l(0) 否则r3.z = r0.z

    ieq r3.w, r2.z, l(0)
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ieq--sm4---asm-
    //如果r2.z == 0 则 r3.w = 1 否则r3.w = 0

    mov r3.x, r2.x
    //r2.x放到r3.x里
    
    and r1.xyzw, r3.xyzw, cb0[r1.x + 0].xyzw
    //bitwise logic and 

    or r1.xy, r1.ywyy, r1.xzxx
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/or--sm4---asm-
    //bitwise logic or
    or r0.z, r1.y, r1.x
    
    store_structured g1.x, r0.w, l(0), r0.z
  endloop
endif
sync_g_t
//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/sync--sm5---asm-

ld_structured r0.x, l(64), l(0), g1.xxxx
//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ld-structured--sm5---asm-
ult r0.x, vThreadID.y, r0.x
movc r0.xy, r0.xxxx, l(0,32,0,0), l(64,96,0,0)
ld_structured r0.y, r0.y, l(0), g1.xxxx
ult r0.y, vThreadID.y, r0.y
movc r0.y, r0.y, l(0), l(32)
iadd r0.x, r0.x, r0.y
iadd r0.y, r0.x, l(16)
ld_structured r0.y, r0.y, l(0), g1.xxxx
ult r0.y, vThreadID.y, r0.y
movc r0.y, r0.y, l(0), l(16)
iadd r0.x, r0.x, r0.y
iadd r0.y, r0.x, l(8)
ld_structured r0.y, r0.y, l(0), g1.xxxx
ult r0.y, vThreadID.y, r0.y
movc r0.y, r0.y, l(0), l(8)
iadd r0.x, r0.x, r0.y
iadd r0.y, r0.x, l(4)
ld_structured r0.y, r0.y, l(0), g1.xxxx
ult r0.y, vThreadID.y, r0.y
movc r0.y, r0.y, l(0), l(4)
iadd r0.x, r0.x, r0.y
iadd r0.y, r0.x, l(2)
ld_structured r0.y, r0.y, l(0), g1.xxxx
ult r0.y, vThreadID.y, r0.y
movc r0.y, r0.y, l(0), l(2)
iadd r0.x, r0.x, r0.y
iadd r0.y, r0.x, l(1)
ld_structured r0.y, r0.y, l(0), g1.xxxx
ult r0.y, vThreadID.y, r0.y
movc r0.y, r0.y, l(0), l(1)
iadd r0.x, r0.x, r0.y
utof r0.y, cb0[65].y
//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/utof--sm4---asm-
//unsigned integer to float

iadd r0.z, r0.x, l(1)
ld_structured r0.z, r0.z, l(0), g1.xxxx
utof r1.y, r0.z
mov r1.x, l(0)
add r0.yz, r0.yyyy, r1.xxyx
ftou r0.yz, r0.yyzy
//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ftou--sm4---asm-
//float to unsigned interger
ld_structured r0.x, r0.x, l(0), g0.xxxx
iadd r0.y, r0.y, vThreadID.y
ult r0.z, r0.y, r0.z
ne r0.w, r0.x, l(0.000000)
//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ne--sm4---asm-
//not equal
and r0.z, r0.w, r0.z
if_nz r0.z
  ld_indexable(buffer)(uint,uint,uint,uint) r0.z, r0.yyyy, t0.yzxw
  mov r0.w, l(0)
  loop
    uge r1.x, r0.w, l(3)
    breakc_nz r1.x
    imad r1.x, l(3), vThreadIDInGroup.x, r0.w
    imad r1.y, l(6), r0.y, r1.x
    ld_indexable(buffer)(float,float,float,float) r1.y, r1.yyyy, t1.yxzw
    mul r1.y, r0.x, r1.y
    dp4 r1.z, cb0[64].xyzw, icb[r0.w + 0].xyzw
    movc r1.z, vThreadIDInGroup.x, cb0[64].w, r1.z
    mul r1.y, r1.z, r1.y
    round_ne r1.y, r1.y
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/round-ne--sm4---asm-
    //Floating-point round to integral float.
    ftoi r1.y, r1.y
    imad r1.x, l(6), r0.z, r1.x
    atomic_iadd u0, r1.x, r1.y
    //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/atomic-iadd--sm5---asm-
    iadd r0.w, r0.w, l(1)
    //r0.w自增1，用来控制循环次数
  endloop
  if_z vThreadIDInGroup.x
  //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/if--sm4---asm-
  //The 32-bit register supplied by src0 is tested at a bit level. If any bit is nonzero, if_z will be true. If all bits are zero, if_nz will be true.
    mul r0.x, r0.x, cb0[65].x
    round_ne r0.x, r0.x
    ftoi r0.x, r0.x
    atomic_iadd u1, r0.y, r0.x
  endif
endif
ret
