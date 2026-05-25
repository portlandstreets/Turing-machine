from django.db import models

class TuringProgram(models.Model):
    title = models.CharField(max_length=100)
    initial_tape = models.CharField(max_length=255, default="101100")
    start_state = models.CharField(max_length=50, default="0")
    blank_symbol = models.CharField(max_length=1, default="_")
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title