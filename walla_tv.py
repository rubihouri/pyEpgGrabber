import requests
from bs4 import BeautifulSoup
import codecs, time
from multiprocessing.pool import ThreadPool,Pool
import base,os
import urllib.request
import datetime, logging

DAYS_TO_SAVE = 5

CHANNELS_DATA = [

    ("345", ("Hot Cinema1", "Hot Cinema1 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cinema1.png"),
    ("339", ("Hot Cinema2", "Hot Cinema2 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cinema2.png"),
    ("3586", ("Hot Cinema3", "Hot Cinema3 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cinema3.png"),
    ("343", ("Hot Cinema4", "Hot Cinema4 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cinema4.png"),        
    ("353", ("Hot 3",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot3.png"),     
    ("3814", ("Travel Channel",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/travel.png"),
    ("3182", ("Hot Zone",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_zone.png"),    
    ("3547", ("HOT קומדי סנטרל",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_comedy.png"),
    ("349", ("Hot בידור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_bidur.png"),        
    ("3835", ("Hot קידס",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_kidz.png"),        
    ("350", ("לולי",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/luli.png"),        
    ("559", ("Hot 8",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot8.png"),       
    ("340", ("Bollywood",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_bollywood.png"),
    ("341", ("Bombay",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_bombay.png"),       
    ("3690", ("Hot HBO",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hot_hbo.png"),            
    ("3635", ("זום",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/zoom.png"),
    ("542", ("ג'וניור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/junior.png"),
	
    ("359", ("MTV Dance",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/mtv_dance.png"),
    ("358", ("MTV Rocks",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/mtv_rocks.png"),
    ("360", ("MTV Hits",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/mtv_hits.png"),
    ("361", ("MTV HD",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/mtv_hd.png"),
	
    #("999", ("Food Network",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/food_network.png"),    
    #("477", ("GINX",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/ginx.png"),
    #("477", ("הירו",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hero.png"),  
    #("477", ("פודי",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/foody.png"),
    #("477", ("Fine Living",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/fine_living.png"),
    #("477", ("Lifetime",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/lifetime.png"),
    #("477", ("Fox Sport",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/fox_sport.png"),    
   
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