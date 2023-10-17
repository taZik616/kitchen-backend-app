#!/bin/bash

# Проверяем наличие файла .env
if [ ! -f .env ]; then
  echo "Файл .env не найден. Пожалуйста, создайте файл .env и укажите в нем переменные SSH_USER, SSH_HOST и SSH_PROJECT_PATH."
  exit 1
fi

source .env

# Архивируем текущую директорию и передаем архив через ssh, затем распаковываем на удаленном сервере
# Как я понял после кучи попыток tar и zip утилиты очень отвратительно работают со исключением файлов и папок.
# Если я например пишу --exclude='./static', то не корневая папка static уберется, а все папки static,
# а если я буду использовать полный путь --exclude="$projDir/static" то вообще не исключается папка) 🫠
tar cz --no-xattrs --no-mac-metadata \
  --exclude='.git' --exclude='.vscode' --exclude='migrations' \
  --exclude='static' --exclude='__pycache__' --exclude='media' . | \
sshpass -p "$SSH_PASSWORD" ssh "$SSH_USER"@"$SSH_HOST" \
  "mkdir -p $SSH_PROJECT_PATH && tar xz -C $SSH_PROJECT_PATH"

# Подключаемся к удаленному серверу и выполняем остальные команды в одном ssh-соединении
sshpass -p "$SSH_PASSWORD" ssh "$SSH_USER"@"$SSH_HOST" "
  # Проверяем наличие Docker на удаленном сервере
  which docker > /dev/null 2>&1
  DOCKER_EXISTS=$?

  if [ \$DOCKER_EXISTS -eq 0 ]; then
    echo 'Docker установлен. Выполняем необходимые команды.'

    cd $SSH_PROJECT_PATH && docker compose -f docker-compose-server.yml up --build -d --force-recreate
  else
    echo 'Docker не установлен. Пожалуйста, установите Docker на сервере.'
  fi
"
exit 0