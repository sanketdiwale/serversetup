# serversetup

simply run main.py as
<pre>python main.py username sitename siteurl</pre>

'username' is the account username under which the server processes are to be run
'sitename' is the name of the root folder under which the django project resides (the root folder name is assumed to be the same as the django project name (name of the directory under which the django project's setting.py exists))
'siteurl' is the url under which the project is to be served in the local development environment (a typical url would look like 'sitex.test')

The main.py

1. adds siteurl as a host pointed to by the local loopback ip 127.0.0.1
2. setups the nginx server configuration with ssl security (http is redirected to https)
3. creates a self-signed-certificate to serve the https traffic
4. sets up gunicorn config and sockets to serve the django project
5. reloads and restarts the nginx and gunicorn processes

The gunicorn sockets and services are given the same name as specified by the 'sitename' argument
