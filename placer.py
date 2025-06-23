
import os
import re as regex
from dataclasses import dataclass as struct
from enum import Enum as enum
from parser import parse_file

### structs and enums

class Place(enum):
	replace = 0
	before = 1
	after = 2

@struct
class Change:
    line: int
    data: str
    place: Place

### constants

CNG_VERSION = 1;

MIB_BYTE_CONV_RATE = 1024*1024;
KIB_BYTE_CONV_RATE = 1024;

MAX_CONF_SIZE = 256 * KIB_BYTE_CONV_RATE;
EXIT_FAILURE = -1;

# setting defaults
DEFAULT_MAX_FILESIZE = 10 * MIB_BYTE_CONV_RATE;
DEFAULT_SEARCH_PATH = "."; # for starting the recousive search for .chg files
DEFAULT_MAX_META_SEARCH = 4 * KIB_BYTE_CONV_RATE;
DEFAULT_WARN_NO_PRIO = "FALSE";

# default values for .cng files
DEFAULT_PRIO = 10;
DEFAULT_SOURCE = "VANILLA";
DEFAULT_PATH = "."; # for finding the original file to copy
DEFAULT_EXT = ".txt";
DEFAULT_TYPE = "TEXT";


### global vars

configVariables = {};
cngFiles = [];

### wrappers for my sanity

# retuns a open file thing or None on error
def _open(path,access):
	try:
		fd = open(path,access);
		return fd;
	except Exception:
		return None;

# wraps print in case musscle memory takes over
def puts(str):
	print(str);


### functions 

# takes in a string and converts it to a bool
# returns: True if string is "true", False is string is "false" or None, if string is neither of those
def str_to_bool(str) -> bool:
	if (str.upper() == "TRUE"):
		return True;
	if (str.upper() == "FALSE"):
		return False;
	return None;


# pritnts string, and enters endless loop until user presses either Y or N
# str: string to print
# returns: True if user typed Y, False if user Typed N
def choice(str) -> bool:
	print(str);
	usrChoice = None;
	while (usrChoice != 'Y' and usrChoice != 'N'):
		usrChoice = input("[Y/N]: ").strip().upper();
	if (usrChoice == 'Y'):
		return True;
	return False;

# finds and reads the config file into configVariables
# returns: True if successful. False if an error occured.
def read_config() -> bool:
	settingsFile = None;

	#find setting file
	if (os.path.isfile("placer_settings.txt")):
		settingsFile = "placer_settings.txt";

	if (settingsFile is None):
		print("Error: could not find placer_settings.txt");
		return False;

	if (os.path.getsize(settingsFile) > MAX_CONF_SIZE):
		print("Warning: Settings file is too big! File is expected to be at most "+str(MAX_CONF_SIZE)+" KiB!\nFile size: " + str(round(os.path.getsize(settingsFile)/KIB_BYTE_CONV_RATE,2)) + " KiB");
		if (choice("Load file anyway?") == False):
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
			configVariables[parts[0].strip().upper()] = parts[1].strip();
		elif parts == 1:
			configVariables[parts[0].strip().upper()] = "";
		else:
			if (data[i].strip() == ""):
				i = i + 1;
				continue;
			else:
				print("Error: Line "+str(i+1)+" in "+settingsFile + " has a syntax error!");
		i = i + 1;

	fd.close();

# sets default configuration value, if the user did not set one
# key: the configucation you want to set, if it is not set already
# default: the value of the configuration
def set_default(key,default):
	if (not (key in configVariables)):
		configVariables[key] = str(default);

# finds all files in SEARCH_PATH, walks subdirs
# returns: list of file paths
def get_files() -> list:
    found = []
    for root, dirs, files in os.walk(configVariables["SEARCH_PATH"]):
        for file in files:
            if file.lower().endswith(".cng"):
                found.append(os.path.join(root, file))
    return found

# gets priority of file. 0 = higest prio. if no prio is given, it uses the default value
# takes: path -> Path to file
# returns: a positive integer for the priority OR None on error
def get_file_prio(path) -> int:

	fd = _open(path,"r");
	if (fd is None):
		puts("Error when opening "+path+"!");
		return None;

	data = fd.read(int(configVariables["MAX_META_SEARCH"]));

	prioMatch = regex.search("^!!PRIO +\\d+",data,regex.MULTILINE | regex.IGNORECASE);
	if (prioMatch is None):
		if (str_to_bool(configVariables["WARN_NO_PRIO"]) == True):
			puts("Warning: File "+path+" has no !!PRIO or the prio is after the first " + configVariables["MAX_META_SEARCH"] + " KiB");
		return int(configVariables["DEFAULT_PRIO"]);

	metaSectionEnd = regex.search("^#!!",data, regex.MULTILINE | regex.IGNORECASE);
	
	if (not (metaSectionEnd is None) and metaSectionEnd.start() < prioMatch.start()):
		print("Warning: used !!PRIO command outside the Meta command Space. Place it before any #!! command!\n\tUsing default prio for "+path);
		return int(configVariables["DEFAULT_PRIO"]);

	fd.close();
	return int( prioMatch.group()[len("!!PRIO"):].strip() );


# gets a list of all files and oders them by priority, stores the result in cngFiles
def load_file_prios():
	for file in get_files():
		prio = get_file_prio(file);
		if (prio is None):
			print("Skipping file "+file);
			continue;
		cngFiles.append( (prio, file) );

	cngFiles.sort();



### main

if (read_config() == False):
	exit(EXIT_FAILURE);

set_default("MAX_FILESIZE",DEFAULT_MAX_FILESIZE);
set_default("SEARCH_PATH",DEFAULT_SEARCH_PATH);
set_default("MAX_META_SEARCH", DEFAULT_MAX_META_SEARCH)
set_default("WARN_NO_PRIO",DEFAULT_WARN_NO_PRIO);

set_default("DEFAULT_PRIO",DEFAULT_PRIO);
set_default("DEFAULT_SOURCE",DEFAULT_SOURCE);
set_default("DEFAULT_PATH",DEFAULT_PATH);
set_default("DEFAULT_EXT",DEFAULT_EXT);
set_default("DEFAULT_TYPE",DEFAULT_TYPE);


load_file_prios();

print(cngFiles);

for file in cngFiles:
	parse_file(file[1]);

