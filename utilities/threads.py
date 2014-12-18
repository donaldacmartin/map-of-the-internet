#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.bgp import BGPDumpExecutor
from multiprocessing import Process
from graphs.chrono_atlas_map import ChronologicalAtlasMap

def run_bgp_dump(files):
    threads   = []
    bgp_dumps = {}
    
    for bgp_file in files:
        thread = Process(target=__bgp_dump_thread, args=(bgp_file, bgp_dumps,))
        threads.append(thread)
        thread.start()
    
    __wait(threads)
    return threads, bgp_dumps
    
def generate_chrono_map(filenames, threads, bgp_dumps, asys_coords, image_db):
    threads = []
    asys_coords = {}
    
    for i in range(1, len(filenames)):
        prev_dump = bgp_dumps[filenames[i-1]]
        curr_dump = bgp_dumps[filenames[i]]
        
        args = (prev_dump, curr_dump, i, image_db, asys_coords,)
        thread = Process(target=__generate_chrono_map_thread, args=args)
        threads.append(thread)
        thread.start()
        
    __wait(threads)
    
def __bgp_dump_thread(file_path, bgp_database):
    bgp = BGPDumpExecutor(file_path)
    bgp_database[file_path] = bgp
    print("Finished")

def __wait(threads):
    for thread in threads:
        thread.join()
        
def __generate_chrono_map_thread(bgp_dump1, bgp_dump2, counter, image_db, asys_coords):
    prev_cxns = bgp_dump1.as_connections
    curr_cxns = bgp_dump2.as_connections
    
    prev_addr = bgp_dump1.as_to_ip_address
    curr_addr = bgp_dump2.as_to_ip_address
    
    chrono = ChronologicalAtlasMap(1920,1080, prev_cxns, curr_cxns, prev_addr, curr_addr, asys_coords)
    chrono.save(str(counter) + ".png")
    image_db[i] = chrono.image