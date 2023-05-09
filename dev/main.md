# Custom Import

This README provides an overview of the custom import template and describes the various import scenarios it can cover. The import template is designed to facilitate the import of custom formats used by enterprise developers and engineers. It offers flexibility and ease of use in handling different import scenarios.

## More details about `sly.app.Import`

`sly.app.Import` class will handle export routines for you:

💻 [Source code](https://github.com/supervisely/supervisely/blob/master/supervisely/app/import_template.py)

- ✅ Check that selected team, workspace, project or dataset exist and that you have access to it
- ⬇️ Download your data from Supervisely platform to remote container or local hard drive if you are debugging your app
- 🪄 Automatically detects app context with all required information for creating import app
- ⬆️ Upload your result data to new or existing Supervisely project
- 🧹 Remove source directory from Team Files after successful import
- 🖼️ Show your project on Supervisely platform workspace tasks page

`sly.app.Import` has a `Context` subclass which contains all required information that you need for exporting your data from Supervisely platform:

- `Team ID` - shows team id where exporting project or dataset is located
- `Workspace ID` - shows workspace id where exporting project or dataset is located
- `Project ID` - id of exporting project
- `Path` - path to your data
- `Is directory` - shows if your data is a directory or file
- `Is on agent` - shows if your data is located on agent or not

`context` variable is passed as an argument to `process` method of class `MyImport` and `context` object will be created automatically when you execute export script.

```python
class MyImport(sly.app.Import):
    def process(self, context: sly.app.Import.Context):
        print(context)
```

Output:

```text
Team ID: 8
Workspace ID: 349
Project ID: 8534
Dataset ID: 22852
Path: /data/my_project.txt
Is directory: False
Is on agent: False
```

if you want to download external data, you should reimplement method `is_path_required` and return `False`:

```python
    def is_path_required(self) -> bool:
        return False
```

## Import Scenarios

The custom import template supports the following import scenarios:

1. Import without template: this scenario allows for importing data without applying import template. It provides a basic import functionality where the data is imported using basic methods from Supervisely SDK.

2. Import from a text file: With this scenario, you can import data using a data from text files in various formats like `.csv`, `.txt`, `.xml`, `.yaml`, `.json` from Supervisely Team Files. Assuming text file contains a link to an image, bitmap, numpy array, or bytes.

3. Import from an archive: this scenario describes importing data using an archive from Supervisely Team Files. The data can be in various formats, such as `.zip` or `.tar`. The import template engine will download the data and pass the path to the archive to `sly.app.Import.Context`.

4. Import from a folder: in this scenario, you can import data using a folder. The import template engine will download specified folder and pass the path to the folder with data to `sly.app.Import.Context`.

5. Import from an agent folder: this scenario involves importing data using a folder stored on an agent. The import template engine will download specified folder from the agent and pass the path to the folder with data to `sly.app.Import.Context`.

6. Import from an external link: with this scenario, you can import data hosted externally (Not on Supervisely instance). In this case you will need to implement downloading part on your own.

7. Import with template using a graphical user interface (GUI): This scenario provides a user-friendly graphical interface for importing your data. The GUI allows users to select the desired folder or archive from Team Files or Drag & Drop option and configure import settings easily. It simplifies the import process and provides an intuitive experience for users.

## Set up an environment for development

We advise reading our [from script to supervisely app](../basics/from-script-to-supervisely-app.md) guide if you are unfamiliar with the [file structure](../basics/from-script-to-supervisely-app.md#repository-structure) of a Supervisely app repository because it addresses the majority of the potential questions.

**For both options, you need to prepare a development environment. Follow the steps below:**

**Step 1.** Prepare `~/supervisely.env` file with credentials. [Learn more here.](../../getting-started/basics-of-authentication.md#how-to-use-in-python)

**Step 2.** Fork and clone [repository](https://github.com/supervisely-ecosystem/export-custom-format) with source code and create [Virtual Environment](https://docs.python.org/3/library/venv.html).

```bash
git clone https://github.com/supervisely-ecosystem/export-custom-format
cd export-custom-format
./create_venv.sh
```

**Step 3.** Open repository directory in Visual Studio Code.

```bash
code -r .
```

**Step 4.** Select created virtual environment as python interpreter.

**Step 5.** Open `local.env` and insert your values here. Learn more about environment variables in our [guide](../../getting-started/environment-variables.md)

```python
TASK_ID=10                    # ⬅️ requires to use advanced debugging
TEAM_ID=8                   # ⬅️ change it
WORKSPACE_ID=349              # ⬅️ change it
PROJECT_ID=18334              # ⬅️ ID of the project that you want to export
DATASET_ID=66325              # ⬅️ ID of the dataset that you want to export (leave empty if you want to export whole project)
SLY_APP_DATA_DIR="results/"   # ⬅️ path to directory for local debugging
```

Please note that the path you specify in the `SLY_APP_DATA_DIR` variable will be used for saving application results and temporary files (temporary files will be removed at the end).

For example:
- path on your local computer could be `/Users/admin/Downloads/`
- path in the current project folder on your local computer could be `results/`

> Don't forget to add this path to `.gitignore` to exclude it from the list of files tracked by Git.

![Change variables in local.env](https://user-images.githubusercontent.com/79905215/236182190-3438d72e-919f-4a8f-9544-a105e8441a5a.gif)

When running the app from Supervisely platform: Project and Dataset IDs will be automatically detected depending on how you run your application.

## How to debug import template

In this tutorial, we will be using the **Run & Debug** section of the VSCode to debug import app.

Import template has 2 launch options for debugging: `Debug` and `Advanced Debug`.
The settings for these options are configured in the `launch.json` file.

![launch.json](https://github.com/supervisely/developer-portal/assets/79905215/3afd0096-7b66-4462-9fc0-f7098d18fc25)

### 1 - `Debug`

This option is a good starting point. In this case app will import data stored on your local drive, you should provide path to data in `local.env`.

```python
FILE="data/my_project.txt"   # ⬅️ path to file that you want to import
```

Data will be uploaded to specified project or dataset on Supervisely platform, but source folder will not be removed and task will not appear on workspace tasks page.

![Debug](https://user-images.githubusercontent.com/79905215/236843626-df94117a-889c-4321-9925-2985896f6f89.gif)

Output of this python program:

```text
Processing: 100%|███████████████████████████████████████████████████████████████████| 5/5 [00:10<00:00,  2.03s/it]
```

### 2 - `Advanced Debug`

This option is useful for final testing and debugging. In this case, data will be downloaded from Supervisely instance Team Files and uploaded to specified project or dataset on Supervisely platform, source folder will be removed, and task will appear on workspace tasks page.

![Advanced Debug](https://user-images.githubusercontent.com/79905215/236843626-df94117a-889c-4321-9925-2985896f6f89.gif)

Output of this python program:

```text
{"message": "progress", "event_type": "EventType.PROGRESS", "subtask": "Processing", "current": 0, "total": 5, "timestamp": "2023-05-09T18:08:54.444Z", "level": "info"}
...
{"message": "progress", "event_type": "EventType.PROGRESS", "subtask": "Processing", "current": 5, "total": 5, "timestamp": "2023-05-09T18:09:04.705Z", "level": "info"}
{"message": "Source directory: '/data/my_project.txt' was successfully removed.", "timestamp": "2023-05-09T18:09:05.849Z", "level": "info"}
{"message": "Result project: id=21357, name=My Project", "timestamp": "2023-05-09T18:09:05.850Z", "level": "info"}
```