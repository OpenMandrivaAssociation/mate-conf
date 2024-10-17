%define api	2
%define major	4
%define girmajor	2.0
%define libname	%mklibname mateconf %{api} %{major}
%define girname	%mklibname mateconf-gir %{girmajor}
%define devname	%mklibname mateconf -d

Name:		mate-conf
Summary:	MATE configuration database system
Version:	1.4.0
Release:	1
License:	GPLv3+
Group:		Graphical desktop/Other
URL:		https://www.mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
Source1:	mateconf.sh
Source2:	mateconf.csh
Source3:	mateconf-schemas.filter
Source4:	mateconf-schemas.script
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
mateconf-sanity-check is a tool to check the sanity of a %{name}
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
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Requires:	%{girname} = %{version}
Provides:	%{name}-devel = %{EVRD}

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
	--enable-gtk \
	--disable-static
%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/mateconf.sh
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/mateconf.csh

mkdir %{buildroot}%{_sysconfdir}/mateconf/schemas

# Provide /usr/lib/mateconfd-2 symlink on lib64 platforms
%if "%{_lib}" != "lib"
mkdir -p %{buildroot}%{_prefix}/lib
ln -s ../%{_lib}/mateconfd-%{api} %{buildroot}%{_prefix}/lib/mateconfd-%{api}
%endif

mkdir -p %{buildroot}%{_sysconfdir}/mateconf/{mateconf.xml.local-defaults,mateconf.xml.local-mandatory,mateconf.xml.system}

cat << EOF > %{buildroot}%{_sysconfdir}/mateconf/2/local-defaults.path
xml:readonly:/etc/mateconf/mateconf.xml.local-defaults
include "\$(HOME)/.mateconf.path.defaults"
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/mateconf/2/local-mandatory.path
xml:readonly:/etc/mateconf/mateconf.xml.local-mandatory
include "\$(HOME)/.mateconf.path.mandatory"
EOF

# automatic install of mateconf schemas on rpm installs
# (see http://wiki.mandriva.com/en/Rpm_filetriggers)
install -d %{buildroot}%{_var}/lib/rpm/filetriggers
install -m 644 %{SOURCE3} %{buildroot}%{_var}/lib/rpm/filetriggers
install -m 755 %{SOURCE4} %{buildroot}%{_var}/lib/rpm/filetriggers

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README TODO
%dir %{_sysconfdir}/mateconf/
%dir %{_sysconfdir}/mateconf/mateconf.xml*
%dir %{_sysconfdir}/mateconf/schemas
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.mate.MateConf.Defaults.conf
%config(noreplace) %{_sysconfdir}/mateconf/%{api}
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_bindir}/mateconf*
%{_libdir}/MateConf/2/
%{_libexecdir}/mateconf-defaults-mechanism
%{_libexecdir}/mateconfd-%{api}
%if "%{_lib}" != "lib"
%{_prefix}/lib/mateconfd-%{api}
%endif
%{_datadir}/MateConf/
%{_datadir}/dbus-1/*/org.mate.MateConf.*
%{_datadir}/polkit-1/actions/org.mate.mateconf.defaults.policy
%{_datadir}/sgml/mateconf/
%{_mandir}/man1/mateconftool-2.1*
%{_var}/lib/rpm/filetriggers/mateconf-schemas.*

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



%changelog
* Fri Jul 27 2012 Matthew Dawkins <mattydaw@mandriva.org> 1.4.0-1
+ Revision: 811328
- new version 1.4.0

* Tue Jun 12 2012 Matthew Dawkins <mattydaw@mandriva.org> 1.2.1-4
+ Revision: 805246
- rebuild to make sure sysconfdir mateconf dirs are pkgd

* Fri Jun 08 2012 Matthew Dawkins <mattydaw@mandriva.org> 1.2.1-3
+ Revision: 803515
- rebuild - copied over filetrigger support from GConf2
- made dev pkg require mate-conf

* Sat Jun 02 2012 Matthew Dawkins <mattydaw@mandriva.org> 1.2.1-2
+ Revision: 802050
- rebuild for mateconf-sanity-check
- split out gir pkg
- utilize api

* Tue Apr 24 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.2.1-1
+ Revision: 793133
- imported package mate-conf

