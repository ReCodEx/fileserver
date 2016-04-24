def hash_file(hash, file_stream):
    """
    Calculate the hash of a file by chunks (without having the whole file in memory)
    :param hash: A hash object to start with (e.g. hashlib.sha1())
    :param file_stream: The source stream
    :return: The result hash
    """

    while True:
        chunk = file_stream.read(65536)

        if (chunk is None or chunk == "" or chunk == b""):
            break

        hash.update(chunk)

    return hash
