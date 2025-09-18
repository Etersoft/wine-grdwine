/*
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

#ifndef GRDIMPL__H__
#define GRDIMPL__H__

#include "wine/unixlib.h"

typedef int __attribute__((ms_abi))
    (*search_usb_device_callback)(const char* path, void* param);

/*
 * Communication to device (which grd_probe_device returned zero).
 */
struct grd_ioctl_device_params
{
    const char *dev_path;
    ULONG prod_id;
    ULONG pack_size;
    void *in;
    ULONG in_size;
    void *out;
    ULONG out_size;
};

/*
 * Check device.
 * Return zero if device is Guardant Sign/Time or Guardant Code.
 */
struct grd_probe_device_params
{
    const char *dev_path;
    ULONG *prod_id;
};

/*
 * Search for all USB devices. Call callback function for each USB device.
 * Return the count of non-zero values which were returned from callback.
 */
struct grd_dev_path
{
    char path[MAX_PATH];
};
struct grd_search_usb_devices_params
{
    struct grd_dev_path *dev_path;
    ULONG max_count;
    ULONG count;
};

enum unix_funcs
{
    unix_grd_ioctl_device,
    unix_grd_probe_device,
    unix_grd_search_usb_devices,
    unix_funcs_count
};

#define GRD_CALL( func, params ) WINE_UNIX_CALL( unix_ ## func, params )

#endif /* !GRDIMPL__H__ */
