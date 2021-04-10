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
    ("TR01", ("ONE 1", "ONE 1 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/one.jpg"),
    ("CH58", ("ONE 2", "ONE 2 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/one2.png"),
    ("PT53", ("Sport1", "Sport1 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/sport1.png"),
    ("PT98", ("Sport2", "Sport2 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/sport2.png"),
    ("CH09", ("Sport3", "Sport3 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/sport3.png"),
    ("CH11", ("Sport4", "Sport4 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/sport4.png"),
    ("PT26", ("Sport 5", "Sport 5 [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_sport.png"),
    ("CH54", ("Sport 5+", "Sport 5+ [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_plus.png"),
    ("PT62", ("Sport 5 Live",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_live.png"),
    ("CH56", ("Sport 5 Stars", "Sport 5 Stars [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_stars.png"),
    ("MU03", ("Sport 5 Gold",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_gold.png"),
    ("CH55", ("Sport 5 4K",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/5_4K.png"),
    ("YESV", ("Yes TV Action", "Yes TV Action [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_tv_action.jpg"),
    ("YESP", ("Yes TV Comedy", "Yes TV Comedy [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_tv_comedy.jpg"),
    ("YESU", ("Yes TV Drama", "Yes TV Drama [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_tv_drama.jpg"),
    ("YSAU", ("Yes ישראלי", "Yes ישראלי [source 2]"), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/yes_israeli.jpg"),
    ("CH13", ("Wiz",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/wiz.png"),
    ("PT91", ("דיסני",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/disney.png"),
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
    ("PT25", ("National Geo",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nat_geo.png"),
    ("CH71", ("National Geo Wild",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nat_geo_wild.jpg"),
    ("PT94", ("Discovery",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/discovery.png"),
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
    ("TV87", ("CBS Reality",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/cbs_real.png"),
    ("TV21", ("ערוץ הקניות",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/buying_channel.png"),    
    ("TV20", ("ויוה",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/viva.png"),
    ("PT60", ("ויוה+",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/viva_plus.png"),
    ("PT30", ("הידברות",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hidabrot.png"),
    ("PT72", ("ים תיכוני",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/channel_25.png"),
    ("CH17", ("חגיגה מזרחית",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/hgiga-mizrhit.png"),
    ("CH18", ("ניק Teen",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/nick_teen.png"),
    ("TV61", ("Animal Planet",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/animal_planet.png"),		
    ("PT39", ("Euro Sport",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/eurosport.png"),
    ("CH33", ("Euro Sport 2",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/eurosport2.png"),
    ("TV37", ("VH1",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/vh1.png"),	
    ("CH65", ("ערוץ ההומור",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/humor.png"),
    ("CH70", ("ערוץ הדרמות הטורקיות",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/turki_drama.png"),	
    ("CH72", ("ערוץ הריאליטי",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/reality.png"),	
    ("CH19", ("ערוץ הכוכבים",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/kids_star.jpg"),	
    ("CH21", ("ONE 4K", ), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/one_4k.png"),
    ("CH43", ("TLC", ), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/tlc.png"),
    ("PT31", ("Club MTV",), "https://raw.githubusercontent.com/rubihouri/pyEpgGrabber/master/images/mtv_dance.png"),    
]



class YES (base.BASE_EPG):
    def __init__ (self,file_out, big_guide, logger):
        base.CHANNELS_DATA = CHANNELS_DATA
        base.BASE_EPG.__init__ (self,'YES', file_out, logger)

        global DAYS_TO_SAVE
        if big_guide:        
            DAYS_TO_SAVE = 7
        else:
            DAYS_TO_SAVE = 3
        
        self.logger.info ('Init Yes with total get time of %d days' % (DAYS_TO_SAVE))

        self.session = requests.Session()
        full_str = self.session.get ("https://www.yes.co.il/content/tvguide")        
        self.session.cookies.clear()

        channels = self.session.post ("https://www.yes.co.il/o/yes/servletlinearsched/getchannels", data={"p_auth": '1111'})
        
        full_str = self.session.get ("https://www.yes.co.il/content/tvguide")
        self.p_auth = full_str.text.split ('authToken')[1].split(';')[0].split('=')[1].replace ('"', '')
        
        if 0:
            channels = self.session.post ("https://www.yes.co.il/o/yes/servletlinearsched/getchannels", data={"p_auth": self.p_auth})
            channels.json()['list']
        
        '''[('YSA1', 'yes MOVIES DRAMA'), ('YSA2', 'yes MOVIES ACTION'), ('YSA3', 'yes MOVIES COMEDY'), ('YSAU', 'yes קולנוע ישראלי'), 
        ('YESU', 'yes TV DRAMA'), ('YESV', 'yes TV ACTION'), ('YESP', 'yes TV COMEDY'), ('YSAT', 'yes דוקו'), ('TV50', 'ישראל פלוס'), 
        ('CH70', 'ערוץ הדרמות הטורקיות+'), ('CH30', 'כאן 11'), ('CH34', 'קשת'), ('CH36', 'רשת'), ('CH65', 'ערוץ ההומור'),
        ('CH80', 'ערוץ הדרמות הטורקיות 2'), ('CH77', 'ערוץ הסרטים הטורקיים'), ('CH81', 'ערוץ השעשועונים'), ('CH72', 'ערוץ הריאליטי'), 
        ('PT92', 'ערוץ 20'), ('TV21', 'ערוץ הקניות'), ('CH75', "ויוה וינטג'"), ('TV67', 'ערוץ 24 החדש'), ('PT72', 'ים תיכוני'), 
        ('CH79', 'ערוץ האח הגדול'), ('PT28', 'ערוץ הטיולים'), ('PT20', 'ערוץ האוכל'), ('PT14', 'ערוץ בריאות'), ('PT63', 'Hala TV'),
        ('TV09', 'החיים הטובים'), ('PT41', 'בית+'), ('CH32', 'מכאן'), ('CH61', 'DIY'), ('TV20', 'ויוה'), ('PT60', 'ויוה+'),
        ('TV10', 'E!'), ('CH62', 'ערוץ האופנה הישראלי'), ('CH86', 'ערוץ קומדי בר'), ('PT94', 'דיסקברי HD'), ('PT25', 'National Geographic'),
        ('TV62', 'Discovery Science'), ('CH71', 'NG WILD'), ('TV19', 'ערוץ ההיסטוריה'), ('PT55', 'היסטוריה HD'), ('TV61', 'Animal Planet'), 
        ('PT13', 'Daystar'), ('CH58', 'ONE2'), ('TR01', 'ONE'), ('PT53', 'ספורט 1 HD'), ('PT98', 'ספורט 2 HD'), ('CH09', 'ספורט 3 HD'), 
        ('CH11', 'ספורט 4 HD'), ('PT26', '5sport HD'), ('CH54', '5PLUS HD'), ('MU03', '5GOLD'), ('PT62', '5LIVE HD'), ('CH56', '5STARS'),
        ('CH55', '5SPORT 4K'), ('PT39', 'EUROSPORT'), ('CH33', 'EUROSPORT 2'), ('PT22', 'ספורט 1 SD'), ('TV87', 'CBS reality'), ('PT12', 'ערוץ אגו'),
        ('CH85', 'MUTV'), ('PT86', 'TRACE ספורט'), ('TV34', 'FTV'), ('CH41', 'CLASSICA'), ('PT31', 'Club MTV'), ('TV37', 'VH1'),
        ('TV51', 'MTV 80s'), ('TV35', 'MTV'), ('PT50', 'MTV HD'), ('TV86', 'MTV MUSIC'), ('CH43', 'TLC'), ('CH17', 'חגיגה מזרחית'),
        ('CH57', 'ערוץ 23 חינוכית'), ('TA02', 'בייבי'), ('TV24', 'הופ!'), ('PT46', 'ילדות ישראלית'), ('PT59', "דיסני ג'וניור"), 
        ('PT69', "ניק ג'וניור"), ('CH19', 'ערוץ הכוכבים'), ('YSA4', 'yes MOVIES KIDS'), ('PT91', 'דיסני HD'), ('PT85', 'Zoom'), 
        ('NK01', 'ניקלודיאון'), ('CH13', 'ערוץ WiZ'), ('TA05', "ג'וניור"), ('CH18', 'Teennick'), ('PT48', 'Jim Jam'), 
        ('PT30', 'ערוץ הידברות'), ('TV43', 'ערוץ 98'), ('TV89', 'ערוץ הכנסת'), ('TV12', 'CNN'), ('TV42', 'SKY NEWS'), 
        ('PT18', 'FRANCE 24'), ('TV13', 'FOX NEWS'), ('TV59', 'בלומברג'), ('PT17', 'ALJAZEERA ENGLISH'), ('TV02', 'METV'),
        ('PT06', 'CCTV NEWS'), ('CH50', 'CGTN DOCUMENTARY'), ('PT44', 'NHK WORLD TV'), ('PT02', 'yesBollywood'), ('CH68', 'BollyShow'), 
        ('PT29', 'אגו טוטאל'), ('TV44', 'RTL'), ('TV46', 'גרמניה SAT3'), ('TV45', 'גרמניה SAT1'), ('TV79', 'GTV'), ('TV49', 'TVE'), 
        ('PT11', 'TVR international'), ('TV57', 'PROTV INTERNATIONAL'), ('TV98', 'ZEE TV'), ('PT64', 'Mediaset'), ('CH74', 'FRANCE 3'), 
        ('TV94', 'FRANCE2'), ('TV47', 'ARTE'), ('TV56', 'Eurostar'), ('TV77', 'RTM'), ('PT19', 'I.E.T.V.'), ('CH87', 'ROTANA CINEMA'), 
        ('TV71', 'LBC'), ('TV73', 'ROTANA'), ('TV76', 'אלגאזירה'), ('TV81', 'CHANNEL 1 RUS'), ('TV82', 'RTR PLANETA'), ('TV83', 'RTV INTERNATIONAL'),
        ('TV85', 'NASHE KINO'), ('CH24', 'REN TV'), ('PT73', 'Vremya'), ('PT74', 'Telecafe'), ('CH76', 'BOBER'), ('CH23', 'Current Time'),
        ('CH04', 'ערוץ TNT'), ('TV60', 'NTV MIR'), ('PT90', 'TV1000 Russian Kino'), ('PT45', 'TVCI'), ('PT15', '1+1'), ('PT36', 'DOM KINO'), 
        ('CH27', 'Investigation Discovery'), ('CH29', 'SHANSON TV'), ('TV65', 'Russian Music Box'), ('PT61', 'CAROUSEL'), ('PT83', 'Jim Jam RUS'),
        ('CH21', 'ONE 4K'), ('TV64', 'Touch'), ('PT05', 'blue HUSTLER')]'''     
        
        self.cache = {}

        for day_value in range (DAYS_TO_SAVE):
            self.get_day_cache(day_value)
            

    def _parse_prog_thread_ (self, input_data):

        ind,url, session = input_data
        progs_data = session.get (url)    
        data = progs_data.json()
        
        
        start_time = datetime.datetime.fromtimestamp (eval (data['Start_Time_Fix_DateTime'][6:-2])/1000)
        end_time = datetime.datetime.fromtimestamp (eval (data['End_Time_Fix_DateTime'][6:-2])/1000)
        
        if start_time > end_time:
            end_time = end_time + datetime.timedelta(days=1)
                               
        return (ind , start_time, end_time, data['Hebrew_Name'], data['PreviewText'])


    def get_day_cache (self, day_value):
            
        now_time = datetime.datetime.now()
        time_to_take = datetime.timedelta(days=day_value) + now_time
        timestr = str (time_to_take.year) + str(time_to_take.month).zfill(2) + str (time_to_take.day).zfill(2)        
        response = self.session.post ("https://www.yes.co.il/o/yes/servletlinearsched/getscheduale", data={"p_auth": self.p_auth, 'startdate':timestr})
        
        self.cache[day_value] = {}
        
        for prog in response.json()['list']:        
            channel_id = prog['channelID']
            if channel_id not in self.cache[day_value]:
                self.cache[day_value][channel_id] = []

            start_date = prog['startDate'][:10]
            
            start_time = datetime.datetime.strptime (start_date + ' ' + prog['startTime'], '%Y-%m-%d %H:%M:%S')
            tokens = prog['broadcastItemDuration'].split(':')
            end_time = start_time + datetime.timedelta(hours=int(tokens[0]), minutes=int(tokens[1]), seconds=int(tokens[2]))                
            self.cache[day_value][channel_id].append (
                [start_time, end_time, prog['scheduleItemName'], prog['scheduleItemSynopsis']]
            )
    
                        
    def _print_channel_progs (self, channel_code):
    
        output = []
                
        for day_value in range (DAYS_TO_SAVE):
        
            if channel_code in self.cache[day_value]:        
                results = self.cache[day_value][channel_code]
                total_results = len (results)
                for ind, prog_data in enumerate(self.cache[day_value][channel_code]):

                    if ind + 1 < total_results:
                        # current end not equal to next show start
                        if prog_data[1] != results[ind+1][0]:
                            prog_data[1] = results[ind+1][0]
                    
                    output += self._print_prog (channel_code , *prog_data)
            else:
                # Some channels doen't have full EPG      
                if day_value < 3:
                    self.logger.error ('Missing channel %s (%s)' % (channel_code, day_value))

        self.logger.info ("Done %s [%s]" % (self.channels[channel_code]['name'][0].encode('utf-16'), channel_code))
            
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