import os
from shutil import unpack_archive

import supervisely as sly
from supervisely.io.fs import download, silent_remove, get_file_name_with_ext, remove_dir
from dotenv import load_dotenv

# load ENV variables for debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


class MyImport(sly.app.Import):
    # override method for external imports outside of Team Files
    def is_path_required(self) -> bool:
        return False

    def process(self, context: sly.app.Import.Context):
        # create api object to communicate with Supervisely Server
        api = sly.Api.from_env()

        # get or create project
        project_id = context.project_id
        if project_id is None:
            project = api.project.create(
                workspace_id=context.workspace_id, name="My Project", change_name_if_conflict=True
            )
            project_id = project.id

        # get or create dataset
        dataset_id = context.dataset_id
        if dataset_id is None:
            dataset = api.dataset.create(
                project_id=project_id, name="ds0", change_name_if_conflict=True
            )
            dataset_id = dataset.id

        # get working directory path (specified in local.env)
        work_dir = sly.app.get_data_dir()
        # link to demo data
        link = "https://github.com/supervisely-ecosystem/template-import-from-file/releases/download/v0.0.1/demo_data.zip"
        # save path for data
        archive_path = os.path.join(work_dir, "demo_data.zip")

        # download file from link
        try:
            download(url=link, save_path=archive_path)
        except Exception as e:
            sly.logger.error(
                "Couldn't download file from link", extra={"link": link, "reason": repr(e)}
            )
            raise e

        # unpack and remove downloaded archive
        unpack_archive(archive_path, extract_dir=work_dir)
        silent_remove(archive_path)

        # read input file, remove empty lines + leading & trailing whitespaces
        images_paths = [os.path.join(work_dir, image_path) for image_path in os.listdir(work_dir)]

        progress = sly.Progress("Processing urls", total_cnt=len(images_paths))
        for img_path in images_paths:
            try:
                img_name = get_file_name_with_ext(img_path)
                # upload image into dataset on Supervisely server
                info = api.image.upload_path(dataset_id, img_name, img_path)
                sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")
            except Exception as e:
                sly.logger.warn("Skip image", extra={"path": img_path, "reason": repr(e)})
            finally:
                # remove local file after upload
                os.remove(img_path)
                progress.iter_done_report()

        # remove local file after upload
        if sly.utils.is_production():
            remove_dir(work_dir)
        return project_id


app = MyImport()
app.run()
