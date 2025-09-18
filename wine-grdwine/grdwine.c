/*
 * GrdWine - Guardant usb dongle helper library for Wine
 *
 * Copyright (C) 2008 Aktiv Co. (Aleksey Samsonov)
 * Copyright (C) 2025 Dmitry Timoshkov for Etersoft
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
 */

#include <stddef.h>
#include <stdarg.h> /* for #include "winbase.h" */
#include <stdlib.h>

#include "ntstatus.h"
#define WIN32_NO_STATUS
#include "windef.h"     /* <wine/windows/windef.h> */
#include "winbase.h"    /* <wine/windows/winbase.h> */
#include "winnt.h"      /* <wine/windows/winnt.h> */
#include "wine/debug.h" /* <wine/debug.h> */
#include "grdimpl.h"

#define GRD_DRIVER_VERSION      0x0540

WINE_DEFAULT_DEBUG_CHANNEL(grdwine);

typedef BOOL (__attribute__((ms_abi)) * GrdWine_SearchUsbDevices_Callback)(LPCSTR lpDevName, LPVOID lpParam);

DWORD WINAPI GrdWine_GetVersion(void)
{
    TRACE("() Version 0x%x\n", GRD_DRIVER_VERSION);
    return GRD_DRIVER_VERSION;
}

DWORD WINAPI GrdWine_SearchUsbDevices(GrdWine_SearchUsbDevices_Callback func, LPVOID param)
{
    struct grd_search_usb_devices_params params;
    NTSTATUS status;
    ULONG i, count = 0;
    int ret;

    TRACE("(%p, %p)\n", func, param);
    if (!func || !param)
        return 0;

    params.max_count = 256;

    for (;;)
    {
        params.count = 0;
        params.dev_path = malloc(params.max_count * sizeof(params.dev_path[0]));
        if (!params.dev_path) return 0;

        TRACE("Call search_usb_devices()\n");
        status = GRD_CALL(grd_search_usb_devices, &params);
        TRACE("Ret search_usb_devices %#lx\n", status);
        if (status != STATUS_BUFFER_TOO_SMALL) break;
        free(params.dev_path);
        params.max_count = params.count;
    }

    if (status == STATUS_SUCCESS)
    {
        for (i = 0; i < params.count; i++)
        {
            TRACE("Call callback(%s,%p)\n", debugstr_a(params.dev_path[i].path), param);
            ret = func(params.dev_path[i].path, param);
            if (ret) count++;
            TRACE("Ret callback %d\n", ret);
        }

        free(params.dev_path);
    }

    return status == STATUS_SUCCESS ? count : 0;
}

BOOL WINAPI GrdWine_DeviceProbe(LPCSTR path, LPDWORD prod_id)
{
    struct grd_probe_device_params params = { path, prod_id };
    NTSTATUS status;

    TRACE("(%s, %p)\n", debugstr_a(path), prod_id);
    if (!path || !prod_id)
        return FALSE;

    TRACE("Call grd_probe_device(%s, %p)\n", debugstr_a(path), prod_id);
    status = GRD_CALL(grd_probe_device, &params);
    TRACE("Ret grd_probe_device %#lx\n", status);

    return status == STATUS_SUCCESS ? TRUE : FALSE;
}

BOOL WINAPI GrdWine_DeviceIoctl(LPCSTR dev_path, DWORD prod_id, DWORD pack_size,
                                LPVOID in, DWORD in_size, LPVOID out, DWORD out_size)
{
    NTSTATUS status;
    struct grd_ioctl_device_params params = { dev_path, prod_id, pack_size, in, in_size, out, out_size };

    TRACE("(%s, %lu, %lu, %p, %lu, %p, %lu)\n",  debugstr_a(dev_path), prod_id, pack_size, in, in_size, out, out_size);
    if (!dev_path || !in || !out)
        return FALSE;

    TRACE("Call grd_ioctl_device(%s, %lu, %lu, %p, %lu, %p, %lu)\n",
          debugstr_a(dev_path), prod_id, pack_size, in, in_size, out, out_size);
    status = GRD_CALL(grd_ioctl_device, &params);
    TRACE("Ret grd_ioctl_device %#lx\n", status);

    return status == STATUS_SUCCESS ? TRUE : FALSE;
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    TRACE("(%p, %lu, %p)\n", hinstDLL, fdwReason, lpvReserved);

    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        DisableThreadLibraryCalls(hinstDLL);
        if (__wine_init_unix_call()) return FALSE;
        break;
    }
    return TRUE;
}
