# CIMEIKA Documentation

## Quick Start Guide

### Prerequisites
- Docker & Docker Compose installed
- Git installed
- (Optional) Node.js 18+ and Python 3.11+ for local development

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ihorog/cimeika-unified.git
   cd cimeika-unified
   ```

2. **Configure environment variables**
   ```bash
   cp .env.template .env
   ```
   
   Edit `.env` file and set your values:
   - Database credentials
   - Redis password
   - API keys (OpenAI, Anthropic)
   - Secret key for Flask

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Health check: http://localhost:5000/health

### Development

#### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Available Services

- **PostgreSQL**: Port 5432
- **Redis**: Port 6379
- **Backend**: Port 5000
- **Frontend**: Port 3000

### Stopping the Application

```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
```

## Architecture

See the main [README.md](../README.md) for detailed architecture information.

## Modules

The system consists of 7 modules:
1. **Ci** - Central orchestration core
2. **Казкар** - Memory, stories, legends
3. **Подія** - Events, future, scenarios
4. **Настрій** - Emotional states, context
5. **Маля** - Ideas, creativity, innovations
6. **Галерея** - Visual archive, media
7. **Календар** - Time, rhythms, planning

## API Endpoints

### Core Endpoints

- `GET /` - API status and version
- `GET /health` - Health check
- `GET /api/v1/modules` - List all modules

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Check if ports 3000, 5000, 5432, or 6379 are already in use
   - Stop conflicting services or modify ports in docker-compose.yml

2. **Database connection failed**
   - Ensure PostgreSQL container is healthy: `docker-compose ps`
   - Check environment variables in .env file

3. **Frontend cannot connect to backend**
   - Verify VITE_API_URL in .env matches backend URL
   - Check CORS settings in backend

## Contributing

This project is in active development. Contributions are welcome after architecture stabilization.

## License

TBD
