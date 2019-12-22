import requests,time
import codecs, os, time, shutil
import yes,hot, walla_tv
import logging,sys
import my_dropbox


file_path = os.path.dirname (os.path.realpath (__file__))
os.chdir (file_path)


def print_header (file_out):    
  
    file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_out.write('<tv>\n')
        

def close_header(file_out,):
    file_out.write('</tv>\n')


logger = None
log_path = os.path.join ('output', 'log.txt')

if os.path.isfile (log_path):
    os.remove (log_path)

def set_logger():

    global logger

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])

    logger = logging.getLogger()   

set_logger()


if __name__ == "__main__":

    try:
        tic = time.time()

        if not os.path.isdir ('output'):
          os.makedirs ('output')        
        
        filename = os.path.join ('output', 'guide.xml')
        file_out = codecs.open(filename, 'w', encoding='utf8')  

        yes_handle = yes.YES(file_out, logger)    
        hot_handle = hot.HOT(file_out, logger)    
        walla_handle = walla_tv.WALLA_TV(file_out, logger)    
        drop_handle = my_dropbox.DropBox ()        
        
        # XML Start
        print_header (file_out)
                    
        # Print Channels Area
        yes_handle.print_channels ()
        #hot_handle.print_channels ()
        walla_handle.print_channels ()
                       
        # Print Prog area
        yes_handle.print_progs ()
        walla_handle.print_progs ()
                
        # When ready replace with 
        #hot_handle.print_progs ()        
        
        if 0:
            hot_data = drop_handle.download_file ('/epg/hot.xml')
            file_out.write(hot_data)
                                      
        # XML Close
        close_header (file_out)

        logger.info ('Total create time %d' % (time.time() - tic))

        file_out.close()

        drop_handle.upload_file (filename, '/epg/guide.xml')
        drop_handle.upload_file (log_path, '/epg/log.txt')  

    except:
        logger.exception ('Error during create')
     
       



