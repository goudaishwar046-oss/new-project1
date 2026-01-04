from app import app
from models import db, User, Scholarship, Application
from werkzeug.security import generate_password_hash

def seed():
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(name='Admin', email='admin@example.com', password_hash=generate_password_hash('adminpass'), role='admin')
            inst = User(name='Institution', email='inst@example.com', password_hash=generate_password_hash('instpass'), role='institution')
            student = User(name='Student', email='student@example.com', password_hash=generate_password_hash('studpass'), role='student')
            db.session.add_all([admin, inst, student])
            db.session.commit()

        # add scholarships
        if not Scholarship.query.first():
            s1 = Scholarship(title='Merit Scholarship', description='For meritorious students', eligibility='GPA > 8', amount='10000')
            s2 = Scholarship(title='Need-based Scholarship', description='For students with financial need', eligibility='Family income < 5L', amount='20000')
            db.session.add_all([s1, s2])
            db.session.commit()

        # add an application by student for first scholarship
        student = User.query.filter_by(email='student@example.com').first()
        scholarship = Scholarship.query.first()
        if student and scholarship and not Application.query.filter_by(student_id=student.id, scholarship_id=scholarship.id).first():
            appn = Application(student_id=student.id, scholarship_id=scholarship.id, documents='{"id":"sample"}')
            db.session.add(appn)
            db.session.commit()

        print('Seeding complete')

if __name__ == '__main__':
    seed()
