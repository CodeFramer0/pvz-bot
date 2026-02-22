Write-Host "🚀 Начинаем бесшовный деплой (DEV)..." -ForegroundColor Cyan

$composeFile = "docker-compose.prod.yml"

# 1. Собираем свежий образ
docker compose -f $composeFile build web

# 2. Запускаем вторую копию (теперь работают старая и новая вместе)
Write-Host "🆙 Запуск новой версии (scaling up to 2)..." -ForegroundColor Yellow
docker compose -f $composeFile up -d --no-deps --scale web=2 web

# 3. Ждем, пока НОВЫЙ контейнер пройдет Healthcheck
Write-Host "⏳ Ожидание прогрева нового контейнера..." -ForegroundColor Gray
$maxRetries = 20
$count = 0
$isHealthy = $false

while ($count -lt $maxRetries) {
    # Фильтруем контейнеры, которые относятся к нашему проекту и сервису web
    $healthyCount = (docker ps --filter "label=traefik.enable=true" --filter "health=healthy" --filter "name=web" -q).Count
    
    if ($healthyCount -ge 2) {
        $isHealthy = $true
        break
    }
    Write-Host "." -NoNewline
    Start-Sleep -Seconds 3
    $count++
}

if (-not $isHealthy) {
    Write-Host "`n❌ Ошибка: Новая версия не прошла Healthcheck! Откат к 1 копии..." -ForegroundColor Red
    docker compose -f $composeFile up -d --scale web=1 web
    exit
}

Write-Host "`n✅ Новая версия готова и принимает трафик!" -ForegroundColor Green

# 4. Удаляем старую версию (Docker прибьет самый старый контейнер)
Write-Host "♻️ Удаление старой версии (scaling down to 1)..." -ForegroundColor Yellow
docker compose -f $composeFile up -d --scale web=1 web

# 5. Рестарт зависимых сервисов
Write-Host "🤖 Обновление бота и воркеров..." -ForegroundColor Cyan
docker compose -f $composeFile restart bot celery-worker celery-beat

# 6. Очистка мусора (неиспользуемые старые образы)
Write-Host "🧹 Очистка старых образов..." -ForegroundColor Gray
docker image prune -f

Write-Host "✨ Деплой завершен успешно!" -ForegroundColor Green
