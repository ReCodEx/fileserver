%define name recodex-fileserver
%define version 1.0.0
%define unmangled_version 1.0.0
%define release 1

Summary: ReCodEx fileserver component
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Petr Stefan <UNKNOWN>
Url: https://github.com/ReCodEx/fileserver
BuildRequires: systemd python3-pip
Requires: systemd httpd python3 python3-pip
Requires: uwsgi uwsgi-router-static uwsgi-router-rewrite uwsgi-plugin-python3

%description
Backend part of ReCodEx programmer testing solution.

%prep
%setup -n %{name}-%{unmangled_version}

%build

%install
mkdir -p %{buildroot}/opt
cp -r . %{buildroot}/opt/recodex-fileserver
mkdir -p %{buildroot}/%{_localstatedir}/recodex-fileserver-data
mkdir -p %{buildroot}/%{_sysconfdir}/uwsgi.d/
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
cp install/fileserver.ini %{buildroot}/%{_sysconfdir}/uwsgi.d/
cp install/010-fileserver.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/
cp install/recodex_htpasswd %{buildroot}/%{_sysconfdir}/httpd/
exit 0

%clean


%post

%postun
%systemd_postun_with_restart 'uwsgi.service'
%systemd_postun_with_restart 'httpd.service'

%pre
getent group recodex >/dev/null || groupadd -r recodex
getent passwd recodex >/dev/null || useradd -r -g recodex -d %{_sysconfdir}/recodex -s /sbin/nologin -c "ReCodEx Code Examiner" recodex
python3 -m pip install -r %{buildroot}/opt/recodex-fileserver/requirements.txt
exit 0

%preun

%files
%defattr(-,root,root)
%dir /opt/recodex-fileserver
%dir %{_localstatedir}/recodex-fileserver-data
/opt/recodex-fileserver/*
/opt/recodex-fileserver/.*
%config(noreplace) %attr(-,recodex,recodex) %{_sysconfdir}/uwsgi.d/fileserver.ini
%config(noreplace) %{_sysconfdir}/httpd/conf.d/010-fileserver.conf
%config(noreplace) %{_sysconfdir}/httpd/recodex_htpasswd

%changelog

