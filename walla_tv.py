import requests
from bs4 import BeautifulSoup
import codecs, time
from multiprocessing.pool import ThreadPool,Pool
import base,os
import urllib.request
import datetime, logging

DAYS_TO_SAVE = 5

CHANNELS_DATA = [

    ("345", ("Hot Cinema1", "Hot Cinema1 [source 2]"), "https://i.ibb.co/MC0hTdF/cinema1.jpg"),
    ("339", ("Hot Cinema2", "Hot Cinema2 [source 2]"), "https://i.ibb.co/7QcP3fy/cinema2.jpg"),
    ("3586", ("Hot Cinema3", "Hot Cinema3 [source 2]"), "https://i.ibb.co/YDD3tL6/cinema3.jpg"),
    ("343", ("Hot Cinema4", "Hot Cinema4 [source 2]"), "https://i.ibb.co/dBMXtBF/cinema4.jpg"),        
    ("353", ("Hot 3",), "https://i.ibb.co/cxwcrf9/hot3.jpg"),     
    ("3814", ("Travel Channel",), "https://i.ibb.co/DMbvqZD/travel.png"),
    ("3182", ("Hot Zone",), "https://i.ibb.co/Dk5T0kx/40666656-2068495396516120-1957389211522826240-n.jpg"),    
    ("3547", ("HOT קומדי סנטרל",), "https://i.ibb.co/KwxJ1YX/40666656-2068495396516120-1957389211522826240-n-Copy-2.jpg"),
    ("349", ("Hot בידור",), "https://i.ibb.co/dLShh9x/40666656-2068495396516120-1957389211522826240-n-Copy.jpg"),        
    ("3835", ("Hot קידס",), "https://www.hot.net.il/UploadedImages//01_2018/logo_kidz_510X287.png"),        
    ("350", ("לולי",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708082-46.jpg"),        
    ("559", ("Hot 8",), "https://i.ibb.co/c2B9DDj/hot8.jpg"),       
    ("340", ("Bollywood",), "https://i.ibb.co/LhnzV5V/hot-bollywood.jpg"),
    ("341", ("Bombay",), "https://i.ibb.co/tqYYY6V/hot-bombay.jpg"),       
    ("3690", ("Hot HBO",), "https://i.ibb.co/vdc4VNY/hot-hbo.jpg"),            
    ("3635", ("זום",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708165-46.jpg"),
    #("999", ("Food Network",), "https://i.ibb.co/KKKVCYv/foor-network.png"),    
    #("477", ("GINX",), "https://i.ibb.co/616J7xg/ginx.png"),
    #("477", ("הירו",), "https://i.ibb.co/Zc70C14/hero.png"),  
    #("477", ("פודי",), "https://i.ibb.co/zh5c7HS/foody.png"),
    #("477", ("Fine Living",), "https://i.ibb.co/Wfm7hbw/fine-living.png"),
    #("477", ("Lifetime",), "https://i.ibb.co/nbCfRbB/lifetime.jpg"),
    #("477", ("Fox Sport",), "https://i.ibb.co/zh5c7HS/foody.png"),    
   
]


class WALLA_TV (base.BASE_EPG):
    def __init__ (self,file_out, logger):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'WALLA_TV', file_out, logger)
        
        self.logger.info ('Init Walla TV with total get time of %d days' % (DAYS_TO_SAVE))
                        
    def _create_date_and_time_ (self, date, the_time):
        #the_time = the_time.replace (':','')+'00'
        #return date + the_time + ' +0200'
        
        date_tag = datetime.datetime.strptime(date+the_time, '%Y-%m-%d%H:%M')    
        return date_tag



    def _print_channel_progs (self, channel_code):
    
        output = []


        page_data = requests.get ('https://tv-guide.walla.co.il/channel/%s' % (channel_code))

        soup = BeautifulSoup(page_data.text, 'html.parser')
        div_data = soup.find_all ('div')[0]

        dates = []
        for day in page_data.text.split ('class="tv-guide-channels-logos"')[1].split ("datetime")[1:DAYS_TO_SAVE + 1]:
            dates.append (day[2:12])

        shows = []
        for fatherindex in range (len (dates)):

            for ind, prog in enumerate (div_data.find_all ('li', attrs={'data-fatherindex': "%d"% fatherindex})):

                prog_str = str (prog)        
                prog_dict = eval (prog_str.split ("data-obj=\'")[1].split ("\' data")[0])


                end_time = self._create_date_and_time_ (dates[fatherindex],prog_dict['end_time'])
                if  ind == 0 and len(shows) and prog_dict['name'] == shows[-1]['name']:                               
                    shows[-1]['end_time'] = end_time
                    
                else:
                    start_time = self._create_date_and_time_ (dates[fatherindex],prog_dict['start_time'])
                    
                    if ind == 0 and len(shows) and start_time!= shows[-1]['end_time']:
                        shows[-1]['end_time'] = start_time
                    
                    shows.append ({
                              'name': prog_dict['name'],
                             'description':  prog_dict['description'],
                             'start_time': start_time,
                             'end_time': end_time,
                    })
         
        for show in shows:
            output += self._print_prog (channel_code, show['start_time'], show['end_time'], show['name'], show['description'])
        return output
                


if __name__ == "__main__":

    filename = os.path.join ('output', 'walla_tv.xml')
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

    walla = WALLA_TV(file_out, logger)
    
    file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_out.write('<tv">\n')
        
    walla.print_channels()
    walla.print_progs()
    
    file_out.write('</tv>\n')
    file_out.close()
    
    import my_dropbox
    drop_handle = my_dropbox.DropBox ()    
    drop_handle.upload_file (filename, '/epg/walla_guide.xml')    