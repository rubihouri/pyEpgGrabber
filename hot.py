import requests
from bs4 import BeautifulSoup
import datetime, json, codecs
import base

CHANNELS_DATA = [
    ("496", ("Hot Cinema1", "Hot Cinema1 [source2]"), "https://i.ibb.co/3m2YKnD/KAN-11.png"),
    ("486", ("Hot Cinema2", "Hot Cinema2 [source2]"), "https://i.ibb.co/3m2YKnD/KAN-11.png"),
    ("493", ("Hot Cinema3", "Hot Cinema3 [source2]"), "https://i.ibb.co/3m2YKnD/KAN-11.png"),
    ("491", ("Hot Cinema4", "Hot Cinema4 [source2]"), "https://i.ibb.co/3m2YKnD/KAN-11.png"),    
    ("477", ("Hot 3",), "https://i.ibb.co/3m2YKnD/KAN-11.png"),     
    ("772", ("Hot HBO",), "https://i.ibb.co/vdc4VNY/hot-hbo.jpg"),    
    ("898", ("Food Network",), "https://i.ibb.co/KKKVCYv/foor-network.png"),
    ("900", ("Travel Channel",), "https://i.ibb.co/DMbvqZD/travel.png"),        
    ("506", ("Hot Zone",), "https://i.ibb.co/Dk5T0kx/40666656-2068495396516120-1957389211522826240-n.jpg"),
    ("682", ("HOT קומדי סנטרל",), "https://i.ibb.co/KwxJ1YX/40666656-2068495396516120-1957389211522826240-n-Copy-2.jpg"),
    ("507", ("Hot בידור",), "https://i.ibb.co/dLShh9x/40666656-2068495396516120-1957389211522826240-n-Copy.jpg"),        
    ("871", ("Hot קידס",), "https://www.hot.net.il/UploadedImages//01_2018/logo_kidz_510X287.png"),
    ("510", ("לולי",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708082-46.jpg"),        
    ("430", ("Hot 8",), "https://i.ibb.co/c2B9DDj/hot8.jpg"),
    ("489", ("Bollywood",), "https://i.ibb.co/LhnzV5V/hot-bollywood.jpg"),
    ("490", ("Bombay",), "https://i.ibb.co/tqYYY6V/hot-bombay.jpg"),
    
    
    #("477", ("GINX",), "https://i.ibb.co/616J7xg/ginx.png"),
    #("477", ("הירו",), "https://i.ibb.co/Zc70C14/hero.png"),  
    #("477", ("פודי",), "https://i.ibb.co/zh5c7HS/foody.png"),
    #("477", ("Fine Living",), "https://i.ibb.co/zh5c7HS/foody.png"),
    #("477", ("Lifetime",), "https://i.ibb.co/zh5c7HS/foody.png"),
    #("477", ("Fox Sport",), "https://i.ibb.co/zh5c7HS/foody.png"),
    

]



DAY_TO_SAVE = 7

class HOT (base.BASE_EPG):
    def __init__ (self,file_out):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,file_out)
            
                    
        current_date = datetime.datetime.now()
        end_date = current_date + datetime.timedelta(days=DAY_TO_SAVE)
        self.start_time_str = datetime.datetime.strftime(current_date, '%Y-%m-%d') + 'T00:00:00.000Z' # 2019-12-17T22:00:00.000Z   
        self.end_time_str = datetime.datetime.strftime(end_date, '%Y-%m-%d') + 'T00:00:00.000Z' # 2019-12-17T22:00:00.000Z   
                                                 
    def _create_date_and_time_ (self, date, duration):
                
        start_time_ttag = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:00') # '2019-12-18T07:30:00'        
        duration_ttag = datetime.datetime.strptime(duration, '%Y-%m-%dT%H:%M:00') # '2019-12-18T07:30:00'
        end_time_ttag = start_time_ttag + datetime.timedelta(minutes=duration_ttag.minute, hours = duration_ttag.hour)


        start_time = datetime.datetime.strftime (start_time_ttag, '%Y%m%d%H%M')  + '00 +0200'# 20191218060500 +0200
        end_time = datetime.datetime.strftime (end_time_ttag, '%Y%m%d%H%M')  + '00 +0200'# 20191218060500 +0200
        return start_time, end_time


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
        
        data_str = self.session.post ("https://www.hot.net.il/Mobile/TV-guid-mobile/GetData.aspx/AdvanceSearch", json = json_data)
        
        
        data_str = data_str.json()
        
        if 'd' in data_str:

            data = json.loads (data_str['d'])[0]['Shows']
                 
            print ('Total Shows: %d' % (len(data)))
                 
            # Run on Shows
            for show in data:
                start_data_and_time,  end_data_and_time = self._create_date_and_time_ (show['StartDate'], show['LengthTime'])
                self._print_prog (channel_code, start_data_and_time, end_data_and_time,show['Name'], show['Synopsis'])
                
        else:
            print ('OPS!!')
                        


hot = HOT()
hot.print_channels()
hot.print_progs()