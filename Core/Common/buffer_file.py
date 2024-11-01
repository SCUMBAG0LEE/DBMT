
from dataclasses import dataclass, field
import os
import struct

@dataclass
class IndexBufferBufFile:
    FilePath:str
    Stride:int
    FileName:str = field(init=False)
    NumberList:list[int] = field(init=False,repr=False)

    # useful attributes
    UniqueNumberList:set[int] = field(init=False,repr=False)
    MaxNumber:int = field(init=False)
    MinNumber:int = field(init=False)
    IndexCount:int = field(init=False)
    UniqueNumberCount:int = field(init=False)

    def __post_init__(self):
        self.FileName = os.path.basename(self.FilePath)
        self.NumberList = self.parse_bin_data(self.Stride)
        # calculate number
        self.UniqueNumberList = set(self.NumberList)
        self.MaxNumber = max(self.NumberList)
        self.MinNumber = min(self.NumberList)
        self.IndexCount = len(self.NumberList)
        self.UniqueNumberCount = len(self.UniqueNumberList)
        
    def parse_bin_data(self, stride):
        if stride not in [2, 4]:
            raise ValueError("Stride must be either 2 or 4")

        format_char = 'H' if stride == 2 else 'I'  # H for unsigned short, I for unsigned int
        with open(self.FilePath, 'rb') as file:
            byte_data = file.read()
            count = len(byte_data) // stride
            unpacked_data = struct.unpack(f'<{count}{format_char}', byte_data[:count*stride])
        
        return list(unpacked_data)
    

class VertexBufferBufFile:
    FilePath:str
    Stride:int
    FileName:str = field(init=False)
    
    def __post_init__(self):
        self.FileName = os.path.basename(self.FilePath)

    def parse_bin_data():
        pass
