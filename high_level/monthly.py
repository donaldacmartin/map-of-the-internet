#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.threads import run_bgp_dump, generate_chrono_map
from utilities.file_search import get_bgp_binaries_in

def generate_monthly_diff():
    bgp_files = __get_list_of_files()
    bgp_dumps = run_bgp_dump(bgp_files)
    generate_chrono_map(bgp_files, bgp_dumps)
    
def __get_list_of_files():
    base_dir  = "/nas05/users/csp/routing-data/archive.routeviews.org/bgpdata/"
    all_files = get_bgp_files_in(base_dir)
    months    = []
    
    for year in range(2001, 2015):
        for month in range(1, 13):
            months.append(__filter_a_file(all_files, year, month))
    
    return months
    
def __filter_a_file(files, month, year):
    name_key = "rib." + str(year) + str(month).zfill(2)
    
    for bgp_file in all_files:
        if name_key in bgp_file:
            return bgp_file
            
    return None