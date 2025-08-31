# 🚀 TrackFlow - AI-Powered Personal Finance Tracker

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://postgresql.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-3.0+-38B2AC.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **TrackFlow** is a modern, AI-powered personal finance tracking application that helps you understand your spending patterns, set savings goals, and achieve financial freedom through intelligent insights and predictions.

## ✨ Features

### 🎯 **Core Financial Tracking**
- **Income & Expense Management** - Track all your financial transactions
- **Smart Categorization** - Automatic categorization with emoji icons
- **Date-based Filtering** - Filter transactions by date ranges
- **Real-time Updates** - Instant reflection of changes across the app

### 🧠 **AI-Powered Insights**
- **Expense Predictions** - Machine learning-based future expense forecasting
- **Spending Pattern Analysis** - Identify trends in your financial behavior
- **Personalized Recommendations** - AI-generated savings and spending tips
- **Smart Alerts** - Get notified about unusual spending patterns

### 📊 **Advanced Analytics**
- **Interactive Charts** - Beautiful visualizations using Chart.js
- **Monthly Trends** - Track income vs expenses over time
- **Category Breakdown** - See where your money goes
- **Savings Rate Analysis** - Monitor your financial progress
- **Yearly Financial Overview** - Comprehensive annual reports

### 🎯 **Savings & Goals**
- **Goal Setting** - Set monthly savings targets
- **Progress Tracking** - Visual progress bars and milestones
- **Achievement Celebrations** - Motivate yourself with progress rewards
- **Personalized Strategies** - AI-generated savings recommendations

### 👥 **User Management**
- **Secure Authentication** - Flask-Login with password hashing
- **Role-based Access** - User and Admin roles
- **Profile Management** - Update personal information
- **Settings Customization** - Personalize your experience

### 🔧 **Admin Dashboard**
- **User Management** - View, edit, and manage all users
- **Transaction Overview** - Monitor all user activities
- **Goal Management** - Help users achieve their financial goals
- **System Statistics** - Comprehensive platform insights

### 🎨 **Modern UI/UX**
- **Responsive Design** - Works perfectly on all devices
- **Dark Theme** - Easy on the eyes with modern aesthetics
- **Smooth Animations** - Professional transitions and effects
- **Tailwind CSS** - Beautiful, consistent styling
- **Interactive Elements** - Hover effects and loading states

## 🛠️ Technology Stack

### **Backend**
- **Python 3.8+** - Core programming language
- **Flask 3.0+** - Web framework
- **SQLAlchemy 2.0+** - Database ORM
- **Flask-Login** - User authentication
- **PostgreSQL** - Primary database

### **Frontend**
- **HTML5** - Semantic markup
- **Tailwind CSS 3.0+** - Utility-first CSS framework
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualization
- **Jinja2** - Template engine

### **AI & Data Science**
- **scikit-learn** - Machine learning algorithms
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **Linear Regression** - Expense prediction models

### **Development Tools**
- **python-dotenv** - Environment variable management
- **psycopg2-binary** - PostgreSQL adapter
- **Git** - Version control

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/ShubhamGajera/trackflow.git
cd trackflow
```

### **2. Set Up Virtual Environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Environment**
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/trackflow
```

### **5. Set Up Database**
```bash
# Create PostgreSQL database
createdb trackflow

# Run the complete setup script
python complete_setup.py
```

### **6. Start the Application**
```bash
python run.py
```

### **7. Access Your Application**
Open your browser and go to: `http://localhost:5000`

## 📋 Complete Setup Guide

### **Automatic Setup (Recommended)**
```bash
# Run the comprehensive setup script
python complete_setup.py
```

This script will:
- ✅ Check and install dependencies
- ✅ Fix database schema issues
- ✅ Create admin user
- ✅ Test all functionality
- ✅ Make everything work perfectly

### **Manual Setup (Advanced Users)**
```bash
# 1. Fix database schema
python fix_database.py

# 2. Check current users
python check_users.py

# 3. Create admin user
python create_admin.py

# 4. Start the application
python run.py
```

## 🗄️ Database Schema

