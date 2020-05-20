## LayConf - Layered Configuration Parser for Python3

### Overview

A simple wrapper over Python's configparsr that reads configuration in the following order:

1. Environment variables
1. Custom configuration ini file  (optional)
1. Default configuration ini file (must exist)

Each config option lookup will fallback to next layer if not found in the present layer.

Convention for env. vars is `{prefix}_{section}_{option}` or `{section}_{option}` if prefix is empty. For example: `LOG_file_backup_count=100`

All lookups are case sensitive.    
 

 ### Example
```python
from layconf import LayConf

# the default config file is cfg/default.ini unless specified other
# custom_config_file_path is an optional layer
# env_prefix is empty by default, which means that environment variable names will be mapped to {section}_{option}
LayConf.init_config(custom_config_file_path="cfg/staging.ini", env_prefix="example")

print("env_name:", LayConf.get("DATABASE", "env_name"))
print("console_enabled:", LayConf.getboolean("LOG", "console_enabled"))
print("file_rotation_size_mb:", LayConf.getint("LOG", "file_rotation_size_mb"))
print("file_rotation_size_mb:", LayConf.getint("LOG", "file_rotation_size_mb"))

# dealing with not exist keys
# be default - raise an Error, as it is recommended to keep defaults for all fields in default.ini
try:
    print("foo:", LayConf.get("FOO", "foo"))
except KeyError:
    print("'foo' not found")
# but it is also possible to specify an inline default
print("foo:", LayConf.get("FOO", "foo", fallback="bar"))
print("foo_number:", LayConf.get("FOO", "foo_number", fallback=33))

# also possible to get an entire config section and read from with an indexer
log_section = LayConf.getsection("LOG")
print("file_enabled:", log_section["file_enabled"])
print("file_backup_count:", log_section.getint("file_backup_count"))
```
Output:

```
% example_LOG_file_backup_count=300 python example_app.py
config env prefix: example
config default: cfg/default.ini
config custom: cfg/staging.ini
env_name: staging
console_enabled: True
file_rotation_size_mb: 10
file_rotation_size_mb: 10
'foo' not found
foo: bar
foo_number: 33
file_enabled: true
file_backup_count: 300
```
### ToDo:

* Packaging to pip
 
### License: 

Apache V2