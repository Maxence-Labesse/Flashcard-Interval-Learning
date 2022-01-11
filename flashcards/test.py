import argparse


def hello(args):
    print('Hello, {0}!'.format(args.name))


def goodbye(args):
    print('Goodbye')


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

hello_parser = subparsers.add_parser('hello')
hello_parser.add_argument('name')  # add the name argument
hello_parser.set_defaults(func=hello)  # set the default function to hello

goodbye_parser = subparsers.add_parser('goodbye')
goodbye_parser.set_defaults(func=goodbye)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)  # call the default function
