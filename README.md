# Hoi4Placer

> [!WARNING]
> This program is not yet working!  
> The documentation has not yet been created!

This is a simple Python program made to make submods more resiliant to updates, without too much manual work.  

Just place this into your mod folder, create the `.cng` files for files you want to change from your parent mod, and then run this file to update your mod.

*This prohect uses python [regex](https://regextutorial.org/), I advice using [regex101.com](https://regex101.com/) with python selected to build the [regex](https://regextutorial.org/) patterns in the `.cng` files.*

# installation

1. Download python
	* Windows: use the Microsoft store and search for python, or download it [here](https://www.python.org/downloads/)
	* Linux with apt: open a terminal and enter these commands: `sudo apt update` and `sudo apt install python3` 
	* Other: Use Google. You may feel free to write a Pull Request to append your instructions here.
2. Download `placer.py` and `player_settings.txt` into your mod folder
3. create the necessary `.cng` files
4. edit `placer_settings.txt` to change or create variables that point at vanilla and parent mods.
5. double click placer.py or open a console to run `python3 placer.py` or `python placer.py`

# Use cases

You can use this program to
* Append data to a file like`supply_nodes.txt`
* Change data like appending traits to a leader
* Copy data out of one file and writing it into another, for example when you only want to keep small parts of a file
* Replace or delete lines from a file, like when you want to add or remove some conditions for a scope

# How it works

This program searches your mod for `.cng` files and parses them.  
The program will copy the original file from Vanilla or a mod, and then add or replace part of the copy with [regex](https://regextutorial.org/).  

For more info, see the documentation.
> [!NOTE]
> The documentation still needs to be written

# Q&A

> Why did you use Python?

I hope that it allows ordinary people to verify that this program is safe, that they can easily make changes, and this also allows for easy cross-platform support.  

> Can you add more features?

Perhaps, it depends on the scope of the feature and my motivation.  
I might add some stuff later, like allowing you to modify things in the data section, but I won't do that for now.

> Can I contribute to this project?

I am not that active on GitHub, but you can fork this project, and if I see that you want to merge something in here, then I might check your changes and merge them in.
Please write Classes and Variables in Carmel case, classes need to start with a Capital, variables not. Functions must be snake case and constants are snake case in ALL CAPS.

> Why did you write your code like that?

I am not a native python programmer, I usually write in C, so I will write with a heavy C accent, and may do weird stuff to be happier, like writing wrappers just so I have errors as values.

> Can I Modify or share this Program?

Yes, this program is under a CC0-1.0 Licence, you can do whatever you want with it, you don't even have to credit me.

# Project Structure

| File/Directory      | Description                                    |
|---------------------|------------------------------------------------|
| LICENCE             | cc0-1.0 Licence file.                          |
| README.md           | This README file.                              |
| placer.py           | The program that is run.                       |
| placer_settings.txt | The config file for placer.py                  |
| *tests/*            | Directory for automated tests                  |
| *_tests/*           | Directory for manual tests in development.     |
| *examples/*         | Example files with instructions to show usage. |
