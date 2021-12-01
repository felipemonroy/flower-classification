"""
MIT License

Copyright (c) 2021 Felipe Monroy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse

from src.catalog import Catalog
from src.download import DataGetter, HTMLDownloader, TGZExtractor
from src.parameters import Parameters


def main(arguments: argparse.Namespace):
    """Main function."""

    catalog = Catalog()
    params = Parameters()

    # Get image data
    downloader = HTMLDownloader(params.download_data.url, catalog.temp.path)
    extractor = TGZExtractor(
        downloader.path, catalog.raw.path, extension=params.download_data.extension
    )
    data_getter = DataGetter(downloader, extractor)
    data_getter.get_data()

    # Get label data
    downloader = HTMLDownloader(
        params.download_labels.url, catalog.raw.path, params.download_labels.name
    )
    data_getter = DataGetter(downloader)
    data_getter.get_data()


def str2bool(value: str) -> bool:
    """Transfrom a string to bool"""
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="classification")

    parser.add_argument(
        "--download",
        "-d",
        type=str2bool,
        nargs="?",
        const=True,
        default=False,
        help="Download the data for %(prog)s.",
    )

    parser.add_argument(
        "--train",
        "-t",
        type=str2bool,
        nargs="?",
        const=True,
        default=True,
        help="Train the %(prog)s.",
    )

    parser.add_argument(
        "--predict",
        "-p",
        type=str2bool,
        nargs="?",
        const=False,
        default=True,
        help="Predict %(prog)s.",
    )

    args = parser.parse_args()

    main(args)
