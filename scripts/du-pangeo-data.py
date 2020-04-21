# auto-generate some GCS metrics

from gcsfs import GCSFileSystem

fs = GCSFileSystem('pangeo-181919')

# https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

# get disk usage of each folder in gs://pangeo-data
with open('du-pangeo-data.csv', 'w') as f:
    f.write('directory, size, nbytes')
    print('directory, size, nbytes')
    for folder in fs.ls('pangeo-data'):
        nbytes = fs.du(folder)
        f.write(f'{folder}, {sizeof_fmt(nbytes)}, {nbytes}')
        print(f'{folder}, {sizeof_fmt(nbytes)}, {nbytes}')

# upload CSV to gs://pangeo-data
fs.put('du-pangeo-data.csv', 'pangeo-data/du-pangeo-data.csv')
