%define		mod_name	sqlinclude
%define		apxs		/usr/sbin/apxs
Summary:	Apache module: mySQL based "Include"-alike configuration command.
Summary(pl):	Modu³ do apache: bazuj±ca na mySQL komenda konfiguracji ala "Include"
Name:		apache-mod_%{mod_name}
Version:	1.4
Release:	3
License:	BSD
Group:		Networking/Daemons
Source0:	http://prdownloads.sourceforge.net/mod-sqlinclude/mod_sqlinclude-%{version}.tgz
# Source0-md5:	ecb1fd5d5a89c55e7dda4a9a456b0c13
URL:		http://sourceforge.net/projects/mod-sqlinclude/
BuildRequires:	apache(EAPI)-devel
BuildRequires:	mysql-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	/etc/httpd

%description
mod_sqlinclude is an Apache Web server module which implements mySQL
based "Include"-alike configuration command. This lets you keep your
httpd config in database (i.e. VHosts etc).

%description -l pl
Modu³ do serwera Apache implementuj±cy bazuj±c± na mySQL komendê
konfiguracyjn± typu "Include". Dziêki temu mo¿esz trzymaæ swoj±
konfiguracjê w bazie SQL.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGE* README* *.sql
%attr(755,root,root) %{_pkglibdir}/*
