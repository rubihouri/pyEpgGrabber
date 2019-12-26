import requests
import datetime, json, codecs
import base, os, logging, gzip

channels_to_save = []

CHANNELS_DATA = [

    ("foodnetwork.il", ("Food Network",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/food_network.png"),
]   

for chan in  CHANNELS_DATA:
    channels_to_save.append (chan[0])


class APOLLO (base.BASE_EPG):
    def __init__ (self,file_out,logger):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'APOLLO', file_out, logger)

        byte_array = requests.get ("https://github.com/Apollo2000/TVGuide/raw/master/utc.lite.xml.gz").content

        path_to_zip_file = 'stam.gz'
        directory_to_extract_to = 'epg_apollo'
        ff = open(path_to_zip_file, 'wb')
        ff.write(byte_array)
        ff.close()

        with gzip.open(path_to_zip_file , 'rb') as f:
            file_content = f.read()
            
        self.lines =  file_content.decode().split('\n')
        
        
    def current_channel (self,line):

        for channel_to_save in channels_to_save:
            if channel_to_save in line:
                return channel_to_save
        return None
        

    def _print_channel_progs (self,channel_guid):


        lines_to_print = []
        take_next_lines = 0
        program_data = []
        lines2save = [ind  for ind,line in enumerate (self.lines) if channel_guid  in line]
        
        # 2 first line channel and logo
        for i in range (lines2save[2], lines2save[-1]+4):
            program_data.append(self.lines[i])

        for program in program_data:
            lines_to_print.append (program + '\n')
            
        return lines_to_print
                                


if __name__ == "__main__":
    filename = os.path.join ('output', 'apollo.xml')
    file_out = codecs.open(filename, 'w', encoding='utf8')  

    log_path = os.path.join ('output', 'log.txt')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])

    logger = logging.getLogger()   

    apollo = APOLLO(file_out,logger)
    
    apollo.print_channels()
    apollo.print_progs()
    
    file_out.flush()
    
    import my_dropbox
    drop_handle = my_dropbox.DropBox ()
    drop_handle.upload_file (filename, '/epg/hot.xml')


    guide_filename = os.path.join ('output', 'hot_guide.xml')
    file_out = codecs.open(guide_filename, 'w', encoding='utf8')  

