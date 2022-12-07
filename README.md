<div align="center" markdown>

<img src="https://user-images.githubusercontent.com/48913536/206195017-ef1fbbae-4102-491e-944a-aa14cb4096d8.png"/>

# Custom Import from File

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-Develop">How to Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/template-import-from-file)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/template-import-from-file)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/template-import-from-file.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/template-import-from-file.png)](https://supervise.ly)

</div>

# Overview

This template is designed as a starting point for developers to create custom import apps for Supervisely platform.
Template app in it's current state will import images to selected project or dataset from links in `.txt` file.

Describe the type of data your app is importing e.g: images, videos, COCO, PascalVoc or any other data format.

Describe an input file structure using examples.

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
  
<img src="">

1. If you want to upload project folder from your computer, choose `Drag & Drop` option. You can upload the project folder to drag-and-drop field or you can click on the drag-and-drop field and choose project from your computer in opened window.
  
<img src=""/>

2. If you want to import project from Team Files, choose `Team Files` option and choose folder to import in the modal window.
  
<img src=""/>

</details>

<details>
<summary open>Run from Project or Dataset</summary>
<br>

Run the application from the context menu of the folder (right mouse button) on Team Files page
  
<img src=""/>

</details>

<details>
<summary open>Run from team files</summary>
<br>

Run the application from the context menu of the folder (right mouse button) on Team Files page
  
<img src=""/>

</details>
