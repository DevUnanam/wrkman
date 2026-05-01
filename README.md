# ArtisanConnect - Local Artisan Marketplace

A Django-based web application that connects clients with verified local artisans for various services including plumbing, electrical work, hairdressing, automotive services, and more.

## Features

### 🎯 Core Features
- **Role-based User System**: Clients, Artisans, and Admin roles
- **Artisan Verification**: Admin approval system for artisan accounts
- **Advanced Search & Filtering**: Search by category, location, price range, and ratings
- **Review & Rating System**: Clients can rate and review artisans
- **Location-based Services**: Nigerian states and cities integration
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

### 👥 User Roles

#### Clients
- Register and create profiles
- Search and filter artisans
- View detailed artisan profiles
- Leave reviews and ratings
- Contact artisans directly

#### Artisans
- Multi-step registration process
- Create detailed service profiles
- Showcase skills and portfolio
- Manage availability status
- Receive and respond to reviews

#### Admin
- Approve/reject artisan registrations
- Manage categories and skills
- Monitor platform activity
- Handle reports and disputes

### 🛠 Technical Features
- Custom Django User Model
- Class-based and function-based views
- Django ORM with optimized queries
- Image upload and management
- AJAX functionality for dynamic content
- Comprehensive admin interface
- Security best practices

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### 

## Models Overview

### User Management
- **User**: Custom user model with role-based permissions
- **ArtisanProfile**: Extended profile for artisan users

### Service Categories
- **Category**: Service categories (Plumbing, Electrical, etc.)
- **Skill**: Specific skills within categories
- **State/City**: Location management

### Reviews & Ratings
- **Review**: Client reviews for artisans
- **ReviewHelpful**: Helpful votes for reviews
- **ReviewReport**: Report system for inappropriate reviews

## Key URLs

- `/` - Homepage
- `/artisans/` - Artisan listing with search/filter
- `/artisan/<id>/` - Artisan detail profile
- `/accounts/login/` - User login
- `/accounts/register/client/` - Client registration
- `/accounts/register/artisan/` - Artisan registration
- `/admin/` - Django admin interface

## Design Theme

The application uses a professional color scheme:
- **Primary**: Navy Blue (#1e3a8a)
- **Secondary**: Lime Green (#65a30d)
- **Background**: White and light grays

## Technologies Used

- **Backend**: Django 4.2.7, Python
- **Frontend**: Tailwind CSS, HTML5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Icons**: Font Awesome
- **Image Processing**: Pillow

## Development Features

- **Sample Data**: Automated sample data generation
- **Admin Interface**: Comprehensive admin panel
- **Search & Filter**: Advanced filtering capabilities
- **Responsive Design**: Mobile-first approach
- **Security**: CSRF protection, form validation

## Customization

### Adding New Categories
1. Create category in admin panel
2. Add corresponding skills
3. Update category icons if needed

### Adding New Locations
1. Add states in admin panel
2. Add cities for each state
3. Update location dropdowns

### Styling Changes
- Modify Tailwind classes in templates
- Update color scheme in `templates/base.html`
- Add custom CSS in static files
