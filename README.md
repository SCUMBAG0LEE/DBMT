# DBMT
专业级DirectX Mod工具箱。
![image](https://github.com/user-attachments/assets/51b34684-b890-411a-b2c7-3e9d64c25282)

# 开发环境
- Windows11
- Visual Studio Code
- Python 3.9
- PyQt5
- PyQt-Fluent-Widgets

# 本地测试开发使用(推荐)
(1)下载此项目源码 `zip` 压缩包解压至文件夹或通过 `git`
```shell
git clone https://github.com/StarBobis/DBMT.git
cd DBMT
```
(2)创建并激活新的 conda 环境
```shell
conda create -n DBMT python=3.9
conda activate DBMT
```
(3)安装依赖
```shell
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```
(4)运行 `main.py` 开始使用
```shell
python main.py
```

# 编译exe并发布(不推荐)
(1)下载并安装pyinstaller
```shell
pip install --upgrade pip
pip install pyinstaller
```
(2)使用pyinstaller编译exe并打包发布。

(3)编译并发布此仓库内容请随发布的exe文件附带完整源码，包括你修改后的内容，详情见LICENSE。

(4)在任何情况下都不推荐使用其它人打包好的exe文件，详情见免责声明。

# 免责声明
本仓库所有内容来源于互联网整合，仅用于学习交流编程技术，基于GPL协议开源。

本仓库仅发布源代码，不会提供exe格式等打包好的文件。

建议自己本地搭建VSCode环境后使用，不推荐使用其它人打包好的exe。

如果实在要使用其它人打包好的exe请使用多种杀毒软件检查，防止电脑中毒，不要信任除了你自己之外的任何人。

使用此工具的使用者需承担所有责任，造成任何后果与本仓库开发者无关，详情见LICENSE。

# 提交反馈与开发交流
QQ群：少女前线2Mod交流群 857993507 

# 灵感来源
- https://github.com/Zzaphkiel/Seraphine
- https://github.com/SpectrumQT/WWMI-TOOLS
- https://github.com/leotorrez/XXMITools
- https://github.com/SpectrumQT/XXMI-Launcher

