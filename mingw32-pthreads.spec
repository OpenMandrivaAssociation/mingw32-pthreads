%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# The tests take ages to run and require Wine.
%define run_tests 0

Name:           mingw32-pthreads
Version:        2.8.0
Release:        %mkrel 3
Summary:        MinGW pthread library

%define crazy_version %(echo %{version}|tr . -)

License:        LGPLv2+
Group:          Development/Other
URL:            https://sourceware.org/pthreads-win32/
Source0:        ftp://sourceware.org/pub/pthreads-win32/pthreads-w32-%{crazy_version}-release.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildArch:      noarch

Patch0:         mingw32-pthreads-2.8.0-use-wine-for-tests.patch
Patch1:         mingw32-pthreads-2.8.0-no-failing-tests.patch
Patch2:		mingw32-pthreads-flags.patch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

%if %{run_tests}
BuildRequires:  wine
%endif


%description
The POSIX 1003.1-2001 standard defines an application programming
interface (API) for writing multithreaded applications. This interface
is known more commonly as pthreads. A good number of modern operating
systems include a threading library of some kind: Solaris (UI)
threads, Win32 threads, DCE threads, DECthreads, or any of the draft
revisions of the pthreads standard. The trend is that most of these
systems are slowly adopting the pthreads standard API, with
application developers following suit to reduce porting woes.

Win32 does not, and is unlikely to ever, support pthreads
natively. This project seeks to provide a freely available and
high-quality solution to this problem.


%prep
%setup -q -n pthreads-w32-%{crazy_version}-release

%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
%{_mingw32_make} clean
%{_mingw32_make} CROSS=%{_mingw32_host}- GC-inlined
%{_mingw32_make} clean
%{_mingw32_make} CROSS=%{_mingw32_host}- GCE-inlined


%check
%if %{run_tests}
pushd tests
%{_mingw32_make} clean
%{_mingw32_make} QAPC= \
  CC=%{_mingw32_cc} XXCFLAGS="-D__CLEANUP_C" TEST=GC all-pass
%{_mingw32_make} clean
%{_mingw32_make} QAPC= \
  CC=%{_mingw32_cc} XXCFLAGS="-D__CLEANUP_C" TEST=GCE all-pass
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}/pthread

install -m 0755 *.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install -m 0644 *.def $RPM_BUILD_ROOT%{_mingw32_bindir}
install -m 0644 *.a $RPM_BUILD_ROOT%{_mingw32_libdir}
install -m 0644 *.h $RPM_BUILD_ROOT%{_mingw32_includedir}/pthread


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc ANNOUNCE BUGS ChangeLog CONTRIBUTORS COPYING COPYING.LIB
%doc FAQ MAINTAINERS NEWS PROGRESS README README.NONPORTABLE TODO
%{_mingw32_bindir}/pthreadGC2.dll
%{_mingw32_bindir}/pthreadGCE2.dll
%{_mingw32_bindir}/pthread.def
%{_mingw32_libdir}/libpthreadGC2.a
%{_mingw32_libdir}/libpthreadGCE2.a
%{_mingw32_includedir}/pthread


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.0-3mdv2011.0
+ Revision: 620356
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 2.8.0-2mdv2010.0
+ Revision: 439931
- rebuild

* Fri Feb 06 2009 Jérôme Soyer <saispo@mandriva.org> 2.8.0-1mdv2009.1
+ Revision: 338143
- import mingw32-pthreads


