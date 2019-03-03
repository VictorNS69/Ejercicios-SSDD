__author__ = "Víctor Nieves Sánchez"
__copyright__ = "Copyright 2019, Víctor Nieves"
__credits__ = ["Víctor Nieves Sánchez", "Máximo García Martínez"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Víctor Nieves Sánchez"
__email__ = "vnievess@gmail.com"
__status__ = "Finished"

import sys
import requests
import os

USAGE = "usage: mpwget [object] ... [server] ...\nUse at least 1 object and 1 server\n" \
        "\tobject\t: object to get\n\tserver\t: server to search"


def parser():
    """
    Parses the arguments and exist if it exist if it is not called correctly
    @:return returns the dictionary with objects and servers
    """
    # Call with no arguments
    if len(sys.argv) < 3:
        print(USAGE)
        exit(0)

    arg = {"objects": [], "servers": []}

    for a in sys.argv[1:]:
        if a[0] == ':':
            arg["servers"].append(a[1:])
        else:
            arg["objects"].append(a)

    # Call with less than 1 object or 1 server
    if len(arg["objects"]) == 0:
        print("At least one object required\n", USAGE)
        exit(0)
    if len(arg["servers"]) == 0:
        print("At least one server required\n", USAGE)
        exit(0)

    return arg


def ping_alive(arg):
    """
    Modifies the input dictionary with the alive servers
    :param arg: dictionary with objects and servers
    :return: The same dictionary with only alive servers
    """
    for server in arg["servers"]:
        try:
            req = requests.head(server)
            if not req.status_code == 200:
                arg["servers"].remove(server)
        except Exception:
            arg["servers"].remove(server)
            print("The server", server, "cannot be reached", file=sys.stderr)
    return arg


def get_sizes(args):
    """
    Calculates the size of every object
    @:param args: dictionary of objects and servers
    @:return Returns the size for every object
    """
    sizes = {}
    for server in args["servers"]:
        for obj in args["objects"]:
            req = requests.head("%s/%s" % (server, obj))
            if not req.status_code == 200:
                print("The object", obj, "cannot be reached in", server, file=sys.stderr)
                args["objects"].remove(obj)
                continue
            sizes[obj] = req.headers["content-length"]
    return sizes


def prepare_package(sizes, args):
    """
    Prepares the bytes of the object to be send to each server
    :param sizes: dictionary with the sizes of each objects
    :param args: dictionary with objects and servers
    :return: a dictionary with objects and list of bytes to be send
    """
    packages = {}
    for obj in sizes:
        package = []
        value = 0
        scope = int(sizes[obj])
        while not value == scope:
            sol = int(sizes[obj]) / len(args["servers"])
            value += round(sol)
            if value > scope:
                value -= round(sol)
                break
            package.append(round(sol))
        if not scope-value == 0:
            package.append(scope-value)
        packages[obj] = package
    return packages


def make_request(args, packages):
    """
    Creates the request of the object
    :param args: dictionary with objects and servers
    :param packages: dictionary of the packages to send
    :return: The string of the retrieved object
    """
    items_list = {}
    for pack in packages:
        last_size = -1
        i = 0
        aux_item = []
        print("Package:", pack)
        for size in packages[pack]:
            next_size = last_size + size
            headers = {"Range": "bytes=%d-%d" % (last_size+1, next_size)}
            url = "%s/%s" % (args["servers"][i], pack)
            print("\t\tFetching:", str(headers).replace("{", "").replace("}", "").replace("'", ""))
            req = requests.get(url, headers=headers).content
            i += 1
            aux_item.append(req)
            last_size = next_size
        print("Total size:", last_size + 1, "Bytes")
        print("-" * 80)
        item = bytes()
        for i in range(0, len(aux_item)):
            item += aux_item[i]
        items_list[pack] = item
    return items_list


def generate_files(items):
    """
    Generates the downloaded objects as files
    :param items: dictionary with objects and its bytes
    :return:the files in the actual directory
    """
    for item in items:
        if not os.path.isdir("objects/"):
            os.makedirs("objects")

        name = str(item).split("/")
        path = "objects/" + name[-1]
        with open(path, "wb") as f:
            f.write(items[item])


if __name__ == "__main__":
    args = parser()
    ping_alive(args)
    if len(args["servers"]) == 0:
        print("Any of the servers is available", file=sys.stderr)
        exit(0)
    sizes = get_sizes(args)
    if len(sizes) == 0:
        print("Any object found in any server", file=sys.stderr)
        exit(0)
    packages = prepare_package(sizes, args)
    items = make_request(args, packages)
    generate_files(items)
    print("Elements downloaded in /objects")
    exit(0)
