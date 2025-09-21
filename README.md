# 🎓 AI Personalized Educational Assistant

A sophisticated Generative AI-powered educational assistant that provides personalized learning experiences, adapting to individual student needs and learning styles. Built with Python, Streamlit, and powered by Grok AI models.

## 🌟 Features

### 🤖 AI-Powered Learning
- **Personalized Content Generation**: Creates custom learning materials based on individual learning styles
- **Adaptive Questioning**: Generates questions tailored to student's current knowledge level
- **Intelligent Explanations**: Provides explanations in multiple formats (visual, auditory, kinesthetic)
- **Real-time Feedback**: Offers immediate, constructive feedback on student responses
- **Demo Mode**: Fully functional demonstration mode without API requirements

### 👤 User Personalization
- **Learning Style Detection**: Automatically identifies and adapts to visual, auditory, or kinesthetic learning preferences
- **Progress Tracking**: Comprehensive analytics on learning progress and performance
- **Difficulty Adjustment**: Dynamic difficulty scaling based on student performance
- **Goal Setting**: Personalized learning goals and milestone tracking
- **Interactive Onboarding**: Guided setup process for new users

### 📊 Analytics & Insights
- **Learning Analytics**: Detailed insights into learning patterns and progress
- **Performance Metrics**: Track engagement, completion rates, and knowledge retention
- **Study Recommendations**: AI-generated study plans and resource suggestions
- **Progress Visualization**: Interactive charts and graphs showing learning journey
- **Session Tracking**: Detailed logging of learning sessions and interactions

### 🎨 Modern Interface
- **Intuitive Design**: Clean, modern Streamlit-based interface
- **Responsive Layout**: Works seamlessly across different screen sizes
- **Multi-page Navigation**: Organized dashboard, learning, chat, and profile pages
- **Interactive Elements**: Engaging UI components for better user experience

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**: Required for running the application
- **pip**: Python package manager
- **Grok API Key**: Optional (demo mode available without API key)
- **Git**: For cloning the repository

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-educational-assistant.git
   cd ai-educational-assistant
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**
   ```bash
   streamlit run src/main.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# AI Configuration
GROK_API_KEY=your_grok_api_key_here
AI_MODEL=x-ai/grok-4
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000
USE_DEMO_MODE=false

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO
DATA_DIR=data

# UI Configuration
UI_THEME=light
```

### API Key Setup

