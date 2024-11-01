from dataclasses import dataclass, field
import os

from Core.Utils.dbmt_file_utils import dbmt_fileutil__list_files
from Common.d3d11_game_type import D3D11GameType,D3D11Element

# Nico: Thanks for SpectrumQT's WWMI project, I learned how to use @dataclass to save my time 
# and lots of other python features so use python can works as good as C++ and better and faster.

@dataclass
class FrameAnalysisUtil:
    WorkFolder:str

    FileNameList:list[str] = field(init=False)

    def __post_init__(self):
        self.FileNameList = dbmt_fileutil__list_files(self.WorkFolder)

    def filter_filename(self,contain:str,suffix:str) -> list[str]:
        new_filename_list = []
        for file_name in self.FileNameList:
            if contain in file_name and file_name.endswith(suffix):
                new_filename_list.append(file_name)
        return new_filename_list
    
    def get_indexlist_by_drawib(self,drawib:str) -> list[str]:
        indexlist = []
        ib_related_filename_list = self.filter_filename(contain=drawib,suffix=".buf")
        for ib_related_filename in ib_related_filename_list:
            indexlist.append(ib_related_filename[0:6])
        return indexlist


@dataclass
class GlobalConfig:
    # We put all loader in a fixed folder structure so can locate them only by game name.
    GameName:str
    # This folder contains all 3dmigoto loader seperated by game name.
    InitialFolderPath:str
    # Where 3Dmigoto's d3d11.dll located.
    LoaderFolder:str = field(init=False)
    # eg: FrameAnalysis-2024-10-30-114032.
    FrameAnalysisFolder:str = field(init=False)
    # path of 3Dmigoto's d3d11.dll located folder + current work frame analysis folder.
    WorkFolder:str = field(init=False)
    # deduped folder path of current frame analysis folder.
    DedupedFolder:str= field(init=False)

    D3D11GameTypeList:list[D3D11GameType] = field(init=False,repr=False)

    def __post_init__(self):
        self.WorkFolder = self.LoaderFolder + self.FrameAnalysisFolder + "\\"
        self.DedupedFolder = self.WorkFolder + "deduped\\" 




    


