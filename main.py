import argparse
import getpass 
import os
import subprocess
import json
from IPython import embed
parser = argparse.ArgumentParser(description='Process some strings')
parser.add_argument('User',metavar='User',type=str,help='provide username under whose homefolder the project files are stored')
parser.add_argument('Sitename',metavar='Sitename',type=str,help='provide foldername under which the project files are stored')
parser.add_argument('SiteURL',metavar='URL',type=str,help='provide URL under which the site is to be served')
args = parser.parse_args()

# add site to /etc/hosts
# requires once, execution of chmod +x manage_localhosts.sh
os.system('. ./manage_localhosts.sh && addhost '+args.SiteURL)
embed()
# setup nginx config
os.system('sudo python nginx_setup.py '+args.User+' '+args.Sitename+' '+args.SiteURL)
print('nginx setup complete')
# setup gunicorn
with open('sites.json','r') as f:
    data = json.load(f)
    ports = list(map(int,data.keys()))
    port = max(max(ports)+1,8001)
os.system('sudo python gunicorn_setup.py '+args.User+' '+args.Sitename+' '+str(port))
print('gunicorn setup complete')
# setup ssl
os.system('sudo python ssl_selfsigned_setup.py '+args.Sitename+' '+args.SiteURL)

# reload and restart the services
# start the gunicorn service as a daemon
os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl start '+args.Sitename+'.socket')
os.system('sudo systemctl enable '+args.Sitename+'.socket')
os.system('sudo systemctl daemon-reload')

# enable site and restart nginx
os.system('sudo nginx_ensite '+args.Sitename)
os.system('sudo service nginx reload')
os.system('sudo service nginx restart')
os.system('sudo service '+args.Sitename+' restart')
print('server for site '+args.Sitename+' is up and running. Visit the site at: '+args.SiteURL)