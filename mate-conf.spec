%define api	2
%define major	4
%define girmajor	2.0
%define libname	%mklibname mateconf %{api} %{major}
%define girname	%mklibname mateconf-gir %{girmajor}
%define devname	%mklibname mateconf -d

Name:		mate-conf
Summary:	MATE configuration database system
Version:	1.2.1
Release:	2
License:	GPLv3+
Group:		Graphical desktop/Other
URL:		http://www.mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
Patch0:		mate-conf-1.2.1-configure.patch
Patch1:		mate-conf-1.2.1-m4.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(MateCORBA-2.0)
BuildRequires:	pkgconfig(polkit-gobject-1)

%description
MateConf is a configuration database system, functionally similar to the
Windows registry but lots better.

%package -n mateconf-sanity-check
Summary:	Sanity checker for %{name}
Group:		%{group}

%description -n mateconf-sanity-check
gconf-sanity-check is a tool to check the sanity of a %{name}
installation.

%package -n %{libname}
Summary:	Mate-conf libraries
Group:		System/Libraries

%description -n %{libname}
MateConf is a configuration database system, functionally similar to the
Windows registry but lots better.

%package -n %{girname}
Summary:	GObject introspection interface library for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject introspection interface library for %{name}.

%package -n %{devname}
Summary:        Mate-conf development files
Group:          Development/C
Requires:	%{libname} = %{version}
Requires:	%{girname} = %{version}
Provides:	%{name}-devel = %{version}
Obsoletes:	%{_lib}mateconf2-devel < 1.2.1-2

%description -n %{devname}
MateConf is a configuration database system, functionally similar to the
Windows registry but lots better.

%prep
%setup -q

%build
NOCONFIGURE=yes ./autogen.sh
%configure2_5x \
	--enable-defaults-service \
	--enable-gsettings-backend=no \
	--disable-static
%make

%install
%makeinstall_std

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README TODO
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.mate.MateConf.Defaults.conf
%dir %{_sysconfdir}/mateconf/
%config(noreplace) %{_sysconfdir}/mateconf/*
%{_bindir}/mateconf*
%{_libdir}/MateConf/2/
%{_libexecdir}/mateconf-defaults-mechanism
%{_libexecdir}/mateconfd-2
%{_datadir}/MateConf/
%{_datadir}/dbus-1/*/org.mate.MateConf.*
%{_mandir}/man1/mateconftool-2.1*
%{_datadir}/polkit-1/actions/org.mate.mateconf.defaults.policy
%{_datadir}/sgml/mateconf/

%files -n mateconf-sanity-check
%{_libexecdir}/mateconf-sanity-check-2

%files -n %{libname}
%{_libdir}/libmateconf-2.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/MateConf-%{girmajor}.typelib

%files -n %{devname}
%{_includedir}/mateconf/2/
%{_libdir}/libmateconf-2.so
%{_libdir}/pkgconfig/mateconf-2.0.pc
%{_datadir}/aclocal/mateconf-2.m4
%{_datadir}/gir-1.0/MateConf-%{girmajor}.gir
%{_datadir}/gtk-doc/html/mateconf/

