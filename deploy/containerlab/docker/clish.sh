#!/bin/sh
# root 的登录 shell：SSH 交互登录进入 vtysh（FRR CLI）；
# ssh root@<host> "show ..." 时以 vtysh -c 执行并退出。
if [ "$1" = "-c" ]; then
  shift
fi
if [ $# -gt 0 ]; then
  exec /usr/bin/vtysh -c "$*"
fi
exec /usr/bin/vtysh
