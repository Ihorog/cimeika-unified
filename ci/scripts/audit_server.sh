#!/data/data/com.termux/files/usr/bin/bash
# Termux Server Audit Script - Fixed version

# Кольори
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Конфігурація
CIT_PORT=${CIT_PORT:-8790}
CIT_HOST=${CIT_HOST:-127.0.0.1}
REPO_PATH=${REPO_PATH:-$HOME/cimeika/cit}
LOG_FILE="$HOME/cimeika_audit_$(date +%Y%m%d_%H%M%S).log"

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
}

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_info() { echo -e "${CYAN}ℹ${NC} $1"; }

exec > >(tee -a "$LOG_FILE") 2>&1

echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         CIMEIKA Termux Server Audit                   ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}\n"
print_info "Початок: $(date '+%Y-%m-%d %H:%M:%S')"
print_info "Лог: $LOG_FILE\n"

# 1. СИСТЕМНА ІНФОРМАЦІЯ
print_header "1. СИСТЕМНА ІНФОРМАЦІЯ"
print_info "Hostname: $(hostname)"
print_info "User: $(whoami)"
print_info "HOME: $HOME"
print_info "PWD: $(pwd)"

# Android через getprop (безпечніше)
if command -v getprop >/dev/null 2>&1; then
    ANDROID_VER=$(getprop ro.build.version.release 2>/dev/null || echo "невідома")
    print_info "Android: $ANDROID_VER"
fi

# 2. РЕСУРСИ
print_header "2. РЕСУРСИ"
echo "Пам'ять:"
free -h 2>/dev/null | awk 'NR==1 || NR==2 {print "  " $0}' || print_warning "free недоступна"

echo -e "\nДиск:"
df -h $HOME 2>/dev/null | awk '{print "  " $0}' || print_warning "df недоступна"

PROCS=$(ps aux 2>/dev/null | wc -l || echo "0")
print_info "Процесів: $PROCS"

# 3. ПАКЕТИ
print_header "3. ПАКЕТИ"

check_pkg() {
    if command -v "$1" >/dev/null 2>&1; then
        VER=$("$1" --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        print_success "$1 (v${VER:-?})"
        return 0
    else
        print_error "$1 відсутній"
        return 1
    fi
}

MISSING=()
for pkg in python git curl jq; do
    check_pkg "$pkg" || MISSING+=("$pkg")
done

[ ${#MISSING[@]} -gt 0 ] && print_warning "Встановити: pkg install ${MISSING[*]}"

# Python модулі
if command -v python >/dev/null 2>&1; then
    python -c "import json, http.server, urllib" 2>/dev/null && \
        print_success "Python stdlib OK"
fi

# 4. РЕПОЗИТОРІЙ
print_header "4. GIT РЕПОЗИТОРІЙ"

if [ -d "$REPO_PATH" ]; then
    print_success "Repo: $REPO_PATH"
    cd "$REPO_PATH" 2>/dev/null || print_error "Не можу перейти в $REPO_PATH"
    
    if [ -d .git ]; then
        BRANCH=$(git branch --show-current 2>/dev/null || echo "?")
        print_info "Гілка: $BRANCH"
        
        COMMIT=$(git log -1 --oneline 2>/dev/null || echo "немає")
        print_info "Commit: $COMMIT"
        
        if git diff-index --quiet HEAD -- 2>/dev/null; then
            print_success "Чиста робоча директорія"
        else
            print_warning "Є незбережені зміни"
        fi
        
        REMOTE=$(git remote get-url origin 2>/dev/null || echo "не налаштовано")
        print_info "Remote: $REMOTE"
    else
        print_warning "Не Git репозиторій"
    fi
else
    print_error "Repo не знайдено: $REPO_PATH"
fi

# 5. CIT СЕРВЕР
print_header "5. CIT СЕРВЕР"

SERVER_FILE="$REPO_PATH/server/cit_server.py"
if [ -f "$SERVER_FILE" ]; then
    print_success "Файл: $SERVER_FILE"
    
    if python -m py_compile "$SERVER_FILE" 2>/dev/null; then
        print_success "Синтаксис Python OK"
    else
        print_error "Помилка синтаксису"
    fi
else
    print_error "server/cit_server.py не знайдено"
fi

# Процес
PID=$(pgrep -f "cit_server.py" 2>/dev/null || echo "")
if [ -n "$PID" ]; then
    print_success "Сервер запущено (PID: $PID)"
    ps -p "$PID" -o pid,%cpu,%mem,etime,cmd 2>/dev/null | tail -1
else
    print_warning "Сервер НЕ запущено"
fi

# 6. API ПЕРЕВІРКА
print_header "6. API ENDPOINTS"

check_api() {
    local url="http://${CIT_HOST}:${CIT_PORT}$1"
    echo -e "\n${CYAN}→${NC} $url"
    
    if ! command -v curl >/dev/null 2>&1; then
        print_warning "curl не встановлено"
        return
    fi
    
    RESP=$(curl -s -w "\n%{http_code}" --max-time 5 "$url" 2>/dev/null || echo -e "\n000")
    CODE=$(echo "$RESP" | tail -1)
    BODY=$(echo "$RESP" | head -n-1)
    
    case "$CODE" in
        200)
            print_success "HTTP 200 OK"
            echo "$BODY" | python -m json.tool 2>/dev/null || echo "$BODY"
            ;;
        000)
            print_error "Сервер недоступний"
            ;;
        *)
            print_warning "HTTP $CODE"
            echo "$BODY"
            ;;
    esac
}

