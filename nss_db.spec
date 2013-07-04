%define pre	pre1
%define	arcver %{version}%{pre}

%if %{_use_internal_dependency_generator}
%define __noautoreq 'GLIBC_PRIVATE'
%else
%define _requires_exceptions GLIBC_PRIVATE
%endif

Summary:	NSS library for DB
Name:		nss_db
Version:	2.2.3
Release:	0.%{pre}.12
License:	GPLv2
Group:		System/Libraries
Url:		http://sources.redhat.com/glibc/
Source0:	ftp://sources.redhat.com/pub/glibc/releases/nss_db-%{arcver}.tar.bz2
Source1:	makedb.man
Source100:	nss_db.rpmlintrc
Patch0:		nss_db-2.2.3pre1-external.patch
Patch1:		nss_db-2.2.3pre1-dbopen.patch
Patch2:		nss_db-2.2.3pre1-dbupgrade.patch
Patch3:		nss_db-2.2-paths.patch
Patch4:		nss_db-2.2-enoent.patch
Patch5:		nss_db-2.2-initialize.patch
Patch6:		nss_db-2.2.3pre1-CVE-2010-0826.diff
BuildRequires:	db_nss52-devel
BuildRequires:	db52-devel
Requires:	make

%description
Nss_db is a set of C library extensions which allow Berkeley Databases
to be used as a primary source of aliases, ethers, groups, hosts,
networks, protocol, users, RPCs, services and shadow
passwords (instead of or in addition to using flat files or NIS).

Install nss_db if you flat name service files are too large and lookups
slow.

%prep
%setup -qn %{name}-%{arcver}
%apply_patches
mkdir -p db_nss/lib
ln -s %{_includedir}/db_nss db_nss/include
ln -s %{_libdir}/libdb_nss.so db_nss/lib/libdb.so

%build
%configure2_5x --with-db=$PWD/db_nss
make

%install
mkdir -p \
	%{buildroot}/%{_lib} \
	%{buildroot}/var/lib/misc \
	%{buildroot}%{_bindir} \
	%{buildroot}%{_mandir}/man1
cp -a src/.libs/libnss_db.so.[0-9]* %{buildroot}/%{_lib}
install -m 755 src/makedb %{buildroot}%{_bindir}
cp -a db-Makefile %{buildroot}/var/lib/misc/Makefile
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/makedb.1

%files
%doc AUTHORS ChangeLog NEWS README
/%{_lib}/libnss_db*2*
%{_bindir}/makedb
%{_mandir}/man1/makedb.1*
/var/lib/misc/Makefile

