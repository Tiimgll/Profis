# PostgreSQL - настройка репликации и заполнение баз тестовыми даннымию

Задача:
Установка и настройка сервера баз данных

1) В качестве серверов баз данных используйте сервера SRV-HQ и SRVBR
2) Разверните сервер баз данных на базе Postgresql
    a. Создайте базы данных prod, test, dev
        * Заполните базы данных тестовыми данными при помощи утилиты pgbench. Коэффицент масштабирования сохраните по умолчанию.
    b. Создайте пользователей produser, testuser, devuser, каждому из пользователей дайте доступ к соответствующей базе данных.
    c. Разрешите внешние подключения для всех пользователей.
    d. Сконфигурируйте репликацию с SRV-HQ на SRV-BR


### SVR-HQ:
Установка пакетов базы данных:

``` bash
apt-get install -y postgresql16 postgresql16-server postgresql16-contrib
```

Создаём системные базы данных:

``` bash
/etc/init.d/postgresql initdb
```
![screen1]()

Включаем и добавляе в автозагрузку PostgreSQL:

``` bash
systemctl enable --now postgresql
```

Разрешаем доступ к PostgreSQL из сети:

``` bash
vim /var/lib/pgsql/data/postgresql.conf
```

в конфигурационном файле находим строку **"listen_addresses = 'localhost'"** и приводим её к следующему виду:

![screen2]()

Перезапускаем PostgreSQL:

``` bash
systemctl restart postgresql
```

Проверяем:

![screen3]()