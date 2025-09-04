# Telegram-бот для продажи подписок Remnawave

Этот Telegram-бот предназначен для автоматизации продажи и управления подписками для панели **Remnawave**. Он интегрируется с API Remnawave для управления пользователями и подписками, а также использует различные платежные системы для приема платежей.

## ✨ Ключевые возможности

### Для пользователей:
-   **Принятие условий сервиса:** Обязательное принятие условий при первом запуске бота
-   **Регистрация и выбор языка:** Поддержка русского и английского языков
-   **Управление балансом:** Пополнение баланса через Tribute, оплата подписок с баланса
-   **Просмотр подписки:** Пользователи могут видеть статус своей подписки, дату окончания и ссылку на конфигурацию
-   **Пробная подписка:** Система пробных подписок для новых пользователей (активируется вручную по кнопке)
-   **Промокоды:** Возможность применять промокоды для получения скидок или бонусных дней
-   **Реферальная программа:** Пользователи могут приглашать друзей и получать за это бонусные дни подписки
-   **Оплата:** Поддержка оплаты через YooKassa, CryptoPay, Telegram Stars и Tribute
-   **Продление подписок:** Автоматическое продление существующих подписок при покупке новых

### Для администраторов:
-   **Защищенная админ-панель:** Доступ только для администраторов, указанных в `ADMIN_IDS`
-   **Управление балансом пользователей:** Пополнение, списание и установка баланса пользователей
-   **Статистика:** Просмотр статистики использования бота (общее количество пользователей, забаненные, активные подписки), недавние платежи и статус синхронизации с панелью
-   **Управление пользователями:** Блокировка/разблокировка пользователей, просмотр списка забаненных и детальной информации о пользователе
-   **Рассылка:** Отправка сообщений всем пользователям, пользователям с активной или истекшей подпиской
-   **Управление промокодами:** Создание, массовое создание и просмотр промокодов
-   **Синхронизация с панелью:** Ручной запуск синхронизации пользователей и подписок с панелью Remnawave
-   **Логи действий:** Просмотр логов всех действий пользователей
-   **Финансовая статистика:** Детальная статистика по доходам (день, неделя, месяц, все время)

## 🚀 Технологии

-   **Python 3.11**
-   **Aiogram 3.x:** Асинхронный фреймворк для Telegram ботов.
-   **aiohttp:** Для запуска веб-сервера (вебхуки).
-   **SQLAlchemy 2.x & asyncpg:** Асинхронная работа с базой данных PostgreSQL.
-   **YooKassa, aiocryptopay:** SDK для интеграции с платежными системами.
-   **Pydantic:** Для управления настройками из `.env` файла.
-   **Docker & Docker Compose:** Для контейнеризации и развертывания.

## ⚙️ Подробная установка и настройка

### 📋 Предварительные требования

