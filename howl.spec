Summary:	Cross platform implementation of Zeroconf
Summary(pl):	Mi�dzyplatformowa implementacja Zeroconf
Name:		howl
Version:	0.9.10
Release:	2
License:	BSD
Group:		Libraries
Source0:	http://www.porchdogsoft.com/download/%{name}-%{version}.tar.gz
# Source0-md5:	444f2c1fe8eaf16d6822c01bfafba99b
Source1:	mDNSResponder.init
Source2:	nifd.init
Source3:	mDNSResponder.conf
Patch0:		%{name}-libdir.patch
Patch1:		%{name}-pkgconfig.patch
Patch2:		%{name}-am.patch
URL:		http://www.porchdogsoft.com/products/howl/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Howl is a cross-platform implementation of Zeroconf networking.
Zeroconf brings a new ease of use to IP networking.

%description -l pl
Howl jest mi�dzyplatformow� implementacj� Zeroconf. Zeroconf przynosi
now� �atwo�� przy pracy w sieci IP.

%package libs
Summary:	Howl libraries
Summary(pl):	Biblioteki howl
Group:		Libraries

%description libs
Howl libraries.

%description libs -l pl
Biblioteki howl.

%package devel
Summary:	Header files for howl library
Summary(pl):	Pliki nag��wkowe biblioteki howl
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for howl library.

%description devel -l pl
Pliki nag��wkowe biblioteki howl.

%package static
Summary:	Static howl library
Summary(pl):	Statyczna biblioteka howl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static howl library.

%description static -l pl
Statyczna biblioteka howl.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mDNSResponder
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/nifd
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/mDNSResponder.conf

# fix up header file directory naming bug
mv $RPM_BUILD_ROOT%{_includedir}/%{name} $RPM_BUILD_ROOT%{_includedir}/%{name}-%{version}

# remove the samples
rm -f $RPM_BUILD_ROOT%{_bindir}/mDNSBrowse
rm -f $RPM_BUILD_ROOT%{_bindir}/mDNSPublish
rm -f $RPM_BUILD_ROOT%{_bindir}/mDNSQuery
rm -f $RPM_BUILD_ROOT%{_bindir}/mDNSResolve

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mDNSResponder
if [ -f /var/lock/subsys/mDNSResponder ]; then
	/etc/rc.d/init.d/mDNSResponder restart >&2
else
	echo "Run \"/etc/rc.d/init.d/mDNSResponder start\" to start mDNSResponder."
fi

/sbin/chkconfig --add nifd
if [ -f /var/lock/subsys/nifd ]; then
	/etc/rc.d/init.d/nifd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/nifd start\" to start nifd."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mDNSResponder ]; then
		/etc/rc.d/init.d/mDNSResponder stop >&2
	fi
	/sbin/chkconfig --del mDNSResponder

	if [ -f /var/lock/subsys/nifd ]; then
		/etc/rc.d/init.d/nifd stop >&2
	fi
	/sbin/chkconfig --del nifd
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/mDNSResponder.conf
%{_datadir}/%{name}
%{_mandir}/man8/*.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/*.html
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}-%{version}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
