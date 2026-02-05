"""
Django management command to import products from locally saved JSON file.
Usage: python manage.py import_from_json
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from products.models import Produk, Kategori, Status


class Command(BaseCommand):
    help = 'Import products from api_data.json file'

    def handle(self, *args, **options):
        # Path to saved JSON file (in project root directory)
        from django.conf import settings
        json_path = settings.BASE_DIR / 'api_data.json'
        
        self.stdout.write(f"Loading data from: {json_path}")
        
        if not json_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {json_path}"))
            return
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
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
            f"Successfully imported products: {created_count} created, {updated_count} updated"
        ))
        
        # Print summary
        self.stdout.write(f"\nDatabase Summary:")
        self.stdout.write(f"  - Total Products: {Produk.objects.count()}")
        self.stdout.write(f"  - Total Categories: {Kategori.objects.count()}")
        self.stdout.write(f"  - Total Statuses: {Status.objects.count()}")
