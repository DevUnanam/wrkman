from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from artisans.models import Category, Skill, State, City, ArtisanProfile
from reviews.models import Review
from core.models import FAQ
from decimal import Decimal
import random
import os
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data for development'

    def download_profile_image(self, seed=None):
        """Download a random profile image from Lorem Picsum"""
        try:
            # Use Lorem Picsum for placeholder images
            # Adding seed for consistent images per artisan
            url = f"https://picsum.photos/300/300?random={seed or random.randint(1, 1000)}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                return ContentFile(response.content, name=f'profile_{seed or random.randint(1000, 9999)}.jpg')
            else:
                self.stdout.write(self.style.WARNING(f'Failed to download image: HTTP {response.status_code}'))
                return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Error downloading profile image: {str(e)}'))
            return None

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

        # Create categories and skills (matching success stories template)
        categories_data = [
            {
                'name': 'Carpentry',
                'description': 'Wood work, furniture, custom builds, repairs',
                'icon': 'fa-hammer',
                'skills': ['Furniture Making', 'Cabinet Installation', 'Door Repair', 'Custom Woodwork', 'Flooring', 'Shelving', 'Deck Building']
            },
            {
                'name': 'Electrical',
                'description': 'Wiring, installations, electrical repairs and maintenance',
                'icon': 'fa-bolt',
                'skills': ['Wiring Installation', 'Lighting Setup', 'Socket Installation', 'Panel Upgrade', 'Generator Repair', 'Solar Installation', 'CCTV Setup']
            },
            {
                'name': 'Plumbing',
                'description': 'Water systems, pipe repair, installation and maintenance',
                'icon': 'fa-wrench',
                'skills': ['Pipe Installation', 'Leak Repair', 'Water Heater Service', 'Drain Cleaning', 'Toilet Repair', 'Bathroom Renovation', 'Kitchen Plumbing']
            },
            {
                'name': 'Painting',
                'description': 'Interior and exterior painting, decorative finishes',
                'icon': 'fa-paint-brush',
                'skills': ['Interior Painting', 'Exterior Painting', 'Wall Preparation', 'Color Consultation', 'Touch-ups', 'Decorative Painting', 'Spray Painting']
            },
            {
                'name': 'Masonry',
                'description': 'Bricklaying, stonework, concrete work, construction',
                'icon': 'fa-home',
                'skills': ['Bricklaying', 'Block Work', 'Stone Installation', 'Concrete Pouring', 'Wall Building', 'Foundation Work', 'Tiling']
            },
            {
                'name': 'Welding',
                'description': 'Metal fabrication, welding, metalwork services',
                'icon': 'fa-cog',
                'skills': ['Arc Welding', 'Gas Welding', 'Metal Fabrication', 'Gate Making', 'Structural Welding', 'Repair Welding', 'Stainless Steel Work']
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

        # Create sample clients (expanded for more reviews)
        client_data = [
            {'username': 'john_client', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'},
            {'username': 'jane_client', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com'},
            {'username': 'mike_client', 'first_name': 'Mike', 'last_name': 'Johnson', 'email': 'mike@example.com'},
            {'username': 'sarah_client', 'first_name': 'Sarah', 'last_name': 'Williams', 'email': 'sarah@example.com'},
            {'username': 'david_client', 'first_name': 'David', 'last_name': 'Brown', 'email': 'david@example.com'},
            {'username': 'mary_client', 'first_name': 'Mary', 'last_name': 'Davis', 'email': 'mary@example.com'},
            {'username': 'james_client', 'first_name': 'James', 'last_name': 'Wilson', 'email': 'james@example.com'},
            {'username': 'patricia_client', 'first_name': 'Patricia', 'last_name': 'Moore', 'email': 'patricia@example.com'},
            {'username': 'robert_client', 'first_name': 'Robert', 'last_name': 'Taylor', 'email': 'robert@example.com'},
            {'username': 'linda_client', 'first_name': 'Linda', 'last_name': 'Anderson', 'email': 'linda@example.com'},
            {'username': 'william_client', 'first_name': 'William', 'last_name': 'Thomas', 'email': 'william@example.com'},
            {'username': 'barbara_client', 'first_name': 'Barbara', 'last_name': 'Jackson', 'email': 'barbara@example.com'},
            {'username': 'richard_client', 'first_name': 'Richard', 'last_name': 'White', 'email': 'richard@example.com'},
            {'username': 'susan_client', 'first_name': 'Susan', 'last_name': 'Harris', 'email': 'susan@example.com'},
            {'username': 'joseph_client', 'first_name': 'Joseph', 'last_name': 'Martin', 'email': 'joseph@example.com'},
            {'username': 'jessica_client', 'first_name': 'Jessica', 'last_name': 'Thompson', 'email': 'jessica@example.com'},
            {'username': 'thomas_client', 'first_name': 'Thomas', 'last_name': 'Garcia', 'email': 'thomas@example.com'},
            {'username': 'nancy_client', 'first_name': 'Nancy', 'last_name': 'Martinez', 'email': 'nancy@example.com'},
            {'username': 'charles_client', 'first_name': 'Charles', 'last_name': 'Robinson', 'email': 'charles@example.com'},
            {'username': 'betty_client', 'first_name': 'Betty', 'last_name': 'Clark', 'email': 'betty@example.com'}
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

        # Create sample artisans (multiple per category for more reviews)
        artisan_data = [
            # Carpentry artisans
            {'username': 'david_carpenter', 'first_name': 'David', 'last_name': 'Okonkwo', 'category': 'Carpentry', 'rate': 2200},
            {'username': 'samuel_woodworker', 'first_name': 'Samuel', 'last_name': 'Adebayo', 'category': 'Carpentry', 'rate': 2800},
            {'username': 'peter_furniture', 'first_name': 'Peter', 'last_name': 'Eze', 'category': 'Carpentry', 'rate': 3200},
            {'username': 'jacob_custom', 'first_name': 'Jacob', 'last_name': 'Okoro', 'category': 'Carpentry', 'rate': 2500},
            
            # Electrical artisans
            {'username': 'fatima_electrician', 'first_name': 'Fatima', 'last_name': 'Abdullahi', 'category': 'Electrical', 'rate': 3000},
            {'username': 'ibrahim_wiring', 'first_name': 'Ibrahim', 'last_name': 'Hassan', 'category': 'Electrical', 'rate': 3500},
            {'username': 'moses_power', 'first_name': 'Moses', 'last_name': 'Bello', 'category': 'Electrical', 'rate': 2800},
            {'username': 'usman_solar', 'first_name': 'Usman', 'last_name': 'Ali', 'category': 'Electrical', 'rate': 4000},
            
            # Plumbing artisans
            {'username': 'ahmed_plumber', 'first_name': 'Ahmed', 'last_name': 'Musa', 'category': 'Plumbing', 'rate': 2500},
            {'username': 'aliyu_pipes', 'first_name': 'Aliyu', 'last_name': 'Garba', 'category': 'Plumbing', 'rate': 2700},
            {'username': 'yusuf_water', 'first_name': 'Yusuf', 'last_name': 'Sani', 'category': 'Plumbing', 'rate': 3100},
            {'username': 'haruna_drain', 'first_name': 'Haruna', 'last_name': 'Ibrahim', 'category': 'Plumbing', 'rate': 2400},
            
            # Painting artisans
            {'username': 'emeka_painter', 'first_name': 'Emeka', 'last_name': 'Nwosu', 'category': 'Painting', 'rate': 1800},
            {'username': 'chidi_colors', 'first_name': 'Chidi', 'last_name': 'Okafor', 'category': 'Painting', 'rate': 2200},
            {'username': 'daniel_brush', 'first_name': 'Daniel', 'last_name': 'Ugwu', 'category': 'Painting', 'rate': 2000},
            {'username': 'anthony_decor', 'first_name': 'Anthony', 'last_name': 'Chukwu', 'category': 'Painting', 'rate': 2500},
            
            # Masonry artisans
            {'username': 'abdul_mason', 'first_name': 'Abdul', 'last_name': 'Yusuf', 'category': 'Masonry', 'rate': 2600},
            {'username': 'mohammed_brick', 'first_name': 'Mohammed', 'last_name': 'Umar', 'category': 'Masonry', 'rate': 3000},
            {'username': 'suleiman_stone', 'first_name': 'Suleiman', 'last_name': 'Audu', 'category': 'Masonry', 'rate': 3400},
            {'username': 'garba_concrete', 'first_name': 'Garba', 'last_name': 'Shehu', 'category': 'Masonry', 'rate': 2800},
            
            # Welding artisans
            {'username': 'sunday_welder', 'first_name': 'Sunday', 'last_name': 'Ogbonna', 'category': 'Welding', 'rate': 3200},
            {'username': 'godwin_metal', 'first_name': 'Godwin', 'last_name': 'Onyema', 'category': 'Welding', 'rate': 3600},
            {'username': 'vincent_fab', 'first_name': 'Vincent', 'last_name': 'Nduka', 'category': 'Welding', 'rate': 4000},
            {'username': 'frank_steel', 'first_name': 'Frank', 'last_name': 'Obi', 'category': 'Welding', 'rate': 3400},
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

                # Download and set profile picture
                profile_image = self.download_profile_image(seed=hash(artisan['username']) % 1000)
                if profile_image:
                    user.profile_picture.save(
                        f'profile_{artisan["username"]}.jpg',
                        profile_image,
                        save=False  # Don't save yet, will save after setting other fields
                    )
                    self.stdout.write(f'Added profile image for {artisan["username"]}')

                # Save user after setting profile picture
                user.save()

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
            else:
                # Update existing artisan with profile picture if they don't have one
                user = User.objects.get(username=artisan['username'])
                if not user.profile_picture:
                    profile_image = self.download_profile_image(seed=hash(artisan['username']) % 1000)
                    if profile_image:
                        user.profile_picture.save(
                            f'profile_{artisan["username"]}.jpg',
                            profile_image,
                            save=True
                        )
                        self.stdout.write(f'Updated profile image for existing artisan: {artisan["username"]}')

                self.stdout.write(f'Artisan already exists: {artisan["username"]}')

        # Create sample reviews with diverse content
        clients = User.objects.filter(role='client')
        artisans = ArtisanProfile.objects.all()

        review_comments = [
            'Excellent work! Very professional and delivered on time. Highly recommend!',
            'Outstanding service with great attention to detail. Will definitely hire again.',
            'Good quality work at a fair price. Professional and reliable.',
            'Amazing craftsmanship! Exceeded my expectations completely.',
            'Professional service from start to finish. Very satisfied with the results.',
            'Quick response time and excellent problem-solving skills.',
            'Very satisfied with the quality and professionalism shown.',
            'Affordable pricing with excellent results. Great value for money.',
            'Punctual, professional, and delivered exactly what was promised.',
            'Excellent communication throughout the project. Highly skilled.',
            'Beautiful work with superb finishing. Completely transformed our space.',
            'Reliable service with top-notch quality. Worth every penny spent.',
            'Creative solutions and expert execution. Truly impressive work.',
            'Patient, thorough, and delivered exceptional results on time.',
            'Professional approach with excellent customer service throughout.',
            'High-quality materials used and excellent workmanship displayed.',
            'Efficient service with great attention to safety and cleanliness.',
            'Innovative approach and excellent technical skills demonstrated.',
            'Dependable service with consistent quality delivery every time.',
            'Expert knowledge with friendly and approachable customer service.',
        ]

        review_titles = [
            'Exceptional Service!',
            'Highly Recommended Professional',
            'Outstanding Quality Work',
            'Excellent Results Delivered',
            'Very Satisfied Customer',
            'Top-Quality Craftsmanship',
            'Professional Excellence',
            'Amazing Transformation',
            'Perfect Job Execution',
            'Superb Professional Service',
            'Great Value for Money',
            'Exceeded Expectations',
            'Reliable and Skilled',
            'Beautiful Finished Work',
            'Expert Level Service'
        ]

        # Ensure each artisan gets multiple reviews
        for artisan in artisans:
            # Create 8-12 reviews for each artisan to ensure good coverage
            num_reviews = random.randint(8, 12)
            available_clients = list(clients)
            
            # If we don't have enough clients, repeat some
            if len(available_clients) < num_reviews:
                selected_clients = available_clients * ((num_reviews // len(available_clients)) + 1)
                selected_clients = selected_clients[:num_reviews]
            else:
                selected_clients = random.sample(available_clients, num_reviews)

            for client in selected_clients:
                if not Review.objects.filter(client=client, artisan=artisan).exists():
                    Review.objects.create(
                        client=client,
                        artisan=artisan,
                        rating=random.randint(3, 5),  # Generally positive ratings
                        title=random.choice(review_titles),
                        comment=random.choice(review_comments),
                        would_recommend=random.choices([True, False], weights=[85, 15])[0]  # 85% would recommend
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