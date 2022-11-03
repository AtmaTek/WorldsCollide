def main():
    import args
    from metadata.flag_metadata_writer import FlagMetadataWriter
    FlagMetadataWriter(args).write()

import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()  # blocks execution until client is attached

if __name__ == '__main__':
    main()
