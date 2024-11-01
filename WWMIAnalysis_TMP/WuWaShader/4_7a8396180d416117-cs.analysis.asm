
cs_5_0
dcl_globalFlags refactoringAllowed
dcl_immediateConstantBuffer { { 1.000000, 0, 0, 0},
                              { 0, 1.000000, 0, 0},
                              { 0, 0, 1.000000, 0},
                              { 0, 0, 0, 1.000000} }
dcl_constantbuffer CB0[66], immediateIndexed
dcl_uav_typed_buffer (uint,uint,uint,uint) u0
dcl_uav_typed_buffer (sint,sint,sint,sint) u1
dcl_input vThreadIDInGroup.x
dcl_input vThreadID.y
dcl_temps 2
dcl_thread_group 2, 32, 1

//正式开始逻辑
ld_uav_typed_indexable(buffer)(sint,sint,sint,sint) r0.x, vThreadID.yyyy, u1.xyzw

itof r0.y, r0.x

//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/mul--sm4---asm-
//Component-wise multiply.
mul r0.y, r0.y, cb0[65].x
//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/ine--sm4---asm-
//Component-wise vector integer not-equal comparison.
ine r0.z, vThreadIDInGroup.x, l(0)
//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/lt--sm4---asm-
//Component-wise vector floating point less-than comparison.
lt r0.w, l(1.000000), r0.y  //判断当前运行次数 * 固定值cb0[65].x后是否小于1

//https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/and--sm4---asm-
//不是求和，而是判断是否都成立
//
and r0.z, r0.w, r0.z


mov r0.w, l(0)
loop
  uge r1.x, r0.w, l(3)
  breakc_nz r1.x
  
  imad r1.x, l(3), vThreadIDInGroup.x, r0.w
  imad r1.x, l(6), vThreadID.y, r1.x
  dp4 r1.y, cb0[64].xyzw, icb[r0.w + 0].xyzw
  movc r1.y, vThreadIDInGroup.x, cb0[64].w, r1.y
  ld_uav_typed_indexable(buffer)(uint,uint,uint,uint) r1.z, r1.xxxx, u0.yzxw
  itof r1.z, r1.z
  mul r1.y, r1.y, r1.z
  div r1.z, r1.y, r0.y
  //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/movc--sm4---asm-
  //这里是判断上面那一堆条件是否成立，来决定移动哪个变量到r1.yyyy里
  movc r1.y, r0.z, r1.z, r1.y

  store_uav_typed u0.xyzw, r1.xxxx, r1.yyyy
  iadd r0.w, r0.w, l(1)
endloop
ret
