%define pre	pre1
%define	arcver %{version}%{pre}

%define build_compat	0
# Allow --with[out] compat rpm command line build
%{?_with_compat: %{expand: %%define build_compat 1}}
%{?_without_compat: %{expand: %%define build_compat 0}}

%if %{_use_internal_dependency_generator}
%define __noautoreq 'GLIBC_PRIVATE'
%else
%define _requires_exceptions GLIBC_PRIVATE
%endif

Summary:	NSS library for DB
Name:		nss_db
Version:	2.2.3
Release:	0.%{pre}.12
License:	GPL
Group:		System/Libraries
URL:		http://sources.redhat.com/glibc/
Source:		ftp://sources.redhat.com/pub/glibc/releases/nss_db-%{arcver}.tar.bz2
Source1:	makedb.man
Source100:	nss_db.rpmlintrc
Patch0:		nss_db-2.2.3pre1-external.patch
Patch1:		nss_db-2.2.3pre1-dbopen.patch
Patch2:		nss_db-2.2.3pre1-dbupgrade.patch
Patch3:		nss_db-2.2-paths.patch
Patch4:		nss_db-2.2-enoent.patch
Patch5:		nss_db-2.2-initialize.patch
Patch6:		nss_db-2.2.3pre1-CVE-2010-0826.diff
Patch10:	nss_db-2.2-compat.patch
BuildRequires:	db_nss-devel
BuildRequires:	db-devel
%if !%{build_compat}
Obsoletes:	%{name}-compat < %{version}-%{release}
%endif
Requires:	make

%description
Nss_db is a set of C library extensions which allow Berkeley Databases
to be used as a primary source of aliases, ethers, groups, hosts,
networks, protocol, users, RPCs, services and shadow
passwords (instead of or in addition to using flat files or NIS).

Install nss_db if you flat name service files are too large and lookups
slow.

%if %{build_compat}
%package	compat
Summary:	NSS compatibility library for DB
Group:		System/Libraries

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
pushd compat
%patch10 -p1 -b .compat
popd
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
mkdir -p %{buildroot}/%{_lib} %{buildroot}/var/lib/misc \
	%{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
cp -a src/.libs/libnss_db.so.[0-9]* %{buildroot}/%{_lib}
install -m 755 src/makedb %{buildroot}%{_bindir}
cp -a db-Makefile %{buildroot}/var/lib/misc/Makefile
%if %{build_compat}
cp -a compat/.libs/libnss_db.so.[0-9]* %{buildroot}/%{_lib}
%endif
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/makedb.1

%files
%doc AUTHORS ChangeLog NEWS README
/%{_lib}/libnss_db*2*
%{_bindir}/makedb
%{_mandir}/man1/makedb.1*
/var/lib/misc/Makefile

%if %{build_compat}
%files compat
%defattr(-,root,root)
/%{_lib}/libnss_db*1*
%endif

%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.3-0.pre1.10mdv2011.0
+ Revision: 666627
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.3-0.pre1.9mdv2011.0
+ Revision: 606827
- rebuild

* Sat Apr 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.3-0.pre1.8mdv2010.1
+ Revision: 535822
- P6: security fix for CVE-2010-0826 (ubuntu)

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.3-0.pre1.7mdv2010.1
+ Revision: 520194
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.2.3-0.pre1.6mdv2010.0
+ Revision: 426256
- rebuild

* Fri Apr 03 2009 Luca Berra <bluca@mandriva.org> 2.2.3-0.pre1.5mdv2009.1
+ Revision: 363755
- upgrade db only if it we have write access to it (#48787)

* Mon Jun 09 2008 Pixel <pixel@mandriva.com> 2.2.3-0.pre1.4mdv2009.0
+ Revision: 217193
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
- no need to explictly require ldconfig (rpm will do it automatically)

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 2.2.3-0.pre1.4mdv2008.1
+ Revision: 133087
- BR db-devel
- kill re-definition of %%buildroot on Pixel's request

  + Luca Berra <bluca@mandriva.org>
    - rebuild for missing symbols on x86_64 (#35416)
    - import nss_db


* Sat Apr 15 2006 Luca Berra <bluca@vodka.it> 2.2.3-0.pre1.3mdk
- disable compat on all arches, and obsolete it if disabled
- use Requires(pre) for ldconfig
- set errno to ENOENT by default so that we don't leave stale errno values
  around in error cases (redhat)
- clear the entire key DBT before handing it to a get() function (redhat)

* Mon Aug 16 2004 Luca Berra <bluca@vodka.it> 2.2.3-0.pre1.2mdk 
- build with libdb_nss
- build of compat lib is now optional (disabled)

* Sat Mar 20 2004 Luca Berra <bluca@vodka.it> 2.2.3-0.pre1.1mdk 
- 2.2.3pre1
- patch to allow building separately from libc
- build with db4.1
- manpage for makedb

* Mon Dec  3 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.2-6mdk
- fix build by removing alpha patch (patch2)
- use %%configure2_5x to pass --build/--host/--target

* Thu Oct 25 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.2-5mdk
- rebuild for db3.3

* Tue Jul  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.2-4mdk
- recompiled for db3.2

* Sun Apr 22 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2-3mdk
- Fix build on Alpha.

* Tue Mar 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.2-2mdk
- corrected path to point to /var/lib/misc as specified in the glibc headers.

* Mon Mar 12 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.2-1mdk
- 2.2

* Tue Dec 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2

* Thu Sep 14 2000 Jakub Jelinek <jakub@redhat.com>
- separate from db3
