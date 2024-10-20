# Nico: I have to say, use python to test is more simple and fast than C++

from global_config import GlobalConfig,FrameAnalysisUtil
from dbmt_log_utils import log_newline,log_info

import os


if __name__ == "__main__":
    wuwa_loader_folder = "C:\\Users\\Administrator\\Desktop\\DBMT\\Games\\WW1.1\\3Dmigoto\\"
    wuwa_frame_analysis_folder = "FrameAnalysis-2024-10-20-134435"
    draw_ib = "94517393"
    g = GlobalConfig(LoaderFolder=wuwa_loader_folder,FrameAnalysisFolder=wuwa_frame_analysis_folder,GameName="WuWa")

    fautil = FrameAnalysisUtil(WorkFolder=g.WorkFolder)
    
    # test if we can get attribute successfully.
    print(fautil.WorkFolder)
    print(fautil.FileNameList)
    log_newline()
    
    # test get ib related files.
    ib_related_files = fautil.filter_filename(contain=draw_ib,suffix=".txt")
    log_info(ib_related_files)
    log_newline()

    # test to get index list by draw ib.
    index_list = fautil.get_indexlist_by_drawib(drawib=draw_ib)
    log_info(index_list)
    log_newline()

    # get index by draw ib and show their related vb files.
    for index in index_list:
        index_vb_files = fautil.filter_filename(contain=index + "-vb",suffix=".buf")
        for index_vb_filename in index_vb_files:
            vb_file_path = g.WorkFolder + index_vb_filename
            filesize = os.path.getsize(vb_file_path)
            log_info(index_vb_filename + " Size: " + str(filesize))
            if "vb0" in index_vb_filename:
                log_info("Position Buffer Found, VertexCount:" + str(filesize / 12))
        log_newline()
    
    # wuwa 1.3 use vb6 as shape key buffer, and all vb5 buffer is not used, vb5 default size is 12, full of empty zero.
    # so we can get shape key buffer if it's vb6 buffer size is not 12 or 0
    
    # Vertex Count is 36277 and vb6 size is 846648 
    print(846648 / 35277)
    log_newline()
    # so we get vb6 stride is 24.

    

