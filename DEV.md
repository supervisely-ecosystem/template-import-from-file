# Create import app from template

## Introduction

In this tutorial, you will learn how to create custom import app to import your data to Supervisely platform using an import template app that we've prepared for you. It will show you how to add the necessary files and structure to create the app from a python script, and how to use it.

<!-- With the help of an import template app that we've developed for you, you will learn how to create a custom import app to upload your data to the Supervisely platform in this tutorial. It will demonstrate how to utilize it as well as how to add the required files and structure to develop the app from a Python script. -->

We will write a simple Python program that downloads a `.txt` file with images links and imports them to a new or existing project.

`my_project.txt`

```text
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-couleur-2317904.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-kammeran-gonzalezkeola-7925859.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-stijn-dijkstra-7177188.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-taryn-elliott-3889728.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-taryn-elliott-9565787.jpg
```

We will go through the following steps:

\*\*\*\*[**Step 1.**](from-script-to-supervisely-app.md#step-1.-python-script) Prepare a tiny python script.

\*\*\*\*[**Step 2.**](from-script-to-supervisely-app.md#step-2.-from-script-to-supervisely-app) \*\*\*\* How to transform this script into Supervisely App

\*\*\*\*[**Step 3.**](from-script-to-supervisely-app.md#step-3.-how-to-add-your-private-app) How to add custom private app into Supervisley Platform.

\*\*\*\*[**Step 4.**](from-script-to-supervisely-app.md#step-4.-run-your-app-in-supervisely) \*\*\*\* How to run it in Supervisely.

{% hint style="info" %}
Everything you need to reproduce [this tutorial is on GitHub](https://github.com/supervisely-ecosystem/hello-world-app): source code and additional app files.
{% endhint %}

## Requirements

Install latest [`supervisely`](https://pypi.org/project/supervisely/) version to have access to all [available widgets](https://ecosystem.supervise.ly/docs/table) and [`names`](https://pypi.org/project/names/) library for names generation

```python
names # requires for names generation
supervisely
```

## Step 1. Set up an environment for development

**Step 1.** Prepare `~/supervisely.env` file with credentials. [Learn more here.](https://developer.supervise.ly/getting-started/basics-of-authentication#how-to-use-in-python)

**Step 2.** Clone [repository](https://github.com/supervisely-ecosystem/template-import-from-file) with source code and create [Virtual Environment](https://docs.python.org/3/library/venv.html).

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
CONTEXT_TEAMID=1              # ⬅️ change it
CONTEXT_WORKSPACEID=1         # ⬅️ change it
CONTEXT_PROJECTID=555         # ⬅️ specify when importing to existing project
CONTEXT_DATASETID=55555       # ⬅️ specify when importing to existing dataset
FILE="/data/my_project.txt"   # ⬅️ remote path from team files starts with '/'
SLY_APP_DATA_DIR="results/"   # ⬅️ path to directory for local debugging
```

For debugging with local file specify absolute or relative path to you file

```python
FILE="data/my_project.txt"    # ⬅️ local path where you file is located on your computer
```

**Step 6.** Now you are all set and we can move straight to the code part

## Step 3. Writing import script

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

**Step 3. Write Import code**

Create a class that inherits from `sly.app.Import` and write `process` method that will handle the file that you specified in the `FILE` variable of the `local.env`. In our case it's called `MyImport`.

`sly.app.Import` class will handle all pre-import routines for you.
It will define destination project and dataset and will download your file to the chosen directory (`SLY_APP_DATA_DIR`) based on what you provided in the `local.env` file for local debugging from `Team Files`.

`sly.app.Import` has a `Context` subclass which contains all required information that you need for importing your file to Supervisely platform. `context` variable is passed as a parameter to `process` method of class `MyImport` and `context` object will be created automatically when you execute import.

```python
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

So all what's left is just read the file and upload items in it to the selected destination.

```python
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
                sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")

                # remove local file after upload
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

## Step 2. From script to Supervisely App

### Repository structure

Supervisely App is just a git repository on Github or Gitlab. For this particular app the files structure should be the following:

```text
.
├── README.md
├── config.json
├── requirements.txt
└── src
    └── main.py
```

Let's explain every file:

* `README.md` \[optional] - contains an explanation of what this app does and how to use it. You can provide here all information that can be useful for the end-user (screenshots, gifs, videos, demos, examples).
* `requirements.txt` \[optional] - here you can specify all Python modules (pip packages) that are needed for your python program. This is a common convention in Python development. In our example we use two additional packages: [`art`](https://pypi.org/project/art/) [![](https://camo.githubusercontent.com/d367bde73fa3ec8a38cc54d187094f0a6d2c24f81ec5bba70cd88dc4d6047467/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f736570616e6468616768696768692f6172742e7376673f7374796c653d736f6369616c266c6162656c3d5374617273)](https://github.com/sepandhaghighi/art)to do cool prints to console and [`black`](https://pypi.org/project/black/) ![GitHub Org's stars](https://img.shields.io/github/stars/psf/black?style=social) for automatic code formatting.

<pre><code><strong># supervisely SDK
</strong><strong>supervisely
</strong>
<strong># used to print cool text to stdout
</strong>art==5.7

# my favorite code formatter
black==22.6.0
</code></pre>

* `config.json` - This file will contain all your app metadata information, like name, description, poster URL, icon URL, app tags for Ecosystem, docker image, and so on. This file will be explained in detail in the next guides.
* `src/main.py` our python program.

The two files below are in the repo but they are used **ONLY** for debug purposes and are provided for your convenience.

```
.
├── create_venv.sh
└── local.env
```

### App configuration

App configuration is stored in `config.json` file. A detailed explanation of all possible fields in app configuration will be covered in other tutorials. Let's check the config for our small app:

```json
{
  "main_script": "src/main.py",
  "headless": true,
  "name": "Hello World!",
  "description": "Demonstrates how to turn your python script into Supervisely App",
  "categories": ["development"],
  "icon": "https://user-images.githubusercontent.com/12828725/182186256-5ee663ad-25c7-4a62-9af1-fbfdca715b57.png",
  "poster": "https://user-images.githubusercontent.com/12828725/182181033-d0d1a690-8388-472e-8862-e0cacbd4f082.png"
}
```

Let's go through the fields:

* `main_script` - relative path to the main script (entry point) in a git repository
* `"headless": true` means that app has no User Interface
* `name`, `description` and `poster` define how the app will look in the Supervisely Ecosystem

![poster, name, descripotion](https://user-images.githubusercontent.com/12828725/182863249-0b4d672f-f50d-4bbb-b769-ec1016539ccd.png)

* `icon`, `categories` - categories help to navigate in the Supervisely Ecosystem and it is a user-friendly way to explore apps

![icon and categories](https://user-images.githubusercontent.com/12828725/182864521-319fb450-d025-4e1c-806e-ebc0dd19260f.png)

## Step 3. How to add your private app

There are two following ways to add an application

### Add app from git repository

Supervisely supports both private and public apps.

🔒 **Private apps** are those that are available only on private Supervisely Instances (Enterprise Edition).

🌎 **Public apps** are available on all private Supervisely Instances and in Community Edition. The guidelines for adding public apps will be covered in other tutorials.

Since Supervisely app is just a git repository, we support public and private repos from the most popular hosting platforms in the world - **GitHub** and **GitLab**. You just need to generate and provide access token to your repo. Learn more in [the documentation](https://docs.supervise.ly/enterprise-edition/advanced-tuning/private-apps).

Go to `Ecosystem` -> `Private Apps` -> `Add private app`.

![Add private app](https://user-images.githubusercontent.com/12828725/182870411-6632dde4-93ed-481c-a8c2-79718b0f5a7d.gif)

### Add app directly to the supervisely instance via apps-cli

Install supervisely-app cli via following command:

```text
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/supervisely/supervisely/master/cli/supervisely-app.sh)"
```

Add `release` and `slug` properties in `config.json`:

```text
  "release": { "version":"v1.0.0", "name":"init" },
  "slug": "<organication_name>/<app-name>",
```

Create .env file `~/supervisely.env` with the following content:

```python
SERVER_ADDRESS="https://<server-address>"
API_TOKEN="4r47N...xaTatb"
```

Go root folder of your app folder and run:

```bash
supervisely-app release
```

As an alternative to creating `~/supervisely.env`, you can use `-t` and `-s` flags when publishing a new version:

```bash
supervisely-app release -s https://<server-address> -t 4r47N...xaTatb
```

## Step 4. Run your app in Supervisely

There are multiple ways how application can be integrated into Supervisely Platform. App can be run from context menu of project / dataset / labeling job / user / and so on ... Or app can be run right from labeling interface. All possible running options will be covered in next tutorials.

For simplicity, we will run our app from the Ecosystem page.

![Let's run our app](https://user-images.githubusercontent.com/12828725/182894602-5ec6a5c6-e954-429b-9fc1-877d662a21ec.gif)
