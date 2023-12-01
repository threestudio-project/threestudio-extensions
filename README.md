<p align="left">
<img alt="threestudio" src="https://github.com/threestudio-project/threestudio-extensions/assets/24589363/ae3a22e3-2ee0-4ffe-85c6-dbe50e64f5b0" width="75%">
</p>

Welcome to the repository for threestudio-extensions. This repository serves as a central hub where you can explore all the currently supported extensions for threestudio in this [url](https://threestudio-project.github.io/threestudio-extensions/).

## How to register your extensions into threestudio-extensions

Add your extension to `threestudio-extensions-list.json` which is located in the roof of this project, then submit a pull request.

## How to write extensions for threestudio

- First, under the original threestudio project, create a new folder within the 'custom' directory and name it, for example `my_extension`.

- Inside this `my_extension` folder, you can implement your extension. It's important to note that any module or class you wish to import as a plugin must be registered with a unique class name to avoid conflicts with other extensions. This is done using the @threestudio.register("my_modules") decorator.

- Finally, create an `__init__.py` file within your `my_extension`` folder. In this file, import the Python files that are part of your extension.

## Acknowledgement

This project was inspired by [Comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager). We are very grateful for their open-source project. 

