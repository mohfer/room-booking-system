# Campus Room Reservation Application

A simple Python and SQLite-based application to manage room reservations in a campus environment. This application features an admin login system, room data management, reservation management, and reservation history tracking.

## Features

- **Admin Login**
  - Admin authentication based on username and password
- **Admin Management**
  - View admin list
  - Add new admin
  - Delete admin (cannot delete your own account)
- **Room Management**
  - View room list
  - Add new room
  - Edit room data
  - Delete room
- **Reservation Management**
  - Add room reservation
  - Edit reservation
  - Mark reservation as complete
  - Automatic schedule conflict checking
- **Reservation History**
  - Store and display complete reservation status logs with timestamp

## Database Structure

The `kampus.db` database consists of the following tables:
- `admin`: Stores admin accounts
- `ruangan`: Stores room data
- `peminjaman`: Stores reservation schedules
- `riwayat_peminjaman`: Stores reservation activity history

## Installation and Running the Program

1. **Clone Repository**
   ```bash
   git clone https://github.com/mohfer/room-booking-system
   cd room-booking-system
   ```

2. **Run the Program**
   Make sure Python 3.x is installed on your system:
   ```bash
   python main.py
   ```

3. **Default Admin Account**
   When first run, the application will automatically create an admin account:
   ```
   Username: admin
   Password: admin123
   ```

## Usage Example

After logging in as admin, you can:
- Add a new admin: `admin2 / anypassword`
- Add a room: "Multimedia Lab", capacity 40
- Create reservation schedules and see automatic schedule conflicts

## System Requirements

- Python 3.x
- SQLite (already integrated in Python's `sqlite3` module)

## Additional Notes

- Date format: `DD-MM-YYYY`
- Time format: `HH:MM` (24-hour)
- This is a CLI (Command Line Interface) based system, suitable for learning or simple systems

---

### License

This project is free to use for educational purposes.