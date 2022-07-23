from django.core.files.storage import default_storage

def copy_file_to_storage(filepath: str) -> str:
    '''
    copies local file to django media storage
    returns storage path
    '''
    filename = filepath.split('/')[-1]
    with open(filepath, 'rb') as f:
        return default_storage.save(filename, f)