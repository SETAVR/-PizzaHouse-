from django.contrib import admin

from .models import Category, Favorite, Order, OrderItem, Pizza, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("pizza", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "is_paid", "total_price", "created_at")
    list_filter = ("status", "is_paid")
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pizza", "author", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("pizza__title", "author__username", "text")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "pizza", "created_at")
