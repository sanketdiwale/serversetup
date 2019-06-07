import argparse
import getpass 
import os
import json

parser = argparse.ArgumentParser(description='Process some strings')
parser.add_argument('User',metavar='User',type=str,help='provide username under whose homefolder the project files are stored')
parser.add_argument('Sitename',metavar='Sitename',type=str,help='provide foldername under which the project files are stored')
parser.add_argument('Port',metavar='Port',type=str,help='provide port under which the gunicorn serves the file')
args = parser.parse_args()

with open('sites.json','r') as f:
    data = json.load(f)
    if args.Port in data.keys():
        if not (data[args.Port]==args.Sitename):
            print(data)
            print('Port already in use by another site, please specify an unused port')
            exit()

with open("gunicorn_service_template.txt", "r") as f:
    template = f.read()

t1 = template.replace('sitex',args.Sitename)
t1 = t1.replace('yourUsername',args.User)


with open('/etc/systemd/system/'+args.Sitename+'.service','w') as f:
    f.write(t1)

print('Created file: /etc/systemd/system/'+args.Sitename+'.service'+' with contents')
print(t1)

with open("gunicorn_socket_template.txt", "r") as f:
    template = f.read()

t1 = template.replace('sitex',args.Sitename)
t1 = t1.replace('yourUsername',args.User)


with open('/etc/systemd/system/'+args.Sitename+'.socket','w') as f:
    f.write(t1)

print('Created file: /etc/systemd/system/'+args.Sitename+'.socket'+' with contents')
print(t1)

# add the gunicorn config
os.system('mkdir -p /home/'+args.User+'/.'+args.Sitename)
with open('gunicorn_config_template.txt','r') as f:
    template = f.read()
t1 = template.replace('sitex',args.Sitename)
t1 = t1.replace('yourUsername',args.User)

t1 = t1.replace('PORT',args.Port)

with open('/home/'+args.User+'/.'+args.Sitename+'/gunicorn_config.py','w') as f:
    f.write(t1)

print('wrote gunicorn config to '+'/home/'+args.User+'/.'+args.Sitename+'/gunicorn_config.py')
data[args.Port]=args.Sitename
with open('sites.json','w') as f:
    json.dump(data,f)