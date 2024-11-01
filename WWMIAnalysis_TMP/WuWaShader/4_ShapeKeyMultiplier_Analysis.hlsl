

Texture1D<float4> IniParams : register(t120);

//声明cs-cb0可以读取，一共66个xyzw数据
cbuffer cb0 : register(b0)
{
    uint4 cb0[66];
}


RWBuffer<uint> u0 : register(u0);
RWBuffer<int> u1 : register(u1);
// RWBuffer<uint4> cb0 : register(u6);

// RWBuffer<float4> DebugRW : register(u7);


#define cmp -


[numthreads(2,32,1)]
//Dispatch 1,1103,1  70592
void main(uint3 vThreadID : SV_DispatchThreadID, uint3 vThreadIDInGroup : SV_GroupThreadID)
{
    //immidiate constant buffer, 常数矩阵
    const float4 icb[] = { 
        { 1.000000, 0, 0, 0},
        { 0, 1.000000, 0, 0},
        { 0, 0, 1.000000, 0},
        { 0, 0, 0, 1.000000}
    };

    float4 r0,r1;

    //获取当前执行的次数，转为float类型
    r0.x = u1[vThreadID.y];
    r0.y = float(r0.x);

    //然后乘以一个奇怪的float数，从cb0的第65传递进来的，uint32值为  872700354
    //cb0[65].x = C2 59 04 34  float值为 1.232611e-07
    r0.y = asfloat(cb0[65].x) * r0.y;

    //判断当前x是否不为0
    r0.z = cmp((int)vThreadIDInGroup.x != 0);

    //判断r0.y是否大于1，
    r0.w = cmp(1 < r0.y);

    //r0.y大于1则r0.z使用当前线程的.x否则变为0
    r0.z = r0.w ? r0.z : 0;

    //最后r0.w归0，用于循环计数
    //到这里我算是能理解为什么SpectrumQT说最难的部分是Shader的ASM逆向了。
    r0.w = 0;

    // DebugRW[vThreadID.y] = float4(cb0[vThreadID.y]);

    while (true) {

        r1.x = cmp((uint)r0.w >= 3);

        if (r1.x != 0) {
            break;
        }


        //3 * Group的x，也就是只能是0或1的值，再加上当前索引
        r1.x = mad(3, (int)vThreadIDInGroup.x, (int)r0.w);

        //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/mad
        //6 * vThreadID.y + r1.x
        r1.x = mad(6, (int)vThreadID.y, (int)r1.x);
        
        //这里cb0[64]到底装的什么玩意呢？
        //https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-dot
        //这里的含义为，根据当前所处的0到4索引，赋予r1.y对应的cb0里的固定值
        r1.y = dot(asfloat(cb0[64].xyzw), icb[r0.w+0].xyzw);
        
        // DebugRW[r0.w] = asfloat(cb0[65].x);
        // DebugRW[4] = asfloat(cb0[64].xyzw);
        // r1.y = 0.00000018;
        
        //判断vThreadIDInGroup.x是否不为0，不为0就用固定死的cb0[64].w，否则就用之前cb0里加载的
        //线程.x是否不为0？这里线程.x 被NumThreads声明所限制，只能为0或1，所以这里是2选1？
        //要么固定值，要么计算出来的值？
        //那么具体实际的用途是什么呢？
        r1.y = vThreadIDInGroup.x ? cb0[64].w : r1.y;

        //根据之前计算的两次r1.x取对应索引处的值
        r1.z = asint(u0[r1.x]);

        
        // DebugRW[r0.w] = asfloat(cb0[65].x);
        // DebugRW[r0.w] = asfloat(cb0[65].x);

        //把自己转换为int
        r1.z = (int)r1.z;
        //然后乘以r1.y
        r1.y = r1.z * r1.y;
        //然后除以r0.y 也就是那个固定死的值
        r1.z = r1.y / r0.y;
        //如果r0.z不为0 则使用r1.z否则使用r1.y
        r1.y = r0.z ? r1.z : r1.y;
        //最后写入u0对应的索引处
        //所以说其实本质是做了一个乘法
        u0[r1.x] = asuint(r1.y);
        //那么这个u0里的内容是什么？u0里的内容就是最终每个顶点展示形态键用的偏移量 vb6槽位
        
        //索引自增1
        r0.w = (int)r0.w + 1;
    }

    return;
}

//总结下来这个HLSL是根据顶点索引，给每一个形态键都做了一个乘法乘以cs-cb0里固定的值 
//主要用到了 cb[65].x和cb[64].xyzw
//但是由于目前暂不清楚形态键的计算原理，所以这里只是一知半解

//这里的乘法可能是为了做矩阵变换，或者大小变换？或者比例变换？
//也许得把第三步先看懂才能看懂这个第四步了。