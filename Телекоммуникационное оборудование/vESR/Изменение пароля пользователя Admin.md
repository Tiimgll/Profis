# Изменение пароля пользователя «admin»

>[!NOTE]

>Стандартный (заводской) профиль:

>log: admin

>pass: password

Для смены пароля пользователя admin - можно воспользоваться следуюшими командами:

``` bash
configure
username admin
password P@ssw0rd
exit
```

Для применения настроек:

``` bash
do commit
do confirm
ёёё