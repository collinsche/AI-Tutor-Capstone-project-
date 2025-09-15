# Installation and Setup Guide

## Prerequisites

Before installing the AI Educational Assistant, ensure you have the following prerequisites:

### System Requirements
- **Python**: Version 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 2GB free space
- **Internet Connection**: Required for AI model access

### Required Accounts
- **OpenAI API Key**: For AI response generation (optional for demo mode)
- **Git**: For version control and repository management

## Installation Methods

### Method 1: Quick Start (Recommended)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ai-educational-assistant.git
   cd ai-educational-assistant
   ```

2. **Create Virtual Environment**
   ```bash
   # Using venv (Python 3.8+)
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env file with your configuration
   nano .env
   ```

5. **Run the Application**
   ```bash
   streamlit run src/main.py
   ```

### Method 2: Development Setup

1. **Clone and Setup**
   ```bash
   git clone https://github.com/yourusername/ai-educational-assistant.git
   cd ai-educational-assistant
   ```

2. **Install in Development Mode**
   ```bash
   pip install -e .
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set Up Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

### Method 3: Docker Installation

1. **Using Docker Compose**
   ```bash
   git clone https://github.com/yourusername/ai-educational-assistant.git
   cd ai-educational-assistant
   docker-compose up -d
   ```

2. **Using Docker**
   ```bash
   docker build -t ai-educational-assistant .
   docker run -p 8501:8501 ai-educational-assistant
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000

# Application Configuration
APP_TITLE=AI Educational Assistant
APP_DEBUG=False
APP_PORT=8501
APP_HOST=localhost

# Database Configuration (if using external database)
DATABASE_URL=sqlite:///data/educational_assistant.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Security Configuration
SECRET_KEY=your_secret_key_here
SESSION_TIMEOUT=3600
```

### Configuration Files

The application uses several configuration files:

- **`src/config.py`**: Main configuration management
- **`requirements.txt`**: Python dependencies
- **`setup.py`**: Package configuration
- **`.env`**: Environment variables

## Verification

### Test Installation

1. **Run Unit Tests**
   ```bash
   python -m pytest tests/ -v
   ```

2. **Check Application Health**
   ```bash
   python -c "import src.main; print('Installation successful!')"
   ```

3. **Verify Dependencies**
   ```bash
   pip list | grep -E "streamlit|openai|plotly"
   ```

### Access the Application

1. **Start the Application**
   ```bash
   streamlit run src/main.py
   ```

2. **Open in Browser**
   - Navigate to: `http://localhost:8501`
   - You should see the AI Educational Assistant interface

## Troubleshooting

### Common Issues

#### Issue 1: Python Version Compatibility
```bash
# Check Python version
python --version

# If version is < 3.8, install Python 3.8+
# On macOS using Homebrew:
brew install python@3.9

# On Ubuntu:
sudo apt update
sudo apt install python3.9
```

#### Issue 2: Package Installation Errors
```bash
# Upgrade pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install with no cache
pip install --no-cache-dir -r requirements.txt
```

#### Issue 3: Streamlit Port Issues
```bash
# Run on different port
streamlit run src/main.py --server.port 8502

# Check port usage
lsof -i :8501  # On macOS/Linux
netstat -ano | findstr :8501  # On Windows
```

#### Issue 4: OpenAI API Issues
```bash
# Test API key
python -c "import openai; openai.api_key='your_key'; print('API key valid')"

# Check API quota
curl -H "Authorization: Bearer your_api_key" https://api.openai.com/v1/usage
```

#### Issue 5: Permission Errors
```bash
# On macOS/Linux
sudo chown -R $USER:$USER .
chmod +x scripts/*.sh

# On Windows (run as administrator)
icacls . /grant %USERNAME%:F /T
```

### Debug Mode

Enable debug mode for detailed error information:

```bash
# Set debug environment variable
export APP_DEBUG=True

# Run with debug logging
streamlit run src/main.py --logger.level debug
```

### Log Files

Check log files for detailed error information:

```bash
# Application logs
tail -f logs/app.log

# Streamlit logs
tail -f ~/.streamlit/logs/streamlit.log
```

## Performance Optimization

### Memory Optimization
```bash
# Monitor memory usage
pip install memory-profiler
python -m memory_profiler src/main.py
```

### Caching Configuration
```python
# In src/config.py, adjust cache settings
CACHE_TTL = 3600  # 1 hour
CACHE_MAX_ENTRIES = 1000
```

## Security Setup

### API Key Security
```bash
# Never commit API keys to version control
echo ".env" >> .gitignore

# Use environment variables in production
export OPENAI_API_KEY="your_key_here"
```

### File Permissions
```bash
# Secure configuration files
chmod 600 .env
chmod 644 src/*.py
```

## Production Deployment

### Using Streamlit Cloud
1. Push code to GitHub repository
2. Connect repository to Streamlit Cloud
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy application

### Using Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run src/main.py --server.port $PORT" > Procfile

# Deploy to Heroku
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### Using Docker in Production
```dockerfile
# Dockerfile for production
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 8501

CMD ["streamlit", "run", "src/main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## Maintenance

### Regular Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update application
git pull origin main
```

### Backup Data
```bash
# Backup user profiles and analytics
cp -r data/ backup/data_$(date +%Y%m%d)/
```

### Monitor Performance
```bash
# Check application health
curl http://localhost:8501/healthz

# Monitor resource usage
top -p $(pgrep -f streamlit)
```

## Support

If you encounter issues not covered in this guide:

1. **Check the FAQ**: See `docs/FAQ.md`
2. **Search Issues**: Check GitHub issues for similar problems
3. **Create Issue**: Submit a detailed bug report
4. **Contact Support**: Email support@yourdomain.com

## Next Steps

After successful installation:

1. **Read the User Guide**: `docs/USER_GUIDE.md`
2. **Explore Features**: Try different learning styles and subjects
3. **Customize Settings**: Adjust configuration for your needs
4. **Contribute**: See `CONTRIBUTING.md` for development guidelines

---

**Note**: This installation guide assumes basic familiarity with command-line interfaces and Python development. For additional help, consult the documentation or reach out to the community.