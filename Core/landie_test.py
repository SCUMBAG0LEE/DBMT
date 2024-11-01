from global_config import GlobalConfig,FrameAnalysisUtil
from Core.Utils.dbmt_log_utils import log_newline,log_info

import os

# 测试Arknights 和 Honor of Kings 
# 这俩的格式是一样的，所以只需要测试其中一个即可。
# 加载Dump于蓝叠模拟器


if __name__ == "__main__":
    draw_ib = "9d14a773"
    g = GlobalConfig(
        LoaderFolder="C:\\Users\\Administrator\\Desktop\\Arknights\\DrawIBRelatedFiles\\",
        FrameAnalysisFolder="FrameAnalysis-2028-08-28-666666",
        GameName="ArkNights")

    fautil = FrameAnalysisUtil(WorkFolder=g.WorkFolder)