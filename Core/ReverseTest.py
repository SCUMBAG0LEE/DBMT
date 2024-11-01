
from BufferFile import IndexBufferBufFile


if __name__ == "__main__":
    testpath = "C:\\Users\\Administrator\\Desktop\\Firefly Naughty Kitten [FULL w ANIM]\\FireflyBodyA.ib"
    ib_buf_file = IndexBufferBufFile(FilePath=testpath,Stride=4)
    print(ib_buf_file)