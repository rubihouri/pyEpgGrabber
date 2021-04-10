#!/usr/bin/python3
import requests,time
import codecs, os, time, shutil
import yes,hot, walla_tv, foody, apollo, partner, fox_sport
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

        set_logger() 
    
        if len (sys.argv) == 1  or sys.argv[1] != '1':
            now_time = datetime.datetime.now ()
            sleep_time = (datetime.timedelta(days=1) + now_time.replace (hour=1, minute=15, second=0) - now_time).seconds
            logger.info ('Sleep %d before start'%sleep_time)
            time.sleep (sleep_time)        
           
        while True:
            try:
                
                tic = time.time()

                if not os.path.isdir ('output'):
                    os.makedirs ('output')

                for guide_name, big_guide in [('guide.xml', True), ('guide2.xml', False)]:

                    filename = os.path.join ('output', guide_name)
                    file_out = codecs.open(filename, 'w', encoding='utf8')  

                    yes_handle = yes.YES(file_out, big_guide, logger)       
                    hot_handle = hot.HOT(file_out, big_guide, logger)
                    #foody_handle = foody.FOODY(file_out, big_guide, logger)                     
                    partner_handle = partner.Partner(file_out, big_guide, logger)                     
                    fox_handle = fox_sport.FoxSport(file_out, big_guide, logger)                     
                    #walla_handle = walla_tv.WALLA_TV(file_out, big_guide, logger)       
                    #apollo_handle = apollo.APOLLO(file_out, logger)    
                    drop_handle = my_dropbox.DropBox ()        

                    # XML Start
                    print_header (file_out)

                    if 0:
                        hot_data = drop_handle.download_file ('/epg/hot.xml')         
                        if hot_data:
                            lines = hot_data.split('\n')
                            # Created in last 3 days
                            if time.time() -  eval (lines[0]) < 3 * 24*60*60:
                                hot_data = '\n'.join (lines[1:])
                            else:
                                hot_data = None

                    # Print Channels Area
                    yes_handle.print_channels ()
                    hot_handle.print_channels ()                        
                    partner_handle.print_channels ()                        
                    fox_handle.print_channels ()                        
                    #foody_handle.print_channels ()                    
                    #walla_handle.print_channels ()
                    #apollo_handle.print_channels ()
                    
                    # Print Prog area
                    yes_handle.print_progs ()
                    hot_handle.print_progs ()                        
                    partner_handle.print_progs ()                    
                    fox_handle.print_progs ()                    
                    #foody_handle.print_progs ()                    
                    #walla_handle.print_progs ()
                           
                    # XML Close
                    close_header (file_out)

                    logger.info ('Total create time %d' % (time.time() - tic))

                    file_out.close()

                    drop_handle.upload_file (filename, '/epg/%s'%(guide_name))
                    
                drop_handle.upload_file (log_path, '/epg/log.txt')                     
                if len (sys.argv) > 1 and sys.argv[1] == '1':
                    logger.info ('bye bye')
                    break
                time.sleep (3600*24)
                
            except:
                logger.exception ('Error in main loop')

    except:
        logger.exception ('Error during create')
       


