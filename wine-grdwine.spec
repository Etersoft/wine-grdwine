# TODO:
%define optflags_lto %nil
# Fedora specific
%define _lto_cflags %{nil}

Name: wine-etersoft-grdwine
Version: 0.5.7.3
Release: alt1

Summary: Guardant usb dongle helper library for Wine

License: LGPLv2
Group: Emulators
Url: https://guardant.com

#Source-url: ftp://ftp.guardant.ru/support/linux/grdwine-%version.tar.gz
# Source-url: https://github.com/Etersoft/grdwine/archive/refs/tags/v%version.tar.gz
Source: %name-%version.tar

Source1: 90-grdnt.rules

ExclusiveArch: %ix86 x86_64

%define libwinedir %_libdir/wine-etersoft

# TODO: use mingw detection from wine or just wait for total PE using
%def_with pebuild

# check if we need wow64 build also
%if "%(test -d %libwinedir/i386-windows && echo 1)" == "1"
%def_with wow64
%endif


%ifarch x86_64 aarch64
    %def_with build64
    %define winearch wine64
    %define winepkgname wine-etersoft-grdwine
    %define winedevpkgname wine-etersoft-devel-tools
    %define opkgname wine-grdwine
%endif

# workaround for https://bugzilla.altlinux.org/38130
# buildwow64 = _arch = x86_64  && with wow64
%if "%_arch" == "x86_64" && %{expand:%%{?_with_wow64:1}%%{!?_with_wow64:0}}
    %def_with buildwow64
    %undefine _with_build64
%endif

%ifarch %ix86
    %def_without build64
    %define winepkgname wine32-etersoft-grdwine
    %define winedevpkgname wine32-etersoft-devel-tools
    %define opkgname wine32-grdwine
%endif

BuildRequires: %winedevpkgname >= 9

# lib.req: ERROR: /tmp/.private/lav/wine-cpcsp_proxy-buildroot/usr/lib64/wine/x86_64-unix/cpcsp_proxy.so: library ntdll.so not found
AutoReq: no

Provides: %opkgname = %EVR
Obsoletes: %opkgname < %EVR

# TODO: move to rpm-macros-wine
# set arch dependent dirs
%ifarch %{ix86}
%define winepedir i386-windows
%define winesodir i386-unix
%endif
%ifarch x86_64
%define winepedir x86_64-windows
%define winesodir x86_64-unix
%endif
%ifarch %{arm}
%define winepedir arm-windows
%define winesodir arm-unix
%endif
%ifarch aarch64
%define winepedir aarch64-windows
%define winesodir aarch64-unix
%endif
%define winepe32dir i386-windows

%add_verify_elf_skiplist %libwinedir/%winesodir/grdwine.dll.so
%add_verify_elf_skiplist %libwinedir/%winesodir/grdwine.so

%description
Guardant usb dongle helper library for Wine.
Implementation of the GrdWine is based on Linux USB Device
Filesystem and Linux USB HID Device Interface.

Supports Guardant Sign/Time and Guardant Code dongles.
Old keys Stealth II and Stealth III are not supported here
(check WINE@Etersoft 2.x to get support).

%if_without build64
%package -n %winepkgname
Group: Development/C
Summary: Guardant usb dongle helper library for Wine

%description -n %winepkgname
Guardant usb dongle helper library for Wine.
Implementation of the GrdWine is based on Linux USB Device
Filesystem and Linux USB HID Device Interface.

Supports Guardant Sign/Time and Guardant Code dongles.
Old keys Stealth II and Stealth III are not supported here
(check WINE@Etersoft 2.x to get support).
%endif

%prep
%setup
%if_with buildwow64
cp -a grdwine grdwine_wow64
%endif

%build
%make_build -C grdwine \
    LIBDIR=%_libdir \
%if_with pebuild
    TARGETDLL=grdwine.dll \
%else
    TARGETDLL="grdwine.dll grdwine.dll.so" \
%endif
    %nil

%if_with buildwow64
%make_build -C grdwine_wow64 \
    LIBDIR=%_libdir \
    WOW64BUILD=yes \
    TARGETDLL=grdwine.dll \
    grdwine.dll
    %nil
%endif

%install
mkdir -p %buildroot%libwinedir/{%winesodir,%winepedir}

cp grdwine/grdwine.so %buildroot%libwinedir/%winesodir
cp grdwine/grdwine.dll %buildroot%libwinedir/%winepedir
%if_with buildwow64
mkdir -p %buildroot%libwinedir/%winepe32dir
cp grdwine_wow64/grdwine.dll %buildroot%libwinedir/%winepe32dir
%endif

%if_without pebuild
cp grdwine/grdwine.dll.so %buildroot%libwinedir/%winesodir
%endif

%if_with build64
install -D -m0644 %SOURCE1 %buildroot%_udevrulesdir/90-grdnt.rules
%endif

%files -n %winepkgname
%libwinedir/%winesodir/grdwine.so
%libwinedir/%winepedir/grdwine.dll
%if_with buildwow64
%libwinedir/%winepe32dir/grdwine.dll
%endif
%if_without pebuild
%libwinedir/%winesodir/grdwine.dll.so
%endif
%if_with build64
%_udevrulesdir/*.rules
%endif

%changelog
* Thu Sep 18 2025 Vitaly Lipatov <lav@altlinux.ru> 0.5.7.3-alt1
- build with wow64 support

* Wed May 22 2024 Vitaly Lipatov <lav@altlinux.ru> 0.5.7.2-alt1
- added guardant Stealth 2 support (eterbug #17339)

* Sat May 20 2023 Vitaly Lipatov <lav@altlinux.ru> 0.5.7.1-alt2
- disable LTO for Fedora too

* Sat Oct 29 2022 Vitaly Lipatov <lav@altlinux.ru> 0.5.7.1-alt1
- update to 0.5.7
- move code changes to patches

* Sun Aug 14 2022 Vitaly Lipatov <lav@altlinux.ru> 0.5.5.1-alt4
- put dlls to _libdir/wine-etersoft

* Thu Jun 09 2022 Vitaly Lipatov <lav@altlinux.ru> 0.5.5.1-alt3
- add udev rules to get correct permissions
- build 32 bit package as wine32-grdwine

* Sat Apr 09 2022 Vitaly Lipatov <lav@altlinux.ru> 0.5.5.1-alt2
- build and pack wine stub
- disable LTO (for a time)

* Thu Apr 01 2021 Vitaly Lipatov <lav@altlinux.ru> 0.5.5.1-alt1
- new version 0.5.5.1 (with rpmrb script)
 + fix build with wine since 6.4
- change download URL

* Tue Jun 23 2020 Vitaly Lipatov <lav@altlinux.ru> 0.5.5-alt2
- add AC_SYS_LARGEFILE to configure.ac

* Thu May 30 2019 Konstantin Kondratyuk <kondratyuk@altlinux.org> 0.5.5-alt1
- new version (0.5.5) with rpmgs script

