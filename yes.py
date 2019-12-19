import requests
from bs4 import BeautifulSoup
import codecs, time
from multiprocessing.pool import ThreadPool,Pool
import base

import urllib.request

DAYS_TO_SAVE = 4
THREADS = 10

CHANNELS_DATA = [
    ("CH30", ("כאן 11", "כאן 11 [source 2]"), "https://i.ibb.co/3m2YKnD/KAN-11.png"),
    ("CH34", ("קשת 12", "קשת 12 [source 2]", "קשת 12 [source 3]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708193-46.jpg"),
    ("CH36", ("רשת 13", "רשת 13 [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708308-46.png"),
    ("TV50", ("ערוץ 9",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708096-46.jpg"),
    ("PT92", ("ערוץ 20",), "https://i.ibb.co/8cLcJY8/img805937.jpg"),
    ("CH57", ("ערוץ 23",), "https://i.ytimg.com/vi/SQ4eYiZ5foo/maxresdefault.jpg"),
    ("TV89", ("הכנסת",), "https://i.ibb.co/TBZXwgQ/kenshet.jpg"),
    ("YES1", ("Yes1", "Yes1 [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707954-46.jpg"),
    ("YES2", ("Yes2", "Yes2 [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707957-46.jpg"),
    ("YES3", ("Yes3", "Yes3 [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707958-46.jpg"),
    ("YES6", ("Yes4", "Yes4 [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708001-46.jpg"),
    ("YES4", ("Yes5", "Yes5 [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708110-46.jpg"),
    ("PT54", ("ONE 1", "ONE 1 [source 2]"), "https://i.ibb.co/vPwm3Vp/ONE-800.jpg"),
    ("CH58", ("ONE 2", "ONE 2 [source 2]"), "https://i.ibb.co/zRBB8cq/9241.png"),
    ("PT53", ("Sport1", "Sport1 [source 2]"), "https://i.ibb.co/4VZTSyK/sport1.png"),
    ("PT23", ("Sport2", "Sport2 [source 2]"), "https://i.ibb.co/4W24rBH/sport2.png"),
    ("CH09", ("Sport3", "Sport3 [source 2]"), "https://i.ibb.co/CtmVM5f/597701.png"),
    ("CH11", ("Sport4", "Sport4 [source 2]"), "https://i.ibb.co/W0TCCmK/7765.png"),
    ("TVR5", ("Sport 5", "Sport 5 [source 2]"), "https://i.ibb.co/0CkcTs6/2788991-46.png"),
    ("TV16", ("Sport 5+", "Sport 5+ [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707998-46.jpg"),
    ("PT62", ("Sport 5 Live",), "https://i.ibb.co/HzrDhSP/2708030-46.png"),
    ("CH56", ("Sport 5 Stars", "Sport 5 Stars [source 2]"), "https://i.ibb.co/gZkCD7K/5-stars.png"),
    ("MU03", ("Sport 5 Gold",), "https://i.ibb.co/pbyGxfL/2708031-46.png"),
    ("YESV", ("Yes Action", "Yes Action [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708074-46.jpg"),
    ("YESP", ("Yes Comedy", "Yes Comedy [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708072-46.jpg"),
    ("YESU", ("Yes Drama", "Yes Drama [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708104-46.jpg"),
    ("YSAU", ("Yes קולנוע ישראלי", "Yes קולנוע ישראלי [source 2]"), "https://i.ibb.co/Sspk1k8/israeli.png"),
    ("CH38", ("Yes Edge",), "https://i.ibb.co/FhMwv62/YES-Edge.png"),
    ("CH13", ("Wiz",), "https://i.ibb.co/nknTqfM/1280px-Wi-Z-Logo-svg.png"),
    ("CH15", ("Yes קידס",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708188-46.jpg"),
    ("PT43", ("דיסני",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708116-46.jpg"),
    ("PT59", ("דיסני ג'וניור",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708138-46.jpg"),
    ("NK01", ("ניקולודיון",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708012-46.jpg"),
    ("PT69", ("ניק ג'וניור",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708159-46.jpg"),
    ("TA05", ("ג'וניור",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708057-46.jpg"),
    ("PT85", ("זום",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708165-46.jpg"),
    ("TV24", ("הופ",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707980-46.jpg"),
    ("PT46", ("הופ ילדות ישראלית",), "https://i.ibb.co/7GJgykh/HopLogo.png"),
    ("TA02", ("בייבי",), "https://i.ibb.co/yN2ZSnx/baby.png"),
    ("PT48", ("גים ג'אם",), "https://i.ibb.co/09PtYwf/1459425982-jimjam-logo.jpg"),
    ("PT12", ("אגו",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708002-46.jpg"),
    ("PT29", ("אגו טוטאל",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708107-46.jpg"),
    ("TV17", ("National Geo",), "https://i.ibb.co/qj0FCyB/National-Geographic-Logo.png"),
    ("PT35", ("National Geo Wild",), "https://i.ibb.co/2dbmjjR/nat-geo-wild-logo-featured.jpg"),
    ("TV18", ("Discovery",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708162-46.jpg"),
    ("TV62", ("Discovery Sicence",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708163-46.jpg"),
    ("PT55", ("ערוץ ההיסטוריה",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707963-46.jpg"),
    ("YSAT", ("Yes דוקו", "Yes דוקו [source 2]"), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708157-46.jpg"),
    ("CH61", ("DIY",), "http://allvectorlogo.com/img/2016/07/diy-network-logo.png"),
    ("PT41", ("+בית",), "https://i.ibb.co/R0VzsHx/2708115-46.jpg"),
    ("PT28", ("ערוץ הטיולים",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708106-46.jpg"),
    ("TV09", ("ערוץ החיים הטובים",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707960-46.jpg"),
    ("PT14", ("ערוץ הבריאות",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708025-46.jpg"),
    ("TV10", ("E!",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708058-46.jpg"),
    ("TV67", ("ערוץ 24",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708013-46.jpg"),
    ("TV86", ("Mtv",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708006-46.jpg"),
    ("PT20", ("ערוץ האוכל",), "https://i.ibb.co/KXktNx1/food-channel.jpg"),
    ("TV87", ("CBS reality",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708070-46.jpg"),
    ("TV21", ("ערוץ הקניות",), "https://i.ibb.co/b2HjfxH/buying-channel.jpg"),
    ("TV20", ("ויוה",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/7/2707989-46.jpg"),
    ("PT60", ("+ויוה",), "https://img.wcdn.co.il/f_auto,w_100/2/7/0/8/2708144-46.gif"),
    ("PT30", ("הידברות",), "https://i.ibb.co/t2SXkZf/hidabrot.jpg"),
    ("PT72", ("ים תיכוני",), "https://images.globes.co.il/images/NewGlobes/big_image_800/2018/CD8E9E2CC494CB98C1B4AD8491B9FF50_800x392.20180729T150714.jpg"),
    ("CH17", ("חגיגה מזרחית",), "https://i.ibb.co/Jc9FcPC/hgiga-mizrhit.png"),
]


class YES (base.BASE_EPG):
    def __init__ (self,file_out):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,file_out)
                        
    def _create_date_and_time_ (self, date, the_time):
        the_time = the_time.replace (':','')+'00'
        return date + the_time + ' +0200'

    def _parse_prog_thread_ (self, input_data):

        ind,url = input_data
        vvv = self.session.get (url)    
        data = vvv.json()
        start_data_and_time = self._create_date_and_time_ (data['Fix_Date'], data['Start_Time_Fix'])
        end_data_and_time = self._create_date_and_time_ (data['Fix_Date'], data['End_Time_Fix'])
        
        return (ind , start_data_and_time, end_data_and_time, data['Hebrew_Name'], data['PreviewText'])


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
            
            for result in results:
                prog_data =  result[1:]
                output += self._print_prog (channel_code , *prog_data)
            
            print ('.', end="", flush=True)
            
        print ('')
        return output
                
