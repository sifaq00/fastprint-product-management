"""
Django management command to fetch products from Fast Print API
and save them to the database.

Usage: python manage.py fetch_products
"""
import hashlib
from datetime import datetime
import requests
from django.core.management.base import BaseCommand
from products.models import Produk, Kategori, Status


class Command(BaseCommand):
    help = 'Fetch products from Fast Print API and save to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date in format DD-MM-YY (default: today)',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Manual username from Fast Print portal',
        )

    def handle(self, *args, **options):
        # Generate credentials based on date
        if options.get('date'):
            date_str = options['date']
        else:
            now = datetime.now()
            date_str = now.strftime('%d-%m-%y')
        
        # Parse date for username
        parts = date_str.split('-')
        day, month, year = parts[0], parts[1], parts[2]
        
        # Use manual username if provided, otherwise generate it
        if options.get('username'):
            username = options['username']
            self.stdout.write(self.style.WARNING(f"Using manual username: {username}"))
        else:
            # Username: tesprogrammer + DDMMYY + C21/C22
            # Note: Username on portal might change suffix periodically (e.g. C21, C22)
            username = f"tesprogrammer{day}{month}{year}C22"
            self.stdout.write(f"Using generated username: {username}")
        
        # Password: MD5 of bisacoding-DD-MM-YY
        password_string = f"bisacoding-{date_str}"
        password_md5 = hashlib.md5(password_string.encode()).hexdigest()
        
        self.stdout.write(f"Using date: {date_str}")
        self.stdout.write(f"Password string: {password_string}")
        
        # API URL
        api_url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        
        try:
            self.stdout.write("Fetching data from API...")
            response = requests.post(api_url, data={
                'username': username,
                'password': password_md5
            }, timeout=30)
            
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"API Error: {response.status_code}"))
                self.stdout.write(response.text)
                return
            
            data = response.json()
            
            if data.get('error') != 0:
                self.stdout.write(self.style.ERROR(f"API returned error: {data}"))
                return
            
            products = data.get('data', [])
            self.stdout.write(f"Found {len(products)} products")
            
            # Process each product
            created_count = 0
            updated_count = 0
            
            for product in products:
                # Get or create Status
                status_name = product.get('status', 'tidak bisa dijual')
                status_obj, _ = Status.objects.get_or_create(
                    nama_status=status_name
                )
                
                # Get or create Kategori
                kategori_name = product.get('kategori', 'Unknown')
                kategori_obj, _ = Kategori.objects.get_or_create(
                    nama_kategori=kategori_name
                )
                
                # Get or create/update Produk
                produk_id = int(product.get('id_produk', 0))
                produk_defaults = {
                    'nama_produk': product.get('nama_produk', ''),
                    'harga': float(product.get('harga', 0)),
                    'kategori': kategori_obj,
                    'status': status_obj,
                }
                
                produk_obj, created = Produk.objects.update_or_create(
                    id_produk=produk_id,
                    defaults=produk_defaults
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            
            self.stdout.write(self.style.SUCCESS(
                f"Successfully synced products: {created_count} created, {updated_count} updated"
            ))
            
            # Print summary
            self.stdout.write(f"\nDatabase Summary:")
            self.stdout.write(f"  - Total Products: {Produk.objects.count()}")
            self.stdout.write(f"  - Total Categories: {Kategori.objects.count()}")
            self.stdout.write(f"  - Total Statuses: {Status.objects.count()}")
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Request Error: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
