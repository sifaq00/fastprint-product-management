from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import hashlib
from datetime import datetime
import requests
from .models import Produk, Kategori, Status
from .serializers import (
    ProdukSerializer,
    ProdukCreateUpdateSerializer,
    KategoriSerializer,
    StatusSerializer
)


class StatusViewSet(viewsets.ModelViewSet):
    """ViewSet untuk Status"""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class KategoriViewSet(viewsets.ModelViewSet):
    """ViewSet untuk Kategori"""
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer


class ProdukViewSet(viewsets.ModelViewSet):
    """ViewSet untuk Produk dengan filter status"""
    queryset = Produk.objects.all().select_related('kategori', 'status').order_by('nama_produk')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProdukCreateUpdateSerializer
        return ProdukSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status (bisa_dijual / tidak_bisa_dijual / all)
        status_filter = self.request.query_params.get('status', 'all')
        
        if status_filter == 'bisa_dijual':
            queryset = queryset.filter(status__nama_status='bisa dijual')
        elif status_filter == 'tidak_bisa_dijual':
            queryset = queryset.filter(status__nama_status='tidak bisa dijual')
            
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """Delete dengan response yang jelas"""
        instance = self.get_object()
        product_name = instance.nama_produk
        self.perform_destroy(instance)
        return Response(
            {'message': f'Produk "{product_name}" berhasil dihapus'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """Delete multiple products by IDs"""
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response(
                {'error': True, 'message': 'Tidak ada produk yang dipilih'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            deleted_count, _ = Produk.objects.filter(id_produk__in=ids).delete()
            return Response({
                'error': False,
                'message': f'{deleted_count} produk berhasil dihapus',
                'deleted': deleted_count
            })
        except Exception as e:
            return Response(
                {'error': True, 'message': f'Error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def import_from_api(self, request):
        """Import products from Fast Print API"""
        try:
            # Generate credentials based on current date
            now = datetime.now()
            date_str = now.strftime('%d-%m-%y')
            day, month, year = date_str.split('-')
            
            # Username: tesprogrammer + DDMMYY + C20
            username = f"tesprogrammer{day}{month}{year}C21"
            
            # Password: MD5 of bisacoding-DD-MM-YY
            password_string = f"bisacoding-{date_str}"
            password_md5 = hashlib.md5(password_string.encode()).hexdigest()
            
            # API URL
            api_url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
            
            # Fetch from API
            response = requests.post(api_url, data={
                'username': username,
                'password': password_md5
            }, timeout=30)
            
            if response.status_code != 200:
                return Response(
                    {'error': True, 'message': f'API Error: {response.status_code}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            data = response.json()
            
            if data.get('error') != 0:
                return Response(
                    {'error': True, 'message': f'API returned error: {data.get("ket", "Unknown")}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            products = data.get('data', [])
            created_count = 0
            updated_count = 0
            
            for product in products:
                # Get or create Status
                status_name = product.get('status', 'tidak bisa dijual')
                status_obj, _ = Status.objects.get_or_create(nama_status=status_name)
                
                # Get or create Kategori
                kategori_name = product.get('kategori', 'Unknown')
                kategori_obj, _ = Kategori.objects.get_or_create(nama_kategori=kategori_name)
                
                # Get or create/update Produk
                produk_id = int(product.get('id_produk', 0))
                produk_defaults = {
                    'nama_produk': product.get('nama_produk', ''),
                    'harga': float(product.get('harga', 0)),
                    'kategori': kategori_obj,
                    'status': status_obj,
                }
                
                _, created = Produk.objects.update_or_create(
                    id_produk=produk_id,
                    defaults=produk_defaults
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            
            return Response({
                'error': False,
                'message': f'Import berhasil! {created_count} produk baru, {updated_count} produk diupdate.',
                'total': len(products),
                'created': created_count,
                'updated': updated_count
            })
            
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': True, 'message': f'Request Error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': True, 'message': f'Error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def index_view(request):
    """View untuk halaman utama"""
    return render(request, 'products/index.html')

