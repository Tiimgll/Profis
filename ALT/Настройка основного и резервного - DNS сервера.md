# Настройка основного и резервного - DNS сервера

Задача: настройка DNS для SRV-HQ и SRV-BR

i. Реализуйте основной DNS сервер компании на SRV-HQ
a. Для всех устройств обоих офисов необходимо создать записи A и PTR.
b. Для всех сервисов предприятия необходимо создать записи CNAME
d. Сконфигурируйте SRV-BR, как резервный DNS сервер. Загрузка записей с SRV-HQ должна быть разрешена только для SRV-BR


### SRV-HQ:

Устанавливаем пакет bind и bind-utils:

``` bash
apt-get update && apt-get install -y bind bind-utils
```

Редактируем конфигурационный файл по пути **"/etc/bind/options.conf"**:

``` bash
nano /etc/bind/options.conf
```

>[!ПРИМЕЧАНИЕ]
>listen-on { any; }; - Этот параметр определяет адреса и порты, на которых DNS-сервер будет слушать запросы. Значение any означает, что сервер будет прослушивать запросы на всех доступных интерфейсах и IP-адресах.

>allow-query { any; }; -  Определяет список IP-адресов или подсетей, которым разрешено отправлять запросы на этот DNS-сервер. Значение any позволяет принимать запросы от всех клиентов.

>allow-transfer { 10.0.20.2; }; - устанавливает возможность передачи зон для slave-серверов.

Правим конфигурационный файл **"/etc/net/ifaces/ens33/resolv.conf"**:

``` bash
cat <<EOF > /etc/net/ifaces/ens33/resolv.conf
search company.prof
nameserver 127.0.0.1
EOF
```

Перезапускаем службу network:

``` bash
systemctl restart network
```

Выполняем запуск и добавление в автозагрузку DNS - сервера:

``` bash
systemctl enable --now bind
```

Проверяем:

``` bash 
ping ya.ru
```

Созданиём зону прямого просмотра и обратного просмотра, добавляем в конфигурационный файл **"/etc/bind/local.conf"**:

``` bash
nano /etc/bind/local.conf
```

>[!ПРИМЕЧАНИЕ]
>zone "..." { ... }; : Это начало определения зоны. В кавычках указывается имя зоны, которое следует разрешать на этом сервере.

>type master; : Это указывает тип зоны. "type master" означает, что эта зона является мастер-зоной, то есть она содержит авторитетные записи, которые могут быть изменены и обновлены на этом сервере.

>file "..."; : Это указывает путь к файлу, который содержит данные зоны. Файлы данных зоны используются для хранения записей DNS, таких как A-записи, CNAME-записи, MX-записи и т. д.

Копируем пример прямой зоны:

``` bash
cp /etc/bind/zone/{localdomain,company.db}
```

Копируем пример для зоны обратного просмотра:

``` bash
cp /etc/bind/zone/127.in-addr.arpa /etc/bind/zone/10.0.10.in-addr.arpa.db
cp /etc/bind/zone/127.in-addr.arpa /etc/bind/zone/20.0.10.in-addr.arpa.db
```

Задаём права - назначаем владельца:

``` bash
chown root:named /etc/bind/zone/company.db
chown root:named /etc/bind/zone/10.0.10.in-addr.arpa.db
chown root:named /etc/bind/zone/20.0.10.in-addr.arpa.db
```

Настраиваем зону прямого просмотра:

``` bash
nano /etc/bind/zone/company.db
```