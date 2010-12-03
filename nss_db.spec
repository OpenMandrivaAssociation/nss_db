%define	name	nss_db
%define version	2.2.3
%define pre	pre1
%define	arcver %{version}%{pre}
%define release %mkrel 0.%{pre}.9

%define build_compat	0
# Allow --with[out] compat rpm command line build
%{?_with_compat: %{expand: %%define build_compat 1}}
%{?_without_compat: %{expand: %%define build_compat 0}}

%define _requires_exceptions GLIBC_PRIVATE

Summary:	NSS library for DB
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		ftp://sources.redhat.com/pub/glibc/releases/nss_db-%{arcver}.tar.bz2
Source1:	makedb.man
URL:		http://sources.redhat.com/glibc/
Patch0:		nss_db-2.2.3pre1-external.patch
Patch1:		nss_db-2.2.3pre1-dbopen.patch
Patch2:		nss_db-2.2.3pre1-dbupgrade.patch
Patch3:		nss_db-2.2-paths.patch
Patch4:		nss_db-2.2-enoent.patch
Patch5:		nss_db-2.2-initialize.patch
Patch6:		nss_db-2.2.3pre1-CVE-2010-0826.diff
Patch10:	nss_db-2.2-compat.patch
License:	GPL
Group:		System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	make
BuildRequires:	db_nss-devel >= 4.2.52-5mdk db-devel
%if %{build_compat}
%else
Obsoletes:	%{name}-compat
%endif

%description
Nss_db is a set of C library extensions which allow Berkeley Databases
to be used as a primary source of aliases, ethers, groups, hosts,
networks, protocol, users, RPCs, services and shadow
passwords (instead of or in addition to using flat files or NIS).

Install nss_db if you flat name service files are too large and lookups
slow.

%if %{build_compat}
%package compat
Summary: NSS compatibility library for DB
Group: System/Libraries

%description compat
Nss_db-compat is a set of C library extensions which allow Berkeley Databases
to be used as a primary source of aliases, ethers, groups, hosts,
networks, protocol, users, RPCs, services and shadow
passwords (instead of or in addition to using flat files or NIS) from
programs linked against glibc 2.0.x.
%endif

%prep
%setup -q -n %{name}-%{arcver}
%patch0 -p1 -b .external
%patch1 -p1 -b .dbopen
%patch2 -p0 -b .dbupgrade
%patch3 -p1 -b .paths
%patch4 -p1 -b .enoent
%patch5 -p1 -b .initialize
%patch6 -p1 -b .CVE-2010-0826
%if %{build_compat}
cp -al src compat
cd compat
%patch10 -p1 -b .compat
cd ..
%endif
mkdir -p db_nss/lib
ln -s %{_includedir}/db_nss db_nss/include
ln -s %{_libdir}/libdb_nss.so db_nss/lib/libdb.so

%build
%configure2_5x --with-db=$PWD/db_nss
%if %{build_compat}
sed -e 's/^INTERFACE = 2/INTERFACE = 1/' src/Makefile > compat/Makefile
%make "SUBDIRS = intl po src compat"
%else
%make
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_lib} %{buildroot}/var/lib/misc \
	%{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
cp -a src/.libs/libnss_db.so.[0-9]* %{buildroot}/%{_lib}
install -m 755 src/makedb %{buildroot}%{_bindir}
cp -a db-Makefile %{buildroot}/var/lib/misc/Makefile
%if %{build_compat}
cp -a compat/.libs/libnss_db.so.[0-9]* %{buildroot}/%{_lib}
%endif
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/makedb.1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
/%{_lib}/libnss_db*2*
%{_bindir}/makedb
%{_mandir}/man1/makedb.1*
/var/lib/misc/Makefile

%if %mdkversion < 200900
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%endif

%if %{build_compat}

%files compat
%defattr(-,root,root)
/%{_lib}/libnss_db*1*

%if %mdkversion < 200900
%post compat -p /sbin/ldconfig

%postun compat -p /sbin/ldconfig
%endif

%endif
