from csdbot_token import EMAIL_DATA
import launch

SMTPFROM = "SMTPFROM"
SMTPTO = "SMTPTO"
SMTPSERVER = "SMTPSERVER"
SMTPUSER = "SMTPUSER"
SMTPPASS = "SMTPPASS"
MESSAGEBODY = "MESSAGEBODY"
SUBJECT = "SUBJECT"
ATTACHMENT = "ATTCHMENT"


def load_json(source):
    with open(source, 'r') as handler:
        return json.load(handler)


def write_emailscript(smtpto, usrdata):
    f_path = os.path.join('data', usrdata['fname'] + user_data['extension'])
    text = "#!/bin/bash"
    text += "\n{}={}".format(SMTPFROM, EMAIL_DATA[SMTPFROM])
    text += "\n{}={}".format(SMTPTO, usrdata['email'])
    text += "\n{}={}".format(SMTPSERVER, EMAIL_DATA[SMTPSERVER])
    text += "\n{}={}".format(SMTPUSER, EMAIL_DATA[SMTPUSER])
    text += "\n{}={}".format(SMTPPASS, EMAIL_DATA[SMTPPASS])
    text += "\n{}={}".format(MESSAGEBODY, usrdata['launch_text'] + '\n' + usrdata['params_text'])
    text += "\n{}={}".format(SUBJECT, '[CSDownloader] Результат запроса')
    if usrdata.get('fname'):
        text += "\n{}={}".format(ATTACHMENT, f_path)
        text += "\nsendEmail -f $SMTPFROM -t $SMTPTO -u $SUBJECT -m $MESSAGEBODY -s $SMTPSERVER -xu $SMTPUSER -xp $SMTPPASS -a $ATTACHMENT"
    else:
        text += "\nsendEmail -f $SMTPFROM -t $SMTPTO -u $SUBJECT -m $MESSAGEBODY -s $SMTPSERVER -xu $SMTPUSER -xp $SMTPPASS -a"


def process_usr_query(source):
    usrdata = load_json(source)
    result = launch.launch(source=user_data.get(PARAMS_SOURCE),
                    task=user_data[TASK],
                    out_format=user_data.get(OUTF, 'CSV'),
                    span=user_data.get(SPAN, 30),
                    out_name=user_data.get(FNAME),
                    demo=user_data[DEMO])
    if user_data.get(FNAME):
        f_path = os.path.join('data', user_data[FNAME] + user_data[EXTENSION])
        bot.send_document(chat_id=chat_id, document=open(f_path, 'rb'))
        os.remove(f_path)
    if user_data.get(PARAMS_SOURCE):
        os.remove(user_data[PARAMS_SOURCE])




if __name__ == '__main__':
    process_usr_query(argv[1])
