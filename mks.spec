#
# Conditional build:
%bcond_without	md5sum	# don't check md5sum for antivirus database (useful
#			when doing ./builder -g -nc )
#
Summary:	An anti-virus utility for Unix
Summary(pl):	Antywirusowe narz�dzie dla Uniks�w
Name:		mks
Version:	1.9.6
Release:	2
License:	This program will be for free till the end of year 2004 (see licence.txt)
Group:		Applications
Source0:	http://download.mks.com.pl/download/linux/mks32-Linux-i386-%(echo %{version} | tr . -).tgz
# Source0-md5:	6d8cfa09835d9856aac92c0d26645336
Source1:	%{name}-vir.cfg
# link to source tgz is inside of http://download.mks.com.pl/download/linux/bazy4.tgz
Source2:	bazy4.tgz
# Source2-md5:	d610eb1d7f6f0f24494463f634223e9d
Source3:	bazy4.tgz.md5sum
# http://www.nzs.pw.edu.pl/~bkorupcz/pub/prog/patches/mksvir-update
Source4:	%{name}vir-update
Source5:	http://download.mks.com.pl/download/linux/mksLinux-contrib.tgz
# Source5-md5:	d73d2ef861b3fddbe4f6dbe60a0a43d1
Source6:	%{name}-cron-updatedb
URL:		http://linux.mks.com.pl/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MKS Antivirus is anti-virus scanner for Unix.

%description -l pl
MKS jest skanerem antywirusowym dla system�w uniksowych.

%package bases
Summary:	Mks Antivirus databases
Summary(pl):	Bazy antywirusowe MKS
Group:		Applications

%description bases
This package contains antivirus databases from 2004/04/10. You shuld
use some automagic script for updating bases, as new worms are being
born.

%description bases -l pl
Pakiet ten zawiera bazy antywirusowe z dnia 2004/04/10. Nale�y u�ywa�
jakich� automagicznych skrypt�w do aktualizacji baz, gdy� wci��
pojawiaj� si� nowe wirusy.

%package updater
Summary:	Mks Antivirus database updater
Summary(pl):	Aktualizator baz antywirusowych MKS
Group:		Applications
Requires:	/usr/bin/wget
Requires:	bc

%description updater
This package contains antivirus databases updater from
http://www.nzs.pw.edu.pl/~bkorupcz/pub/prog/patches/mksvir-update and
an appropriate crontab.daily entry.

%description updater -l pl
Pakiet ten zawiera akualizator baz antywirusowych z
http://www.nzs.pw.edu.pl/~bkorupcz/pub/prog/patches/mksvir-update oraz
odpowiedni wpis w crontab.daily.

%prep
cd %{_sourcedir}
%{?with_md5sum: md5sum -c bazy4.tgz.md5sum}
cd -

%setup -q -c -a2 -a5
mv mks*/* ./

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/lib/%{name},%{_sysconfdir}/cron.d,%{_bindir},%{_sbindir}}

install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/mks_vir.cfg
install mks32.static	$RPM_BUILD_ROOT%{_bindir}/mks32
install bazy4/*.dat	$RPM_BUILD_ROOT%{_var}/lib/%{name}
install %{SOURCE4}	$RPM_BUILD_ROOT%{_bindir}
install %{SOURCE6}	$RPM_BUILD_ROOT%{_sbindir}/mksvir-cron-updatedb

cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}
5 * * * *     root    %{_sbindir}/mksvir-cron-updatedb
EOF

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
%doc CHANGE1.TXT postfix1.htm postfix2.txt postfix3.txt readme.txt CONTRIB licencja.txt licence.txt
%attr(755,root,root) %{_bindir}/mks32
%attr(755,root,root) %dir %{_var}/lib/%{name}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mks_vir.cfg

%files bases
%defattr(644,root,root,755)
%attr(644,root,root) %verify(not md5 size mtime) %{_var}/lib/%{name}/*

%files updater
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mksvir-update
%attr(755,root,root) %{_sbindir}/mksvir-cron-updatedb
%attr(640,root,root) %{_sysconfdir}/cron.d/*
