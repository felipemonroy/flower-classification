import logging
import os
import shutil
from csv import DictReader

logger = logging.getLogger("default")


def label_data(
    labels_path: str,
    img_path: str,
    output_path: str,
) -> None:
    """
    Divide the images into different folders depending on their label.
    """

    logger.info("Labelling data...")

    with open(labels_path, "r", encoding="utf-8") as read_obj:
        csv_dict_reader = DictReader(read_obj)

        for row in csv_dict_reader:
            full_img_path = os.path.join(img_path, row["path"])
            file_name = os.path.split(full_img_path)[-1]
            out_path = os.path.join(output_path, row["label"], file_name)
            out_folder = os.path.join(output_path, row["label"])

            if not os.path.isdir(out_folder):
                os.makedirs(out_folder)

            shutil.copy(full_img_path, out_path)
