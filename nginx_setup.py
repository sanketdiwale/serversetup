import argparse
import getpass 

parser = argparse.ArgumentParser(description='Process some strings')
parser.add_argument('User',metavar='User',type=str,help='provide username under whose homefolder the project files are stored')
parser.add_argument('Sitename',metavar='Sitename',type=str,help='provide foldername under which the project files are stored')
parser.add_argument('SiteURL',metavar='URL',type=str,help='provide URL under which the site is to be served')
args = parser.parse_args()


with open("nginx_template.txt", "r") as f:
    template = f.read()


t1 = template.replace('sitex',args.Sitename)
t1 = t1.replace('yourUsername',args.User)
t1 = t1.replace('siteurl',args.SiteURL)


with open('/etc/nginx/sites-available/'+args.Sitename,'w') as f:
    f.write(t1)

print('Created file: /etc/nginx/sites-available/'+args.Sitename+' with contents')
print(t1)