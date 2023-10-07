# Проект

## Для работы форматирования и линтнга необходимо выполнить следующие шаги:

Установить расширения для VS Code `ms-python.isort`, `VisualStudioExptTeam.vscodeintellicode`, `ms-python.python`, `ms-python.pylint`, `ms-python.autopep8`

Установить зависимости из файла `reqs.txt`(не забыть выбрать необходимый интерпретатор python в настройках vs code)

```sh
pip install -r reqs.txt
```

## Выпуск сертификата

Для выпуска сертификата используется такая команда

```sh
docker run -it --rm -p 80:80 --name certbot -v "/etc/letsencrypt:/etc/letsencrypt" -v "/var/lib/letsencrypt:/var/lib/letsencrypt" certbot/certbot certonly --standalone -d pixreceipt.ru --register-unsafely-without-email --agree-tos
```

## Может быть полезно

Удалить все второстепенные папки указанные в соответствии с `.gitignore`:

> Не забудьте сохранить .env файл если он имеется в проекте

```sh
git clean -f -X -d
```

Поменять файлы проекта и запустить его на удаленном сервере можно с помощью скрипта `deploy-to-server.sh` запустив:

```sh
/bin/bash deploy-to-server.sh
```

> Скорее всего вам нужно будет также установить **sshpass** - `brew install hudochenkov/sshpass/sshpass`

Чистка docker - если хотите заново развернуть backend

```sh
docker rm $(docker ps -aq)
docker volume rm $(docker volume ls -q)
docker image prune
docker builder prune
docker container prune
docker system prune
docker rmi --force $(docker images -aq)
docker system prune --all --force --volumes
```

Лучший вариант

```sh
systemctl stop docker && rm -rf /var/lib/docker && systemctl start docker
```

Если `docker compose down` не отключает network: `docker-compose down --remove-orphans`
Список занятых портов: `sudo netstat -ltupan`

> `docker: open /var/lib/docker/tmp/GetImageBlob180706573: no such file or directory.`
> Решение: `systemctl restart docker`

Войти в запущенный докер процесс

```sh
docker ps
docker exec -it CONTAINER_ID bash
```
