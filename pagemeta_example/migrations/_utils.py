from django.core.files.storage import default_storage

def copy_file_to_storage(filepath: str, force: bool=False) -> str:
    '''
    copies local file to django media storage
    returns storage path
    '''
    filename = filepath.split('/')[-1]
    
    # returning if file already exists
    if default_storage.exists(filename) and not force:
        return filename

    with open(filepath, 'rb') as f:
        return default_storage.save(filename, f)