**Системные требования:**
- Ubuntu 20.04+ / CentOS 8+ / Debian 11+ (или любая Linux-система)
- Минимум 2GB RAM, 10GB свободного места (рекомендуется 4GB+)
- Docker 20.10+ и Docker Compose 2.0+
- Домен с SSL-сертификатом (Let's Encrypt)
- Nginx (для обратного прокси)
- Python 3.11+ (для локальной разработки)

**Сервисы и токены:**
- Токен Telegram-бота (получить у [@BotFather](https://t.me/BotFather))
- Рабочая панель Remnawave с API доступом
- Настроенные платежные системы (YooKassa, CryptoPay, Tribute)
- VPS/сервер с публичным IP
- Настроенный почтовый сервер (для уведомлений)

**Рекомендации по безопасности:**
- Используйте сильные пароли для базы данных
- Регулярно обновляйте систему и зависимости
- Настройте файрвол (UFW/iptables)
- Используйте fail2ban для защиты от брутфорса
- Регулярно создавайте резервные копии базы данных

### 🚀 Пошаговая установка

#### Шаг 1: Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагрузка для применения изменений
sudo reboot
```

#### Шаг 2: Клонирование и настройка проекта

```bash
# Клонирование репозитория
git clone https://github.com/machka-pasla/remnawave-tg-shop.git
cd remnawave-tg-shop

# Создание файла конфигурации
cp .env.example .env
nano .env
```

#### Шаг 3: Настройка переменных окружения

**Основные настройки (обязательные):**

```env
# === ОСНОВНЫЕ НАСТРОЙКИ ===
BOT_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMIN_IDS=12345678,98765432
DEFAULT_LANGUAGE=ru
DISABLE_WELCOME_MESSAGE=false

# === ВЕБХУКИ ===
WEBHOOK_BASE_URL=https://your-domain.com
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8080

# === ПОДДЕРЖКА И ССЫЛКИ ===
SUPPORT_LINK=https://t.me/your_support
SUBSCRIPTION_MINI_APP_URL=https://t.me/your_bot/app
TERMS_OF_SERVICE_URL=https://your-domain.com/terms
SERVER_STATUS_URL=https://status.your-domain.com
```

**Настройки базы данных:**

```env
# === БАЗА ДАННЫХ ===
DATABASE_URL=postgresql+asyncpg://postgres:your_password@remnawave-tg-shop-db:5432/remnawave_tg_shop
POSTGRES_DB=remnawave_tg_shop
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
```

**Настройки платежных систем:**

```env
# === YOOKASSA ===
YOOKASSA_ENABLED=true
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key
YOOKASSA_PAYMENT_SUBJECT=service

# === CRYPTOPAY ===
CRYPTOPAY_ENABLED=true
CRYPTOPAY_TOKEN=your_cryptopay_token

# === TELEGRAM STARS ===
STARS_ENABLED=true

# === TRIBUTE ===
TRIBUTE_ENABLED=true
TRIBUTE_BALANCE_URL=https://t.me/tribute/app?startapp=your_app
TRIBUTE_SKIP_NOTIFICATIONS=false
```

**Настройки подписок:**

```env
# === ПОДПИСКИ ===
# 1 месяц
1_MONTH_ENABLED=true
RUB_PRICE_1_MONTH=150.0
STARS_PRICE_1_MONTH=150
TRIBUTE_LINK_1_MONTH=https://t.me/tribute/app?startapp=your_app_1m

# 3 месяца
3_MONTHS_ENABLED=true
RUB_PRICE_3_MONTHS=400.0
STARS_PRICE_3_MONTHS=400
TRIBUTE_LINK_3_MONTHS=https://t.me/tribute/app?startapp=your_app_3m

# 6 месяцев
6_MONTHS_ENABLED=true
RUB_PRICE_6_MONTHS=750.0
STARS_PRICE_6_MONTHS=750
TRIBUTE_LINK_6_MONTHS=https://t.me/tribute/app?startapp=your_app_6m

# 12 месяцев
12_MONTHS_ENABLED=true
RUB_PRICE_12_MONTHS=1400.0
STARS_PRICE_12_MONTHS=1400
TRIBUTE_LINK_12_MONTHS=https://t.me/tribute/app?startapp=your_app_12m
```

**Настройки панели Remnawave:**

```env
# === ПАНЕЛЬ REMNAWAVE ===
PANEL_API_URL=https://your-panel.com/api
PANEL_API_KEY=your_api_key
PANEL_WEBHOOK_SECRET=your_webhook_secret
USER_SQUAD_UUIDS=squad1,squad2
USER_TRAFFIC_LIMIT_GB=100
USER_TRAFFIC_STRATEGY=RESET
```

**Настройки пробного периода:**

```env
# === ПРОБНЫЙ ПЕРИОД ===
TRIAL_ENABLED=true
TRIAL_DURATION_DAYS=3
TRIAL_TRAFFIC_LIMIT_GB=10
```

#### Шаг 4: Настройка Nginx

Создайте конфигурацию Nginx:

```bash
sudo nano /etc/nginx/sites-available/remnawave-bot
```

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL сертификаты (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL настройки
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Вебхуки для платежных систем
    location /webhook/yookassa {
        proxy_pass http://localhost:8080/webhook/yookassa;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /webhook/cryptopay {
        proxy_pass http://localhost:8080/webhook/cryptopay;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /webhook/tribute {
        proxy_pass http://localhost:8080/webhook/tribute;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /webhook/panel {
        proxy_pass http://localhost:8080/webhook/panel;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Telegram webhook (динамический путь)
    location ~ ^/([0-9]+:[A-Za-z0-9_-]+)$ {
        proxy_pass http://localhost:8080/$1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Активируйте конфигурацию:

```bash
sudo ln -s /etc/nginx/sites-available/remnawave-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Шаг 5: Получение SSL сертификата

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получение сертификата
sudo certbot --nginx -d your-domain.com

# Автообновление сертификата
sudo crontab -e
# Добавьте строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Шаг 6: Запуск бота

```bash
# Сборка и запуск контейнеров
docker compose build --no-cache
docker compose up -d

# Проверка статуса
docker compose ps

# Просмотр логов
docker compose logs -f remnawave-tg-shop
```

#### Шаг 7: Миграция базы данных

```bash
# Запуск миграции для добавления поля terms_accepted
docker compose exec remnawave-tg-shop python migration_add_terms_accepted.py
```

#### Шаг 8: Проверка работы

```bash
# Проверка доступности вебхуков
curl -I https://your-domain.com/webhook/yookassa
curl -I https://your-domain.com/webhook/cryptopay
curl -I https://your-domain.com/webhook/tribute
curl -I https://your-domain.com/webhook/panel

# Проверка логов на ошибки
docker compose logs remnawave-tg-shop | grep ERROR
```

### 🔧 Полезные команды

```bash
# Перезапуск бота
docker compose restart remnawave-tg-shop

# Обновление бота
git pull
docker compose build --no-cache remnawave-tg-shop
docker compose up -d

# Просмотр логов в реальном времени
docker compose logs -f remnawave-tg-shop

# Подключение к контейнеру
docker compose exec remnawave-tg-shop bash

# Остановка всех сервисов
docker compose down

# Полная очистка (включая данные)
docker compose down -v
```

### 🚨 Устранение неполадок

**Проблема: 502 Bad Gateway**
```bash
# Проверьте, запущен ли контейнер
docker compose ps

# Проверьте логи
docker compose logs remnawave-tg-shop

# Перезапустите контейнер
docker compose restart remnawave-tg-shop
```

**Проблема: Вебхуки не работают**
```bash
# Проверьте конфигурацию Nginx
sudo nginx -t

# Проверьте доступность порта
netstat -tlnp | grep 8080

# Проверьте логи Nginx
sudo tail -f /var/log/nginx/error.log
```

**Проблема: Ошибки базы данных**
```bash
# Проверьте подключение к БД
docker compose exec remnawave-tg-shop-db psql -U postgres -d remnawave_tg_shop

# Запустите миграцию
docker compose exec remnawave-tg-shop python migration_add_terms_accepted.py
```

### 📊 Мониторинг

**Настройка мониторинга логов:**
```bash
# Установка logrotate для логов Docker
sudo nano /etc/logrotate.d/docker-compose
```

```
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
```

**Автоматический перезапуск при сбоях:**
```bash
# Добавьте в crontab
crontab -e

# Проверка каждые 5 минут
*/5 * * * * cd /path/to/remnawave-tg-shop && docker compose ps | grep -q "Up" || docker compose up -d
```

### 🔒 Настройка безопасности

**Настройка файрвола:**
```bash
# Установка UFW
sudo apt install ufw -y

# Базовые правила
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Разрешить SSH (замените 22 на ваш порт SSH)
sudo ufw allow 22

# Разрешить HTTP и HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Включить файрвол
sudo ufw enable
```

**Настройка fail2ban:**
```bash
# Установка fail2ban
sudo apt install fail2ban -y

# Создание конфигурации
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
```

**Создание резервных копий:**
```bash
# Создание скрипта резервного копирования
sudo nano /usr/local/bin/backup-bot.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/backups/remnawave-bot"
DATE=$(date +%Y%m%d_%H%M%S)

# Создание директории для бэкапов
mkdir -p $BACKUP_DIR

# Бэкап базы данных
docker compose exec -T remnawave-tg-shop-db pg_dump -U postgres remnawave_tg_shop > $BACKUP_DIR/db_backup_$DATE.sql

# Бэкап конфигурации
cp .env $BACKUP_DIR/env_backup_$DATE

# Удаление старых бэкапов (старше 7 дней)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "env_backup_*" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Сделать скрипт исполняемым
sudo chmod +x /usr/local/bin/backup-bot.sh

# Добавить в crontab (ежедневно в 2:00)
crontab -e
# Добавить строку:
# 0 2 * * * /usr/local/bin/backup-bot.sh
```

### 🔄 Обновление и обслуживание

**Автоматическое обновление:**
```bash
# Создание скрипта обновления
nano update-bot.sh
```

```bash
#!/bin/bash
cd /path/to/remnawave-tg-shop

# Создание бэкапа перед обновлением
/usr/local/bin/backup-bot.sh

# Обновление кода
git pull origin main

# Пересборка и перезапуск
docker compose build --no-cache
docker compose down
docker compose up -d

# Проверка статуса
sleep 10
docker compose ps

echo "Update completed"
```

**Мониторинг ресурсов:**
```bash
# Установка htop для мониторинга
sudo apt install htop -y

# Мониторинг логов в реальном времени
docker compose logs -f --tail=100 remnawave-tg-shop

# Проверка использования диска
df -h

# Проверка использования памяти
free -h
```

## 🐳 Docker

Файлы `Dockerfile` и `docker-compose.yml` уже настроены для сборки и запуска проекта. `docker-compose.yml` использует готовый образ с GitHub Container Registry, но вы можете раскомментировать `build: .` для локальной сборки.

## 📁 Структура проекта

```
.
├── bot/
│   ├── filters/          # Пользовательские фильтры Aiogram
│   ├── handlers/         # Обработчики сообщений и колбэков
│   ├── keyboards/        # Клавиатуры
│   ├── middlewares/      # Промежуточные слои (i18n, проверка бана)
│   ├── services/         # Бизнес-логика (платежи, API панели)
│   ├── states/           # Состояния FSM
│   └── main_bot.py       # Основная логика бота
├── config/
│   └── settings.py       # Настройки Pydantic
├── db/
│   ├── dal/              # Слой доступа к данным (DAL)
│   ├── database_setup.py # Настройка БД
│   └── models.py         # Модели SQLAlchemy
├── locales/              # Файлы локализации (ru, en)
├── .env.example          # Пример файла с переменными окружения
├── Dockerfile            # Инструкции для сборки Docker-образа
├── docker-compose.yml    # Файл для оркестрации контейнеров
├── requirements.txt      # Зависимости Python
└── main.py               # Точка входа в приложение
```

## 📖 Примеры использования

### Создание промокода
1. Зайдите в админ-панель бота
2. Выберите "Промокоды" → "Создать промокод"
3. Укажите код, количество бонусных дней и максимальное количество активаций
4. Промокод готов к использованию

### Управление балансом пользователя
1. В админ-панели выберите "Баланс"
2. Введите ID пользователя или @username
3. Выберите операцию: пополнение, списание или установка баланса
4. Укажите сумму

### Настройка платежных систем
```env
# Включение YooKassa
YOOKASSA_ENABLED=true
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key

# Включение Tribute для пополнения баланса
TRIBUTE_ENABLED=true
TRIBUTE_BALANCE_URL=https://t.me/tribute/app?startapp=your_app
```

## ❓ FAQ

**Q: Как добавить нового администратора?**
A: Добавьте ID пользователя в переменную `ADMIN_IDS` в файле `.env` через запятую.

**Q: Как изменить цены на подписки?**
A: Отредактируйте соответствующие переменные в `.env` файле (например, `RUB_PRICE_1_MONTH`).

**Q: Почему не работают вебхуки?**
A: Проверьте настройки Nginx, убедитесь что SSL сертификат действителен и контейнер запущен.

**Q: Как отключить пробный период?**
A: Установите `TRIAL_ENABLED=false` в файле `.env`.

**Q: Как изменить язык по умолчанию?**
A: Измените `DEFAULT_LANGUAGE` в `.env` на `ru` или `en`.

**Q: Как обновить бота?**
A: Выполните `git pull` и `docker compose build --no-cache && docker compose up -d`.

## 🔮 Планы на будущее

- Расширенные типы промокодов (скидки в процентах)
- Интеграция с дополнительными платежными системами
- Система уведомлений о скором окончании подписки
- Экспорт статистики в CSV/Excel
- API для внешних интеграций

## ❤️ Поддержка

- **Карты РФ и зарубежные:** [Tribute](https://t.me/tribute/app?startapp=dqdg)
- **Crypto:** `USDT TRC-20 TT3SqBbfU4vYm6SUwUVNZsy278m2xbM4GE`
- **Telegram:** [@your_support](https://t.me/your_support)

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.
