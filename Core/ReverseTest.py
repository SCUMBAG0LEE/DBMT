
from Core.Common.buffer_file import IndexBufferBufFile


if __name__ == "__main__":
    mod_root_folder = "C:\\Users\\Administrator\\Desktop\\Firefly Naughty Kitten [FULL w ANIM]\\"
    testpath = mod_root_folder + "FireflyBodyA.ib"
    ib_buf_file = IndexBufferBufFile(FilePath=testpath,Stride=4)
    print(ib_buf_file)

    # How to manually reverse a mod.
    # 1.fill a dict thant contains category name and buf file path

    category_name__buf_file_path__dict = {}
    category_name__buf_file_path__dict["Position"] = mod_root_folder + "FireflyBodyPosition.buf"
    category_name__buf_file_path__dict["Position"] = mod_root_folder + "FireflyBodyTexcoord.buf"
    category_name__buf_file_path__dict["Position"] = mod_root_folder + "FireflyHairBlend.buf"

    # trigger auto game type detect to know which GameType it use.
    