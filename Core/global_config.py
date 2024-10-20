from dataclasses import dataclass, field
import os

from dbmt_file_utils import dbmt_fileutil__list_files

# Nico: Thanks for SpectrumQT's WWMI project, I learned how to use @dataclass to save my time 
# and lots of other python features so use python can works as good as C++.

@dataclass
class GlobalConfig:
    LoaderFolder:str
    FrameAnalysisFolder:str
    GameName:str

    WorkFolder:str = field(default='', init=False)
    DedupedFolder:str= field(default='', init=False)

    def __post_init__(self):
        self.WorkFolder = self.LoaderFolder + self.FrameAnalysisFolder + "\\"
        self.DedupedFolder = self.WorkFolder + "deduped\\" 

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




    


