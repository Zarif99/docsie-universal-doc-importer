import os

from giturlparse import parse
from swag_auth.gitlab.connectors import GitlabSwaggerDownloader

from docsie_universal_importer.repo_map import RepositoryMap
from docsie_universal_importer.utils import get_repo_content_path


class GitlabImporter(GitlabSwaggerDownloader):
    provider_id = 'gitlab'

    def get_repo_map(self, url, extensions):
        owner, repo_name, branch, path = self._parse_url(url=url)

        repo = self.get_user_repo(f'{owner}/{repo_name}')
        if not branch:
            branch = self.get_default_branch(repo)

        contents = repo.repository_tree()
        repo_map = RepositoryMap(repo_name, extensions)
        while contents:
            file_content = contents.pop(0)
            if file_content['type'] == "tree":
                contents.extend(repo.repository_tree(file_content['path'], ref=branch))
            else:
                extension = os.path.splitext(file_content['path'])[1][1:]
                if extension in extensions:
                    repo_map.add_path(f"{branch}/{file_content['path']}")
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

    def _parse_url(self, url: str) -> tuple:
        p = parse(url)
        repo_name = p.repo
        owner = p.owner
        b = p.branch
        if b:
            branch = b.split('/', 1)[0]
            path = b.replace(f'{branch}/', '')
        else:
            branch = p.path.split('/', 1)[0]
            path = p.path.replace(f"{branch}/", '')

        if repo_name == '-':
            repo_name = p.data.get('groups_path')

        return owner, repo_name, branch, path


connector_classes = [GitlabImporter]
