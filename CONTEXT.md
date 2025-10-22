# 🚀 Контекст проекта nginx-cicd-demo

## 📍 Роль этого проекта
**nginx-cicd-demo - это ИНФРАСТРУКТУРНЫЙ ПРОЕКТ**, который обеспечивает:
- ✅ Kubernetes кластер (Kind) на сервере 185.8.22.53
- ✅ Ingress Nginx Controller для маршрутизации трафика
- ✅ Cert-manager для автоматических SSL сертификатов
- ✅ Базовую инфраструктуру для ВСЕХ приложений

## 🎯 Архитектура "Хаб и спицы"

Сервер 185.8.22.53 (Kubernetes Cluster)
├── 🏗️ nginx-cicd-demo/ (ИНФРАСТРУКТУРА)
│ ├── Ingress Controller
│ ├── Cert Manager
│ └── Общие ресурсы
│
├── 🌐 Приложение 1: clerikc.ru (уже работает)
├── 📊 Приложение 2: zabbix.clerikc.ru (будет отдельно)
├── 🗄️ Приложение 3: app.clerikc.ru (будет отдельно)
└── 📝 Приложение N: *.clerikc.ru (будут отдельно)


## ✅ Что уже настроено в инфраструктуре
- **Kubernetes кластер**: Kind (3 ноды)
- **Ingress Controller**: Nginx с портами 30080/30443
- **SSL**: Let's Encrypt через cert-manager
- **CI/CD базовый**: GitHub Actions для деплоя инфраструктуры
- **Доменная зона**: clerikc.ru готова для субдоменов

## 🛠️ Команды для проверки инфраструктуры
```bash
# Проверить базовую инфраструктуру
kubectl get pods -A
kubectl get ingress -A  
kubectl get certificate -A

# Логи ingress controller
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller --tail=10

# Проверить текущее приложение
curl -f https://clerikc.ru