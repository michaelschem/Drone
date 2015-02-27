import re, os, glob

out_num = 0

# read files from directory "Unclean" which is in this python script's root, too
# Ex: Dir/camera_output_cleaner.py and Dir/Unclean/...
for filename in glob.iglob(os.path.join('Unclean','*.txt')):
    with open(filename,'r') as f:
        # open file as read only
        camera_data_text = f.read()
        # open file as write only
        out_num+=1
        # output cleaned files to this directory
        out_file = 'Clean/clean2_'+str(out_num)+'.bin'
        cleaned_data_output = open(out_file,'wb')

        # replace V2 with space
        regex = re.compile('[Vv][2]')
        camera_data_text = regex.sub(' ',camera_data_text)

        # remove other strings that are longer than 2 chars
        regex = re.compile('\S{3,}')
        camera_data_text = regex.sub('',camera_data_text,4)

        # remove spaces
        regex = re.compile(' +')
        camera_data_text = regex.sub('',camera_data_text)

        # remove any strings that clearly aren't hex
        regex = re.compile('[^ABCDEF\s\d]\d{0,}')
        camera_data_text = regex.sub('',camera_data_text)

        # remove any 1-2char strings left alone on their own lines
        regex = re.compile('\n[\w\d]{1,2}\n')
        camera_data_text = regex.sub('',camera_data_text)

        # # remove all empty lines followed by another empty line
        regex = re.compile('\n(?=\n)')
        camera_data_text = regex.sub('',camera_data_text)

        # # reinsert spaces to show each byte
        # camera_data_text = re.sub('([\d\w]{2})','\\1 ',camera_data_text)

        # # reinsert extra new lines between lines
        # camera_data_text = re.sub('(\n)','\\1\n',camera_data_text)

        # convert to actual hex
        # def string_to_hex(string_hex):
        #     hex_string = hex(0)
        #     for char in string_hex:
        #         if char is 'A':
        #             hex_string = hex(10)
        #             cleaned_data_output.write(hex_string.encode('utf-8'))
        #         elif char is 'B':
        #             hex_string = hex(11)
        #             cleaned_data_output.write(hex_string.encode('utf-8'))
        #         elif char is 'C':
        #             hex_string = hex(12)
        #             cleaned_data_output.write(hex_string.encode('utf-8'))
        #         elif char is 'D':
        #             hex_string = hex(13)
        #             cleaned_data_output.write(hex_string.encode('utf-8'))
        #         elif char is 'E':
        #             hex_string = hex(14)
        #             cleaned_data_output.write(hex_string.encode('utf-8'))
        #         elif char is 'F':
        #             hex_string = hex(15)
        #             cleaned_data_output.write(hex_string.encode('utf-8'))
        #         elif char is not '\n':
        #             hex_string = hex(int(ord(char)))
        #             cleaned_data_output.write(hex_string.encode('utf-8'))
        #         else:
        #             newline = '\n'
        #             cleaned_data_output.write(newline.encode('utf-8'))

        # string_to_hex(camera_data_text)
        cleaned_data_output.write(camera_data_text.encode('utf-8'))

