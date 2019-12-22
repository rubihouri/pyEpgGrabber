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
    ("YES1", ("Yes1", "Yes1 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes1.png"),
    ("YES2", ("Yes2", "Yes2 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes2.png"),
    ("YES3", ("Yes3", "Yes3 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes3.png"),
    ("YES6", ("Yes4", "Yes4 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes4.png"),
    ("YES4", ("Yes5", "Yes5 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes5.png"),
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
    ("YESV", ("Yes Action", "Yes Action [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_action.png"),
    ("YESP", ("Yes Comedy", "Yes Comedy [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_comedy.png"),
    ("YESU", ("Yes Drama", "Yes Drama [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_drama.png"),
    ("YSAU", ("Yes קולנוע ישראלי", "Yes קולנוע ישראלי [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/israeli.png"),
    ("CH38", ("Yes Edge",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_edge.png"),
    ("CH13", ("Wiz",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/wiz.png"),
    ("CH15", ("Yes קידס",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_kidz.png"),
    ("PT43", ("דיסני",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/disney.png"),
    ("PT59", ("דיסני ג'וניור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/disney_jr.png"),
    ("NK01", ("ניקולודיון",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nick.png"),
    ("PT69", ("ניק ג'וניור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nick_jr.png"),
    ("TA05", ("ג'וניור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/junior.png"),
    #("PT85", ("זום",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708165-46.jpg"),
    ("TV24", ("הופ",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hop.png"),
    ("PT46", ("הופ ילדות ישראלית",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hop_yaldoot.png"),
    ("TA02", ("בייבי",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/baby.png"),
    ("PT48", ("גים ג'אם",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/jimjam.png"),
    #("PT12", ("אגו",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708002-46.jpg"),
    ("PT29", ("אגו טוטאל",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/ego_total.png"),
    ("TV17", ("National Geo",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nat_geo.png"),
    ("PT35", ("National Geo Wild",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nat_geo_wild.jpg"),
    ("TV18", ("Discovery",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/discovery.png"),
    ("TV62", ("Discovery Sicence",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/discovery_sicence.png"),
    ("TV19", ("ערוץ ההיסטוריה",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/history.png"),
    ("YSAT", ("Yes דוקו", "Yes דוקו [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_docu.png"),
    ("CH61", ("DIY",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/diy.png"),
    ("PT41", ("בית+",), "https://i.ibb.co/R0VzsHx/2708115-46.jpg"),
    ("PT28", ("ערוץ הטיולים",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708106-46.jpg"),
    ("TV09", ("ערוץ החיים הטובים",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707960-46.jpg"),
    ("PT14", ("ערוץ הבריאות",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708025-46.jpg"),
    ("TV10", ("E!",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708058-46.jpg"),
    ("TV67", ("ערוץ 24",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708013-46.jpg"),
    ("TV35", ("Mtv",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708006-46.jpg"),
    ("PT20", ("ערוץ האוכל",), "https://i.ibb.co/KXktNx1/food-channel.jpg"),
    ("TV87", ("CBS reality",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708070-46.jpg"),
    ("TV21", ("ערוץ הקניות",), "https://i.ibb.co/b2HjfxH/buying-channel.jpg"),
    ("TV20", ("ויוה",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707989-46.jpg"),
    ("PT60", ("ויוה+",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708144-46.gif"),
    ("PT30", ("הידברות",), "https://i.ibb.co/t2SXkZf/hidabrot.jpg"),
    ("PT72", ("ים תיכוני",), "https://images.globes.co.il/images/NewGlobes/big_image_800/2018/CD8E9E2CC494CB98C1B4AD8491B9FF50_800x392.20180729T150714.jpg"),
    ("CH17", ("חגיגה מזרחית",), "https://i.ibb.co/Jc9FcPC/hgiga-mizrhit.png"),
    ("CH18", ("ניק Teen",), "https://github.com/rubihouri/pyEpgGrabber/blob/master/images/nick_teen.png?raw=true"),
    
]



class YES (base.BASE_EPG):
    def __init__ (self,file_out, logger):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'YES', file_out, logger)
        
        self.logger.info ('Init Yes with total get time of %d days' % (DAYS_TO_SAVE))
                        

    def _parse_prog_thread_ (self, input_data):

        ind,url = input_data
        vvv = self.session.get (url)    
        data = vvv.json()
        
        
        start_time = datetime.datetime.fromtimestamp (eval (data['Start_Time_Fix_DateTime'][6:-2])/1000)
        end_time = datetime.datetime.fromtimestamp (eval (data['End_Time_Fix_DateTime'][6:-2])/1000)
        
        if start_time > end_time:
            end_time = end_time + datetime.timedelta(days=1)
                               
        return (ind , start_time, end_time, data['Hebrew_Name'], data['PreviewText'])


    def _print_channel_progs (self, channel_code):
    
        output = []

        for day_value in range (DAYS_TO_SAVE):
            data = self.session.get ("https://www.yes.co.il/content/YesChannelsHandler.ashx?action=GetDailyShowsByDayAndChannelCode&dayValue=%s&dayPartByHalfHour=0&channelCode=%s" % (day_value, channel_code))            
            data_text = data.text[4:-5]
            
            urls = []

            for ind,line in enumerate (data_text.split ('span class="text"')):
                                                                       
                if 'Schedule_Item_ID=' in line:
                    prog_id = line.split ('Schedule_Item_ID=')[1].split()[0].replace('"','')                                       
                    urls.append ((ind, "https://www.yes.co.il/content/YesChannelsHandler.ashx?action=GetProgramDataByScheduleItemID&ScheduleItemID=%s" % (prog_id)))
            
                        
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
            
            print ('.', end="", flush=True)
            
        print ("")
            
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
