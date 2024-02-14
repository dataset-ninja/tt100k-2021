import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_ext, get_file_name
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    train_images_path = "/home/alex/DATASETS/TODO/Traffic-Sign Wild/tt100k_2021/train"
    other_images_path = "/home/alex/DATASETS/TODO/Traffic-Sign Wild/tt100k_2021/other"
    test_images_path = "/home/alex/DATASETS/TODO/Traffic-Sign Wild/tt100k_2021/test"
    json_path = "/home/alex/DATASETS/TODO/Traffic-Sign Wild/tt100k_2021/annotations_all.json"
    batch_size = 30
    images_ext = ".jpg"

    ds_name_to_data = {
        "train": train_images_path,
        "other": other_images_path,
        "test": test_images_path,
    }

    def create_ann(image_path):
        labels = []

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 2048  # image_np.shape[0]
        img_wight = 2048  # image_np.shape[1]

        image_name = get_file_name(image_path)

        ann_data = name_to_data.get(image_name)
        if ann_data is not None:
            for curr_ann_data in ann_data:
                curr_class_name = curr_ann_data["category"]
                obj_class = meta.get_obj_class(curr_class_name)
                bbox_coord = curr_ann_data["bbox"]
                rectangle = sly.Rectangle(
                    top=int(bbox_coord["ymin"]),
                    left=int(bbox_coord["xmin"]),
                    bottom=int(bbox_coord["ymax"]),
                    right=int(bbox_coord["xmax"]),
                )
                label_rectangle = sly.Label(rectangle, obj_class)
                labels.append(label_rectangle)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    all_classes = []
    anns_data = load_json_file(json_path)
    classes_names = anns_data["types"]
    for class_name in classes_names:
        obj_class = sly.ObjClass(class_name, sly.Rectangle)
        all_classes.append(obj_class)

    name_to_data = {}
    images_to_data = anns_data["imgs"]
    for im_name, im_data in images_to_data.items():
        name_to_data[im_name] = im_data["objects"]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=all_classes)
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, images_path in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_names = [
            im_name for im_name in os.listdir(images_path) if get_file_ext(im_name) == images_ext
        ]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [
                os.path.join(images_path, image_name) for image_name in images_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
