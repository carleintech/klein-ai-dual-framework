# Contributing to Klein AI Dual Framework

We welcome contributions to the Klein AI Dual Framework! This project was built for the AI Accelerate Hackathon 2025 and demonstrates a dual-AI architecture for safe, trustworthy AI interactions.

## 🚀 Quick Start

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🏗️ Development Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Git

### Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## 📋 Code Style

- **Python**: Follow PEP 8, use Black formatter
- **TypeScript**: Follow ESLint rules, use Prettier
- **Commits**: Use conventional commits (feat:, fix:, docs:, etc.)

## 🛡️ Security

If you discover a security vulnerability, please email [your-email@domain.com] instead of opening a public issue.

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be acknowledged in the README and project documentation.

---

Built for AI Accelerate Hackathon 2025 🏆
