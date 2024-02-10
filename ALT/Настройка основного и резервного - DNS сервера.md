# Настройка основного и резервного - DNS сервера

Задача: настройка DNS для SRV-HQ и SRV-BR

1. Реализуйте основной DNS сервер компании на SRV-HQ

    a. Для всех устройств обоих офисов необходимо создать записи A и PTR.
    
    b. Для всех сервисов предприятия необходимо создать записи CNAME
    
    d. Сконфигурируйте SRV-BR, как резервный DNS сервер. Загрузка записей с SRV-HQ должна быть разрешена только для SRV-BR


## SRV-HQ:

Устанавливаем пакет bind и bind-utils:

``` bash
apt-get update && apt-get install -y bind bind-utils
```

Редактируем конфигурационный файл по пути **"/etc/bind/options.conf"**:

``` bash
nano /etc/bind/options.conf
```

![screen1](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/1.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

>[!NOTE]
>listen-on { any; }; - Этот параметр определяет адреса и порты, на которых DNS-сервер будет слушать запросы. Значение any означает, что сервер будет прослушивать запросы на всех доступных интерфейсах и IP-адресах.

>[!NOTE]
>allow-query { any; }; -  Определяет список IP-адресов или подсетей, которым разрешено отправлять запросы на этот DNS-сервер. Значение any позволяет принимать запросы от всех клиентов.

>[!NOTE]
>allow-transfer { 10.0.20.2; }; - устанавливает возможность передачи зон для slave-серверов.

Правим конфигурационный файл **"/etc/net/ifaces/ens33/resolv.conf"**:

``` bash
nano /etc/net/ifaces/enp0s3/resolv.conf
```

``` bash
search company.prof
nameserver 127.0.0.1
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

![screen2](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/2.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

Созданиём зону прямого просмотра и обратного просмотра, добавляем в конфигурационный файл **"/etc/bind/local.conf"**:

``` bash
nano /etc/bind/local.conf
```

![screen3](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/3.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

>[!NOTE]
>zone "..." { ... }; : Это начало определения зоны. В кавычках указывается имя зоны, которое следует разрешать на этом сервере.

>[!NOTE]
>type master; : Это указывает тип зоны. "type master" означает, что эта зона является мастер-зоной, то есть она содержит авторитетные записи, которые могут быть изменены и обновлены на этом сервере.

>[!NOTE]
>file "..."; : Это указывает путь к файлу, который содержит данные зоны. Файлы данных зоны используются для хранения записей DNS, таких как A-записи, CNAME-записи, MX-записи и т. д.

Копируем пример прямой зоны:

``` bash
cp /etc/bind/zone/{localdomain,company.db}
```

Копируем пример для зоны обратного просмотра:

``` bash
cp /etc/bind/zone/127.in-addr.arpa /etc/bind/zone/10.0.10.in-addr.arpa.db
```
``` bash
cp /etc/bind/zone/127.in-addr.arpa /etc/bind/zone/20.0.10.in-addr.arpa.db
```

Задаём права - назначаем владельца:

``` bash
chown root:named /etc/bind/zone/company.db
```
``` bash
chown root:named /etc/bind/zone/10.0.10.in-addr.arpa.db
```
``` bash
chown root:named /etc/bind/zone/20.0.10.in-addr.arpa.db
```

Настраиваем зону прямого просмотра:

``` bash
nano /etc/bind/zone/company.db
```

![screen4](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/4.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

>[!NOTE]
>Запись типа NS определяет авторитетные DNS-серверы для определенной зоны.

>[!NOTE]
>Запись типа A связывает доменное имя с IPv4-адресом. Она используется для преобразования доменного имени в соответствующий IP-адрес.

>[!NOTE]
>Запись типа CNAME используется для создания псевдонима (алиаса) для другого доменного имени. Она указывает, что одно доменное имя является псевдонимом (алиасом) для другого "канонического" доменного имени.

Настраиваем зону прямого просмотра для сети 10.0.10.0/24:

``` bash
nano /etc/bind/zone/10.0.10.in-addr.arpa.db
```

![screen5](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/5.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

Настраиваем зону прямого просмотра для сети 10.0.20.0/24:

``` bash 
nano /etc/bind/zone/20.0.10.in-addr.arpa.db
```

![screen6](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/6.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

Утилитой **"named-checkconf"** с ключём **"-z"** проверяем что файл зон не содержитат ошибок и загружаются:

![screen7](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/7.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

Перезагружаем службу bind:

``` bash
systemctl restart bind
```

Проверяем зону прямого просмотра:

![screen8](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/8.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

Зоны обратного просмотра:

![screen9](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/9.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)


## SRV-BR:
Настраиваем как резервный DNS сервер

Устанавливаем пакет **bind** и **bind-utils**:

``` bash
apt-get update && apt-get install -y bind bind-utils
```

Редактируем конфигурационный файл по пути **"/etc/bind/options.conf":**

``` bash
nano /etc/bind/options.conf
```

![screen10](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/10.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

добавляем в конфигурационный файл **"/etc/bind/local.conf"** следующую информацию:

``` bash
nano /etc/bind/local.conf
```

![screen11](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/11.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

Правим конфигурационный файл "/etc/net/ifaces/ens33/resolv.conf":

``` bash
cat <<EOF > /etc/net/ifaces/ens33/resolv.conf
search company.prof
nameserver 10.0.10.2
nameserver 10.0.20.2
EOF
```

Перезапускаем службу **network**:

``` bash
systemctl restart network
```

Выполняем запуск и добавление в автозагрузку DNS - сервера:

``` bash
systemctl enable --now bind
```

Чтобы bind работал в режиме **SLAVE**, нужно выполнить:

``` bash
control bind-slave enabled
```

Должны появиться файлы зон по пути **"/etc/bind/zone/slave/"**:

![screen12](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/12.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)

работоспособность с CLI-BR:

![screen13](https://github.com/Tiimgll/Profis/blob/main/pic/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0/13.%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE%20-%20DNS%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0.png)
