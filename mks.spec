# conditional build:
# _without_md5sum --don't check md5sum for antivirus database (useful
#	when doing ./builder -g -nc )
#
# TODO:
# - Update database as cron-job
Summary:	An anti-virus utility for Unix
Summary(pl):	Antywirusowe narzêdzie dla Unixów
Name:		mks
Version:	1.7.4
Release:	1
License:	distributable
Group:		Applications
Source0:	http://download.mks.com.pl/download/linux/%{name}Linux-1-7-4.tgz
# Source0-md5:	e5acbc439505c297a7532534c6ce2dd1
Source1:	%{name}-vir.cfg
Source2:	http://download.mks.com.pl/download/linux/bazy3.tgz
# Source2-md5:	d1fef367c839d1259d8be36061eec068
Source3:	bazy3.tgz.md5sum
Requires:	/usr/bin/wget
# http://www.nzs.pw.edu.pl/~bkorupcz/pub/prog/patches/mksvir-update
Source4:	%{name}vir-update
URL:		http://linux.mks.com.pl/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86}

%description
MKS Antivirus is anti-virus scanner for Unix.

%description -l pl
MKS jest skanerem antywirusowym dla systemów uniksowych.

%package bases
Summary:	Mks Antivirus databases
Summary(pl):	Bazy antywirusowe mks
Group:		Applications

%description bases
This package contains antivirus databases from 2003/05/08.

%description bases -l pl
Pakiet ten zawiera bazy antywirusowe z dnia 2003/05/08.

%prep
cd %{_sourcedir}
%{!?_without_md5sum: md5sum -c bazy3.tgz.md5sum}
cd -
%setup -q -c -a 2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/lib/%{name},%{_sysconfdir}/cron.daily}
install -D %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/mks_vir.cfg
install -D mks32.static	$RPM_BUILD_ROOT%{_bindir}/mks32
install bazy3/*.dat	$RPM_BUILD_ROOT%{_var}/lib/%{name}/
install %{SOURCE4}	$RPM_BUILD_ROOT%{_bindir}
ln -sf %{_bindir}/mksvir-update $RPM_BUILD_ROOT/etc/cron.daily/mksvir-update

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGE1.TXT  LICENCJA.TXT readme.txt CONTRIB
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %dir %{_var}/lib/%{name}
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mks_vir.cfg
%attr(644,root,root) %{_sysconfdir}/cron.daily/*

%files bases
%defattr(644,root,root,755)
%attr(644,root,root) %verify(not md5 size mtime) %{_var}/lib/%{name}/*
