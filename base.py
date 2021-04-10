import codecs, time, datetime
import requests
from multiprocessing.pool import ThreadPool,Pool

CHANNELS_DATA = []
THREADS = 10

is_dst = time.daylight and time.localtime().tm_isdst > 0
utc_offset = - (time.altzone if is_dst else time.timezone)
utc_offset=int (utc_offset/3600)

class BASE_EPG ():
    def __init__ (self,base_name,file_out, logger):
        self._base_name = base_name
        self.file_out = file_out
        self.channels = {} 
        self.session = requests.Session()
        self.last_print_prog = None
        self.logger = logger

        for data in CHANNELS_DATA:
            self.add_channel_to_dict (*data)
            
        self._total_channels = len (self.channels)
        self.logger.info ("Init %s with total channels %s" % (self._base_name,self._total_channels))
                        

    def _print_prog (self, channel, start_time, end_time, name, description):
        last_prog_key = (name, start_time)

        if description:
            description = description.replace ('&', 'ו')
        if name:
            name = name.replace ('&', 'ו')
        
        output = []
        if last_prog_key != self.last_print_prog:
        
            start_time_str =  datetime.datetime.strftime (start_time, '%Y%m%d%H%M')  + '00 +0%d00' % (utc_offset)
            end_time_str =  datetime.datetime.strftime (end_time, '%Y%m%d%H%M')  + '00 +0%d00' % (utc_offset)
        
            output.append ('\t<programme start="%s" stop="%s" channel="%s">\n' %(start_time_str, end_time_str, channel))
            output.append  ('\t\t<title lang="he">%s</title>\n'%(name))
            output.append  ('\t\t<desc lang="he">%s</desc>\n'%(description))
            output.append  ('\t</programme>\n')
            
            self.last_print_prog = last_prog_key
                  
        return output

    def print_channels(self,):

        for channel_name in self.channels:
        
            for i in range (len(self.channels[channel_name]['name'])):
            
                if i == 0:
                    channel_id = channel_name
                else:
                    channel_id = str(channel_name) + '_%s' % (i+1)
            
                self.file_out.write('   <channel id="%s">\n' % (channel_id))
                self.file_out.write('     <display-name lang="he">%s</display-name>\n'% (self.channels[channel_name]['name'][i]))
                self.file_out.write('     <icon src="%s" />\n'% (self.channels[channel_name]['logo']))                
                self.file_out.write('   </channel>\n')
    
    
    
    def add_channel_to_dict (self, channel_code, channel_name, logo) :   
    
            self.channels[channel_code] = {'name' : channel_name, 'logo':logo}
           
        
    def print_progs (self,):
         
        tic = time.time()

        results = []

        if 1:
            self.logger.info ('Getting %s channels' % (self._total_channels))
            pool = ThreadPool(THREADS)
            results = pool.map(self._print_channel_progs, self.channels)
            pool.close()
            pool.join()

        else:        
            for ind, channel in enumerate (self.channels):
                self.logger.info ('Getting %s (%s/%s)' % (channel, ind+1, self._total_channels))
                lines = self._print_channel_progs (channel)                
                results.append (lines)
        
        for ind, channel in enumerate (self.channels):
            lines = results[ind]
            for i in range (len (self.channels[channel]['name'])):
                for line in lines:                    
                    if i != 0 and 'channel=' in line:
                        line = line.replace ('channel="%s"'%channel, 'channel="%s_%s"'%(channel,i+1))
                        
                    self.file_out.write (line)
            
        self.logger.info ('Total get time %.2f' % (time.time() - tic))

                
