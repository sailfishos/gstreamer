%define		gstreamer	gstreamer
%define		majorminor	1.0
%define         _glib2          2.32.0

Name: 		%{gstreamer}1.0
Version: 	1.2.0
Release: 	1
Summary: 	GStreamer streaming media framework runtime

Group: 		Applications/Multimedia
License: 	LGPL
URL:		http://gstreamer.freedesktop.org/
Source: 	http://gstreamer.freedesktop.org/src/gstreamer/%{name}-%{version}.tar.xz

BuildRequires: 	pkgconfig(glib-2.0) >= %{_glib2}
BuildRequires: 	bison
BuildRequires: 	flex
BuildRequires: 	pkgconfig(check)
BuildRequires:  python
BuildRequires:  autoconf213
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

%package devel
Summary: 	Libraries/include files for GStreamer streaming media framework
Group: 		Development/Libraries

Requires: 	%{name} = %{version}-%{release}
Requires: 	glib2-devel >= %{_glib2}
Requires:	check-devel

%description devel
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer, as well as general and API
documentation.

%package tools
Summary: 	Tools for GStreamer streaming media framework
Group: 		Applications/Multimedia

Requires: 	%{name} = %{version}-%{release}

%description tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

This package contains some GStreamer useful tools

%prep
%setup -q -n %{name}-%{version}/gstreamer

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
  --with-package-name='Jolla GStreamer package' \
  --with-package-origin='http://jolla.com' \
  --enable-debug \
  --enable-introspection=no \
  --disable-nls \
  --disable-examples \
  --enable-docbook=no \
  --enable-gtk-doc=no \
  --enable-gtk-doc-html=no \
  --enable-gtk-doc-pdf=no \
  --disable-trace \
  --disable-alloc-trace

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

# Clean out files that should not be part of the rpm.
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majorminor}
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -fr $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
%{_libexecdir}/gstreamer-%{majorminor}/gst-plugin-scanner

%files devel
%defattr(-, root, root, -)
%{_includedir}/gstreamer-%{majorminor}/gst/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/base
%{_includedir}/gstreamer-%{majorminor}/gst/check
%{_includedir}/gstreamer-%{majorminor}/gst/controller
%{_includedir}/gstreamer-%{majorminor}/gst/net
%{_libdir}/libgstreamer-%{majorminor}.so
%{_libdir}/libgstbase-%{majorminor}.so
%{_libdir}/libgstcheck-%{majorminor}.so*
%{_libdir}/libgstcontroller-%{majorminor}.so
%{_libdir}/libgstnet-%{majorminor}.so
%{_datadir}/aclocal/gst-element-check-%{majorminor}.m4
%{_libdir}/pkgconfig/gstreamer-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{majorminor}.pc

%files tools
%defattr(-, root, root, -)
%{_bindir}/gst-inspect-%{majorminor}
%{_bindir}/gst-launch-%{majorminor}
%{_bindir}/gst-typefind-%{majorminor}
%{_mandir}/man1/gst-inspect-%{majorminor}.*
%{_mandir}/man1/gst-launch-%{majorminor}.*
%{_mandir}/man1/gst-typefind-%{majorminor}.*
