import dropbox
import config

class DropBox:
    def __init__(self, ):
        self.access_token = config.token        
        self.dbx = dropbox.Dropbox(self.access_token)

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """        

        with open(file_from, 'rb') as f:
            self.dbx.files_upload(f.read(), file_to,  mode=dropbox.files.WriteMode.overwrite)


    def download_file(self, file_source):
        try:
            ff = self.dbx.files_download(file_source)
            data = ff[1].content.decode()
            return data
        except:
            return None

