
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
ld_uav_typed_indexable(buffer)(sint,sint,sint,sint) r0.x, vThreadID.yyyy, u1.xyzw
itof r0.y, r0.x
mul r0.y, r0.y, cb0[65].x
ine r0.z, vThreadIDInGroup.x, l(0)
lt r0.w, l(1.000000), r0.y
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
  movc r1.y, r0.z, r1.z, r1.y
  store_uav_typed u0.xyzw, r1.xxxx, r1.yyyy
  iadd r0.w, r0.w, l(1)
endloop
ret
