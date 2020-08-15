%define name recodex-fileserver
%define short_name fileserver
%define version 1.2.2
%define unmangled_version 7d9f435f19f24a909106a2badd7ff5a108068f59
%define release 2

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
%{?fedora:BuildRequires: python3-devel python3-pip}
%{?rhel:BuildRequires: python36 python36-devel}
Requires: systemd httpd
%{?fedora:Requires: python3 python3-flask python3-click}
%{?rhel:Requires: python36 python3-mod_wsgi}

Source0: https://github.com/ReCodEx/%{short_name}/archive/%{unmangled_version}.tar.gz#/%{short_name}-%{unmangled_version}.tar.gz

%description
Fileserver is a backend part of ReCodEx code examiner, an educational application for evaluating programming assignments. 

%prep
%setup -n %{short_name}-%{unmangled_version}

%build

%install
mkdir -p %{buildroot}/opt
cp -r . %{buildroot}/opt/recodex-fileserver
mkdir -p %{buildroot}/%{_localstatedir}/recodex-fileserver
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
cp install/010-fileserver.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/
cp install/recodex_htpasswd %{buildroot}/%{_sysconfdir}/httpd/
exit 0

%clean


%post
%if 0%{?rhel}
	pip3 install -r /opt/recodex-fileserver/requirements.txt
%endif
%systemd_post 'httpd.service'

%postun
%systemd_postun_with_restart 'httpd.service'

%pre
getent group recodex >/dev/null || groupadd -r recodex
getent passwd recodex >/dev/null || useradd -r -g recodex -d %{_sysconfdir}/recodex -s /sbin/nologin -c "ReCodEx Code Examiner" recodex
exit 0

%preun
%systemd_preun 'httpd.service'

%files
%defattr(-,root,root)
%dir /opt/recodex-fileserver
%dir %{_localstatedir}/recodex-fileserver
/opt/recodex-fileserver/*
/opt/recodex-fileserver/.*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/010-fileserver.conf
%config(noreplace) %{_sysconfdir}/httpd/recodex_htpasswd

%changelog

