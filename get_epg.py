#!/usr/bin/python3
import requests,time
import codecs, os, time, shutil
import yes,hot, walla_tv, foody, apollo
import logging,sys
import my_dropbox
import datetime,time


file_path = os.path.dirname (os.path.realpath (__file__))
os.chdir (file_path)


def print_header (file_out):    
  
    file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_out.write('<tv>\n')
        

def close_header(file_out,):
    file_out.write('</tv>\n')


logger = None
log_path = os.path.join ('output', 'log.txt')

def set_logger():

    if os.path.isfile (log_path):
      os.remove (log_path)
  
    global logger

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])

    logger = logging.getLogger()   

    
    
if __name__ == "__main__":

    try:

        if len (sys.argv) == 1  or sys.argv[1] != '1':
          now_time = datetime.datetime.now ()
          sleep_time = (datetime.timedelta(days=1) + now_time.replace (hour=1, minute=0, second=0) - now_time).seconds
          print ('Sleep %d before start'%sleep_time)
          time.sleep (sleep_time)        
        while True:    
          set_logger()
          tic = time.time()

          if not os.path.isdir ('output'):
            os.makedirs ('output')        

          filename = os.path.join ('output', 'guide.xml')
          file_out = codecs.open(filename, 'w', encoding='utf8')  

          yes_handle = yes.YES(file_out, logger)       
          hot_handle = hot.HOT(file_out, logger)    
          walla_handle = walla_tv.WALLA_TV(file_out, logger)    
          foody_handle = foody.FOODY(file_out, logger)    
          apollo_handle = apollo.APOLLO(file_out, logger)    
          drop_handle = my_dropbox.DropBox ()        

          # XML Start
          print_header (file_out)

          # Print Channels Area
          yes_handle.print_channels ()
          #hot_handle.print_channels ()
          walla_handle.print_channels ()
          foody_handle.print_channels ()
          apollo_handle.print_channels ()

          # Print Prog area
          yes_handle.print_progs ()
          walla_handle.print_progs ()
          foody_handle.print_progs ()
          apollo_handle.print_progs ()

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
          if len (sys.argv) != 1:
             break
          time.sleep (3600*24)

    except:
        logger.exception ('Error during create')
       