check_api "/health"

# Chat test (якщо є ключ)
if [ -n "${OPENAI_API_KEY:-}" ]; then
    print_info "OPENAI_API_KEY налаштовано"
    
    CHAT_URL="http://${CIT_HOST}:${CIT_PORT}/chat"
    echo -e "\n${CYAN}→${NC} POST $CHAT_URL"
    
    CHAT=$(curl -s -X POST "$CHAT_URL" \
        -H "Content-Type: application/json" \
        -d '{"message":"test"}' \
        --max-time 10 2>/dev/null || echo '{"error":"timeout"}')
    
    if echo "$CHAT" | grep -q '"ok".*true'; then
        print_success "Chat працює"
        echo "$CHAT" | python -m json.tool 2>/dev/null
    else
        print_warning "Chat не відповідає"
        echo "$CHAT"
    fi
else
    print_warning "OPENAI_API_KEY не налаштовано"
fi

# 7. ЛОГИ
print_header "7. ЛОГИ"

LOGS="$REPO_PATH/logs"
if [ -d "$LOGS" ]; then
    COUNT=$(find "$LOGS" -type f -name "*.log" 2>/dev/null | wc -l)
    print_info "Log файлів: $COUNT"
    
    LATEST=$(find "$LOGS" -type f -name "*.log" 2>/dev/null | sort | tail -1)
    if [ -n "$LATEST" ]; then
        echo -e "\nОстанні 5 рядків $(basename "$LATEST"):"
        echo "────────────────────────────────"
        tail -5 "$LATEST" 2>/dev/null || print_warning "Не можу прочитати"
    fi
else
    print_warning "Логи не знайдені: $LOGS"
fi

# 8. МЕРЕЖА
print_header "8. МЕРЕЖА"

if command -v ip >/dev/null 2>&1; then
    echo "Інтерфейси:"
    ip -br addr 2>/dev/null | grep -v "DOWN" | while read line; do echo "  $line"; done
elif command -v ifconfig >/dev/null 2>&1; then
    ifconfig 2>/dev/null | grep -E "inet |UP" | head -10
else
    print_warning "ip/ifconfig недоступні"
fi

# 9. ENV
print_header "9. ЗМІННІ СЕРЕДОВИЩА"

for var in HOME PATH OPENAI_API_KEY CIT_PORT; do
    if [ -n "${!var:-}" ]; then
        [ "$var" = "OPENAI_API_KEY" ] && VAL="***" || VAL="${!var}"
        print_info "$var = $VAL"
    else
        print_warning "$var не налаштовано"
    fi
done

# 10. РЕКОМЕНДАЦІЇ
print_header "10. РЕКОМЕНДАЦІЇ"

RECS=()
[ ${#MISSING[@]} -gt 0 ] && RECS+=("pkg install ${MISSING[*]}")
[ -z "$PID" ] && RECS+=("Запустити: cd $REPO_PATH && python server/cit_server.py")
[ -z "${OPENAI_API_KEY:-}" ] && RECS+=("export OPENAI_API_KEY=your_key")

if [ ${#RECS[@]} -gt 0 ]; then
    for rec in "${RECS[@]}"; do print_warning "$rec"; done
else
    print_success "Все налаштовано!"
fi

# ПІДСУМОК
print_header "ЗАВЕРШЕНО"
print_success "Звіт збережено: $LOG_FILE"
print_info "Час: $(date '+%H:%M:%S')"
echo ""
