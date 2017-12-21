import re
import cProfile
from .server import start
from os import listdir
from os.path import isfile, join

def profile(url, width, redis=None, palette=None, realm=None):
    """Runs cProfile benchmarks and outputs into benchmarks directory as
    profile[idx].txt with idx being the highest number in the directory.

    :param cmd: The name of the command to profile
    :param url: The url of the websocket connection
    :param redis: The URI of the Redis DB
    :param palette: The color :class:`Palette`
    """
    profile_path = 'benchmarks/'
    files = [re.findall(r'\d+', f) for f in listdir(profile_path)
             if isfile(join(profile_path, f))]
    files = [val for sublist in files for val in sublist]
    files.sort(key=int)
    file_idx = files[-1]
    next_idx = str(int(file_idx)+1)

    cProfile.runctx(
            'start(url, width, redis=redis, palette=palette, realm=realm)', globals(),
            {'url': url, 'width': width, 'redis': redis, 'palette': palette, 'realm': realm},
            filename='benchmarks/profile' + next_idx + '.txt')
