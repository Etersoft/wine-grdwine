MODULE   = grdwine.dll
UNIXLIB  = grdwine.so

CROSSBUILD =
WOW64BUILD =

LIBDIR = /usr/lib
#LIBDIR = /usr/lib/x86_64-linux-gnu

ifeq ($(shell echo $(LIBDIR) | grep -q 64 && echo -n x86_64),x86_64)
WINEARCH = x86_64-windows
UNIXARCH = x86_64-unix
else
WINEARCH = i686-windows
UNIXARCH = i386-unix
ifeq ($(shell arch),x86_64)
CROSSBUILD = -m32
endif
endif

ifeq ($(WOW64BUILD),yes)
WINEARCH = i686-windows
UNIXARCH =
ifeq ($(shell arch),x86_64)
CROSSBUILD = -m32
endif
endif

UNIXGCC  = gcc $(CROSSBUILD) -DWINE_UNIX_LIB -fPIC -I/usr/include/wine/windows

WINELIBDIR = $(LIBDIR)/wine-etersoft

#
ifeq ($(shell test -e $(WINELIBDIR)/$(UNIXARCH)/ntdll.dll.so || ! test "$(TARGETDLL)" = "grdwine.dll" && echo -n yes),yes)
WINEGCC = winegcc $(CROSSBUILD)
TARGETDLL=grdwine.dll.so
else
WINEGCC  = winegcc -b $(WINEARCH) -D__WINE_PE_BUILD
TARGETDLL=grdwine.dll
endif

CFLAGS   = -g -O2 -Wall -D__WINESRC__
IMPORTS  = ntdll kernel32 crypt32 advapi32
LIBS     = $(IMPORTS:%=-l%)
#UNIXLIBS = -ldl
UNIXLIBS = -ldl $(WINELIBDIR)/$(UNIXARCH)/ntdll.so
DEPS     = Makefile grdimpl.h
UNIXDEPS = Makefile grdimpl.h
OBJ      = grdwine.c grdwine.spec
UNIXOBJ  = grdimpl_linux.c

all: grdwine.so $(TARGETDLL)

%.cross.o: %.c $(DEPS)
	$(WINEGCC) -c -o $@ $< $(CFLAGS)

%.o: %.c $(UNIXDEPS)
	$(UNIXGCC) -c -o $@ $< $(CFLAGS)

grdwine.so: $(UNIXOBJ)
	$(UNIXGCC) -o $@ $^ -shared $(CFLAGS) $(UNIXLIBS)
	#strip $@

ifeq ($(TARGETDLL),grdwine.dll)
grdwine.dll: $(OBJ)
	$(WINEGCC) -o $@ $^ -shared -Wl,--wine-builtin $(CFLAGS) $(LIBS)
	#strip $@
else
grdwine.dll: grdwine.spec
	$(WINEGCC) -o $@ -Wb,--fake-module -shared $^ -mno-cygwin
endif

grdwine.dll.so: $(OBJ)
	$(WINEGCC) -o $@ $^ -shared -Wl,--wine-builtin $(CFLAGS) $(LIBS)
	#strip $@

clean:
	rm -f *.o *.so *.dll *.lib
