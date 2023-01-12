import os
from shutil import unpack_archive

import supervisely as sly
from supervisely.io.fs import download, silent_remove, get_file_name_with_ext
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

        # get working directory path (specified in local.env)
        work_dir = sly.app.get_data_dir()
        # link to demo data
        link = "https://github.com/supervisely-ecosystem/template-import-from-file/releases/download/untagged-4ed984324128e4e02891/demo_data.zip"
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
                info = api.image.upload_path(context.dataset_id, img_name, img_path)
                sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")
                # remove local file after upload
                os.remove(img_path)
            except Exception as e:
                sly.logger.warn("Skip image", extra={"path": img_path, "reason": repr(e)})
            finally:
                progress.iter_done_report()

        # remove local file after upload
        if sly.utils.is_production():
            os.remove(context.path)
        return context.project_id


app = MyImport()
app.run()
