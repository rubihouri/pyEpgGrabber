import codecs, time
import requests

CHANNELS_DATA = []

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
        
        output = []
        if 1 or last_prog_key != self.last_print_prog:
        
            output.append ('\t<programme start="%s" stop="%s" channel="%s">\n' %(start_time, end_time, channel))
            output.append  ('\t\t<title>%s</title>\n'%(name))
            output.append  ('\t\t<desc>%s</desc>\n'%(description))
            output.append  ('\t</programme>\n')
            
            self.last_print_prog = last_prog_key
                  
        return output

    def print_channels(self,):

        for channel_name in self.channels:

            self.file_out.write('   <channel id="%s">\n' % (channel_name))
            for i in range (len(self.channels[channel_name]['name'])):        
                self.file_out.write('     <display-name>%s</display-name>\n'% (self.channels[channel_name]['name'][i]))
            self.file_out.write('     <icon src="%s" />\n'% (self.channels[channel_name]['logo']))                
            self.file_out.write('   </channel>\n')
    
    
    def add_channel_to_dict (self, channel_code, channel_name, logo) :   
    
            self.channels[channel_code] = {'name' : channel_name, 'logo':logo}
           
        
    def print_progs (self,):
   
        tic = time.time()
        for ind, channel in enumerate (self.channels):
            self.logger.info ('Getting %s (%s/%s)' % (channel, ind+1, self._total_channels))
            lines = self._print_channel_progs (channel)
            
            for line in lines:                    
                self.file_out.write (line)
                
            if 0:
                for i in range (len (self.channels[channel]['name'])):
                    for line in lines:                    
                        if i != 0 and 'channel=' in line:
                            line = line.replace ('channel="%s"'%channel, 'channel="%s_%s"'%(channel,i+1))
                            
                        self.file_out.write (line)
                
        self.logger.info ('Total get time %.2f' % (time.time() - tic))
            

                
