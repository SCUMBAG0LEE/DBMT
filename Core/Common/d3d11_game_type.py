
import os
import json

from typing import List,Dict
from dataclasses import dataclass, field

from ..utils.dbmt_file_utils import dbmt_fileutil__list_files


@dataclass
class D3D11Element:
    SemanticName:str
    SemanticIndex:str
    Format:str
    ByteWidth:int
    # Which type of slot and slot number it use? eg:vb0
    ExtractSlot:str
    # Is it from pointlist or trianglelist or compute shader?
    ExtractTechnique:str
    # Human named category, also will be the buf file name suffix.
    Category:str

    # Fixed items
    InputSlot:str = field(default="0", init=False, repr=False)
    InputSlotClass:str = field(default="per-vertex", init=False, repr=False)
    InstanceDataStepRate:str = field(default="0", init=False, repr=False)

    # Calculated Items
    ElementNumber:int = field(init=False)
    AlignedByteOffset:int = field(init=False)

    def __post_init__(self):
        pass

    def get_indexed_semantic_name(self)->str:
        if self.SemanticIndex == "0":
            return self.SemanticName
        else:
            return self.SemanticName + self.SemanticIndex



# Designed to read from json file for game type config
@dataclass
class D3D11GameType:
    # Read config from json file, easy to modify and test.
    FilePath:str = field(repr=False)

    # Original file name.
    FileName:str = field(init=False,repr=False)
    # The name of the game type, usually the filename without suffix.
    GameTypeName:str = field(init=False)
    # Is GPU-PreSkinning or CPU-PreSkinning
    GPU_PreSkinning:bool = field(init=False,default=False)
    # All element name ordered.
    OrderedElementNameList:list[D3D11Element] = field(init=False,repr=False)


    def __post_init__(self):
        self.FileName = os.path.basename(self.FilePath)
        self.GameTypeName = os.path.splitext(self.FileName)[0]

        # TODO read config from json file.
        with open(self.FilePath, 'r', encoding='utf-8') as f:
            game_type_json = json.load(f)
        
        self.GPU_PreSkinning = game_type_json["GPU-PreSkinning"]



    
@dataclass
class D3D11GameTypeLv2:
    GameTypeConfigFolderPath:str

    CurrentD3D11GameTypeList:List[D3D11GameType] = field(init=False)
    GameTypeName_D3D11GameType_Dict:Dict[str,D3D11GameType] = field(init=False)
    Ordered_GPU_CPU_D3D11GameTypeList:List[D3D11GameType] = field(init=False)

    def __post_init__(self):
        self.CurrentD3D11GameTypeList = []
        self.GameTypeName_D3D11GameType_Dict = {}
        self.Ordered_GPU_CPU_D3D11GameTypeList = []

        filelist = dbmt_fileutil__list_files(self.GameTypeConfigFolderPath)
        for json_file_name in filelist:
            if not json_file_name.endswith(".json"):
                continue
            game_type = D3D11GameType(os.path.join(self.GameTypeConfigFolderPath, json_file_name))
            self.CurrentD3D11GameTypeList.append(game_type)
            game_type_name = os.path.splitext(json_file_name)[0]
            self.GameTypeName_D3D11GameType_Dict[game_type_name] = game_type
        
        # First add GPU-PreSkinning then add CPU-PreSkinning 
        # to make sure auto game type detect will first detect GPU-PreSkinning GameType.
        for game_type in self.CurrentD3D11GameTypeList:
            if game_type.GPU_PreSkinning:
                self.Ordered_GPU_CPU_D3D11GameTypeList.append(game_type)
        for game_type in self.CurrentD3D11GameTypeList:
            if not game_type.GPU_PreSkinning:
                self.Ordered_GPU_CPU_D3D11GameTypeList.append(game_type)

    def get_unique_gametype_list(self):
        pass