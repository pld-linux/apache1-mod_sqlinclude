%define		mod_name	sqlinclude
%define		apxs		/usr/sbin/apxs1
Summary:	Apache module: mySQL based "Include"-alike configuration command
Summary(pl):	Modu³ do apache: bazuj±ca na mySQL komenda konfiguracji ala "Include"
Name:		apache1-mod_%{mod_name}
Version:	1.4
Release:	2
License:	BSD
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mod-sqlinclude/mod_sqlinclude-%{version}.tgz
# Source0-md5:	ecb1fd5d5a89c55e7dda4a9a456b0c13
URL:		http://sourceforge.net/projects/mod-sqlinclude/
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	mysql-devel
Requires(triggerpostun):	%{apxs}
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

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
%{__make} \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1.4-1.2
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc CHANGE* README* *.sql
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
