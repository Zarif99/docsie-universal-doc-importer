import os

from swag_auth.bitbucket.connectors import BitbucketSwaggerDownloader

from docsie_universal_importer.repo_map import RepositoryMap
from docsie_universal_importer.utils import get_repo_content_path


class BitbucketImporter(BitbucketSwaggerDownloader):
    provider_id = 'bitbucket'

    def get_repo_map(self, url, extensions):
        owner, repo_name, branch, path = self._parse_url(url=url)
        repo = self.get_user_repo(f'{owner}/{repo_name}')

        if not branch:
            branch = self.get_default_branch(repo)

        contents = self.get_file_content(repo=repo, path=path, ref=branch)

        repo_map = RepositoryMap(repo_name, extensions)
        while contents:
            file_content = contents.pop(0)
            if file_content.get('type') == "commit_directory":
                contents.extend(self.get_file_content(repo=repo, path=file_content.get('path'), ref=branch))
            else:
                extension = os.path.splitext(file_content.get('path'))[1][1:]

                if extension in extensions:
                    repo_map.add_path(f'{branch}/{file_content.get("path")}')

        return {owner: repo_map.as_dict()}

    def get_files(self, repo_map):
        owner, repo_name, branch = '', '', ''
        for key, value in repo_map.items():
            owner, repo_name, repo_map = key, list(value)[0], value
            break
        urls = get_repo_content_path(repo_map)
        repo = self.get_user_repo(f'{owner}/{repo_name}')
        for url in urls:
            branch, url = url.split('/', 1)[0], url.split('/', 1)[1]
            content = self.get_file_content(repo, url, branch)
            yield url, content


connector_classes = [BitbucketImporter]
