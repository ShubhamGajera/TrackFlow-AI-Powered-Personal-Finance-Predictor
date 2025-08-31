# 🚀 TrackFlow Setup Guide

## Quick Setup Instructions

### 1. **Run the Complete Setup Script**
```bash
python complete_setup.py
```

This script will:
- ✅ Install all required packages
- ✅ Fix database schema issues
- ✅ Create admin user
- ✅ Test all functionality
- ✅ Make everything work perfectly

### 2. **Start the Application**
```bash
python run.py
```

### 3. **Access Your Website**
Open your browser and go to: `http://localhost:5000`

## 🔧 Manual Configuration (if needed)

### **Database Configuration**
Create a `.env` file in your project root with:

```env
# Secret key for Flask sessions
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database connection URL
DATABASE_URL=postgresql://postgres:password@localhost:5432/trackflow

# Flask environment
FLASK_ENV=development
DEBUG=True
```

### **PostgreSQL Setup**
1. Install PostgreSQL
2. Create database: `createdb trackflow`
3. Update `.env` with your credentials

### **Individual Scripts**
If you need to run scripts separately:

```bash
# Fix database schema
python fix_database.py

# Check users
python check_users.py

# Create admin user
python create_admin.py
```

## 🎯 **Default Admin Credentials**
- **Username**: admin
- **Password**: admin123
- **Email**: admin@trackflow.com

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Database Connection Error**
   - Check PostgreSQL service is running
   - Verify database credentials in `.env`

2. **Admin Access Issues**
   - Run `python check_users.py` to see current users
   - Run `python create_admin.py` to create admin

3. **Unicode Errors (Windows)**
   - All scripts now work without emoji characters
   - Use simple text output

### **Get Help**
- Check this guide first
- Run `python complete_setup.py` for automatic fixes
- Check error messages in the terminal

## 🎉 **You're Ready!**
Your TrackFlow website is now **100% complete and functional** with:
- ✅ Complete financial tracking system
- ✅ Beautiful, responsive UI
- ✅ AI-powered insights
- ✅ Admin dashboard
- ✅ All features working perfectly

**Happy tracking! 🚀** 