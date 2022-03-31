from argparse import ArgumentParser

from app import consts
from app.proxyserver import ProxyServer


def get_args_parser() -> ArgumentParser:
    """Build argument parser."""
    parser = ArgumentParser(description="Hacker News proxy")
    parser.add_argument(
        "-l",
        "--length",
        nargs="?",
        type=int,
        const=consts.WORD_LEN,
        default=consts.WORD_LEN,
        help="specifies the length of the word to add characters",
        dest="word_len",
    )
    parser.add_argument(
        "-t",
        "--text",
        nargs="?",
        type=str,
        const=consts.WORD_APP,
        default=consts.WORD_APP,
        help="Text appended to matched by length words",
        dest="word_app",
    )
    parser.add_argument(
        "-u",
        "--url",
        nargs="?",
        type=str,
        const=consts.TARGET_URL,
        default=consts.TARGET_URL,
        help="Proxyfied server URL (e.g. 'https://test.com/')",
        dest="target_url",
    )
    parser.add_argument(
        "-p",
        "--port",
        nargs="?",
        type=int,
        const=consts.PORT,
        default=consts.PORT,
        help="HTTP proxy server listen port",
        dest="port",
    )
    parser.add_argument(
        "-a",
        "--addr",
        nargs="?",
        type=str,
        const=consts.SOURCE_IPV4,
        default=consts.SOURCE_IPV4,
        help="HTTP proxy server binded address",
        dest="source_ipv4",
    )
    return parser


def main():
    """Run Hacker News server."""
    parser = get_args_parser()
    args = parser.parse_args()
    args.regex_patcher = False
    #: add trailing slash
    if args.target_url[-1] != '/':
        args.target_url += '/'
    pr = ProxyServer(args)
    pr.run()


if __name__ == "__main__":
    main()
