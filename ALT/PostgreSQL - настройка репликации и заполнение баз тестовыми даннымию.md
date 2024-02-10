# PostgreSQL - настройка репликации и заполнение баз тестовыми даннымию

Задача:

Установка и настройка сервера баз данных

1) В качестве серверов баз данных используйте сервера SRV-HQ и SRV-BR
2) Разверните сервер баз данных на базе Postgresql
    
    a. Создайте базы данных prod, test, dev. Заполните базы данных тестовыми данными при помощи утилиты pgbench. Коэффицент масштабирования сохраните по умолчанию.
    
    b. Создайте пользователей produser, testuser, devuser, каждому из пользователей дайте доступ к соответствующей базе данных.
    
    c. Разрешите внешние подключения для всех пользователей.
    
    d. Сконфигурируйте репликацию с SRV-HQ на SRV-BR


## SVR-HQ:
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
nano /var/lib/pgsql/data/postgresql.conf
```

в конфигурационном файле находим строку **"listen_addresses = 'localhost'"** и приводим её к следующему виду:

![screen2](https://github.com/Tiimgll/Profis/blob/main/pic/2.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

Перезапускаем PostgreSQL:

``` bash
systemctl restart postgresql
```

Проверяем:

![screen3](https://github.com/Tiimgll/Profis/blob/main/pic/3.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

### Создаём базы данных и пользователей с необходимыми правами:
Для заведения пользователей и создания баз данных, необходимо 
переключиться в учётную запись "postgres":

``` bash
psql -U postgres
```

![screen4](https://github.com/Tiimgll/Profis/blob/main/pic/4.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

зададим пароль для пользователя "postgres":

``` bash
ALTER USER postgres WITH ENCRYPTED PASSWORD 'P@ssw0rd';
```

Создаём базы данных "prod","test" и "dev":

``` bash
CREATE DATABASE prod;
```
``` bash
CREATE DATABASE test;
```
``` bash
CREATE DATABASE dev;
```

Создаём пользователей "produser","testuser" и "devuser":

``` bash
CREATE USER produser WITH PASSWORD 'P@ssw0rd';
```
``` bash
CREATE USER testuser WITH PASSWORD 'P@ssw0rd';
```
``` bash
CREATE USER devuser WITH PASSWORD 'P@ssw0rd';
```

Назначаем для каждой базы данных соответствующего владельца:

для базы данных "prod" назначаем владельцем пользователя "produser":

``` bash
GRANT ALL PRIVILEGES ON DATABASE prod to produser;
```

для базы данных "test" назначаем владельцем пользователя "testuser":

``` bash
GRANT ALL PRIVILEGES ON DATABASE test to testuser;
```

для базы данных "dev" назначаем владельцем пользователя "devuser":

``` bash
GRANT ALL PRIVILEGES ON DATABASE dev to devuser;
```

Выйти из учет записи "Postgres"

``` bash
\q
```

Заполняем базы данных тестовыми данными при помощи утилиты pgbench:

``` bash
pgbench -U postgres -i prod
```
``` bash
pgbench -U postgres -i test
```
``` bash
pgbench -U postgres -i dev
```

Проверяем:

``` bash
psql -U postgres
```
``` bash
\c prod
```
``` bash
\dt+
```

![screen5](https://github.com/Tiimgll/Profis/blob/main/pic/5.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

Аналогично и для других баз данных:

![screen6](https://github.com/Tiimgll/Profis/blob/main/pic/6.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

Выйти из учет записи "prod"

``` bash
\q
```

Настраиваем парольную аутентификацию для удалённого доступа:

``` bash
nano /var/lib/pgsql/data/pg_hba.conf
```

добавляем следующую запись:

![screen7](https://github.com/Tiimgll/Profis/blob/main/pic/7.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

перезапускаем PostgreSQL:

``` bash
systemctl restart postgresql
```

## SRV-BR:
Установка пакетов базы данных:

``` bash
apt-get install -y postgresql16 postgresql16-server postgresql16-contrib
```

Проверяем, подключаемся с SRV-BR к SRV-HQ:

Из под пользователя "produser" к базе данных "prod":

![screen8](https://github.com/Tiimgll/Profis/blob/main/pic/8.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

Из под пользователя "testuser" к базе данных "test":

![screen9](https://github.com/Tiimgll/Profis/blob/main/pic/9.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

Из под пользователя "devuser" к базе данных "dev":

![screen10](https://github.com/Tiimgll/Profis/blob/main/pic/10.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

## Настраиваем репликацию с SRV-HQ на SRV-BR:

## SRV-HQ:

Открываем конфигурационный файл **"/var/lib/pgsql/data/postgresql.conf"**:

``` bash
nano /var/lib/pgsql/data/postgresql.conf
```

Редактируем следующие параметры:

![screen11](https://github.com/Tiimgll/Profis/blob/main/pic/11.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

![screen12](https://github.com/Tiimgll/Profis/blob/main/pic/12.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

![screen13](https://github.com/Tiimgll/Profis/blob/main/pic/13.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

![screen14](https://github.com/Tiimgll/Profis/blob/main/pic/14.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

>[!NOTE]
>wal_level указывает, сколько информации записывается в WAL (журнал операций, который используется для репликации);

>[!NOTE]
>max_wal_senders — количество планируемых слейвов;

>[!NOTE]
>max_replication_slots — максимальное число слотов репликации; 

>[!NOTE]
>hot_standby — определяет, можно или нет подключаться к postgresql для выполнения запросов в процессе восстановления;

>[!NOTE]
>hot_standby_feedback — определяет, будет или нет сервер slave сообщать мастеру о запросах, которые он выполняет.


Перезапускаем службу postgresql:

``` bash
systemctl restart postgresql
```
## SRV-BR:
Останавливаем службу postgres:

``` bash
systemctl stop postgresql
```

Удаляем содержимое каталога с данными:

``` bash
rm -rf /var/lib/pgsql/data/*
```

И реплицируем данные с SRV-HQ сервера:

``` bash
pg_basebackup -h 10.0.10.2 -U postgres -D /var/lib/pgsql/data --wal-method=stream --write-recovery-conf
```

![screen15]()

Назначаем владельца:

``` bash
chown -R postgres:postgres /var/lib/pgsql/data/
```

Снова запускаем сервис postgresql:

``` bash
systemctl start postgresql
```

## Проверяем репликацию:
## SRV-HQ:
Создаём тестовую базу данных:

``` bash
psql -U postgres
```

``` bash
CREATE DATABASE test_replica;
```

![screen16](https://github.com/Tiimgll/Profis/blob/main/pic/16.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)

## SRV-BR:
Смотрим список всех баз данных:

![screen17](https://github.com/Tiimgll/Profis/blob/main/pic/17.PostgreSQL%20-%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%B0%D0%B7%20%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%D1%8E.png)
