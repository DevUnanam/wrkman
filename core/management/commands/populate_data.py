from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from artisans.models import Category, Skill, State, City, ArtisanProfile
from reviews.models import Review
from core.models import FAQ
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data for development'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@artisanconnect.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin123'))
        
        # Create all 36 Nigerian states and FCT with major cities
        states_cities = {
            'Abia': ['Umuahia', 'Aba', 'Arochukwu', 'Ohafia', 'Ikwuano'],
            'Adamawa': ['Yola', 'Mubi', 'Numan', 'Jimeta', 'Ganye'],
            'Akwa Ibom': ['Uyo', 'Ikot Ekpene', 'Oron', 'Eket', 'Abak'],
            'Anambra': ['Awka', 'Onitsha', 'Nnewi', 'Ekwulobia', 'Ihiala'],
            'Bauchi': ['Bauchi', 'Azare', 'Jama\'are', 'Misau', 'Katagum'],
            'Bayelsa': ['Yenagoa', 'Sagbama', 'Brass', 'Ekeremor', 'Kolokuma'],
            'Benue': ['Makurdi', 'Gboko', 'Otukpo', 'Katsina-Ala', 'Vandeikya'],
            'Borno': ['Maiduguri', 'Biu', 'Bama', 'Dikwa', 'Gubio'],
            'Cross River': ['Calabar', 'Ugep', 'Ikom', 'Obudu', 'Ogoja'],
            'Delta': ['Asaba', 'Warri', 'Sapele', 'Ughelli', 'Agbor'],
            'Ebonyi': ['Abakaliki', 'Afikpo', 'Onueke', 'Ezza', 'Ishielu'],
            'Edo': ['Benin City', 'Auchi', 'Ekpoma', 'Uromi', 'Igarra'],
            'Ekiti': ['Ado Ekiti', 'Ikere', 'Oye', 'Ijero', 'Ise'],
            'Enugu': ['Enugu', 'Nsukka', 'Oji River', 'Awgu', 'Udi'],
            'Gombe': ['Gombe', 'Billiri', 'Kaltungo', 'Dukku', 'Bajoga'],
            'Imo': ['Owerri', 'Orlu', 'Okigwe', 'Mbaitoli', 'Nkwerre'],
            'Jigawa': ['Dutse', 'Hadejia', 'Kazaure', 'Ringim', 'Gumel'],
            'Kaduna': ['Kaduna', 'Zaria', 'Kafanchan', 'Kagoro', 'Saminaka'],
            'Kano': ['Kano', 'Wudil', 'Gwarzo', 'Rano', 'Karaye'],
            'Katsina': ['Katsina', 'Daura', 'Funtua', 'Malumfashi', 'Kankia'],
            'Kebbi': ['Birnin Kebbi', 'Argungu', 'Yauri', 'Zuru', 'Bagudo'],
            'Kogi': ['Lokoja', 'Okene', 'Kabba', 'Anyigba', 'Idah'],
            'Kwara': ['Ilorin', 'Offa', 'Omu-Aran', 'Lafiagi', 'Kaiama'],
            'Lagos': ['Ikeja', 'Victoria Island', 'Ikoyi', 'Lekki', 'Surulere', 'Yaba', 'Mushin', 'Agege', 'Alimosho', 'Epe'],
            'Nasarawa': ['Lafia', 'Keffi', 'Akwanga', 'Nasarawa', 'Doma'],
            'Niger': ['Minna', 'Bida', 'Kontagora', 'Suleja', 'New Bussa'],
            'Ogun': ['Abeokuta', 'Sagamu', 'Ijebu Ode', 'Ota', 'Ilaro'],
            'Ondo': ['Akure', 'Ondo', 'Owo', 'Ikare', 'Okitipupa'],
            'Osun': ['Osogbo', 'Ife', 'Ilesha', 'Ede', 'Iwo'],
            'Oyo': ['Ibadan', 'Ogbomoso', 'Oyo', 'Iseyin', 'Saki'],
            'Plateau': ['Jos', 'Bukuru', 'Pankshin', 'Shendam', 'Mangu'],
            'Rivers': ['Port Harcourt', 'Obio-Akpor', 'Okrika', 'Eleme', 'Bonny'],
            'Sokoto': ['Sokoto', 'Tambuwal', 'Gwadabawa', 'Bodinga', 'Illela'],
            'Taraba': ['Jalingo', 'Wukari', 'Bali', 'Gembu', 'Serti'],
            'Yobe': ['Damaturu', 'Potiskum', 'Gashua', 'Nguru', 'Geidam'],
            'Zamfara': ['Gusau', 'Kaura Namoda', 'Talata Mafara', 'Anka', 'Tsafe'],
            'Federal Capital Territory': ['Garki', 'Maitama', 'Wuse', 'Gwarinpa', 'Kubwa', 'Asokoro', 'Jabi', 'Utako', 'Nyanya', 'Karu']
        }
        
        # State codes for Nigerian states
        state_codes = {
            'Abia': 'AB',
            'Adamawa': 'AD', 
            'Akwa Ibom': 'AK',
            'Anambra': 'AN',
            'Bauchi': 'BA',
            'Bayelsa': 'BY',
            'Benue': 'BE',
            'Borno': 'BO',
            'Cross River': 'CR',
            'Delta': 'DE',
            'Ebonyi': 'EB',
            'Edo': 'ED',
            'Ekiti': 'EK',
            'Enugu': 'EN',
            'Gombe': 'GO',
            'Imo': 'IM',
            'Jigawa': 'JI',
            'Kaduna': 'KD',
            'Kano': 'KN',
            'Katsina': 'KT',
            'Kebbi': 'KE',
            'Kogi': 'KO',
            'Kwara': 'KW',
            'Lagos': 'LA',
            'Nasarawa': 'NA',
            'Niger': 'NI',
            'Ogun': 'OG',
            'Ondo': 'ON',
            'Osun': 'OS',
            'Oyo': 'OY',
            'Plateau': 'PL',
            'Rivers': 'RI',
            'Sokoto': 'SO',
            'Taraba': 'TA',
            'Yobe': 'YO',
            'Zamfara': 'ZA',
            'Federal Capital Territory': 'FC'
        }
        
        for state_name, cities in states_cities.items():
            state, created = State.objects.get_or_create(
                name=state_name,
                defaults={'code': state_codes.get(state_name, state_name[:2].upper())}
            )
            if created:
                self.stdout.write(f'Created state: {state_name}')
            
            for city_name in cities:
                city, created = City.objects.get_or_create(
                    name=city_name,
                    state=state
                )
                if created:
                    self.stdout.write(f'Created city: {city_name}, {state_name}')
        
        # Create categories and skills
        categories_data = [
            {
                'name': 'Plumbing',
                'description': 'Water systems, pipe repair, leak fixes',
                'icon': 'fa-wrench',
                'skills': ['Pipe Installation', 'Leak Repair', 'Water Heater Service', 'Drain Cleaning', 'Toilet Repair']
            },
            {
                'name': 'Electrical',
                'description': 'Wiring, installations, electrical repairs',
                'icon': 'fa-bolt',
                'skills': ['Wiring Installation', 'Lighting Setup', 'Socket Installation', 'Panel Upgrade', 'Generator Repair']
            },
            {
                'name': 'Hairdressing',
                'description': 'Hair styling, cutting, treatments',
                'icon': 'fa-cut',
                'skills': ['Hair Cutting', 'Hair Styling', 'Hair Coloring', 'Braiding', 'Hair Treatment']
            },
            {
                'name': 'Automotive',
                'description': 'Car repair and maintenance services',
                'icon': 'fa-car',
                'skills': ['Engine Repair', 'Brake Service', 'Oil Change', 'Tire Service', 'AC Repair']
            },
            {
                'name': 'Home Teaching',
                'description': 'Private tutoring and lessons',
                'icon': 'fa-graduation-cap',
                'skills': ['Mathematics', 'English', 'Science', 'Computer Skills', 'Music Lessons']
            },
            {
                'name': 'Carpentry',
                'description': 'Wood work, furniture, repairs',
                'icon': 'fa-hammer',
                'skills': ['Furniture Making', 'Cabinet Installation', 'Door Repair', 'Custom Woodwork', 'Flooring']
            },
            {
                'name': 'Cleaning',
                'description': 'House cleaning and maintenance',
                'icon': 'fa-broom',
                'skills': ['House Cleaning', 'Office Cleaning', 'Deep Cleaning', 'Carpet Cleaning', 'Window Cleaning']
            },
            {
                'name': 'Painting',
                'description': 'Interior and exterior painting',
                'icon': 'fa-paint-brush',
                'skills': ['Interior Painting', 'Exterior Painting', 'Wall Preparation', 'Color Consultation', 'Touch-ups']
            }
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon']
                }
            )
            if created:
                self.stdout.write(f'Created category: {cat_data["name"]}')
            
            for skill_name in cat_data['skills']:
                skill, created = Skill.objects.get_or_create(
                    name=skill_name,
                    category=category,
                    defaults={'description': f'{skill_name} services'}
                )
                if created:
                    self.stdout.write(f'Created skill: {skill_name}')
        
        # Create sample clients
        client_data = [
            {'username': 'john_client', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'},
            {'username': 'jane_client', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com'},
            {'username': 'mike_client', 'first_name': 'Mike', 'last_name': 'Johnson', 'email': 'mike@example.com'},
            {'username': 'sarah_client', 'first_name': 'Sarah', 'last_name': 'Williams', 'email': 'sarah@example.com'},
        ]
        
        for client in client_data:
            if not User.objects.filter(username=client['username']).exists():
                User.objects.create_user(
                    username=client['username'],
                    password='password123',
                    first_name=client['first_name'],
                    last_name=client['last_name'],
                    email=client['email'],
                    role='client'
                )
                self.stdout.write(f'Created client: {client["username"]}')
        
        # Create sample artisans
        artisan_data = [
            {'username': 'ahmed_plumber', 'first_name': 'Ahmed', 'last_name': 'Hassan', 'category': 'Plumbing', 'rate': 2500},
            {'username': 'fatima_electrician', 'first_name': 'Fatima', 'last_name': 'Abdullahi', 'category': 'Electrical', 'rate': 3000},
            {'username': 'kemi_hairdresser', 'first_name': 'Kemi', 'last_name': 'Adebayo', 'category': 'Hairdressing', 'rate': 1500},
            {'username': 'ibrahim_mechanic', 'first_name': 'Ibrahim', 'last_name': 'Musa', 'category': 'Automotive', 'rate': 2000},
            {'username': 'grace_teacher', 'first_name': 'Grace', 'last_name': 'Okoro', 'category': 'Home Teaching', 'rate': 2500},
            {'username': 'david_carpenter', 'first_name': 'David', 'last_name': 'Okonkwo', 'category': 'Carpentry', 'rate': 2200},
            {'username': 'aisha_cleaner', 'first_name': 'Aisha', 'last_name': 'Bello', 'category': 'Cleaning', 'rate': 1200},
            {'username': 'emeka_painter', 'first_name': 'Emeka', 'last_name': 'Nwosu', 'category': 'Painting', 'rate': 1800},
        ]
        
        states = list(State.objects.all())
        
        for artisan in artisan_data:
            if not User.objects.filter(username=artisan['username']).exists():
                # Create user
                user = User.objects.create_user(
                    username=artisan['username'],
                    password='password123',
                    first_name=artisan['first_name'],
                    last_name=artisan['last_name'],
                    email=f'{artisan["username"]}@example.com',
                    role='artisan',
                    is_active=True,
                    is_verified=True
                )
                
                # Create artisan profile
                category = Category.objects.get(name=artisan['category'])
                random_state = random.choice(states)
                random_city = random.choice(list(random_state.cities.all()))
                
                profile = ArtisanProfile.objects.create(
                    user=user,
                    category=category,
                    state=random_state,
                    city=random_city,
                    bio=f'Experienced {artisan["category"].lower()} professional with {random.randint(2, 15)} years of experience. Committed to quality work and customer satisfaction.',
                    hourly_rate=Decimal(str(artisan['rate'])),
                    years_of_experience=random.randint(2, 15),
                    is_verified=True
                )
                
                # Add random skills from category
                category_skills = list(category.skills.all())
                if category_skills:
                    selected_skills = random.sample(category_skills, min(3, len(category_skills)))
                    profile.skills.set(selected_skills)
                
                self.stdout.write(f'Created artisan: {artisan["username"]}')
        
        # Create sample reviews
        clients = User.objects.filter(role='client')
        artisans = ArtisanProfile.objects.all()
        
        review_comments = [
            'Excellent work! Very professional and timely.',
            'Great service, would definitely recommend.',
            'Good quality work at fair price.',
            'Professional and reliable. Will hire again.',
            'Outstanding service and attention to detail.',
            'Quick response and excellent results.',
            'Very satisfied with the quality of work.',
            'Affordable and efficient service.',
        ]
        
        review_titles = [
            'Great Service!',
            'Highly Recommended',
            'Professional Work',
            'Excellent Results',
            'Very Satisfied',
            'Quality Service',
            'Will Hire Again',
            'Outstanding Work'
        ]
        
        for artisan in artisans:
            # Create 1-5 random reviews for each artisan
            num_reviews = random.randint(1, 5)
            selected_clients = random.sample(list(clients), min(num_reviews, len(clients)))
            
            for client in selected_clients:
                if not Review.objects.filter(client=client, artisan=artisan).exists():
                    Review.objects.create(
                        client=client,
                        artisan=artisan,
                        rating=random.randint(3, 5),  # Generally good ratings
                        title=random.choice(review_titles),
                        comment=random.choice(review_comments),
                        would_recommend=random.choice([True, True, True, False])  # 75% would recommend
                    )
        
        # Create FAQs
        faqs_data = [
            {
                'question': 'How do I find artisans in my area?',
                'answer': 'Use our search feature to filter artisans by location, category, and rating. You can also browse by specific services you need.',
                'order': 1
            },
            {
                'question': 'Are all artisans verified?',
                'answer': 'Yes, all artisans go through our verification process which includes background checks and skill assessment before being approved.',
                'order': 2
            },
            {
                'question': 'How do I book an artisan?',
                'answer': 'Visit the artisan\'s profile page and contact them directly through the platform to discuss your needs and schedule.',
                'order': 3
            },
            {
                'question': 'What if I\'m not satisfied with the service?',
                'answer': 'You can leave a review and contact our support team. We work to resolve any issues and maintain quality standards.',
                'order': 4
            },
            {
                'question': 'How do I become a verified artisan?',
                'answer': 'Register as an artisan, complete your profile with relevant skills and experience, and wait for admin approval.',
                'order': 5
            }
        ]
        
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'order': faq_data['order']
                }
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq_data["question"]}')
        
        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
        self.stdout.write(
            self.style.SUCCESS('Login credentials:')
        )
        self.stdout.write('Admin: admin/admin123')
        self.stdout.write('Clients: john_client/password123, jane_client/password123, etc.')
        self.stdout.write('Artisans: ahmed_plumber/password123, fatima_electrician/password123, etc.')