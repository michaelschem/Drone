"""Cleans the weird camera output files we keep getting"""

import re, os, glob

__out_num__ = 0

# read files from directory "Unclean" which is in this python script's root, too
# Ex: Dir/camera_output_cleaner.py and Dir/Unclean/...
for filename in glob.iglob(os.path.join('Unclean', '*.txt')):
    with open(filename, 'r') as f:
        # open file as read only
        camera_data_text = f.read()
        # open file as write only
        __out_num__ += 1
        # output cleaned files to this directory
        out_file = 'Clean/clean2_'+str(__out_num__)+'.txt'
        cleaned_data_output = open(out_file, 'w')

        # replace V2 with space
        regex = re.compile('[Vv]')
        camera_data_text = regex.sub(' ', camera_data_text)

        # remove any strings that clearly aren't hex
        regex = re.compile('[^ABCDEF\d\n]{0,}')
        camera_data_text = regex.sub('', camera_data_text)

        # remove all other random characters
        regex = re.compile('([ABCDEF\d]{113})')
        newlist = re.findall(regex,camera_data_text)

        # # reinsert spaces to show each byte
        # camera_data_text = re.sub('([\d\w]{2})','\\1 ',camera_data_text)

        # string_to_hex(camera_data_text)
        for item in newlist:
            print item
            cleaned_data_output.write(item)

