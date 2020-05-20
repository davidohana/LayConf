from layconf import LayConf


def main():
    # the default config file is cfg/default.ini unless specified other
    # custom_config_file_path is an optional layer
    # env_prefix is empty by default, which means that environment variable names will be
    # mapped to {section}_{option}
    LayConf.init_config(custom_config_file_path="cfg/staging.ini", env_prefix="example")

    print("env_name:", LayConf.get("DATABASE", "env_name"))
    print("console_enabled:", LayConf.getboolean("LOG", "console_enabled"))
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


if __name__ == '__main__':
    main()
