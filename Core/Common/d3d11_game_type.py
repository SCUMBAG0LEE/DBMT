
from dataclasses import dataclass, field
import os


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
    FilePath:str
    # Original file name.
    FileName:str = field(init=False)
    # The name of the game type, usually the filename without suffix.
    GameTypeName:str = field(init=False)
    # All element name ordered.
    OrderedElementNameList:list[D3D11Element] = field(init=False)


    def __post_init__(self):
        pass
    