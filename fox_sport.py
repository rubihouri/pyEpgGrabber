import requests
import datetime, json, codecs
import base, os, logging,time

CHANNELS_DATA = [
    ("ESE1", ("Fox Sport", ), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/fox_sport.png"),

]

DAYS_TO_SAVE = 7

class FoxSport (base.BASE_EPG):    
    def __init__ (self,file_out,big_guide, logger):
        global DAYS_TO_SAVE
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'HOT', file_out, logger)
        
        if big_guide:        
            DAYS_TO_SAVE = 7
        else:
            DAYS_TO_SAVE = 3
                                
        current_date = datetime.datetime.now()
        end_date = current_date + datetime.timedelta(days=DAYS_TO_SAVE)
        self.start_time_str = datetime.datetime.strftime(current_date, '%Y-%m-%d') + 'T00:00:00.000Z' # 2019-12-17T22:00:00.000Z   
        self.end_time_str = datetime.datetime.strftime(end_date, '%Y-%m-%d') + 'T00:00:00.000Z' # 2019-12-17T22:00:00.000Z   
        
        self.logger.info ('Init Fox Sport with total get time of %d days' % (DAYS_TO_SAVE))
                                                 
    def _create_date_and_time_ (self, date, duration):
                
        start_time_ttag = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:00') # '2019-12-18T07:30:00'        
        duration_ttag = datetime.datetime.strptime(duration, '%Y-%m-%dT%H:%M:00') # '2019-12-18T07:30:00'
        end_time_ttag = start_time_ttag + datetime.timedelta(minutes=duration_ttag.minute, hours = duration_ttag.hour)

        return start_time_ttag, end_time_ttag


    def _print_channel_progs (self, channel_code):
    
        output = []
        now_time = datetime.datetime.now () 
        now_time = now_time.replace (hour=0, minute=0, second=0)
        
        for ind in range (DAYS_TO_SAVE):
        
            try:
                date2take = now_time + datetime.timedelta(days=ind)
                date_str = str(date2take.year) + '%02d'%(date2take.month) + '%02d'%(date2take.day)
                data = requests.get("https://tv.foxsportsasia.com/getEPG.php?lang=en&channelCode=%s&date=%s" % (channel_code, date_str)).json()
                
                for prog in data[channel_code]:

                    start_time =  datetime.datetime.strptime (prog['date'] + ' ' + prog['start_time'], '%m-%d-%y %H:%M:%S')
                    start_time = start_time - datetime.timedelta(hours=5)
                    
                    tokens = list (map (int, prog['duration'].split(':')))
                    end_time =  start_time + datetime.timedelta(hours=tokens[0], minutes=tokens[1], seconds=tokens[2])
                    
                    live_str = ''
                    if prog['live'] == 'L':
                        live_str = 'Live - '
                    
                    prog_data = (start_time, end_time, live_str + prog['programme'], prog['programme'])
                    output += self._print_prog (channel_code , *prog_data)
            except:
                print ('Error in %s' % (channel_code))
                continue
                            
        print ("Done %s [%s]" % (self.channels[channel_code]['name'][0].encode('utf-16'), channel_code))        
        
        return output
                        


if __name__ == "__main__":
    filename = os.path.join ('output', 'fox.xml')
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
    file_out.write (str(time.time()) + '\n')
    fox = FoxSport(file_out,True, logger)
    
    fox.print_progs()
    
    file_out.flush()
    
    import my_dropbox
    drop_handle = my_dropbox.DropBox ()
    drop_handle.upload_file (filename, '/epg/fox.xml')


    guide_filename = os.path.join ('output', 'hot_guide.xml')
    file_out = codecs.open(guide_filename, 'w', encoding='utf8')  
    
    if 0:
        file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file_out.write('<tv>\n')
        
        hot = HOT(file_out,logger)
        hot.print_channels()
        hot.print_progs()
        
        file_out.write('</tv>\n')    
        file_out.close()
    
        drop_handle.upload_file (guide_filename, '/epg/hot_guide.xml')
    
