<div align="center" markdown>

<img src="https://user-images.githubusercontent.com/48913536/207625734-ccef5e02-911a-4ef6-b58a-d664891cc4b2.png"/>

# Custom Import from File

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-Run">How to Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](../../../../supervisely-ecosystem/template-import-from-file)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/template-import-from-file)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/template-import-from-file.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/template-import-from-file.png)](https://supervisely.com)

</div>

# Overview

This template is designed as a starting point for developers to create custom import apps for Supervisely platform.
Template app in it's current state will import images to selected project or dataset from links in `.txt` file.

Describe the type of data your app is importing e.g: images, videos, COCO, PascalVoc or any other data format.

Explain an input file structure using examples.

**Example:**

my_project.txt
```text
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-couleur-2317904.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-kammeran-gonzalezkeola-7925859.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-stijn-dijkstra-7177188.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-taryn-elliott-3889728.jpg
https://github.com/supervisely-ecosystem/demo-data-for-import-template/releases/download/images/pexels-taryn-elliott-9565787.jpg
```

If input data is an archive, provide an example of it's structure using `tree` or similar tool

**Example:**

```text
data.tar
├── image_1.jpg
├── image_2.jpg
└── image_3.jpg
```

Insert a link to demo data for users.

# How to Run

App can be launched from ecosystem, project, dataset, or file in team files.

<details>
<summary>Run from ecosystem</summary>
<br>

Click `Run application` button on the right side of the app page. Modal window will be opened.

<div align="center">
  <img src="https://user-images.githubusercontent.com/48913536/206448473-a88fe24b-02fc-480c-92cd-9a9d8279e78e.png">
</div>

Choose file to import in the modal window.

<div align="center">
  <img src="https://user-images.githubusercontent.com/48913536/206448478-fbac83f4-9bad-4ae9-b873-d678c9c0abf5.png" width=60%/>
</div>

</details>

<details>
<summary open>Run from Project or Dataset</summary>
<br>

If you want to upload your data to existing Project or Dataset run the application from the context menu of the Project or Dataset.

<div align="center">
  <img src="https://user-images.githubusercontent.com/48913536/206448464-236eef87-308b-449e-991f-e7dcbd9fe53d.png"/>
</div>

You can upload the file to drag-and-drop field or you can click on the drag-and-drop field and choose file from your computer in opened window.

<div align="center">
  <img src="https://user-images.githubusercontent.com/48913536/206448491-7fcdd407-591b-426d-bf03-05074cc99c1d.png" width=60%/>
</div>

</details>

<details>
<summary open>Run from team files</summary>
<br>

Run the application from the context menu of the file (right mouse button) on Team Files page

<div align="center">
  <img src="https://user-images.githubusercontent.com/48913536/206448485-32cf4cc6-84dd-4615-a100-6db8ee27689e.png"/>
</div>

</details>
