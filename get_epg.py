import requests
import codecs, os, time, shutil
import yes,hot
import logging,sys


file_path = os.path.dirname (os.path.realpath (__file__))
os.chdir (file_path)


def print_header (file_out):    
  
    file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_out.write('<tv generator-info-name="WebGrab+Plus/w MDB &amp; REX Postprocess -- version V2.1.5 -- Jan van Straaten" generator-info-url="http://www.webgrabplus.com">\n')
        

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
        filename = os.path.join ('output', 'guide.xml')
        file_out = codecs.open(filename, 'w', encoding='utf8')  

        yes_handle = yes.YES(file_out, logger)    
        hot_handle = hot.HOT(file_out, logger)    
        
        
        # XML Start
        print_header (file_out)
                    
        # Print Channels Area
        yes_handle.print_channels ()
        hot_handle.print_channels ()
        
        # Print Prog area
        yes_handle.print_progs ()
        
        hot_file = os.path.join(r'c:\Users\Rubi\Dropbox\epg','hot.xml')
        if os.path.isfile (os.path.join(r'c:\Users\Rubi\Dropbox\epg','hot.xml')):
            for line in os.open (hot_file,'r').readlines():
                file_out.write(line)
                
            
            
        # XML Close
        close_header (file_out)

        logger.info ('Total create time %d' % (time.time() - tic))

        import upload_file
        drop_handle = upload_file.DropBox ()
        drop_handle.upload_file (filename, '/epg/guide.xml')

        #shutil.copyfile(filename, os.path.join(r'c:\Users\Rubi\Dropbox\epg','guide.xml'))
        
    except:
        logger.exception ('Error during create')
     
    drop_handle.upload_file (log_path, '/epg/log.txt')     



