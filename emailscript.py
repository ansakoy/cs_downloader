from csdbot_token import EMAIL_DATA
import launch
from sys import argv
import json
import os

# BASH SCRIPT FIELDS
SMTPFROM = "SMTPFROM"
SMTPTO = "SMTPTO"
SMTPSERVER = "SMTPSERVER"
SMTPUSER = "SMTPUSER"
SMTPPASS = "SMTPPASS"
MESSAGEBODY = "MESSAGEBODY"
SUBJECT = "SUBJECT"
ATTACHMENT = "ATTCHMENT"


# USER_DATA FIELDS
MODE_CHOICE = 'mode_choice'
TASK = 'task'
EXT = 'ext'
SPAN = 'span'
DEMO = 'demo'
UPLOAD = 'upload'
LAUNCH = 'launch'
LAUNCH_TEXT = 'launch_text'
PARAMS_TEXT = 'params_text'
FNAME = 'fname'
OUTF = 'outf'
EXTENSION = 'extension'
PARAMS_SOURCE = 'params_source'
EMAIL = 'email'



def load_json(source):
    with open(source, 'r') as handler:
        return json.load(handler)


def write_emailscript(usrdata, msg):
    if usrdata.get(FNAME):
        f_path = os.path.join(os.path.join(os.getcwd(), 'data', usrdata[FNAME] + usrdata[EXTENSION])
    text = "#!/bin/bash"
    text += '\n{}="{}"'.format(SMTPFROM, EMAIL_DATA[SMTPFROM])
    text += "\n{}={}".format(SMTPTO, usrdata[EMAIL])
    text += "\n{}={}".format(SMTPSERVER, EMAIL_DATA[SMTPSERVER])
    text += "\n{}={}".format(SMTPUSER, EMAIL_DATA[SMTPUSER])
    text += '\n{}="{}"'.format(SMTPPASS, EMAIL_DATA[SMTPPASS])
    text += '\n{}="{}"'.format(MESSAGEBODY, msg)
    text += '\n{}="{}"'.format(SUBJECT, '[CSDownloader] Результат запроса')
    if usrdata.get(FNAME):
        text +=' \n{}="{}"'.format(ATTACHMENT, f_path)
        # text += "\nsendEmail -f $SMTPFROM -t $SMTPTO -u $SUBJECT -o message-file={} -s $SMTPSERVER -xu $SMTPUSER -xp $SMTPPASS -a $ATTACHMENT".format(msg_file)
        text += "\nsendEmail -f $SMTPFROM -t $SMTPTO -u $SUBJECT -m $MESSAGEBODY -s $SMTPSERVER -xu $SMTPUSER -xp $SMTPPASS -a $ATTACHMENT"
    else:
        # text += "\nsendEmail -f $SMTPFROM -t $SMTPTO -u $SUBJECT -o message-file={} -s $SMTPSERVER -xu $SMTPUSER -xp $SMTPPASS".format(msg_file)
        text += "\nsendEmail -f $SMTPFROM -t $SMTPTO -u $SUBJECT -m $MESSAGEBODY -s $SMTPSERVER -xu $SMTPUSER -xp $SMTPPASS"
    with open('emailbashscript', 'w') as handler:
        handler.write(text)



def process_usr_query(source):
    user_data = load_json(source)
    result = launch.launch(source=user_data.get(PARAMS_SOURCE),
                    task=user_data[TASK],
                    out_format=user_data.get(OUTF, 'CSV'),
                    span=user_data.get(SPAN, 30),
                    out_name=user_data.get(FNAME),
                    demo=user_data[DEMO])
    msg = user_data[LAUNCH_TEXT] + '\n\n' + user_data[PARAMS_TEXT] + '\n\n' + result
    # msg_file = '{}.txt'.format(user_data[USRID])
    # with open(msg_file, 'w') as handler:
    #     handler.write(msg)
    # write_emailscript(user_data, msg_file)
    write_emailscript(user_data, msg)
    os.system('chmod +x emailbashscript')
    os.system('./emailbashscript')
    # os.remove(msg_file)
    if user_data.get(FNAME):
        f_path = os.path.join('data', user_data[FNAME] + user_data[EXTENSION])
        os.remove(f_path)
    if user_data.get(PARAMS_SOURCE):
        os.remove(user_data[PARAMS_SOURCE])
    os.remove(source)


if __name__ == '__main__':
    process_usr_query(argv[1])
