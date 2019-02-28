import argparse


def possible_server(args):
    """
    If the args starts with : it is a possible server
    """
    return str(args).startswith(":")


def parsing():
    """
    Parser
    @:return returns the dictionary with objects and servers
    """
    parser = argparse.ArgumentParser(prog="mpwget")

    # At least 1 object
    parser.add_argument("object", nargs="+", help="the objects to get")
    # At least 1 server
    parser.add_argument("server", nargs="+", help="the servers to search")

    args = parser.parse_args()

    # Initialize an empty dictionary with objects and servers (lists)
    d = {"objects": [], "servers": []}

    for l in args.object, args.server:
        for item in l:
            if possible_server(item):
                d["servers"].append(item)
            else:
                d["objects"].append(item)

    return d


def main():
    args = parsing()
    print("objects:", args["objects"])
    print("servers:", args["servers"])


if __name__ == "__main__":
    print("MAIN")
    main()
