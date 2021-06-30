def get_repo_content_path(data: dict):
    """
    Return all content path
    :param data:
    :return: list of all paths:
    :rtype: list:
    """
    paths = []
    for key, files in data.items():
        for file in files:
            if isinstance(file, dict):
                for k, v in file.items():
                    s = get_repo_content_path(file)
                    for item in s:
                        path = k + '/' + item
                        paths.append(path)
            else:
                path = file
                paths.append(path)
    return paths
