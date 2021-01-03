import requests

import codecs, time
from multiprocessing.pool import ThreadPool,Pool
import base,os
import urllib.request
import datetime, logging

DAYS_TO_SAVE = 7
THREADS = 10

CHANNELS_DATA = [
    
    ("CH30", ("כאן 11", "כאן 11 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/KAN_11.png"),
    ("CH34", ("קשת 12", "קשת 12 [source 2]", "קשת 12 [source 3]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/keshet.png"),
    ("CH36", ("רשת 13", "רשת 13 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/reshet.png"),
    ("TV50", ("ערוץ 9",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/channel_9.png"),
    ("PT92", ("ערוץ 20",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/channel_20.jpg"),
    ("CH57", ("ערוץ 23",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/channel_23.png"),    
    ("TV89", ("הכנסת",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/kenshet.jpg"),
    ("YSA1", ("Yes Movies Drama", "Yes Movies Drama [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_movies_drama.jpg"),
    ("YSA2", ("Yes Movies Action", "Yes Movies Action [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_movies_action.jpg"),
    ("YSA3", ("Yes Movies Comedy", "Yes Movies Comedy [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_movies_comedy.jpg"),
    ("YSA4", ("Yes Movies Kids", "Yes Movies Kids [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_movies_kids.jpg"),
    ("PT54", ("ONE 1", "ONE 1 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/one.jpg"),
    ("CH58", ("ONE 2", "ONE 2 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/one2.png"),
    ("PT53", ("Sport1", "Sport1 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/sport1.png"),
    ("PT23", ("Sport2", "Sport2 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/sport2.png"),
    ("CH09", ("Sport3", "Sport3 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/sport3.png"),
    ("CH11", ("Sport4", "Sport4 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/sport4.png"),
    ("TVR5", ("Sport 5", "Sport 5 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_sport.png"),
    ("TV16", ("Sport 5+", "Sport 5+ [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_plus.png"),
    ("PT62", ("Sport 5 Live",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_live.png"),
    ("CH56", ("Sport 5 Stars", "Sport 5 Stars [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_stars.png"),
    ("MU03", ("Sport 5 Gold",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_gold.png"),
    ("CH55", ("Sport 5 4K",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_4K.png"),
    ("YESV", ("Yes TV Action", "Yes TV Action [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_tv_action.jpg"),
    ("YESP", ("Yes TV Comedy", "Yes TV Comedy [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_tv_comedy.jpg"),
    ("YESU", ("Yes TV Drama", "Yes TV Drama [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_tv_drama.jpg"),
    ("YSAU", ("Yes ישראלי", "Yes ישראלי [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_israeli.jpg"),
    ("CH13", ("Wiz",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/wiz.png"),
    ("PT43", ("דיסני",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/disney.png"),
    ("PT59", ("דיסני ג'וניור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/disney_jr.png"),
    ("NK01", ("ניקולודיון",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nick.png"),
    ("PT69", ("ניק ג'וניור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nick_jr.png"),
    #("TA05", ("ג'וניור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/junior.png"),
    #("PT85", ("זום",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/zoom.png"),
    ("TV24", ("הופ",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hop.png"),
    ("PT46", ("הופ ילדות ישראלית",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hop_yaldoot.png"),
    ("TA02", ("בייבי",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/baby.png"),
    ("PT48", ("גים ג'אם",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/jimjam.png"),
    #("PT12", ("אגו",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/ego.png"),
    ("PT29", ("אגו טוטאל",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/ego_total.png"),
    ("TV17", ("National Geo",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nat_geo.png"),
    ("PT35", ("National Geo Wild",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nat_geo_wild.jpg"),
    ("TV18", ("Discovery",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/discovery.png"),
    ("TV62", ("Discovery Science",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/discovery_sicence.png"),
    ("PT55", ("ערוץ ההיסטוריה",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/history.png"),
    ("YSAT", ("Yes דוקו", "Yes דוקו [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_doco.jpg"),
    ("CH61", ("DIY",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/diy.png"),
    ("PT41", ("בית+",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/bait.png"),
    ("PT28", ("ערוץ הטיולים",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/tiyulim.png"),
    ("TV09", ("ערוץ החיים הטובים",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/haim_tovim.png"),
    ("PT14", ("ערוץ הבריאות",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/beriut.png"),    
    ("TV10", ("E!",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/e!.png"),
    ("TV67", ("ערוץ 24",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/channel_24.png"),
    ("TV35", ("MTV Music",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/mtv.png"),
    ("PT20", ("ערוץ האוכל",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/food_channel.png"),
    ("TV87", ("CBS reality",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cbs_real.png"),
    ("TV21", ("ערוץ הקניות",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/buying_channel.png"),    
    ("TV20", ("ויוה",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/viva.png"),
    ("PT60", ("ויוה+",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/viva_plus.png"),
    ("PT30", ("הידברות",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hidabrot.png"),
    ("PT72", ("ים תיכוני",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/channel_25.png"),
    ("CH17", ("חגיגה מזרחית",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hgiga-mizrhit.png"),
    ("CH18", ("ניק Teen",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nick_teen.png"),
    ("TV61", ("Animal Planet",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/animal_planet.png"),		
    ("TV29", ("Euro Sport",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/eurosport.png"),
    ("CH33", ("Euro Sport 2",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/eurosport2.png"),
    ("TV37", ("VH1",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/vh1.png"),	
    ("CH65", ("ערוץ ההומור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/humor.png"),
    ("CH70", ("ערוץ הדרמות הטורקיות",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/turki_drama.png"),	
    ("CH72", ("ערוץ הריאליטי",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/reality.png"),	
    ("CH19", ("ערוץ הכוכבים",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/kids_star.jpg"),	
    ("CH21", ("ONE 4K", ), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/one_4k.png"),
    
]



class YES (base.BASE_EPG):
    def __init__ (self,file_out, logger):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'YES', file_out, logger)
        
        self.logger.info ('Init Yes with total get time of %d days' % (DAYS_TO_SAVE))
                        

    def _parse_prog_thread_ (self, input_data):

        ind,url, session = input_data
        vvv = session.get (url)    
        data = vvv.json()
        
        
        start_time = datetime.datetime.fromtimestamp (eval (data['Start_Time_Fix_DateTime'][6:-2])/1000)
        end_time = datetime.datetime.fromtimestamp (eval (data['End_Time_Fix_DateTime'][6:-2])/1000)
        
        if start_time > end_time:
            end_time = end_time + datetime.timedelta(days=1)
                               
        return (ind , start_time, end_time, data['Hebrew_Name'], data['PreviewText'])


    def _print_channel_progs (self, channel_code):
    
        output = []
        
        session = requests.Session()

        for day_value in range (DAYS_TO_SAVE):
            data = session.get ("https://www.yes.co.il/content/YesChannelsHandler.ashx?action=GetDailyShowsByDayAndChannelCode&dayValue=%s&dayPartByHalfHour=0&channelCode=%s" % (day_value, channel_code))            
            data_text = data.text[4:-5]
            
            urls = []

            for ind,line in enumerate (data_text.split ('span class="text"')):
                                                                       
                if 'Schedule_Item_ID=' in line:
                    prog_id = line.split ('Schedule_Item_ID=')[1].split()[0].replace('"','')                                       
                    urls.append ((ind, "https://www.yes.co.il/content/YesChannelsHandler.ashx?action=GetProgramDataByScheduleItemID&ScheduleItemID=%s" % (prog_id),session))
            
                        
            pool = ThreadPool(THREADS)
            results = pool.map(self._parse_prog_thread_, urls)
            pool.close()
            pool.join()
            results.sort()
            
            total_results = len (results)
            for ind, result in enumerate (results):
                prog_data =  list (result[1:])
                
                if ind + 1 < total_results:
                    # current end not equal to next show start
                    if prog_data[1] != results[ind+1][1]:
                        prog_data[1] = results[ind+1][1]
                
                output += self._print_prog (channel_code , *prog_data)
            
            #print ('.', end="", flush=True)
            
        self.logger.info ("Done %s [%s]" % (self.channels[channel_code]['name'][0], channel_code))
            
        return output
                


if __name__ == "__main__":

    filename = os.path.join ('output', 'yes.xml')
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

    yes = YES(file_out, logger)
    
    file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_out.write('<tv">\n')
        
    yes.print_channels()
    yes.print_progs()
    
    file_out.write('</tv>\n')
    file_out.close()
    
    import my_dropbox
    drop_handle = my_dropbox.DropBox ()
    drop_handle.upload_file (filename, '/epg/yes_guide.xml')   