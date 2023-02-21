def key_function(prefix, key, version):
    return f"{prefix}:{key.replace(' ', '')}:{version}"
