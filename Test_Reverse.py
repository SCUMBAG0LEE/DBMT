import os

from Core.common.buffer_file import IndexBufferBufFile
from Core.common.global_config import GlobalConfig
from Core.utils.dbmt_log_utils import log_newline

if __name__ == "__main__":
    mod_root_folder = "C:\\Users\\Administrator\\Desktop\\Firefly Naughty Kitten [FULL w ANIM]\\"
    testpath = os.path.join(mod_root_folder, "FireflyBodyA.ib")
    ib_buf_file = IndexBufferBufFile(FilePath=testpath,Stride=4)
    print(ib_buf_file)
    log_newline()

    # How to manually reverse a mod.
    # 1.fill a dict thant contains category name and buf file path

    category_name_buf_file_path_dict = {}
    category_name_buf_file_path_dict["Position"] = os.path.join(mod_root_folder, "FireflyBodyPosition.buf")
    category_name_buf_file_path_dict["Texcoord"] = os.path.join(mod_root_folder, "FireflyBodyTexcoord.buf")
    category_name_buf_file_path_dict["Blend"] = os.path.join(mod_root_folder, "FireflyHairBlend.buf")

    # trigger auto game type detect to know which GameType it use.
    g = GlobalConfig(
        GameName="SRMI",
        GameLoaderPath="C:\\Users\\Administrator\\Desktop\\LoadersDev\\",
        ConfigFolderPath="C:\\Users\\Administrator\\Desktop\\DBMT-GUI\\Configs\\")
    
    gametype:str = g.D3D11GameTypeConfig.detect_game_type_reverse(category_name_buf_file_path_dict)
    print(gametype)
