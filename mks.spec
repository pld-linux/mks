#
# conditional build:
# _without_md5sum --don't check md5sum for antivirus database (useful
#	when doing ./builder -g -nc )
#
# TODO:
# - Update database as cron-job
Summary:	An anti-virus utility for Unix
Summary(pl):	Antywirusowe narzêdzie dla Unixów
Name:		mks
Version:	1.9.1
Release:	1
License:	distributable
Group:		Applications
Source0:	http://download.mks.com.pl/download/linux/mks32-1-9-1-Linux-i386.tgz
# Source0-md5:	e3a7a221db91988a77419b09342fa7bb
Source1:	%{name}-vir.cfg
Source2:	http://download.mks.com.pl/download/linux/bazy4.tgz
# Source2-md5:	9c9f70b50c2ed23ee20064686604084b
Source3:	bazy4.tgz.md5sum
# http://www.nzs.pw.edu.pl/~bkorupcz/pub/prog/patches/mksvir-update
Source4:	%{name}vir-update
Source5:	http://download.mks.com.pl/download/linux/mksLinux-contrib.tgz
# Source5-md5:	d73d2ef861b3fddbe4f6dbe60a0a43d1
Requires:	/usr/bin/wget
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
This package contains antivirus databases from 2003/06/25.

%description bases -l pl
Pakiet ten zawiera bazy antywirusowe z dnia 2003/06/25.

%prep
cd %{_sourcedir}
%{!?_without_md5sum: md5sum -c bazy4.tgz.md5sum}
cd -

%setup -q -c -a2 -a5
mv mks*/* ./

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/lib/%{name},%{_sysconfdir}/cron.daily,%{_bindir}}

install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/mks_vir.cfg
install mks32.static	$RPM_BUILD_ROOT%{_bindir}/mks32
install bazy4/*.dat	$RPM_BUILD_ROOT%{_var}/lib/%{name}
install %{SOURCE4}	$RPM_BUILD_ROOT%{_bindir}
ln -sf %{_bindir}/mksvir-update $RPM_BUILD_ROOT/etc/cron.daily/mksvir-update

mv CONTRIB/CHANGE1.TXT .
mv CONTRIB/postfix1.htm .
mv CONTRIB/postfix2.txt .
mv CONTRIB/postfix3.txt .
mv CONTRIB/readme.txt .
mv CONTRIB/2002 CONTRIB.2002
rm -rf CONTRIB
mv CONTRIB.2002 CONTRIB

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGE1.TXT postfix1.htm postfix2.txt postfix3.txt readme.txt CONTRIB licencja.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %dir %{_var}/lib/%{name}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mks_vir.cfg
%{_sysconfdir}/cron.daily/*

%files bases
%defattr(644,root,root,755)
%attr(644,root,root) %verify(not md5 size mtime) %{_var}/lib/%{name}/*
