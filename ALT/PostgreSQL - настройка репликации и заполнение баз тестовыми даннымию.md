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
![screen1](https://github.com/Tiimgll/Profis/blob/main/pic/1.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

Включаем и добавляе в автозагрузку PostgreSQL:

``` bash
systemctl enable --now postgresql
```

Разрешаем доступ к PostgreSQL из сети:

``` bash
vim /var/lib/pgsql/data/postgresql.conf
```

в конфигурационном файле находим строку **"listen_addresses = 'localhost'"** и приводим её к следующему виду:

![screen2](https://github.com/Tiimgll/Profis/blob/main/pic/2.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

Перезапускаем PostgreSQL:

``` bash
systemctl restart postgresql
```

Проверяем:

![screen3](https://github.com/Tiimgll/Profis/blob/main/pic/3.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)