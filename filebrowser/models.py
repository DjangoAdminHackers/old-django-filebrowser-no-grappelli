#make sure sorl.thumbnail kvstore is updated after a file is changed in FileBrowser

try:
    import os.path
    from filebrowser.views import filebrowser_post_upload, filebrowser_post_rename, filebrowser_post_delete
    from sorl.thumbnail import delete
    from filebrowser.settings import DIRECTORY

    def delete_thumbnail_cache(sender, path, file, **kwargs):
        delete(file.path, delete_file=False)

    filebrowser_post_upload.connect(delete_thumbnail_cache, sender=None)

    def delete_thumbnail_cache_after_deletion(sender, path, filename, **kwargs):
        file_path = os.path.join(path, filename)
        delete(file_path, delete_file=False)
    filebrowser_post_delete.connect(delete_thumbnail_cache_after_deletion, sender=None)

    def regenerate_thumbnail_cache_after_rename(sender, path, filename, new_filename, **kwargs):
        kv_store_path = os.path.join(DIRECTORY, path, new_filename) #relative to MEDIA_ROOT
        kv_store_path_old_file = os.path.join(DIRECTORY, path, filename) #relative to MEDIA_ROOT
        delete(kv_store_path, delete_file=False)
        delete(kv_store_path_old_file, delete_file=False)
    filebrowser_post_rename.connect(regenerate_thumbnail_cache_after_rename, sender=None)

except ImportError:
    pass

