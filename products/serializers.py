from rest_framework import serializers
from .models import Produk, Kategori, Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id_status', 'nama_status']


class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = ['id_kategori', 'nama_kategori']


class ProdukSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source='kategori.nama_kategori', read_only=True)
    status_nama = serializers.CharField(source='status.nama_status', read_only=True)
    
    class Meta:
        model = Produk
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'kategori_nama', 'status', 'status_nama']
    
    def validate_nama_produk(self, value):
        """Validasi: nama_produk harus diisi"""
        if not value or not value.strip():
            raise serializers.ValidationError("Nama produk harus diisi")
        return value.strip()
    
    def validate_harga(self, value):
        """Validasi: harga harus berupa angka positif"""
        if value is None:
            raise serializers.ValidationError("Harga harus diisi")
        if value < 0:
            raise serializers.ValidationError("Harga harus berupa angka positif")
        return value


class ProdukCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer untuk create/update dengan validasi ketat"""
    
    class Meta:
        model = Produk
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status']
        read_only_fields = ['id_produk']
    
    def validate_nama_produk(self, value):
        """Validasi: nama_produk harus diisi"""
        if not value or not value.strip():
            raise serializers.ValidationError("Nama produk harus diisi")
        return value.strip()
    
    def validate_harga(self, value):
        """Validasi: harga harus berupa angka positif"""
        if value is None:
            raise serializers.ValidationError("Harga harus diisi")
        if value < 0:
            raise serializers.ValidationError("Harga harus berupa angka positif")
        return value
