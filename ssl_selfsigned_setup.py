import argparse
import getpass 
import os

parser = argparse.ArgumentParser(description='Process some strings')
parser.add_argument('Sitename',metavar='Sitename',type=str,help='provide foldername under which the project files are stored')
parser.add_argument('URL',metavar='URL',type=str,help='provide url under the site is served by nginx')
args = parser.parse_args()


with open("ssl_conf_selfsigned_template.txt", "r") as f:
    template = f.read()


t1 = template.replace('sitex',args.Sitename)
t1 = t1.replace('URL',args.URL)
def writeFile(string,filelocation,filename):
    with open(filelocation+filename,'w') as f:
        f.write(string)
    print('Created file: '+filelocation+filename+' with contents')
    print(string)

writeFile(t1,'/etc/ssl/',args.Sitename+'.conf')

os.system('sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/'+args.Sitename+'.key -out /etc/ssl/certs/'+args.Sitename+'.crt -config /etc/ssl/'+args.Sitename+'.conf')

with open("/etc/nginx/sites-available/"+args.Sitename, "r") as f:
    siteconfig = f.read()

t1 = siteconfig.replace('#ssl_certificate','ssl_certificate')
t1 = t1.replace('#ssl_certificate_key','ssl_certificate_key')
t1 = t1.replace('#ssl_protocols','ssl_protocols')

writeFile(t1,'/etc/nginx/sites-available/',args.Sitename)

print('Updated nginx config with ssl info, remember to reload the service with:')
print('sudo service nginx reload')