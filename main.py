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
import logging
import logging.config

import splitfolders
import yaml

from src.catalog import Catalog
from src.download import html_download, tgz_extract
from src.parameters import Parameters
from src.split import label_data

with open("config/logging.yml", "rt", encoding="utf-8") as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("default")


def main(arguments: argparse.Namespace):
    """Main function."""

    logger.info("Loading configuration...")

    catalog = Catalog()
    params = Parameters()

    if arguments.download:

        logger.info("Getting data...")

        # Get image data
        compressed_file = html_download(
            url=params.download_data.url, destination=catalog.temp.path
        )
        tgz_extract(
            source=compressed_file,
            destination=catalog.temp.path,
            extension=params.download_data.extension,
        )

        # Get label data
        labels_file = html_download(
            url=params.download_labels.url,
            destination=catalog.temp.path,
            name=params.download_labels.name,
        )

        # Organise the images
        label_data(
            labels_path=labels_file,
            img_path=catalog.temp.path,
            output_path=catalog.raw.path,
        )

        # Split the images
        logger.info("Splitting images...")
        splitfolders.ratio(
            catalog.raw.path,
            output=catalog.data.path,
            seed=params.split.seed,
            ratio=params.split.ratio,
            group_prefix=None,
        )

    if arguments.train:
        pass

    if arguments.predict:
        pass


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
