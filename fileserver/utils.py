def hash_file(hash, byte_stream):
    """
    Calculate the hash of a file by chunks (without having the whole file in memory)
    :param hash: A hash object to start with (e.g. hashlib.sha1())
    :param file_stream: The source stream. It must return bytes on read (e.g. io.BytesIO).
    :return: The result hash
    """

    while True:
        chunk = byte_stream.read(65536)

        if type(chunk) is not bytes:
            raise TypeError("only byte streams can be encoded")

        if not chunk:
            break

        hash.update(chunk)

    return hash
