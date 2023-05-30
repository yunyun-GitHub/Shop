#!/bin/bash
# 切換到項目根目錄
cd /Server/
config="./deployment/server.conf"

# 读取migrate的值
migrate=$(sed -n 's/^migrate=//p' "${config}")
# 判断migrate的值是否为True
if [ "${migrate}" == "True" ]; then
  # 如果是True，修改migrate的值为False
  sed -i 's/^migrate=.*/migrate=False/' "${config}"
  # 同步到数据库中
  python manage.py migrate
fi

# 执行command选项的参数
exec "$@"