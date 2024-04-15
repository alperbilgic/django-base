from django.db import models


class UserRole(models.TextChoices):
    NONE = "none"
    STUDENT = "student"
    TEACHER = "teacher"
    STAFF = "staff"
    EDITOR = "editor"
    ADMIN = "admin"

    @property
    def primacy(self):
        return {
            UserRole.STUDENT.value: 1,
            UserRole.TEACHER.value: 2,
            UserRole.STAFF.value: 3,
            UserRole.EDITOR.value: 4,
            UserRole.ADMIN.value: 5,
        }.get(self.value, 0)

    def __lt__(self, other):
        self_level = self.primacy
        other_level = other.primacy
        return self_level < other_level

    def __gt__(self, other):
        self_level = self.primacy
        other_level = other.primacy
        return self_level > other_level

    def __le__(self, other):
        self_level = self.primacy
        other_level = other.primacy
        return self_level <= other_level

    def __ge__(self, other):
        self_level = self.primacy
        other_level = other.primacy
        return self_level >= other_level

    def __eq__(self, other):
        self_level = self.primacy
        other_level = other.primacy
        return self_level == other_level

    def __ne__(self, other):
        self_level = self.primacy
        other_level = other.primacy
        return self_level != other_level
