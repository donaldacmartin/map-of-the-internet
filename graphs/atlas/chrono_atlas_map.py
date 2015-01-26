#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from graphs.atlas.atlas_map import AtlasMap, GLOBAL
from base_atlas import BaseAtlas, GLOBAL
from graphs.graph import LIGHT_GREY, LIGHT_GREEN, DARK_RED

"""
ChronoAtlasMap
"""

class ChronologicalAtlas(BaseAtlas):
    def __init__(self, width, height, old_bgp, new_bgp, region=GLOBAL):
        super(ChronologicalAtlas, self).__init__(width, height, region)

        self.resolve_bgp_to_asys_coords(old_bgp)
        self.resolve_bgp_to_asys_coords(new_bgp)

        old_cxns = old_bgp.asys_connections
        new_cxns = new_bgp.asys_connections

        unchanged = old_cxns.intersection(new_cxns)
        removed   = old_cxns.difference(new_cxns)
        added     = new_cxns.difference(old_cxns)

        self.draw_international_boundaries()

        self.draw_connections(unchanged, LIGHT_GREY)
        self.draw_connections(removed, DARK_RED)
        self.draw_connections(added, LIGHT_GREEN)
