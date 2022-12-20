# Create import app from template

## Introduction

In this tutorial, you will learn how to create custom import app for uploading your data to Supervisely platform using an import template app that we have prepared for you.

We advise reading our [from script to supervisely app](https://developer.supervise.ly/app-development/basics/from-script-to-supervisely-app) guide if you are unfamiliar with the [file structure](https://developer.supervise.ly/app-development/basics/from-script-to-supervisely-app#repository-structure) of a Supervisely app repository because it addresses the majority of the potential questions.

We will go through the following steps:

[**Step 1.**](#step-1-set-up-an-environment-for-development) Set up an environment for development.

[**Step 2.**](#step-2-how-to-debug-import-app) How to debug import app.

[**Step 3.**](#step-3-how-to-write-an-import-script) How to write an import script.

[**Step 4.**](#step-4-how-to-run-it-in-supervisely) How to run it in Supervisely.

Everything you need to reproduce [this tutorial is on GitHub](https://github.com/supervisely-ecosystem/hello-world-app): source code and additional app files.

## Step 1. Set up an environment for development

**Step 1.** Prepare `~/supervisely.env` file with credentials. [Learn more here.](https://developer.supervise.ly/getting-started/basics-of-authentication#how-to-use-in-python)

**Step 2.** Fork and clone [repository](https://github.com/supervisely-ecosystem/template-import-from-file) with source code and create [Virtual Environment](https://docs.python.org/3/library/venv.html).

```bash
git clone https://github.com/supervisely-ecosystem/template-import-from-file
cd template-import-from-file
./create_venv.sh
```

**Step 3.** Open repository directory in Visual Studio Code.

```bash
code -r .
```

**Step 4.** Select created virtual environment as python interpreter.

**Step 5.** Open `local.env` and insert your values here. Learn more about environment variables in our [guide](https://developer.supervise.ly/getting-started/environment-variables)

```python
TASK_ID=10                    # ⬅️ requires to use advanced debugging
TEAM_ID=1                     # ⬅️ change it
WORKSPACE_ID=1                # ⬅️ change it
PROJECT_ID=555                # ⬅️ specify when importing to existing project
DATASET_ID=55555              # ⬅️ specify when importing to existing dataset
FILE="data/my_project.txt"    # ⬅️ path to file that you want to import
SLY_APP_DATA_DIR="results/"   # ⬅️ path to directory for local debugging
```

## Step 2. How to debug import app

Import template has 2 launch options for debugging:

* `Debug: local file` - works with local file on your computer
* `Advanced debug: team files file` - download file from team files

We've prepared `my_project.txt` as a sample file. It contains 5 links to images that will be imported to the specified project and dataset.

Upload this file to `Team Files` to use with advanced debug.

`my_project.txt`

```text
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-couleur-2317904.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-kammeran-gonzalezkeola-7925859.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-stijn-dijkstra-7177188.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-taryn-elliott-3889728.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-taryn-elliott-9565787.jpg
```

<div align="center" markdown>
    <img src="https://user-images.githubusercontent.com/48913536/208120526-f35e4032-ad28-4f75-a614-938d29400426.png"/>
</div>

**Option 1. Debug: local file**

This option is good starting point, use it for debugging import template with your local file.

Specify path to your file in `local.env` - `FILE` variable, it can be absolute or relative path from project root ridectory.

```python
FILE="data/my_project.txt"    # ⬅️ change it
```

**Option 2. Advanced debug: team files file**

The advanced debugging option is somewhat identical, however it will download files from `Team Files` instead. This option is an example how production apps work in Supervisely platform.

Specify path to your file in `local.env` - `FILE` variable.
Notice that all paths in `Team Files` start with `/`. To ensure that path to your file is correct, use context menu of the file -> copy path.

<img src="https://user-images.githubusercontent.com/48913536/208065484-a674dc8b-ceb5-4fbd-aefb-bf7f93fb407e.png"/>

```python
FILE="/data/my_project.txt"    # ⬅️ change it
```

## Step 3. How to write an import script

**Step 1. Import libraries**

```python
import os
from pathlib import Path

import requests
import supervisely as sly
from dotenv import load_dotenv
```

**Step 2. Load environment variables**

Load ENV variables for debug, has no effect in production

```python
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
```

**Step 3. Write Import script**

Create a class that inherits from `sly.app.Import` and write `process` method that will handle the file that you specified in the `FILE` variable of the `local.env`. In this example our class called `MyImport`.

`sly.app.Import` class will handle all pre-import routines for you.
It will define destination project and dataset and will download your file to the chosen directory (`SLY_APP_DATA_DIR`) based on what you provided in the `local.env` file for local debugging from `Team Files`.

`sly.app.Import` has a `Context` subclass which contains all required information that you need for importing your file to Supervisely platform:

* Team ID - destination team id
* Workspace ID - destination workspace id
* Project ID - destination project id (differs from project id in `local.env` if you have specified it)
* Dataset ID - destination dataset id (differs from dataset id in `local.env` if you have specified it)
* Path: data/my_project.txt - Local path to downloaded file
* Is directory: False - Determines if path is a directory

 `context` variable is passed as a parameter to `process` method of class `MyImport` and `context` object will be created automatically when you execute import.

```python
class MyImport(sly.app.Import):
    def process(self, context: sly.app.Import.Context):
        print(context)
```

Output:

```text
Team ID: 1
Workspace ID: 1
Project ID: 5556
Dataset ID: 55556
Path: data/my_project.txt
Is directory: False
```

Now let's get to the code part

```python
class MyImport(sly.app.Import):
    def process(self, context: sly.app.Import.Context):
        # create api object to communicate with Supervisely Server
        api = sly.Api.from_env()

        # read input file, remove empty lines + leading & trailing whitespaces
        with open(context.path) as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        # create progress object to track uploading
        progress = sly.Progress("Processing urls", total_cnt=len(lines))
        # process text file and remove empty lines
        for index, img_url in enumerate(lines):
            try:
                img_ext = Path(img_url).suffix
                img_name = f"{index:03d}{img_ext}"
                img_path = os.path.join(sly.app.get_data_dir(), img_name)

                # download image from url
                response = requests.get(img_url)
                with open(img_path, "wb") as file:
                    file.write(response.content)

                # upload image into dataset on Supervisely server
                info = api.image.upload_path(context.dataset_id, img_name, img_path)
                sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")

                # remove image after upload
                os.remove(img_path)
            except Exception as e:
                sly.logger.warn("Skip image", extra={"url": img_url, "reason": repr(e)})
            finally:
                progress.iter_done_report()

        # remove local file after upload
        if sly.utils.is_production():
            os.remove(context.path)
        return context.project_id
```

Create `MyImport` object and execute `run` method to start import

```python
app = MyImport()
app.run()
```

Output of this python program:

```text
Importing to created Project: id=556, name=my_project
Importing to created Dataset: id=55556, name=ds0
{"message": "progress", "event_type": "EventType.PROGRESS", "subtask": "Processing urls", "current": 0, "total": 5, "timestamp": "2022-12-15T19:07:51.368Z", "level": "info"}
{"message": "progress", "event_type": "EventType.PROGRESS", "subtask": "Processing urls", "current": 1, "total": 5, "timestamp": "2022-12-15T19:07:53.672Z", "level": "info"}
{"message": "progress", "event_type": "EventType.PROGRESS", "subtask": "Processing urls", "current": 2, "total": 5, "timestamp": "2022-12-15T19:07:56.947Z", "level": "info"}
{"message": "progress", "event_type": "EventType.PROGRESS", "subtask": "Processing urls", "current": 3, "total": 5, "timestamp": "2022-12-15T19:08:00.423Z", "level": "info"}
{"message": "progress", "event_type": "EventType.PROGRESS", "subtask": "Processing urls", "current": 4, "total": 5, "timestamp": "2022-12-15T19:08:03.767Z", "level": "info"}
{"message": "progress", "event_type": "EventType.PROGRESS", "subtask": "Processing urls", "current": 5, "total": 5, "timestamp": "2022-12-15T19:08:06.085Z", "level": "info"}              
```

## Step 4. How to run it in Supervisely

Submitting an app to the Supervisely Ecosystem isn’t as simple as pushing code to github repository, but it’s not as complicated as you may think of it either.

Please follow this [link](https://developer.supervise.ly/app-development/basics/add-private-app) for instructions on adding your app. We have produced a step-by-step guide on how to add your application to the Supervisely Ecosystem.
