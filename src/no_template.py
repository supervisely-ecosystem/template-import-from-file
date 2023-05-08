import os
import shutil
from pathlib import Path

import requests
from tqdm import tqdm
from dotenv import load_dotenv
import supervisely as sly

# load ENV variables for debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

# create api object to communicate with Supervisely Server
api = sly.Api.from_env()

# get current context of import
TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
PROJECT_ID = sly.env.project_id(raise_not_found=False)
DATASET_ID = sly.env.dataset_id(raise_not_found=False)
PATH_TO_FILE = sly.env.file()

# define local storage directory for files and create it
STORAGE_DIR = sly.app.get_data_dir()
if os.path.exists(STORAGE_DIR) is False:
    os.mkdir(STORAGE_DIR)

# get project and dataset info or create new ones if not specified
if PROJECT_ID is None:
    project = api.project.create(
        workspace_id=WORKSPACE_ID, name="My Project", change_name_if_conflict=True
    )
else:
    project = api.project.get_info_by_id(PROJECT_ID)
if DATASET_ID is None:
    dataset = api.dataset.create(project_id=project.id, name="ds0", change_name_if_conflict=True)
else:
    dataset = api.dataset.get_info_by_id(DATASET_ID)

# get file name and specify local path to download
file_info = api.file.get_info_by_path(team_id=TEAM_ID, remote_path=PATH_TO_FILE)
local_file_path = os.path.join(STORAGE_DIR, file_info.name)
# download file from Supervisely Team Files to local storage
api.file.download(team_id=TEAM_ID, remote_path=PATH_TO_FILE, local_save_path=local_file_path)

# read input file, remove empty lines + leading & trailing whitespaces
with open(local_file_path) as file:
    lines = [line.strip() for line in file.readlines() if line.strip()]

# process text file and remove empty lines with sly tqdm progress bar
with tqdm(total=len(lines)) as pbar:
    for index, img_url in enumerate(lines):
        try:
            img_ext = Path(img_url).suffix
            img_name = f"{index:03d}{img_ext}"
            img_path = os.path.join(sly.app.get_data_dir(), img_name)
            # download image
            response = requests.get(img_url)
            with open(img_path, "wb") as file:
                file.write(response.content)
            # upload image into dataset on Supervisely server
            info = api.image.upload_path(dataset.id, img_name, img_path)
            sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")
            # remove local file after upload
            os.remove(img_path)
        except Exception as e:
            sly.logger.warn("Skip image", extra={"url": img_url, "reason": repr(e)})
        finally:
            pbar.update(1)

# remove local storage directory with files
shutil.rmtree(STORAGE_DIR)
