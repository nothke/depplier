import xml.etree.ElementTree as et
import configparser
import os, sys

# FIND FILES

ini_filename = "deps.ini"

filename = ""

ini_exists = False

for file in os.listdir(os.getcwd()):
    if file.endswith("vcxproj") and filename == "":
        print("Found:", file)
        filename = file

    if file == ini_filename and not ini_exists:
        ini_exists = True

if filename == "":
    input(".vcxproj file not found in this folder")
    sys.exit(0)

if not ini_exists:
    input(ini_filename + " does not exist in this folder")
    sys.exit(0)

# EXTRACT XML

xmlns = 'http://schemas.microsoft.com/developer/msbuild/2003'

et.register_namespace('', xmlns)
xmlns = '{' + xmlns + '}'
tree = et.parse(filename)
root = tree.getroot()

# CREATE CONFIGS from ini

class Configuration:
    def __init__(self, name):
        self.name = name
        self.includes = []
        self.libdirs = []
        self.deps = []

    def dump(self):
        print("--- Config: ", self.name)
        print("includes:")
        print(*self.includes, sep = ", ")  
        print("includes:")
        print(*self.libdirs, sep = ", ")
        print("deps:")
        print(*self.deps, sep = ", ")
        print("---")

configs = []

def parse_list(_ini, _section, _label):
    #print("Parsing ", _section, _label)

    if not _ini[_section].__contains__(_label):
        return []

    _text = _ini[_section][_label]
    _splits = _text.split('\n')
    _arr = []
    for split in _splits:
        split = split.strip()
        if (split != ""):
            _arr.append(split)

    return _arr


# parse ini
ini = configparser.ConfigParser()
ini.read("deps.ini")
sections = ini.sections()
for section in sections:
    config = Configuration(section)
    config.includes = parse_list(ini, section, "include")
    config.libdirs = parse_list(ini, section, "libdir")
    config.deps = parse_list(ini, section, "deps")
    configs.append(config)

    # append solution dir
    for i in range(len(config.includes)):
        config.includes[i] = "$(SolutionDir)" + config.includes[i]

    for i in range(len(config.libdirs)):
        config.libdirs[i] = "$(SolutionDir)" + config.libdirs[i]

# find ALL config
config_all = next((c for c in configs if c.name == "ALL"), None)

all_includes_joined = ""
all_libdirs_joined = ""
all_deps_joined = ""

if config_all is not None:
    all_includes_joined = ";".join(config_all.includes)
    all_libdirs_joined = ";".join(config_all.libdirs)
    all_deps_joined = ";".join(config_all.deps)
else:
    print("[ALL] configuration not found, omitting")

#print("All includes:", all_includes_joined)
#print("All libdirs:", all_libdirs_joined)
#print("All deps:", all_deps_joined)

# debug configs
#for config in configs:
    #config.dump()

# PROCESS XML and replace nodes

def serialize_list(strlist, all_joined, additionals):
    joined = ""

    for strl in strlist:
        if strl == "":
            print("FAIL")

    if len(strlist) != 0:
        joined = ";".join(strlist)

    if all_joined != "":
        if joined == "":
            joined = all_joined
        else:
            joined = all_joined + ";" + joined

    if joined != "":
        joined += ";"

    joined += additionals

    return joined

for child in root.findall(xmlns + "ItemDefinitionGroup"):
    # print(child.get("Condition"))
    text = child.get("Condition")

    # configuraiton
    splits = text.split("'")
    config_name = splits[3]
    #print(splits[3])

    # find a configuration with this name
    config = next((x for x in configs if x.name == config_name), None)

    if config is None:
        print("Configuration", config_name, "not found in ini, omitting")
        continue

    # Additional Include Directories
    xml_clcompile = child.find(xmlns + "ClCompile")
    xml_includes = xml_clcompile.find(xmlns + "AdditionalIncludeDirectories")

    if xml_includes is not None:
        xml_includes.text = serialize_list(config.includes, all_includes_joined, "%(AdditionalIncludeDirectories)")

    xml_link = child.find(xmlns + "Link")

    # Additional Library Directories
    xml_libdirs = xml_link.find(xmlns + "AdditionalLibraryDirectories")

    if xml_libdirs is not None:
        #print("LIBDIRS:", xml_libdirs.text)
        xml_libdirs.text = serialize_list(config.libdirs, all_libdirs_joined, "%(AdditionalLibraryDirectories)")

    # Additional Dependencies
    xml_deps = xml_link.find(xmlns + "AdditionalDependencies")

    if xml_deps is not None:
        #print("DEPS:", xml_deps.text)
        xml_deps.text = serialize_list(config.deps, all_deps_joined, "%(AdditionalDependencies)")

# SAVE XML to vcxproj
tree.write(filename, 'utf-8', True)

print("")
input("Successfully assigned deps to " + filename)