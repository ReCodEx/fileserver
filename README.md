# ReCodEx fileserver
[![Build 
Status](https://img.shields.io/travis/ReCodEx/fileserver/master.svg?label=Build%20status)](https://travis-ci.org/ReCodEx/fileserver)
[![Wiki](https://img.shields.io/badge/docs-wiki-orange.svg)](https://github.com/ReCodEx/wiki/wiki)
[![GitHub release](https://img.shields.io/github/release/recodex/fileserver.svg)](https://github.com/ReCodEx/wiki/wiki/Changelog)

The fileserver component provides a shared file storage between the frontend and
the backend. It is written in Python 3 using Flask web framework. Fileserver
stores files in configurable filesystem directory, provides file deduplication
and HTTP access. To keep the stored data safe, the fileserver should not be
visible from public internet. Instead, it should be accessed indirectly through
the REST API.

## Installation

### COPR Installation

The RPM packages available for CentOS and Fedora will install recodex-fileserver
into `/opt` directory and update Apache configuration to deploy the fileserver
as `mod_wsgi` service. The actual working directory will be in `/var/recodex-fileserver`.

```
# dnf install yum-plugin-copr
# dnf copr enable semai/ReCodEx
# dnf install recodex-fileserver
```

After installation you should check the Apache configuration and possibly update
it (e.g., change the port on which the service is running). It is **strongly
recommended** to change the HTTP authentication credentials, which are stored in
`/etc/httpd/recodex_htpasswd` (use Apache `htpasswd` CLI tool).

Finally, you need to restart HTTP service.
```
# systemctl restart httpd
```


### Manual Installation

To install and use the fileserver, it is necessary to have Python3 with `pip`
package manager installed. It is needed to install the dependencies. From
clonned repository run the following command:

```
$ pip install -r requirements.txt
```

That is it. Fileserver does not need any special installation. It is possible to
build and install _rpm_ package or install it without packaging the same way as
monitor, but it is only optional. The installation would provide you with script
`recodex-fileserver` in you `PATH`. No systemd unit files are provided, because
of the configuration and usage of fileserver component is much different to our
other Python parts.

#### Usage

There are several ways of running the ReCodEx fileserver. We will cover three 
typical use cases.

##### Running in development mode

For simple development usage, it is possible to run the fileserver in the
command line. Allowed options are described below.

```
usage: fileserver.py {runserver,shell} [--directory WORKING_DIRECTORY] ...
```

- **runserver** argument starts the Flask development server (i.e. `app.run()`).
  As additional argument can be given a port number.
- **shell** argument instructs Flask to run a Python shell inside application
  context.

Simple development server can be run as

```
$ python3 fileserver.py runserver
```

When run like this command, the fileserver creates a temporary directory where
it stores all the files and which is deleted when it exits.

##### Running as WSGI script in a web server

If you need features such as HTTP authentication (recommended) or efficient
serving of static files, it is recommended to run the app in a full-fledged web
server (such as Apache or Nginx) using WSGI. Apache configuration can be
generated by `mkconfig.py` script from the repository.

```
usage: mkconfig.py apache [-h] [--port PORT] --working-directory
                          WORKING_DIRECTORY [--htpasswd HTPASSWD]
                          [--user USER]
```

- **port** -- port where the fileserver should listen
- **working_directory** -- directory where the files should be stored
- **htpasswd** -- path to user file for HTTP Basic Authentication
- **user** -- user under which the server should be run

##### Running using uWSGI

Another option is to run fileserver as a standalone app via uWSGI service. Setup
is also quite simple, configuration file can be also generated by `mkconfig.py`
script.

1. (Optional) Create a user for running the fileserver
2. Make sure that your user can access your clone of the repository
3. Run `mkconfig.py` script.
	```
	usage: mkconfig.py uwsgi [-h] [--user USER] [--port PORT]
	                         [--socket SOCKET]
                             --working-directory WORKING_DIRECTORY
	```

	- **user** -- user under which the server should be run
	- **port** -- port where the fileserver should listen
	- **socket** -- path to UNIX socket where the fileserver should listen
	- **working_directory** -- directory where the files should be stored
	
4. Save the configuration file generated by the script and run it with uWSGI, 
   either directly or using systemd. This depends heavily on your distribution.
5. To integrate this with another web server, see the [uWSGI 
   documentation](http://uwsgi-docs.readthedocs.io/en/latest/WebServers.html)

Note that the ways distributions package uWSGI can vary wildly. In Debian 8 it
is necessary to convert the configuration file to XML and make sure that the
python3 plugin is loaded instead of python. This plugin also uses Python 3.4,
even though the rest of the system uses Python 3.5 - make sure to install
dependencies for the correct version.

## Documentation

Feel free to read the documentation on [our wiki](https://github.com/ReCodEx/wiki/wiki).
