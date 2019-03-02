import sys
import requests


def parser():
    """
    Parses the arguments
    @:return returns the dictionary with objects and servers
    """
    # TODO: empty parameters --> usage message
    # TODO: it must have at least 1 object and 1 server
    arg = {"objects": [], "servers": []}
    for a in sys.argv[1:]:
        if a[0] == ':':
            arg["servers"].append(a[1:])
        else:
            arg["objects"].append(a)
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
    # print("arg in ping", arg)
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
        for size in packages[pack]:
            next_size = last_size + size +1
            headers = {"Range": "bytes=%d-%d" % (last_size+1, next_size)}
            print("headers", headers)
            url = "%s/%s" % (args["servers"][i], pack)
            req = requests.get(url, headers=headers).content
            i += 1
            aux_item.append(req)
            last_size = next_size
        item = "".join(map(str, aux_item)).replace("b", "").replace("'", "")
        items_list[pack] = item
    return items_list


if __name__ == "__main__":
    args = parser()
    ping_alive(args)
    sizes = get_sizes(args)
    packages = prepare_package(sizes, args)
    items = make_request(args, packages)
    for item in items:
        print(item, items[item])

    print("mine\t", items["~fperez/reto2.txt"])
    print("max\t", "acdefghijacdefghijacdefghijacdefghijABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJAABCDEFGHIJABCDEFGHIJacdefghijacdefghija")
    print("web\t", "ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghija" )

