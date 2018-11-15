#!/usr/bin/python

import os

def worker_space():
    return os.path.split(os.path.realpath(__file__))[0]

def go_path():
    return os.environ.get('GOPATH').split(":")

def check_env():
    dir = worker_space()
    idx = dir.rfind('src')
    if idx < 0:
        return False
    path = go_path()
    for p in path:
        if p.strip('/') == dir[:idx].strip('/'):
            return True

    return False

def regin():
    src = 'src'
    space = worker_space()
    index = space.rfind(src)
    head = space[:index].rstrip('/')
    tail = space[index:].lstrip(src).strip('/')
    print("Project Is >> ", tail)
    
    os.system("rm -rf %s"%(space + "/api/*"))
    
    files = os.listdir(space + "/proto")
    for file in files:
        if not file.endswith('.proto'):
            continue

        path = space + "/proto/" + file
        base = head + "/src"
        order = "cd %s; protoc -I %s --go_out=plugins=grpc:. %s"%(base, base, path)
        print(">>> ", order)
        os.system(order)


def main():
    if not check_env():
        print('project not in gopath')
        exit(1)

    regin()

if __name__ == '__main__':
    main()