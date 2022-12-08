import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import supervisely as sly

# load ENV variables for debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


class MyImport(sly.app.Import):
    def process(self, context: sly.app.Import.Context):
        # create api object to communicate with Supervisely Server
        api = sly.Api.from_env()

        # read input file, remove empty lines + leading & trailing whitespaces
        with open(context.path) as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        # process text file and remove empty lines
        progress = sly.Progress("Processing urls", total_cnt=len(lines))
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
                info = api.image.upload_path(context.dataset_id, img_name, img_path)
                sly.logger.trace(
                    f"Image has been uploaded: id={info.id}, name={info.name}"
                )

                # remove local file after upload
                os.remove(img_path)
            except Exception as e:
                sly.logger.warn("Skip image", extra={"url": img_url, "reason": repr(e)})
            finally:
                progress.iter_done_report()

        if sly.utils.is_production():
            os.remove(context.path)
        return context.project_id


app = MyImport()
app.run()