1. **Get a Grok API Key**:
   - Visit [X.AI Console](https://console.x.ai/)
   - Sign up or log in to your account
   - Create a new API key
   - Copy the key (starts with 'xai-')

2. **Configure the API Key**:
   - Open the `.env` file
   - Replace `your_grok_api_key_here` with your actual key
   - Save the file

3. **Test the API Key**:
   ```bash
   python test_api.py
   ```

### Demo Mode

The application includes a fully functional demo mode that works without an API key:
- Pre-configured responses for common educational scenarios
- Complete UI functionality
- User profile management
- Learning analytics
- Perfect for demonstrations and testing

To enable demo mode, set `USE_DEMO_MODE=true` in your `.env` file.

## 📁 Project Structure

```
ai-educational-assistant/
├── src/                          # Source code
│   ├── main.py                   # Main Streamlit application
│   ├── app_router.py            # Application routing and navigation
│   ├── educational_assistant.py  # Core AI assistant logic
│   ├── user_profile.py          # User profile management
│   ├── learning_analytics.py    # Analytics and tracking
│   ├── onboarding.py           # User onboarding system
│   ├── learning_paths.py       # Learning path generation
│   ├── enhanced_chat.py        # Chat interface
│   ├── adaptive_quiz.py        # Adaptive quiz system
│   ├── content_generator.py    # Content generation
│   ├── dashboard.py            # Dashboard interface
│   ├── config.py              # Configuration management
│   └── utils.py               # Utility functions
├── tests/                       # Test suite
│   └── test_educational_assistant.py
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # System architecture
│   ├── INSTALLATION.md          # Detailed installation guide
│   └── USER_GUIDE.md           # User manual
├── presentation/                # Project presentation materials
├── video/                      # Video demonstration files
├── data/                       # Data storage directory
├── requirements.txt            # Python dependencies
├── setup.py                   # Package setup configuration
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🎯 Key Components

### Educational Assistant Core
The heart of the system, powered by Grok AI models, provides:
- Intelligent content generation
- Adaptive learning pathways
- Personalized explanations
- Interactive Q&A sessions

### User Profile System
Comprehensive user management including:
- Learning style preferences
- Subject interests and goals
- Progress tracking and analytics
- Session history and statistics

### Learning Analytics
Advanced analytics engine that tracks:
- Learning patterns and trends
- Performance metrics
- Engagement statistics
- Personalized recommendations

### Multi-page Interface
Organized navigation with dedicated pages for:
- **Dashboard**: Overview of progress and quick actions
- **Learning**: Interactive learning modules and quizzes
- **Chat**: AI-powered conversational learning
- **Profile**: User settings and preferences

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_educational_assistant.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Suite
```bash
# Comprehensive system test
python src/test_runner.py

# Demo mode test
python test_demo_mode.py

# API key test
python test_api.py
```

## 🚀 Usage

### Getting Started

1. **First Launch**: Complete the interactive onboarding process
2. **Set Learning Goals**: Define your subjects and objectives
3. **Choose Learning Style**: Select visual, auditory, or kinesthetic preferences
4. **Start Learning**: Access personalized content and quizzes

### Main Features

#### Dashboard
- View learning progress and statistics
- Access recent activities and achievements
- Quick navigation to all features

#### Learning Modules
- **Adaptive Quizzes**: Questions that adjust to your skill level
- **Content Generation**: Custom study materials and summaries
- **Learning Paths**: Structured learning sequences

#### AI Chat
- Ask questions in natural language
- Get explanations tailored to your learning style
- Receive personalized study recommendations

#### Analytics
- Track learning streaks and session duration
- Monitor progress across different subjects
- View detailed performance metrics

## 🔧 Troubleshooting

### Common Issues

**Application won't start**:
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**API key issues**:
```bash
# Test API key
python test_api.py

# Use demo mode
# Set USE_DEMO_MODE=true in .env file
```

**Port already in use**:
```bash
# Use different port
streamlit run src/main.py --server.port 8502
```

### Debug Mode

Enable debug mode for detailed error information:
```bash
# Set debug environment variable
export DEBUG=true

# Run with debug logging
streamlit run src/main.py --logger.level debug
```

## 📊 Performance

### System Requirements
- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: 500MB for application and dependencies
- **Network**: Internet connection for AI API calls (optional in demo mode)

### Performance Metrics
- **Startup Time**: < 5 seconds
- **Response Time**: < 2 seconds for most operations
- **Memory Usage**: ~200MB typical usage
- **Concurrent Users**: Supports multiple users with session isolation
## 🤝 Contributing

We welcome contributions to improve the AI Educational Assistant! Here's how you can help:

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Run tests**:
   ```bash
   python src/test_runner.py
   python -m pytest tests/ -v
   ```
5. **Submit a pull request**

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and modular

### Testing

- Write tests for new features
- Ensure all existing tests pass
- Test both API and demo modes
- Include edge case testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Grok AI**: For providing the powerful language model capabilities
- **Streamlit**: For the excellent web application framework
- **Python Community**: For the amazing ecosystem of libraries
- **Contributors**: Thank you to all who have contributed to this project

## 📞 Support

### Getting Help

- **Documentation**: Check the [docs/](docs/) directory for detailed guides
- **Issues**: Report bugs or request features on GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions

### Contact

- **Project Maintainer**: [Your Name](mailto:your.email@example.com)
- **GitHub**: [Project Repository](https://github.com/yourusername/ai-educational-assistant)

## 🗺️ Roadmap

### Current Version (v1.0.0)
- ✅ Core AI assistant functionality
- ✅ User profile management
- ✅ Learning analytics
- ✅ Multi-page interface
- ✅ Demo mode support

### Upcoming Features (v1.1.0)
- 🔄 Advanced learning path algorithms
- 🔄 Collaborative learning features
- 🔄 Mobile-responsive design improvements
- 🔄 Additional AI model support

### Future Plans (v2.0.0)
- 📋 Multi-language support
- 📋 Advanced analytics dashboard
- 📋 Integration with external learning platforms
- 📋 Voice interaction capabilities

## 📈 Changelog

### Version 1.0.0 (Current)
- Initial release with core functionality
- AI-powered personalized learning
- Comprehensive user profile system
- Learning analytics and progress tracking
- Multi-page Streamlit interface
- Demo mode for testing and presentations

## 🔮 Future Enhancements

- Multi-language support
- Voice interaction capabilities
- Mobile application
- Integration with Learning Management Systems (LMS)
- Advanced AI models and techniques
- Collaborative learning features
- Gamification elements

---

**Made with ❤️ for education and learning**

*This project aims to make personalized education accessible to everyone through the power of AI.*