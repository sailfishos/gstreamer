%define    gstreamer  gstreamer
%define    majorminor  1.0

%global _vpath_srcdir subprojects/gstreamer
%global _vpath_builddir subprojects/gstreamer/_build

Name:          %{gstreamer}%{majorminor}
Version:       1.22.10
Release:       1
Summary:       GStreamer streaming media framework runtime
License:       LGPLv2+
URL:           http://gstreamer.freedesktop.org/
Source:        %{name}-%{version}.tar.gz
Source1:       gstreamer1.0.conf
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: bison
BuildRequires: flex
BuildRequires: pkgconfig(check)
BuildRequires: pkgconfig(libdw)
BuildRequires: meson
BuildRequires: libtool
BuildRequires: gettext-devel
Patch1:        deactivate_max_size_time.patch

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

%package libgstcheck
Summary: GStreamer unit test library
Requires: %{name} = %{version}-%{release}

%description libgstcheck
%{summary}.

%package devel
Summary:  Libraries/include files for GStreamer streaming media framework
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libgstcheck = %{version}-%{release}
Requires: glib2-devel
Requires: check-devel

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
Summary:  Tools for GStreamer streaming media framework
Requires: %{name} = %{version}-%{release}

%description tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

This package contains some GStreamer useful tools

%prep
%autosetup -p1 -n %{name}-%{version}/gstreamer

%build
%meson \
  -Dpackage-name='SailfishOS GStreamer package' \
  -Dpackage-origin='http://sailfishos.org/' \
  -Dgst_debug=true \
  -Dintrospection=enabled \
  -Dnls=disabled \
  -Dexamples=disabled \
  -Ddoc=disabled \
  -Dbash-completion=disabled \
  -Dtracer_hooks=true \
  -Dlibunwind=disabled \
  -Ddbghelp=disabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT
%meson_install
install -m 644 -D %SOURCE1 $RPM_BUILD_ROOT/%{_sysconfdir}/pulse/xpolicy.conf.d/gstreamer1.0.conf

# Clean out files that should not be part of the rpm.
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majorminor}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gstreamer-%{majorminor}
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Remove docs
rm -fr $RPM_BUILD_ROOT/%{_mandir}
rm -f $RPM_BUILD_ROOT/%{_libexecdir}/gstreamer-%{majorminor}/gst-hotdoc-plugins-scanner
rm -f $RPM_BUILD_ROOT/%{_libexecdir}/gstreamer-%{majorminor}/gst-plugins-doc-cache-generator
# Remove GDB
rm -fr $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/gdb
rm -fr $RPM_BUILD_ROOT/%{_datadir}/gstreamer-%{majorminor}/gdb
rm -fr $RPM_BUILD_ROOT/%{_datadir}/gdb

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%license subprojects/gstreamer/COPYING
%dir %{_libdir}/gstreamer-%{majorminor}
%dir %{_libexecdir}/gstreamer-%{majorminor}
%dir %{_datadir}/gstreamer-%{majorminor}
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoretracers.so
%{_libexecdir}/gstreamer-%{majorminor}/gst-plugin-scanner
%{_libexecdir}/gstreamer-%{majorminor}/gst-ptp-helper
%{_libdir}/girepository-1.0/Gst-1.0.typelib
%{_libdir}/girepository-1.0/GstBase-1.0.typelib
%{_libdir}/girepository-1.0/GstCheck-1.0.typelib
%{_libdir}/girepository-1.0/GstController-1.0.typelib
%{_libdir}/girepository-1.0/GstNet-1.0.typelib

%files libgstcheck
%defattr(-, root, root, -)
%{_libdir}/libgstcheck-%{majorminor}.so.*

%files devel
%defattr(-, root, root, -)
%{_includedir}/gstreamer-%{majorminor}/gst/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/base
%{_includedir}/gstreamer-%{majorminor}/gst/check
%{_includedir}/gstreamer-%{majorminor}/gst/controller
%{_includedir}/gstreamer-%{majorminor}/gst/net
%{_libdir}/libgstreamer-%{majorminor}.so
%{_libdir}/libgstbase-%{majorminor}.so
%{_libdir}/libgstcheck-%{majorminor}.so
%{_libdir}/libgstcontroller-%{majorminor}.so
%{_libdir}/libgstnet-%{majorminor}.so
%{_datadir}/aclocal/gst-element-check-%{majorminor}.m4
%{_libdir}/pkgconfig/gstreamer-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{majorminor}.pc
%{_datadir}/gir-1.0/Gst-1.0.gir
%{_datadir}/gir-1.0/GstBase-1.0.gir
%{_datadir}/gir-1.0/GstCheck-1.0.gir
%{_datadir}/gir-1.0/GstController-1.0.gir
%{_datadir}/gir-1.0/GstNet-1.0.gir

%files tools
%defattr(-, root, root, -)
%{_bindir}/gst-inspect-%{majorminor}
%{_bindir}/gst-launch-%{majorminor}
%{_bindir}/gst-typefind-%{majorminor}
%{_bindir}/gst-stats-%{majorminor}
%{_bindir}/gst-tester-%{majorminor}
%{_sysconfdir}/pulse/xpolicy.conf.d/gstreamer1.0.conf
