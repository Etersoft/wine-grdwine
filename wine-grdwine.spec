# TODO:
%define optflags_lto %nil

Name: wine-etersoft-grdwine
Version: 0.5.5.1
Release: alt4

Summary: Guardant usb dongle helper library for Wine

License: LGPLv2
Group: Emulators
Url: https://guardant.com

#Source-url: ftp://ftp.guardant.ru/support/linux/grdwine-%version.tar.gz
# Source-url: https://github.com/Etersoft/grdwine/archive/refs/tags/v%version.tar.gz
Source: %name-%version.tar

Source1: 90-grdnt.rules

BuildRequires: libwine-devel >= 6.23

ExclusiveArch: %ix86 x86_64

%ifarch x86_64 aarch64
  %def_with build64
  %define winepkgname wine-etersoft-grdwine
%else
  %def_without build64
  %define winepkgname wine32-etersoft-grdwine
%endif


%define libwinedir %_libdir/wine-etersoft

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

%add_verify_elf_skiplist %libwinedir/%winesodir/grdwine.dll.so

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

%build
#autoreconf
./bootstrap.sh

%if_with build64
%configure \
	--enable-win64 \
%else
%configure \
%endif
	--with-wineincs=%_includedir \
	--with-wineso=%buildroot/%libwinedir/%winesodir \
	--with-winepe=%buildroot/%libwinedir/%winepedir

%make_build

%install
%makeinstall_std
%if_with build64
install -D -m0644 %SOURCE1 %buildroot%_udevrulesdir/90-grdnt.rules
%endif

%files -n %winepkgname
%libwinedir/%winesodir/grdwine.dll.so
%libwinedir/%winepedir/grdwine.dll
%if_with build64
%_udevrulesdir/*.rules
%endif

%changelog
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

