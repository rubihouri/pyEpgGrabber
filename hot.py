import requests
import datetime, json, codecs
import base, os, logging,time

CHANNELS_DATA = [
    ("496", ("Hot Cinema1", "Hot Cinema1 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cinema1.png"),
    ("486", ("Hot Cinema2", "Hot Cinema2 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cinema2.png"),
    ("493", ("Hot Cinema3", "Hot Cinema3 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cinema3.png"),
    ("491", ("Hot Cinema4", "Hot Cinema4 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cinema4.png"),        
    ("477", ("Hot 3",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot3.png"),     
    ("772", ("Hot HBO",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_hbo.png"), 
    ("898", ("Food Network",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/food_network.png"),
    ("900", ("Travel Channel",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/travel.png"),
    ("506", ("Hot Zone",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_zone.png"),    
    ("682", ("HOT קומדי סנטרל",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_comedy.png"),
    ("507", ("Hot בידור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_bidur.png"),        
    ("871", ("Hot קידס",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_kidz.png"),        
    ("510", ("לולי",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/luli.png"),        
    ("430", ("Hot 8",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot8.png"),       
    ("489", ("Bollywood",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_bollywood.png"),
    ("490", ("Bombay",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_bombay.png"),                  
    ("738", ("זום",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/zoom.png"),
    
    

]



DAYS_TO_SAVE = 7

class HOT (base.BASE_EPG):
    def __init__ (self,file_out,logger):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'HOT', file_out, logger)
            
                    
        current_date = datetime.datetime.now()
        end_date = current_date + datetime.timedelta(days=DAYS_TO_SAVE)
        self.start_time_str = datetime.datetime.strftime(current_date, '%Y-%m-%d') + 'T00:00:00.000Z' # 2019-12-17T22:00:00.000Z   
        self.end_time_str = datetime.datetime.strftime(end_date, '%Y-%m-%d') + 'T00:00:00.000Z' # 2019-12-17T22:00:00.000Z   
        
        self.logger.info ('Init HOT with total get time of %d days' % (DAYS_TO_SAVE))
                                                 
    def _create_date_and_time_ (self, date, duration):
                
        start_time_ttag = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:00') # '2019-12-18T07:30:00'        
        duration_ttag = datetime.datetime.strptime(duration, '%Y-%m-%dT%H:%M:00') # '2019-12-18T07:30:00'
        end_time_ttag = start_time_ttag + datetime.timedelta(minutes=duration_ttag.minute, hours = duration_ttag.hour)

        return start_time_ttag, end_time_ttag


    def _print_channel_progs (self, channel_code):

        json_data = {
                    "lcid":1037,
                    "text":"",
                    "channel":channel_code,
                    "genre":-1,
                    "ageRating":-1,
                    "startDateWithTime":self.start_time_str,
                    "endDateWithTime":self.end_time_str,
                    "pageIndex":1,
                    "pageSize":500,
                    "productionYear":-1,
                    "productionCountry":-1,
                    "orderby":""
        }
        
        output = []
        
        try:
            data_str = self.session.post ("https://www.hot.net.il/Mobile/TV-guid-mobile/GetData.aspx/AdvanceSearch", json = json_data)
            
            
            data_str = data_str.json()
            
            if 'd' in data_str:

                data = json.loads (data_str['d'])[0]['Shows']
                     
                self.logger.info  ('Total Shows: %d' % (len(data)))
                     
                # Run on Shows
                for show in data:
                    start_data_and_time,  end_data_and_time = self._create_date_and_time_ (show['StartDate'], show['LengthTime'])
                    output += self._print_prog (channel_code, start_data_and_time, end_data_and_time,show['Name'], show['Synopsis'])
            self.logger.info ('Done channle %s' % (channel_code))
             
        except:
            self.logger.exception ('Error during get channel %s' % (channel_code))
        
        return output
                        


if __name__ == "__main__":
    filename = os.path.join ('output', 'hot.xml')
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
    hot = HOT(file_out,logger)
    
    hot.print_progs()
    
    file_out.flush()
    
    import my_dropbox
    drop_handle = my_dropbox.DropBox ()
    drop_handle.upload_file (filename, '/epg/hot.xml')


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
    
