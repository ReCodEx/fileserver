%define name recodex-fileserver
%define short_name fileserver
%define version 1.2.1
%define unmangled_version f6424325b666d71a3dc35b90497a41303db3d3f8
%define release 3

Summary: ReCodEx fileserver component
Name: %{name}
Version: %{version}
Release: %{release}
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Petr Stefan <UNKNOWN>
Url: https://github.com/ReCodEx/fileserver
BuildRequires: systemd
%{?fedora:BuildRequires: python3-pip}
Requires: systemd httpd
Requires: uwsgi uwsgi-router-static uwsgi-router-rewrite uwsgi-plugin-python3
%{?fedora:Requires: python3 python3-pip}
%{?rhel:Requires: python34 python34-setuptools}

Source0: https://github.com/ReCodEx/%{short_name}/archive/%{unmangled_version}.tar.gz#/%{short_name}-%{unmangled_version}.tar.gz

%description
Backend part of ReCodEx programmer testing solution.

%prep
%setup -n %{short_name}-%{unmangled_version}

%build

%install
mkdir -p %{buildroot}/opt
cp -r . %{buildroot}/opt/recodex-fileserver
mkdir -p %{buildroot}/%{_localstatedir}/recodex-fileserver
mkdir -p %{buildroot}/%{_sysconfdir}/uwsgi.d/
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
cp install/fileserver.ini %{buildroot}/%{_sysconfdir}/uwsgi.d/
cp install/010-fileserver.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/
cp install/recodex_htpasswd %{buildroot}/%{_sysconfdir}/httpd/
exit 0

%clean


%post
%if 0%{?rhel}
	easy_install-3.4 pip
%endif
python3 -m pip install -r /opt/recodex-fileserver/requirements.txt
%systemd_post 'uwsgi.service'
%systemd_post 'httpd.service'

%postun
%systemd_postun_with_restart 'uwsgi.service'
%systemd_postun_with_restart 'httpd.service'

%pre
getent group recodex >/dev/null || groupadd -r recodex
getent passwd recodex >/dev/null || useradd -r -g recodex -d %{_sysconfdir}/recodex -s /sbin/nologin -c "ReCodEx Code Examiner" recodex
exit 0

%preun
%systemd_preun 'uwsgi.service'
%systemd_preun 'httpd.service'

%files
%defattr(-,root,root)
%dir /opt/recodex-fileserver
%dir %{_localstatedir}/recodex-fileserver
/opt/recodex-fileserver/*
/opt/recodex-fileserver/.*
%config(noreplace) %attr(-,recodex,recodex) %{_sysconfdir}/uwsgi.d/fileserver.ini
%config(noreplace) %{_sysconfdir}/httpd/conf.d/010-fileserver.conf
%config(noreplace) %{_sysconfdir}/httpd/recodex_htpasswd

%changelog

