from sys import argv
from parallel.utils import *
from parallel.arguments import *

from visualisation.atlas.base import *
from visualisation.atlas.standard import StandardAtlas
from visualisation.atlas.heat import HeatAtlas
from visualisation.ring.standard import StandardRing
from visualisation.ring.staggered import StaggeredRing

def organise_arguments():
    if not 5 <= len(argv) <= 6:
        print("Incorrect argument usage")
        print("Arguments: GRAPH_TYPE DATE RESOLUTION [REGION] OUTPUT_FILENAME")
        exit()

    graph_type      = get_graph_type(argv[1])
    date            = get_date(argv[2])
    width, height   = get_resolution(argv[3])
    region          = None if len(argv) < 6 else get_region(argv[4])
    output_filename = argv[4] if len(argv) < 6 else argv[5]

    return graph_type, date, width, height, region, output_filename

def get_region(arg):
    if arg not in ["GLOBAL", "AFRICA", "EUROPE", "NORTH_AMERICA", "SOUTH_AMERICA"]:
        print("Region must be one of the following:")
        print("AFRICA")
        print("EUROPE")
        print("NORTH_AMERICA")
        print("SOUTH_AMERICA")
        exit()

    if arg == "AFRICA":
        return AFRICA
    elif arg == "EUROPE":
        return EUROPE
    elif arg == "NORTH_AMERICA":
        return NORTH_AMERICA
    elif arg == "SOUTH_AMERICA":
        return SOUTH_AMERICA

    return GLOBAL

def get_graph_type(arg):
    graph_types = ["STANDARD_ATLAS", "HEAT_ATLAS", "STANDARD_RING",
                   "STAGGERED_RING"]

    if arg not in graph_types:
        print("Invalid graph type")
        print("Options are: ")

        for graph in graph_types:
            print("- " + graph)

        exit()

    return arg

def generate_graph(graph_type, parser, width, height, region):
    if graph_type == "STANDARD_ATLAS":
        return StandardAtlas(parser, width, height, region)
    elif graph_type == "HEAT_ATLAS":
        return HeatAtlas(parser, width, height, region)
    elif graph_type == "STANDARD_RING":
        return StandardRing(parser, width, height)
    elif graph_type == "STAGGERED_RING":
        return StaggeredRing(parser, width, height)

if __name__ == "__main__":
    graph_type, date, width, height, region, output_filename = organise_arguments()

    print("Gathering a list of files to parse")
    bgp_files = get_router_files_for_date(date.year, date.month, date.day)
    parallel_index = get_index_file(bgp_files)

    print("Parsing BGP files in parallel (" + str(len(bgp_files)) + ")")
    parsing_stdout = run_parallel_parser(parallel_index)

    print("Collating parsed data")
    dump_locations = get_parser_dumps_from_parallel_stdout(parsing_stdout)
    parser         = merge_parsers(dump_locations, [bgp_files])[0]

    print("Drawing graph")
    graph = generate_graph(graph_type, parser, width, height, region)
    graph.save(output_filename)
