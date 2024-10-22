
cs_5_0    //使用compute shader , shader model 5.0 模型
dcl_globalFlags refactoringAllowed    //标志位声明，允许重构
dcl_constantbuffer CB0[3], immediateIndexed //仅读取cs-cb0的前三行数据，每行长度为16，每4个字节为一个数据，组成数据的xyzw
dcl_uav_typed_buffer (uint,uint,uint,uint) u0 //输出 int4类型的u0
dcl_input vThreadID.x     //读取输入线程id
dcl_temps 1               //定义一个临时寄存器
dcl_thread_group 64, 1, 1 //线程组为64 * 1 * 1
iadd r0.x, vThreadID.x, cb0[1].x  // r0.x = vThreadID.x + cb0[1].x  由于cb0[1].x永远为0，这里实际上就是vThreadID.x赋值到r0.x
ult r0.y, r0.x, cb0[2].x    //如果r0.x < cb0[2].x 则r0.y 设为1，否则设为0
if_nz r0.y                //如果r0.x 不小于 cb0[2].x，则写出数据，由此可以推断出cb0[2].x控制着运行次数
  store_uav_typed u0.xyzw, r0.xxxx, cb0[0].xyzw 
  //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/store-uav-typed--sm5---asm-
  //目标uav，目标地址，写入内容
  //这里就是要把cb0[0].xyzw 写入u0.xyzw的r0.xxxx的位置
  //这里cb0[0].xyzw永远为0，r0.xxxx则是vThreadID.x
  //所以写出UAV的大小是由Dispatch调用的参数得到的。
  //查看日志可以得到：000001 Dispatch(ThreadGroupCountX:3308, ThreadGroupCountY:1, ThreadGroupCountZ:1)
  //写出u0的大小为846648
  //3308 * 64 = 211712  这里乘64是因为dcl_thread_group 64, 1, 1， 所以可以共触发211712次操作上限，但是实际操作数为211662，存储在cs-cb0中
  //211662 * 4 = 846648 正好得到最终u0的大小，这里的4是因为要写到r0.xxxx，r0.xxxx是由cs-cb0的4字节int控制的，所以这里r0.x一个也是4字节
  //最终这里u0要填写的内容是ShapeKey，长度为24，846648 / 24 = 35277 就是最终的顶点数。
endif
ret
