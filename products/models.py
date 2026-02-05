from django.db import models


class Status(models.Model):
    """Status model - bisa dijual / tidak bisa dijual"""
    id_status = models.AutoField(primary_key=True)
    nama_status = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'status'
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.nama_status


class Kategori(models.Model):
    """Kategori produk"""
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'kategori'
        verbose_name_plural = 'Kategoris'

    def __str__(self):
        return self.nama_kategori


class Produk(models.Model):
    """Produk model"""
    id_produk = models.AutoField(primary_key=True)
    nama_produk = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.CASCADE,
        related_name='products'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='products'
    )

    class Meta:
        db_table = 'produk'
        verbose_name_plural = 'Produks'

    def __str__(self):
        return self.nama_produk
