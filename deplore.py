import xml.etree.ElementTree as et
import configparser
import os, sys

ini_filename = "deps.ini"

filename = ""

ini_exists = False

for file in os.listdir(os.getcwd()):
    if file.endswith("vcxproj"):
        print("Found:", file)
        filename = file

    if file == ini_filename:
        ini_exists = True

if filename == "":
    input("vcxproj not found in this folder")
    sys.exit(0)

if not ini_exists:
    input(ini_filename + " does not exist")
    sys.exit(0)

xmlns = 'http://schemas.microsoft.com/developer/msbuild/2003'

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

et.register_namespace('', xmlns)
xmlns = '{' + xmlns + '}'
tree = et.parse("ProjectTest_original.vcxproj")
root = tree.getroot()

configs = []

def parse_list(_ini, _section, _label):
    print("Parsing ", _section, _label)

    if not _ini[_section].__contains__(_label):
        return []

    _text = _ini[_section][_label]
    _splits = _text.split('\n')
    _arr = []
    for split in _splits:
        split = split.strip()
        if (split != ""):
            print(split)
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
    print("ALL not found")

# debug configs
#for config in configs:
    #config.dump()

print("\nTAG\n")

for child in root.findall(xmlns + "ItemDefinitionGroup"):
    # print(child.get("Condition"))
    text = child.get("Condition")

    # configuraiton
    splits = text.split("'")
    config_name = splits[3]
    print(splits[3])

    # find a configuration with this name
    config = next((x for x in configs if x.name == config_name), None)

    if config is None:
        print("config not found: ", config_name)
        continue

    # Additional Include Directories
    xml_clcompile = child.find(xmlns + "ClCompile")
    xml_includes = xml_clcompile.find(xmlns + "AdditionalIncludeDirectories")

    if xml_includes is not None:
        # split includes by ;
        for split in xml_includes.text.split(';'):
            print(split)

        includes_joined = ";".join(config.includes)
        includes_joined += ";%(AdditionalIncludeDirectories)"
        if all_includes_joined != "":
            includes_joined = all_includes_joined + ";" + includes_joined
        #print("JOINED: ",includes_joined)

        xml_includes.text = includes_joined

    xml_link = child.find(xmlns + "Link")

    # Additional Library Directories
    xml_libdirs = xml_link.find(xmlns + "AdditionalLibraryDirectories")

    if xml_libdirs is not None:
        print("LIBDIRS:", xml_libdirs.text)

        libdirs_joined = ";".join(config.libdirs)
        libdirs_joined += ";%(AdditionalLibraryDirectories)"
        if all_libdirs_joined != "":
            libdirs_joined = all_libdirs_joined + ";" + libdirs_joined

        xml_libdirs.text = libdirs_joined

    # Additional Dependencies
    xml_deps = xml_link.find(xmlns + "AdditionalDependencies")

    if xml_deps is not None:
        print("DEPS:", xml_deps.text)

        deps_joined = ";".join(config.deps)
        deps_joined += ";%(AdditionalDependencies)"
        if all_deps_joined != "":
            deps_joined = all_deps_joined + ";" + deps_joined

        xml_deps.text = deps_joined


tree.write(filename, 'utf-8', True)