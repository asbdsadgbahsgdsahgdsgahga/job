# Institution Website

A modern, responsive website for educational institutions built with HTML, CSS, JavaScript frontend and Python/PHP backend with database connectivity.

## Features

### Frontend
- **Modern Design**: Clean, professional design with smooth animations
- **Responsive Layout**: Works perfectly on all devices (desktop, tablet, mobile)
- **Interactive Elements**: Smooth scrolling, form validation, dynamic content
- **Beautiful UI**: Modern gradients, shadows, and typography
- **Accessibility**: Proper semantic HTML and ARIA labels

### Backend
- **Python Flask API**: RESTful API endpoints for data handling
- **PHP Admin Panel**: Complete admin interface for content management
- **Database Integration**: SQLite database for data persistence
- **Form Processing**: Secure form submission and validation
- **CORS Support**: Cross-origin resource sharing enabled

### Key Sections
1. **Hero Section**: Eye-catching landing area with call-to-action
2. **About Section**: Institution information with statistics
3. **Programs Section**: Academic programs showcase
4. **Admissions Section**: Application form with step-by-step process
5. **Faculty Section**: Faculty member profiles
6. **Contact Section**: Contact form and information
7. **Admin Panel**: Complete content management system

## Technology Stack

### Frontend
- HTML5
- CSS3 (with modern features like Grid, Flexbox, Animations)
- JavaScript (ES6+)
- Font Awesome Icons
- Google Fonts (Poppins)

### Backend
- **Python**: Flask framework for API
- **PHP**: Admin panel and additional backend functionality
- **Database**: SQLite for data storage
- **APIs**: RESTful endpoints for data operations

## Installation & Setup

### Prerequisites
- Python 3.7+
- PHP 7.4+
- Web server (Apache/Nginx) or Python development server

### Step 1: Clone/Download the Project
```bash
# If using git
git clone <repository-url>
cd institution-website

# Or download and extract the files
```

### Step 2: Set Up Python Backend

1. **Install Python Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the Flask Application**:
```bash
cd backend
python app.py
```

The Flask server will start on `http://localhost:5000`

### Step 3: Set Up PHP Admin Panel

1. **Configure Database** (if using MySQL instead of SQLite):
   - Create a MySQL database named `institution_db`
   - Update database credentials in `backend/admin.php`

2. **Access Admin Panel**:
   - Place `admin.php` in your web server directory
   - Access via `http://your-domain/admin.php`

### Step 4: Configure Frontend

1. **Update API Endpoints** (if needed):
   - Open `js/script.js`
   - Update API URLs to match your backend server

2. **Customize Content**:
   - Edit `index.html` to update institution information
   - Modify `css/style.css` for branding colors
   - Update images and content as needed

## File Structure

```
institution-website/
├── index.html              # Main website page
├── css/
│   └── style.css          # Main stylesheet
├── js/
│   └── script.js          # Frontend JavaScript
├── backend/
│   ├── app.py             # Python Flask API
│   ├── admin.php          # PHP Admin Panel
│   └── institution.db     # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
└── README.md             # This file
```

## API Endpoints

### Python Flask API (`http://localhost:5000`)

#### Admissions
- `POST /api/admissions` - Submit admission application

#### Contact
- `POST /api/contact` - Submit contact message

#### Data Retrieval
- `GET /api/programs` - Get all active programs
- `GET /api/faculty` - Get all active faculty members
- `GET /api/stats` - Get website statistics

#### Admin Endpoints
- `GET /api/admin/admissions` - Get all admissions
- `GET /api/admin/messages` - Get all contact messages
- `POST /api/admin/programs` - Add new program
- `POST /api/admin/faculty` - Add new faculty member

### PHP Admin Panel
- Access via web browser
- Manage admissions, messages, programs, and faculty
- View statistics and analytics

## Database Schema

### Admissions Table
```sql
CREATE TABLE admissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    program TEXT NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Contact Messages Table
```sql
CREATE TABLE contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Programs Table
```sql
CREATE TABLE programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    duration TEXT NOT NULL,
    category TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Faculty Table
```sql
CREATE TABLE faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    bio TEXT,
    email TEXT,
    image_url TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Customization

### Colors and Branding
Edit `css/style.css` to update:
- Primary colors (`#3498db`)
- Secondary colors (`#2c3e50`)
- Gradients and backgrounds
- Typography and spacing

### Content Updates
1. **Institution Information**: Update in `index.html`
2. **Programs**: Add via admin panel or database
3. **Faculty**: Add via admin panel or database
4. **Contact Information**: Update in HTML

### Adding New Features
1. **New Sections**: Add HTML structure in `index.html`
2. **Styling**: Add CSS in `css/style.css`
3. **Functionality**: Add JavaScript in `js/script.js`
4. **Backend**: Add API endpoints in `backend/app.py`

## Security Considerations

1. **Input Validation**: All forms include client and server-side validation
2. **SQL Injection Protection**: Using parameterized queries
3. **XSS Protection**: Proper HTML escaping
4. **CORS Configuration**: Configured for cross-origin requests
5. **Admin Authentication**: Session-based authentication for admin panel

## Performance Optimization

1. **Image Optimization**: Use compressed images
2. **CSS/JS Minification**: Minify for production
3. **Caching**: Implement browser caching
4. **CDN**: Use CDN for external resources
5. **Database Indexing**: Index frequently queried columns

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Common Issues

1. **Flask Server Not Starting**:
   - Check if port 5000 is available
   - Verify Python dependencies are installed
   - Check for syntax errors in `app.py`

2. **Database Issues**:
   - Ensure write permissions in backend directory
   - Check SQLite installation
   - Verify database file creation

3. **Admin Panel Access**:
   - Check PHP installation
   - Verify web server configuration
   - Check database connection settings

4. **Form Submissions Not Working**:
   - Check API endpoint URLs
   - Verify CORS configuration
   - Check browser console for errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Future Enhancements

- [ ] Email notifications
- [ ] File upload functionality
- [ ] Advanced admin features
- [ ] Multi-language support
- [ ] SEO optimization
- [ ] Analytics integration
- [ ] Payment integration
- [ ] Student portal
- [ ] Course management system 