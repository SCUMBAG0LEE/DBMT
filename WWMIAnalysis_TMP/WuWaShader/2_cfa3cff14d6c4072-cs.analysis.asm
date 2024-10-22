
cs_5_0
dcl_globalFlags refactoringAllowed
dcl_constantbuffer CB0[3], immediateIndexed
dcl_uav_typed_buffer (sint,sint,sint,sint) u0
dcl_input vThreadID.x
dcl_temps 1
dcl_thread_group 64, 1, 1
iadd r0.x, vThreadID.x, cb0[1].x
ult r0.y, r0.x, cb0[2].x
if_nz r0.y
  store_uav_typed u0.xyzw, r0.xxxx, cb0[0].xyzw
endif
ret
//看完第一个的话，第二个基本上和第一个一样，都是写出空数据，但是这次读取的cb0[2].x的数据肯定变了
//这里显示是cb0[2].x是35277 最终输出u0大小为141108 输出长度仍为4

