
import os
import re
from dataclasses import dataclass as struct
from enum import Enum as enum

# structs and enums

class Place(enum):
	replace = 0
	before = 1
	after = 2

@struct
class Change:
    line: int
    data: str
    place: Place

# constants

MIB_BYTE_CONV_RATE = 1024*1024
DEFAULT_MAX_FILESIZE = 10 * MIB_BYTE_CONV_RATE;
DEFAULT_SEARCH_PATH = ".";

# global vars

usrVariables = {};


# wrappers for my sanity

def _open(path,access):
	try:
		fd = open(path,access);
		return fd;
	except Exception:
		return None;

def puts(str):	# in case musscle memory takes over
	print(str);

# functions 

def choice(str) -> bool:
	print(str);
	usrChoice = None;
	while (usrChoice != 'Y' and usrChoice != 'N'):
		usrChoice = input("[Y/N]: ").strip().upper();
	if (usrChoice == 'Y'):
		return True;
	return False;


def read_config() -> bool:
	settingsFile = None;

	#find setting file
	if (os.path.isfile("placer_settings.txt")):
		settingsFile = "placer_settings.txt";

	if (settingsFile is None):
		print("Error: could not find placer_settings.txt");
		return False;

	if (os.path.getsize(settingsFile) > 1 * MIB_BYTE_CONV_RATE):
		print("Error: Settings file is too big! File is expected to be less than 1 MiB!");
		return False;

	fd = _open(settingsFile, "r");

	if (fd is None):
		print("Error: could not open "+settingsFile);
		return False;

	data = fd.read().splitlines();

	i = 0;
	while (i < len(data)):
		parts = data[i].split("=");
		if (len(parts) == 2):
			usrVariables[parts[0].strip().upper()] = parts[1].strip();
		elif parts == 1:
			usrVariables[parts[0].strip().upper()] = "";
		else:
			if (data[i].strip() == ""):
				i = i + 1;
				continue;
			else:
				print("Error: Line "+str(i+1)+" in "+settingsFile + " has a syntax errro!");
		i = i + 1;

	fd.close();

def set_default(key,default):
	if (not (key in usrVariables)):
		usrVariables[key] = default;

def get_files() -> list:
    found = []
    for root, dirs, files in os.walk(usrVariables["SEARCH_PATH"]):
        for file in files:
            if file.lower().endswith(".cng"):
                found.append(os.path.join(root, file))
    return found

def get_file_prio(path) -> int:
	print("TODO IMPLEMENT! FILE: "+path);

def parse_file(path):
	print("TODO IMPLEMENT! FILE: "+path);

# main

read_config();

set_default("MAX_FILESIZE",DEFAULT_MAX_FILESIZE);
set_default("SEARCH_PATH",DEFAULT_SEARCH_PATH);

for file in get_files():
	get_file_prio(file);