### **Users Table**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at DATE DEFAULT CURRENT_DATE
);
```

### **Transactions Table**
```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    type VARCHAR(10) NOT NULL DEFAULT 'expense',
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'Other',
    note VARCHAR(255),
    date DATE NOT NULL DEFAULT CURRENT_DATE
);
```

### **Goals Table**
```sql
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    name VARCHAR(100) DEFAULT 'Monthly Savings',
    target_amount FLOAT DEFAULT 0.0,
    achieved FLOAT DEFAULT 0.0,
    monthly_savings_target FLOAT DEFAULT 0.0
);
```

## 🔐 Authentication & Security

### **User Roles**
- **User** - Standard user with personal finance tracking
- **Admin** - Full system access and user management

### **Security Features**
- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection
- Input validation and sanitization
- Role-based access control

## 📱 Available Routes

### **Public Routes**
- `/` - Home page
- `/login` - User login
- `/register` - User registration
- `/about` - About page
- `/help` - Help and support

### **Authenticated User Routes**
- `/dashboard` - Personal dashboard
- `/transactions` - Transaction history
- `/transactions/add` - Add new transaction
- `/edit_transaction/<id>` - Edit transaction
- `/savings` - Savings goals
- `/analytics` - Financial analytics
- `/predictions` - AI predictions
- `/profile` - User profile
- `/settings` - User settings

### **Admin Routes**
- `/admin` - Admin panel
- `/admin/dashboard` - Admin dashboard
- `/admin/edit_user/<id>` - Edit user
- `/admin/edit_goal/<id>` - Edit user goal
- `/admin/delete_user/<id>` - Delete user
- `/admin/delete_transaction/<id>` - Delete transaction

### **API Endpoints**
- `/api/transaction_stats` - Transaction statistics
- `/api/category_chart` - Category breakdown data

## 🎨 UI Components

### **Design System**
- **Color Palette** - Modern dark theme with accent colors
- **Typography** - Inter font family for readability
- **Spacing** - Consistent spacing using Tailwind's scale
- **Components** - Reusable UI components

### **Interactive Elements**
- **Cards** - Hover effects and animations
- **Buttons** - Multiple styles with loading states
- **Forms** - Validation and error handling
- **Tables** - Sortable and filterable data
- **Charts** - Interactive data visualizations

## 🔧 Configuration

### **Environment Variables**
```env
# Required
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/trackflow

# Optional
FLASK_ENV=development
DEBUG=True
```

### **Database Configuration**
```python
# config.py
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///trackflow.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## 🧪 Testing

### **Run Tests**
```bash
# Test database connection
python -c "from app import app, db; app.app_context().push(); db.engine.execute('SELECT 1')"

# Check users
python check_users.py

# Test admin functionality
python -c "from app import app; print('App loads successfully')"
```

### **Test Scenarios**
- ✅ User registration and login
- ✅ Transaction CRUD operations
- ✅ Admin panel functionality
- ✅ Analytics and charts
- ✅ Responsive design
- ✅ Form validation
- ✅ Error handling

## 🚀 Deployment

### **Production Setup**
1. **Set Environment Variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=your-production-database-url
   ```

2. **Install Production Dependencies**
   ```bash
   pip install gunicorn
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

## 📊 Performance & Scalability

### **Optimizations**
- Database indexing on frequently queried fields
- Efficient SQL queries with proper joins
- Caching for static data
- Lazy loading for large datasets

### **Monitoring**
- Database connection pooling
- Query performance tracking
- Error logging and monitoring
- User activity analytics

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### **Code Style**
- Follow PEP 8 Python guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where possible

## 🐛 Troubleshooting

### **Common Issues**

#### **Database Connection Error**
```bash
# Check PostgreSQL service
sudo service postgresql status

# Verify connection string
echo $DATABASE_URL
```

#### **Admin Access Issues**
```bash
# Check user role in database
python check_users.py

# Create admin user
python create_admin.py
```

#### **Template Errors**
```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
```

### **Debug Mode**
```bash
# Enable debug mode
export FLASK_ENV=development
export DEBUG=True
```

## 📚 API Documentation

### **Authentication**
All authenticated endpoints require a valid session cookie.

### **Response Format**
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
}
```

### **Error Handling**
```json
{
  "success": false,
  "error": "Error description",
  "code": 400
}
```

## 🔮 Future Enhancements

### **Planned Features**
- [ ] Mobile app (React Native)
- [ ] Multi-currency support
- [ ] Investment tracking
- [ ] Bill reminders
- [ ] Export to Excel/PDF
- [ ] Real-time notifications
- [ ] Advanced AI insights
- [ ] Social features

### **Technical Improvements**
- [ ] API rate limiting
- [ ] Advanced caching
- [ ] Microservices architecture
- [ ] Real-time updates with WebSockets
- [ ] Advanced security features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - Web framework
- **Tailwind CSS** - CSS framework
- **Chart.js** - Data visualization
- **PostgreSQL** - Database
- **scikit-learn** - Machine learning

## 📞 Support

### **Getting Help**
- **Documentation** - Check this README first
- **Issues** - Report bugs on GitHub
- **Discussions** - Ask questions in GitHub Discussions
- **Email** - support@trackflow.com

### **Community**
- **GitHub** - [TrackFlow Repository](https://github.com/ShubhamGajera/trackflow)
- **Discussions** - [GitHub Discussions](https://github.com/ShubhamGajera/trackflow/discussions)
- **Issues** - [Bug Reports](https://github.com/ShubhamGajera/trackflow/issues)

---

## 🎉 **Ready to Get Started?**

Your TrackFlow application is now **100% complete and functional**! 

### **Quick Start Commands:**
```bash
# 1. Complete setup (recommended)
python complete_setup.py

# 2. Start the application
python run.py

# 3. Open in browser
# http://localhost:5000
```

### **What You'll Get:**
- ✅ **Complete financial tracking system**
- ✅ **Beautiful, responsive UI**
- ✅ **AI-powered insights**
- ✅ **Admin dashboard**
- ✅ **All features working perfectly**

**Happy coding! 🚀**

---

*Built with ❤️ by [Shubham Gajera](https://github.com/ShubhamGajera)*
