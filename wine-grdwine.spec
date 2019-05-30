Name: wine-grdwine
Version: 0.5.5
Release: alt1

Summary: Guardant usb dongle helper library for Wine
License: LGPLv2
Group: Emulators

Url: https://guardant.com
Packager: Konstantin Kondratyuk <kondratyuk@altlinux.org>

# Source-url: ftp://ftp.guardant.ru/support/linux/grdwine-%version.tar.gz
Source: %name-%version.tar

%description
Guardant usb dongle helper library for Wine. Implementation of the GrdWine is based on Linux USB Device Filesystem and Linux USB HID Device Interface.

%prep
%setup

%build
%configure \
	--with-wineincs=/usr/include \
	--with-winedlls=/usr/lib/wine

%make_build

%install
%makeinstall_std

%files

%changelog
* Thu May 30 2019 Konstantin Kondratyuk <kondratyuk@altlinux.org> 0.5.5-alt1
- new version (0.5.5) with rpmgs script

