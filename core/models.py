from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    cgpa = models.FloatField()
    internships = models.IntegerField()
    projects = models.IntegerField()
    technical_skills_score = models.IntegerField()
    hackerrank_score = models.IntegerField()
    placement_status = models.CharField(max_length=50, blank=True)
    prediction_probability = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.placement_status or 'Not predicted yet'}"

    class Meta:
        ordering = ['-created_at']