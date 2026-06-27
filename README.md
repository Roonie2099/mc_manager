# 🎮 Minecraft Mod Manager

A lightweight Minecraft mod manager written in Python.

Minecraft Mod Manager is a simple command-line (Terminal/Command Prompt) application that helps you manage your Minecraft mods without manually moving `.jar` files every time you want to switch modpacks.

It allows you to create **instances** (collections of mods), quickly switch between them, and maintain a list of **Always Mods** that stay enabled regardless of the selected instance.

> **Current Version:** v1.0 (Beta)
> <img width="936" height="497" alt="image" src="https://github.com/user-attachments/assets/941a4dd2-24e3-4488-aac2-a323e0d89322" />

---

# Features

* Add mods to the active Minecraft `mods` folder.
* Remove mods from the active Minecraft `mods` folder.
* Create and manage multiple mod instances.
* Instantly switch between different instances.
* Support **Always Mods**, which remain enabled for every instance.
* Automatically removes missing mods from saved instance data.
* Lightweight and portable.
* Runs in the Windows Terminal / Command Prompt.

---

# Installation

1. Create a new folder (recommended name: **mc_manager**).
2. Put the following into that folder:

   * `mod_manager.exe`
   * `mods_storage` folder
3. Move the **mc_manager** folder into your Minecraft **game** folder (the folder containing the `mods` folder).
4. Put all of your `.jar` mods into the `mods_storage` folder.

Your folder structure should look like this:

```text
game
│
├── mods
│
└── mc_manager
    ├── mod_manager.exe
    ├── mods_storage
    └── mod_instance_data.json
```

The JSON file will be created automatically the first time you run the program.

---

# Running the Program

There are three ways to launch Minecraft Mod Manager.

### Option 1

Open the **mc_manager** folder and double-click:

```
mod_manager.exe
```

### Option 2

Create a desktop shortcut for:

```
mod_manager.exe
```

and launch it from the shortcut.

### Option 3

Go to the newest released version and follow the instructions in README or description

The program runs inside the Windows Terminal / Command Prompt.

---

# Definitions

### Instance

An **Instance** is a collection of mods that you want to use together.
Each instance stores its own list of mods.

---

### Always Mods

**Always Mods** are mods that will always be enabled, regardless of the selected instance.
These mods don't need to be added to every instance separately.

---

# Source Code

`mod_manager.py` is the original Python source code used to build `mod_manager.exe`.

Feel free to study, modify, or reuse the code.

Running the Python version requires Python to be installed.
