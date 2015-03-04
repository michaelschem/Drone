"""Cleans the weird camera output files we keep getting and converts to hex"""

import re, os, glob, array

__out_num__ = 0

# convert to actual hex
def string_to_hex(string_hex):

    hex_string = string_hex.decode('hex')
    hex_string = array.array('B', hex_string)
    cleaned_data_output.write(hex_string)

# read files from directory "Unclean" which is in this python script's root, too
# Ex: Dir/camera_output_cleaner.py and Dir/Unclean/...
for filename in glob.iglob(os.path.join('Unclean', '*.txt')):
    with open(filename, 'rb') as f:
        # open file as read only
        camera_data_text = f.read()
        print filename
        # open file as write only
        __out_num__ += 1
        # output cleaned files to this directory
        out_file = 'Clean/clean2_'+str(__out_num__)+'.bin'
        cleaned_data_output = open(out_file, 'wb')

        # remove any strings that clearly aren't hex
        regex = re.compile('[^ABCDEF0123456789\n]{0,}')
        camera_data_text = regex.sub('', camera_data_text)

        # remove all other random characters
        regex = re.compile('([ABCDEF\d]{112})')
        newlist = re.findall(regex,camera_data_text)

        for item in newlist:
            item = string_to_hex(item)

