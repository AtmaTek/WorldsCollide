def main():
    from metadata.objective_metadata_writer import ObjectiveMetadataWriter
    metadata_writer = ObjectiveMetadataWriter()
    metadata_writer.write()

# import debugpy
# debugpy.listen(5678)
# debugpy.wait_for_client()  # blocks execution until client is attached

if __name__ == '__main__':
    main()
