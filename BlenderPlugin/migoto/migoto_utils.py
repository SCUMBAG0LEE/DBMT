import re
import numpy
import operator  # to get function names for operators like @, +, -
import struct
import os
import bpy
import json

from glob import glob

def matmul(a, b):
    return operator.matmul(a, b)  # the same as writing a @ b


def keys_to_ints(d):
    return {k.isdecimal() and int(k) or k: v for k, v in d.items()}


def keys_to_strings(d):
    return {str(k): v for k, v in d.items()}


# This used to catch any exception in run time and raise it to blender output console.
class Fatal(Exception):
    pass


f32_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]32)+_FLOAT''')
f16_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]16)+_FLOAT''')
u32_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]32)+_UINT''')
u16_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]16)+_UINT''')
u8_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]8)+_UINT''')
s32_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]32)+_SINT''')
s16_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]16)+_SINT''')
s8_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]8)+_SINT''')
unorm16_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]16)+_UNORM''')
unorm8_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]8)+_UNORM''')
snorm16_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]16)+_SNORM''')
snorm8_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD]8)+_SNORM''')

misc_float_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD][0-9]+)+_(?:FLOAT|UNORM|SNORM)''')
misc_int_pattern = re.compile(r'''(?:DXGI_FORMAT_)?(?:[RGBAD][0-9]+)+_[SU]INT''')


def EncoderDecoder(fmt):
    if f32_pattern.match(fmt):
        return (lambda data: b''.join(struct.pack('<f', x) for x in data),
                lambda data: numpy.frombuffer(data, numpy.float32).tolist())
    if f16_pattern.match(fmt):
        return (lambda data: numpy.fromiter(data, numpy.float16).tobytes(),
                lambda data: numpy.frombuffer(data, numpy.float16).tolist())
    if u32_pattern.match(fmt):
        return (lambda data: numpy.fromiter(data, numpy.uint32).tobytes(),
                lambda data: numpy.frombuffer(data, numpy.uint32).tolist())
    if u16_pattern.match(fmt):
        return (lambda data: numpy.fromiter(data, numpy.uint16).tobytes(),
                lambda data: numpy.frombuffer(data, numpy.uint16).tolist())
    if u8_pattern.match(fmt):
        return (lambda data: numpy.fromiter(data, numpy.uint8).tobytes(),
                lambda data: numpy.frombuffer(data, numpy.uint8).tolist())
    if s32_pattern.match(fmt):
        return (lambda data: numpy.fromiter(data, numpy.int32).tobytes(),
                lambda data: numpy.frombuffer(data, numpy.int32).tolist())
    if s16_pattern.match(fmt):
        return (lambda data: numpy.fromiter(data, numpy.int16).tobytes(),
                lambda data: numpy.frombuffer(data, numpy.int16).tolist())
    if s8_pattern.match(fmt):
        return (lambda data: numpy.fromiter(data, numpy.int8).tobytes(),
                lambda data: numpy.frombuffer(data, numpy.int8).tolist())

    if unorm16_pattern.match(fmt):
        return (
            lambda data: numpy.around((numpy.fromiter(data, numpy.float32) * 65535.0)).astype(numpy.uint16).tobytes(),
            lambda data: (numpy.frombuffer(data, numpy.uint16) / 65535.0).tolist())
    if unorm8_pattern.match(fmt):
        return (lambda data: numpy.around((numpy.fromiter(data, numpy.float32) * 255.0)).astype(numpy.uint8).tobytes(),
                lambda data: (numpy.frombuffer(data, numpy.uint8) / 255.0).tolist())
    if snorm16_pattern.match(fmt):
        return (
            lambda data: numpy.around((numpy.fromiter(data, numpy.float32) * 32767.0)).astype(numpy.int16).tobytes(),
            lambda data: (numpy.frombuffer(data, numpy.int16) / 32767.0).tolist())
    if snorm8_pattern.match(fmt):
        return (lambda data: numpy.around((numpy.fromiter(data, numpy.float32) * 127.0)).astype(numpy.int8).tobytes(),
                lambda data: (numpy.frombuffer(data, numpy.int8) / 127.0).tolist())

    raise Fatal('File uses an unsupported DXGI Format: %s' % fmt)


# 这里是用于判断数据与标准数据长度差距的
components_pattern = re.compile(r'''(?<![0-9])[0-9]+(?![0-9])''')

def format_components(fmt):
    return len(components_pattern.findall(fmt))


def format_size(fmt):
    matches = components_pattern.findall(fmt)
    return sum(map(int, matches)) // 8


# Read Main.json from DBMT folder and then get current game name.
def get_current_game_from_main_json() ->str:
    current_game = ""
    main_setting_path = os.path.join(bpy.context.scene.mmt_props.path, "Configs\\Main.json")
    if os.path.exists(main_setting_path):
        main_setting_file = open(main_setting_path)
        main_setting_json = json.load(main_setting_file)
        main_setting_file.close()
        current_game = main_setting_json["GameName"]
    return current_game


# Get current output folder.
def get_output_folder_path() -> str:
    mmt_path = bpy.context.scene.mmt_props.path
    current_game = get_current_game_from_main_json()
    output_folder_path = mmt_path + "Games\\" + current_game + "\\3Dmigoto\\Mods\\output\\"
    return output_folder_path


# Get mmt path from bpy.context.scene.mmt_props.path.
def get_mmt_path()->str:
    return bpy.context.scene.mmt_props.path


# Get Games\\xxx\\Config.json path.
def get_game_config_json_path()->str:
    return os.path.join(bpy.context.scene.mmt_props.path, "Games\\" + get_current_game_from_main_json() + "\\Config.json")


# get all xxx-1 from xxx-1.ib xxx-1.vb xxx-1.fmt from our drawib folder to get all possible model name prefix.
def get_prefix_set_from_import_folder(import_folder_path:str) ->list:
    # 读取文件夹下面所有的vb和ib文件的prefix
    prefix_set = set()
    # (1) 获取所有ib文件前缀列表
    # self.report({'INFO'}, "Folder Name：" + import_folder_path)
    # 构造需要匹配的文件路径模式
    file_pattern = os.path.join(import_folder_path, "*.ib")
    # 使用 glob.glob 获取匹配的文件列表
    txt_file_list = glob(file_pattern)
    for txt_file_path in txt_file_list:
        # 如果文件名不包含-则属于我们自动导出的文件名，则不计入统计
        if os.path.basename(txt_file_path).find("-") == -1:
            continue

        # self.report({'INFO'}, "txt file: " + txt_file_path)
        txt_file_splits = os.path.basename(txt_file_path).split("-")
        ib_file_name = txt_file_splits[0] + "-" + txt_file_splits[1]
        ib_file_name = ib_file_name[0:len(ib_file_name) - 3]
        prefix_set.add(ib_file_name)
    prefix_list = list(prefix_set)

    # Sort to make sure name is ordered by partname number.
    prefix_list.sort()
    return prefix_list