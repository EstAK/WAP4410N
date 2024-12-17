# How to perform the firmware extraction
## Uboot
the classical way is to dump the whole flash using `md <start> <size>` with `<size>` in DWORD *(for this device)* then process the `xxd` like output using a [script](../scripts/parse-uboot-dump.py).
1. connect to virtual terminal (GNU Screen will be assumed for the following)
2. interrupt the normal boot process and enter the uboot console
3. `bdinfo` should give enough information to perform the dump *([info](#Memories-locations))*
4. start your the screen log `CTRL + a + H` *(the terminal will be saved to `screenlog.0`)*
5. in your virtual terminal, `md 0xBF000000 2097152` *(this will take ~50 min)*
### Reconnaissance
#### Memories locations
the flash chip is a **MXIC-29LV640DBTC**

```sh
ar7100> bdinfo
boot_params = 0x81F63FB0
memstart    = 0x80000000
memsize     = 0x02000000
flashstart  = 0xBF000000
flashsize   = 0x00800000
flashoffset = 0x0002F690
ethaddr     = CC:EF:48:86:EB:04
ip_addr     = 192.168.1.10
baudrate    = 115200 bps
```
## Root console 
this system uses mtd partitions for the flash memory. To get the partition table, 

```sh
[VAP0 @ wap86eb04]# cat /proc/mtd
dev:    size   erasesize  name
mtd0: 00040000 00010000 "u-boot"
mtd1: 00010000 00010000 "u-boot-env"
mtd2: 00650000 00010000 "rootfs"
mtd3: 00140000 00010000 "uImage"
mtd4: 00010000 00010000 "nvram"
mtd5: 00010000 00010000 "calibration"
```

then to extract them either use the builtin `ftp` utilities and setup an `ftp` server on your computer or install a newer version of busybox and use `netcat`
### ftp
1. setup an `ftp` server on your computer 
2. upload the file to the server `busybox ftpput <computer ip> <remote-file> <local-file>`
### netcat
assuming that you have downloaded a newer version of busybox,
1. on the computer `nc -l 5555`
2. on the router `cat /dev/mtdblock* | busybox nc -u <computer ip> 5555 > firmware.bin`
