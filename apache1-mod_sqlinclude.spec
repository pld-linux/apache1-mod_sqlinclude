%define		mod_name	sqlinclude
%define		apxs		/usr/sbin/apxs1
Summary:	Apache module: mySQL based "Include"-alike configuration command
Summary(pl):	Modu� do apache: bazuj�ca na mySQL komenda konfiguracji ala "Include"
Name:		apache1-mod_%{mod_name}
Version:	1.4
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mod-sqlinclude/mod_sqlinclude-%{version}.tgz
# Source0-md5:	ecb1fd5d5a89c55e7dda4a9a456b0c13
URL:		http://sourceforge.net/projects/mod-sqlinclude/
BuildRequires:	apache1-devel
BuildRequires:	mysql-devel
Requires(post,preun):	%{apxs}
Requires:	apache1
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)

%description
mod_sqlinclude is an Apache Web server module which implements mySQL
based "Include"-alike configuration command. This lets you keep your
httpd config in database (i.e. VHosts etc).

%description -l pl
Modu� do serwera Apache implementuj�cy bazuj�c� na mySQL komend�
konfiguracyjn� typu "Include". Dzi�ki temu mo�esz trzyma� swoj�
konfiguracj� w bazie SQL.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__make} \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGE* README* *.sql
%attr(755,root,root) %{_pkglibdir}/*
