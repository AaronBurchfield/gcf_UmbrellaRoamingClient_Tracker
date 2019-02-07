import requests

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape

env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

BASEURL = "https://disthost.umbrella.com/roaming/upgrade/mac"
TRACKS = [
    'internal',
    'dogfood',
    'beta',
    'stage',
    'production-1',
    'production-2',
    'production-3',
]


def get_track_version(track):
    manifest_url = '/'.join([BASEURL, track, 'manifest.json'])
    response = requests.get(manifest_url)
    data = response.json()

    version = data.get('nextVersion')
    filename = data.get('downloadFilename')
    download_url = '/'.join([BASEURL, track, filename])

    return {
        'version': version,
        'url': download_url
    }


def get_track_versions():
    versions = {}
    for track in TRACKS:
        track_data = get_track_version(track)
        versions[track] = track_data

    return versions


def main(request=None):
    data = get_track_versions()

    template = env.get_template('page.html')
    html = template.render(data=data)
    return html


if __name__ == '__main__':
    main()
