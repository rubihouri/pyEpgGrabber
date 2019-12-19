import requests
import codecs, os, time, shutil
import yes


file_path = os.path.dirname (os.path.realpath (__file__))
os.chdir (file_path)


def print_header (file_out):    
  
    file_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_out.write('<tv generator-info-name="WebGrab+Plus/w MDB &amp; REX Postprocess -- version V2.1.5 -- Jan van Straaten" generator-info-url="http://www.webgrabplus.com">\n')
        

def close_header(file_out,):
    file_out.write('</tv>\n')



if __name__ == "__main__":

    tic = time.time()
    filename = os.path.join ('output', 'guide.xml')
    file_out = codecs.open(filename, 'w', encoding='utf8')  
    
    yes_handle = yes.YES(file_out)    
    
    
    # XML Start
    print_header (file_out)
                
    # Print Channels Area
    yes_handle.print_channels ()
    
    # Print Prog area
    yes_handle.print_progs ()
        
    # XML Close
    close_header (file_out)

    print ('Total create time %d'  % (time.time () - tic))

    shutil.copyfile(filename,os.path.join(r'c:\Users\Rubi\Dropbox\epg','guide.xml'))

