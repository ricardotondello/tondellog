import argparse

from tondellog.config import Config
from tondellog.generator import ChangeLogGenerator


def init_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Init the config file in './tondellog.config'")

    parser_output = subparsers.add_parser("output", help = "Output the changelog file")
    parser_output.add_argument("file", nargs='?', default="./CHANGELOG.md", help="The file to output the changelog")
    parser_output.add_argument("branch1", nargs='?', default="master", help="Branch to campare")
    parser_output.add_argument("branch2", nargs='?', default="develop", help="Branch base")
    
    return parser


def main():
    parser = init_args()
    args = parser.parse_args()
    if args.command == 'init':
        cfg = Config.from_prompt()
        cfg.save()
    elif args.command == 'output':
        cfg = Config.load()
        gen = ChangeLogGenerator.from_config(cfg, output=args.file, branch1=args.branch1, branch2=args.branch2)
        gen.generate()
    else:
        parser.print_help()
