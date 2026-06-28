from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_completed(self):
        places = self.places.all()
        return places.exists() and all(p.visited for p in places)

    def __str__(self):
        return self.name


class Place(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='places')
    external_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'external_id')

    def __str__(self):
        return self.title