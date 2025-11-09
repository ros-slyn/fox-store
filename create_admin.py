from app import app, db
from models.users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect, Boolean, Column

def setup_admin():
    print("🚀 Starting admin setup...")

    with app.app_context():
        # Step 1: Add is_admin column if it doesn't exist
        print("📋 Step 1: Checking database structure...")
        try:
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('customer')]

            if 'is_admin' not in columns:
                print("➕ Adding is_admin column to customer table...")
                # Use raw SQL ALTER TABLE (SQLAlchemy does not support dynamic column add via ORM)
                db.engine.execute('ALTER TABLE customer ADD COLUMN is_admin BOOLEAN DEFAULT FALSE')
                print("✅ is_admin column added successfully!")
            else:
                print("✅ is_admin column already exists")
        except Exception as e:
            print(f"❌ Database error: {e}")
            return

        # Step 2: Create or update admin user
        print("\n👤 Step 2: Setting up admin user...")
        try:
            admin_email = 'admin@fox.com'
            admin_user = Users.query.filter_by(email=admin_email).first()

            if not admin_user:
                admin_user = Users(
                    name="FOX Admin",
                    email=admin_email,
                    password=generate_password_hash("admin123"),
                    gender="male",
                    profile="Administrator",
                    is_admin=True
                )
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Admin user created successfully!")
                print(f"   📧 Email: {admin_email}")
                print("   🔑 Password: admin123")
            else:
                admin_user.is_admin = True
                admin_user.name = "FOX Admin"
                admin_user.password = generate_password_hash("admin123")
                db.session.commit()
                print("✅ Existing user updated to admin!")

            # Step 3: Verify admin
            verified_admin = Users.query.filter_by(email=admin_email).first()
            if verified_admin and verified_admin.is_admin:
                print("✅ Admin user verified successfully!")
                print(f"   Name: {verified_admin.name}")
                print(f"   Email: {verified_admin.email}")
                print(f"   Is Admin: {verified_admin.is_admin}")

                password_correct = check_password_hash(verified_admin.password, "admin123")
                print(f"   Password verification: {password_correct}")
            else:
                print("❌ Admin verification failed!")

        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            db.session.rollback()

    print("\n🎉 Admin setup completed!")

if __name__ == "__main__":
    setup_admin()
