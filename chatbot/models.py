from django.db import models
from pgvector.django import VectorField

class DocumentoChunk(models.Model):
    nombre_archivo = models.CharField(max_length=255)
    contenido = models.TextField()
    # 384 es la dimensión del modelo all-MiniLM-L6-v2 que usamos antes
    embedding = VectorField(dimensions=384)

    def __str__(self):
        return f"Chunk de {self.nombre_archivo}"