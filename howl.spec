Summary:	Cross platform implementation of Zeroconf
Summary(pl.UTF-8):	Międzyplatformowa implementacja Zeroconf
Name:		howl
Version:	1.0.0
Release:	7
License:	APSL / Other (see COPYING)
Group:		Libraries
Source0:	http://www.porchdogsoft.com/download/%{name}-%{version}.tar.gz
# Source0-md5:	c389d3ffba0e69a179de2ec650f1fdcc
Source1:	mDNSResponder-%{name}.init
Source2:	nifd.init
Source3:	mDNSResponder.conf
Patch0:		%{name}-libdir.patch
Patch1:		%{name}-pkgconfig.patch
Patch2:		%{name}-am.patch
Patch3:		%{name}-alpha.patch
Patch4:		%{name}-link.patch
URL:		http://www.porchdogsoft.com/products/howl/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Howl is a cross-platform implementation of Zeroconf networking.
Zeroconf brings a new ease of use to IP networking.

%description -l pl.UTF-8
Howl jest międzyplatformową implementacją Zeroconf. Zeroconf przynosi
nową łatwość przy pracy w sieci IP.

%package libs
Summary:	Howl libraries
Summary(pl.UTF-8):	Biblioteki howl
Group:		Libraries
Provides:	mdns-howl-libs

%description libs
Howl libraries.

%description libs -l pl.UTF-8
Biblioteki howl.

%package devel
Summary:	Header files for howl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki howl
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	mdns-howl-devel

%description devel
Header files for howl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki howl.

%package static
Summary:	Static howl library
Summary(pl.UTF-8):	Statyczna biblioteka howl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	mdns-howl-static

%description static
Static howl library.

%description static -l pl.UTF-8
Statyczna biblioteka howl.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mDNSResponder
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/nifd
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/mDNSResponder.conf

# fix up header file directory naming bug
mv $RPM_BUILD_ROOT%{_includedir}/%{name} $RPM_BUILD_ROOT%{_includedir}/%{name}-%{version}

# remove the samples
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mDNSBrowse
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mDNSPublish
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mDNSQuery
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mDNSResolve

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mDNSResponder
%service mDNSResponder restart

/sbin/chkconfig --add nifd
%service nifd restart

%preun
if [ "$1" = "0" ]; then
	%service mDNSResponder stop
	/sbin/chkconfig --del mDNSResponder

	%service nifd stop
	/sbin/chkconfig --del nifd
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%attr(755,root,root) %{_bindir}/autoipd
%attr(755,root,root) %{_bindir}/mDNSResponder
%attr(755,root,root) %{_bindir}/nifd
%attr(754,root,root) /etc/rc.d/init.d/mDNSResponder
%attr(754,root,root) /etc/rc.d/init.d/nifd
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/mDNSResponder.conf
%{_datadir}/%{name}
%{_mandir}/man8/autoipd.8*
%{_mandir}/man8/mDNSResponder.8*
%{_mandir}/man8/nifd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhowl.so.*.*.*
%ghost %{_libdir}/libhowl.so.0
%attr(755,root,root) %{_libdir}/libmDNSResponder.so.*.*.*
%ghost %{_libdir}/libmDNSResponder.so.0

%files devel
%defattr(644,root,root,755)
%doc docs/*.html
%{_libdir}/libhowl.so
%{_libdir}/libmDNSResponder.so
%{_libdir}/libhowl.la
%{_libdir}/libmDNSResponder.la
%{_includedir}/%{name}-%{version}
%{_pkgconfigdir}/howl.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhowl.a
%{_libdir}/libmDNSResponder.a
