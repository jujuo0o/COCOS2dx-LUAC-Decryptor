import argparse
from decryptor import Decryptor

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file")
    group.add_argument("-p", "--pid")
    group.add_argument("-g", "--gadget")
    parser.add_argument("-l", "--lib", default="libqpry_lua.so")
    parser.add_argument("-o", "--offset", default="0x005FFB38")
    parser.add_argument("--lua-header", default="RY_QP_2016")
    parser.add_argument("--folder")
    
    args = parser.parse_args()
    if args.file or args.pid or args.gadget and args.folder:
        decryptor = Decryptor(args.file, args.pid, args.gadget, args.lua_header)
        decryptor.run(args.folder, args.lib, args.offset)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()