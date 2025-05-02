# CampusMart

CampusMart is a Django-based web application that allows university students to create accounts and post items for sale. This Phase 1 submission includes user registration, login/logout functionality, and listing creation with a daily posting limit.

## Features Implemented (Final)
- User registration with name, username, email, and password
- User login and logout with session management
- Listing creation with title, description, price, condition, photo upload, and status (Available/Unavailable)
- Edit and delete own listings
- Browse all available listings in a grid view with pagination (20 per page)
- Search listings by title and description keywords
- Seller-buyer messaging system with inbox view
- Purchase additional daily listings using Krato$Coin via an external REST API
- Permissions enforced: only listing owners can edit/delete their own listings

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CampusMart.git
   cd CampusMart
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the app**
   Open your browser and go to `http://localhost:8000/`

## Notes
- Media files (uploaded photos) are stored in the /media/ folder and served locally.
- Users must be logged in to create, edit, or delete listings.
- Each user can post 3 free listings per day. Additional listings can be purchased using Krato$Coin.
- The external REST API is used for coin-based transactions (with proper token-based authentication).
