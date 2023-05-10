import os
from dotenv import load_dotenv
import supervisely as sly

# load ENV variables for debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


class MyImport(sly.app.Import):
    def process(self, context: sly.app.Import.Context):
        # create api object to communicate with Supervisely Server
        api = sly.Api.from_env()

        # list images in directory
        images_names = []
        images_paths = []
        for file in os.listdir(context.path):
            file_path = os.path.join(context.path, file)
            images_names.append(file)
            images_paths.append(file_path)

        # process images and upload them by paths
        progress = sly.Progress("Processing images", total_cnt=len(images_names))
        for img_name, img_path in zip(images_names, images_paths):
            try:
                # upload image into dataset on Supervisely server
                info = api.image.upload_path(
                    dataset_id=context.dataset_id, name=img_name, path=img_path
                )
                sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")

                # remove local file after upload
                if sly.utils.is_production():
                    os.remove(img_path)
            except Exception as e:
                sly.logger.warn("Skip image", extra={"name": img_name, "reason": repr(e)})
            finally:
                progress.iter_done_report()

        return context.project_id


app = MyImport()
app.run()
