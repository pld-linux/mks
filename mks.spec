Summary:	An anti-virus utility for Unix
Summary(pl):	Antywirusowe narzêdzie dla Unixów
Name:		mks
Version:	1.4.0
Release:	1
License:	distributable
Group:		Applications
Source0:	http://download.mks.com.pl/files/%{name}linux.tgz
Source1:	%{name}-vir.cfg
Source2:	http://mksupdate.mks.com.pl/mkslinux/bazy.tgz
URL:		http://linux.mks.com.pl/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MKS Antivirus is anti-virus scanner for Unix.

%description -l pl
MKS jest skanerem antywirusowym dla systemów uniksowych.

%prep
%setup -q -c -a 2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_var}/lib/%{name}
install -D %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/mks_vir.cfg
install -D mks32	$RPM_BUILD_ROOT%{_bindir}/mks32
install    *.dat	$RPM_BUILD_ROOT%{_var}/lib/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc readme.txt CONTRIB/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %dir %{_var}/lib/%{name}
%attr(644,root,root) %verify(not md5 size mtime) %{_var}/lib/%{name}/*
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mks_vir.cfg
