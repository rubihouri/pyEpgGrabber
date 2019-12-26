import requests
from bs4 import BeautifulSoup
import codecs, time
from multiprocessing.pool import ThreadPool,Pool
import base,os
import urllib.request
import datetime, logging

DAYS_TO_SAVE = 7

CHANNELS_DATA = [

    ("FOODY", ("פודי",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/foody.png"),
  
   
]


class FOODY (base.BASE_EPG):
    def __init__ (self,file_out, logger):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'FOODY', file_out, logger)
        
        self.logger.info ('Init Foody with total get time of %d days' % (DAYS_TO_SAVE))
                        

    def _print_channel_progs (self, channel_code):
    
    
        prog_shows = {
            ((14,00),(14,30)): ("סופר שי-לי", 'השפית והמתכונאית שי-לי ליפא מבשלת בכל פרק 3 מנות קלות להכנה ומתכון נוסף סופר-דופר מיוחד'),
            ((14,30),(15,00)): ("ישראל אהרוני", "ישראל אהרוני מבשל"),
            ((15,00),(15,30)): ("מתכון מנצח", "בחרת הבלוגרים של פודי מפתיעה במתכונים מושלמים שתמיד מצליחים. בואו לגלות את המתכונים הכי אהובים של הבלוגרים המובילים בארץ"),
            ((15,30),(16,00)): ("מסעדת הפועלים של שגב", "השף משה שגב מבשל"),
            ((16,00),(16,30)): ("הצד שלו הצד שלה", "השף מאיר אדוני והילה אלפרט יוצאים כל אחד למסע בעקבות חומר גלם או השראה וחוזרים לבשל יחד במטבח בעקבות המפגש"),
            ((16,30),(17,00)): ("קרין גורן", "כל הסודות המתוקים של קרין גורן"),
            ((17,00),(17,30)): ("2 גברים ומקרר", "אודי ברקן ואושר אידלמן מבשלים יחד"),
            ((17,30),(18,00)): ("המושחתים של פודי", "המאכלים המושחתים ביותר מבית מיטב השפים והבלוגרים"),
                
        }
        

        now_time = datetime.datetime.now()        
        shows = []
        for i in range (DAYS_TO_SAVE):
            week_day = (now_time.weekday() + 2 ) % 8
                
            total_iters = 24*2 if week_day in [6,7] else 14*2
            
            day_time = now_time.replace (hour=0,minute=0)
            
            for i in range (total_iters):
                stop_time = day_time + datetime.timedelta (minutes = 30)
                shows.append ({
                          'name': "ערוץ פודי",
                         'description':  "ערוץ פודי",
                         'start_time': day_time ,
                         'end_time': stop_time,
                }) 
                
                day_time = stop_time
                
            
            if week_day not in [6,7]:
                 
                for prog_time, prog_name  in prog_shows.items():
                
                    start_time = now_time.replace (hour=prog_time[0][0],minute=prog_time[0][1])
                    end_time = now_time.replace (hour=prog_time[1][0],minute=prog_time[1][1])                
                    shows.append ({
                              'name': prog_name[0],
                             'description': prog_name[1],
                             'start_time': start_time,
                             'end_time': end_time,
                    })  



                total_iters = round ((((now_time.replace (hour=23,minute=59)  -  end_time).seconds) / 60.) / 60.) * 2
                day_time = end_time
                for i in range (total_iters):
                    stop_time = day_time + datetime.timedelta (minutes = 30)
                    shows.append ({
                              'name': "פודי",
                             'description':  "ערוץ פודי",
                             'start_time': day_time ,
                             'end_time': stop_time,
                    }) 
                    
                    day_time = stop_time

    
            

            now_time += datetime.timedelta (days = 1)
      

        output = []
        for show in shows:
            output += self._print_prog (channel_code, show['start_time'], show['end_time'], show['name'], show['description'])
        return output
                


if __name__ == "__main__":

    filename = os.path.join ('output', 'foody.xml')
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

    foody = FOODY(file_out, logger)
    
    file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_out.write('<tv">\n')
        
    foody.print_channels()
    foody.print_progs()
    
    file_out.write('</tv>\n')
    file_out.close()
    
    import my_dropbox
    drop_handle = my_dropbox.DropBox ()    
    drop_handle.upload_file (filename, '/epg/foody.xml')