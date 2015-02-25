class MergedParser(object):
    def __init__(self, bgp_dump1, bgp_dump2):
        self.merge_connections(bgp_dump1, bgp_dump2)
        self.merge_lookup(bgp_dump1, bgp_dump2)

    def merge_connections(self, bgp_dump1, bgp_dump2):
        merged = bgp_dump1.asys_connections.union(bgp_dump2.asys_connections)
        self.asys_connections = merged

    def merge_lookup(self, bgp_dump1, bgp_dump2):
        self.ip_addr_to_asys = bgp_dump1.ip_addr_to_asys
        self.ip_addr_to_asys.update(bgp_dump2.ip_addr_to_asys)
