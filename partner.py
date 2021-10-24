import requests

import codecs, time
from multiprocessing.pool import ThreadPool,Pool
import base,os
import urllib.request
import datetime, logging

DAYS_TO_SAVE = 7
THREADS = 10

CHANNELS_DATA = [
    ("1190", ("ערוץ הילדים", ), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yeladim.png"),
    ("1240", ("הירו", ), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hero.png"),
    ("1293", ("פודי", ), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/foody.png"),
]

headers_prog = {"subCategory": "EventTitle", "platform": "WEB", "appName": "TV", "brand": "orange", "category": "TV","lang": "he-il"} 
url_prog = "https://my.partner.co.il/TV.Services/MyTvSrv.svc/SeaChange/GetEventTitleBO"

class Partner (base.BASE_EPG):

    def __init__ (self,file_out, big_guide, logger):
        global DAYS_TO_SAVE
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'Partner', file_out, logger)        
        self.logger.info ('Init Partner with total get time of %d days' % (DAYS_TO_SAVE))
        self.session = requests.Session()

        url =  "https://my.partner.co.il/TV.Services/MyTvSrv.svc/SeaChange/GetEpg"
        data = {"param": "post data"}
        headers = {"subCategory": "EPG", "platform": "WEB", "appName": "TV", "brand": "orange", "category": "TV","lang": "he-il","Accept-Encoding":"gzip,deflate"} 
        
        self.channels_cache = None
        for i in range (3):
            try:
                if not self.channels_cache:
                    self.channels_cache = self.session.post (url, json=data, headers=headers).json()['data']
            except:
                self.channels_cache = None

        if big_guide:        
            DAYS_TO_SAVE = 7
        else:
            DAYS_TO_SAVE = 2

        now_time = datetime.datetime.now () 
        self.end_time_to_save = (datetime.timedelta(days=DAYS_TO_SAVE) + now_time.replace (hour=0, minute=0, second=0)).timestamp()


    def get_prog_id (self, eventId):
        data = {"eventId": eventId}

        prog_data = None
        for i in range (3):
            try:
                if not prog_data:
                    prog_data = self.session.post (url_prog, json=data, headers=headers_prog).json()  
            except:
                prog_data = None
                                
        return prog_data['data']['name'], prog_data['data']['shortSynopsis']

    def _print_channel_progs (self, channel_code):

        output = []
        now_time = time.time()
        for channel in self.channels_cache:
            try:
                if channel['id'] == channel_code:
                    for event in channel['events']:
                        prog_name, prog_info = self.get_prog_id(event['id'])            
                        
                        #14/04/2021 13:45
                        start_time =  datetime.datetime.strptime (event['start'], '%d/%m/%Y %H:%M')
                        end_time =  datetime.datetime.strptime (event['end'], '%d/%m/%Y %H:%M')
                        
                        if end_time.timestamp() < now_time or start_time.timestamp() > self.end_time_to_save:
                            continue
                                            
                        prog_data = (start_time, end_time, prog_name, prog_info)
                        output += self._print_prog (channel_code , *prog_data)
            except:
                print ('Error in %s' % (channel_code))

        self.logger.info ("Done %s [%s]" % (self.channels[channel_code]['name'][0].encode('utf-16'), channel_code))                    
                    
        return output


if __name__ == "__main__":

    filename = os.path.join ('output', 'partner.xml')
    file_out = codecs.open(filename, 'w', encoding='utf8')  

    if not os.path.isdir ('output'):
        os.makedirs ('output')
    
    log_path = os.path.join ('output', 'log.txt')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])

    logger = logging.getLogger()   

    partner = Partner(file_out, False ,logger)
    
    file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_out.write('<tv">\n')
        
    partner.print_channels()
    partner.print_progs()
    
    file_out.write('</tv>\n')
    file_out.close()
    
    import my_dropbox
    drop_handle = my_dropbox.DropBox ()
    drop_handle.upload_file (filename, '/epg/partner_guide.xml')