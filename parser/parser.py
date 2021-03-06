#!/usr/bin/env python
# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from exception import *
from utilities.file.name import get_date_for_filename
from ip_utils import ip_to_int, int_to_ip, cidr_to_int, IPV4_ADDRESSABLE_SPACE

class Parser(object):
    """
    High level parser object to store information across the various low-level
    parsers. This object does not actually parse any files - this work should
    be carried out by subclasses of this object.
    """
    def __init__(self, filename=None):
        self.datetime               = None if filename is None else get_date_for_filename(filename)
        self.asys_to_ip_addr        = {}
        self.ip_addr_to_asys        = {}
        self.asys_connections       = set()
        self.asys_size              = {}
        self.visible_blocks         = []
        self.ip_block_path          = {}
        self.highest_ip_encountered = 0

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------

    def get_visible_space_size(self):
        block_sizes = [cidr_to_int(cidr) for (_, cidr) in self.visible_blocks]
        return sum(block_sizes)

    def get_block_size_totals(self):
        totals = [0] * 32

        for (ip, cidr) in self.visible_blocks:
            totals[cidr - 1] += 1

        return totals

    # --------------------------------------------------------------------------
    # Recording data from derived parsers
    # --------------------------------------------------------------------------

    def record_line_details(self, ip_addr, cidr_size, asys_path):
        self.record_asys_connections(asys_path)
        self.record_ip_addr_asys(ip_addr, asys_path)
        self.record_asys_path(ip_addr, asys_path)

        if not self.ip_addr_already_recorded(ip_addr):
            self.record_asys_size(asys_path, cidr_size)
            self.mark_block_visible(ip_addr, cidr_size)

    def record_asys_connections(self, asys_path):
        for counter in range(1, len(asys_path)):
            prev_asys  = asys_path[counter - 1]
            curr_asys  = asys_path[counter]

            if prev_asys == curr_asys:
                continue

            connection = (min(prev_asys, curr_asys), max(prev_asys, curr_asys))
            self.asys_connections.add(connection)

    def ip_addr_already_recorded(self, ip_addr):
        ip_as_int = ip_to_int(ip_addr)
        return ip_as_int < self.highest_ip_encountered

    def record_ip_addr_asys(self, ip_addr, asys_path):
        dest_asys = asys_path[-1]

        if dest_asys not in self.asys_to_ip_addr:
            self.asys_to_ip_addr[dest_asys] = set()

        if ip_addr not in self.ip_addr_to_asys:
            self.ip_addr_to_asys[ip_addr] = set()

        self.asys_to_ip_addr[dest_asys].add(ip_addr)
        self.ip_addr_to_asys[ip_addr].add(dest_asys)

    def record_asys_size(self, asys_path, cidr_size):
        asys = asys_path[-1]
        size = cidr_to_int(cidr_size)

        if asys in self.asys_size:
            self.asys_size[asys] += size
        else:
            self.asys_size[asys] = size

    def record_asys_path(self, ip_addr, asys_path):
        if ip_addr not in self.ip_block_path:
            self.ip_block_path[ip_addr] = []

        self.ip_block_path[ip_addr].append(asys_path)

    def mark_block_visible(self, ip_addr, cidr_size):
        ip_as_int = ip_to_int(ip_addr)
        ip_block  = (ip_as_int, cidr_size)
        size      = cidr_to_int(cidr_size)

        self.visible_blocks.append(ip_block)
        self.highest_ip_encountered = ip_as_int + size

    def integrity_check(self):
        visible_space = self.get_visible_space_size()

        if visible_space > IPV4_ADDRESSABLE_SPACE:
            raise ParserError("Visible space too large")
