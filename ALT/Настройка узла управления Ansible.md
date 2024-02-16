# Настройка узла управления Ansible

Задача: настройка узла управления Ansible

a)	Настройте узел управления на базе SRV-BR

  a.	Установите Ansible.

b)	Сконфигурируйте инвентарь по пути /etc/ansible/inventory. Инвентарь должен содержать три группы устройств:

  a.	Networking

  b.	Servers

  c.	Clients

c)	Напишите плейбук в /etc/ansible/gathering.yml для сбора информации об IP адресах и именах всех устройств (и клиенты, и серверы, и роутеры). Отчет должен быть сохранен в /etc/ansible/output.yaml, в формате ПОЛНОЕ_ДОМЕННОЕ_ИМЯ – АДРЕС

Установим ansible:

``` bash
apt-get update && apt-get install -y ansible sshpass
``` 

Создаем и открываем плейбук:

``` bash 
nano /etc/ansible/inventory
```

Создадим плейбук:

``` bash
nano /etc/ansible/gathering.ym
```

``` bash
---
- name: Gather information about devices
  hosts: all
  tasks:
    - name: Gather IP addresses and hostnames
      debug:
        msg: "{{ inventory_hostname }} - {{ hostvars[inventory_hostname]['ansible_host'] }}"
  gather_facts: no
```


