import os
from typing import Union

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.models import AbstractUser 
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.db.models import ImageField

from PIL import Image
from sorl.thumbnail import get_thumbnail

from authpage.models import User

class ProfilepageView(DetailView):
    model = User
    template_name = "profilepage/profilepage.html"
    context_object_name = "user"
    pk_url_kwarg = "pk"

    def post(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        if self.request.session.get("username") != self.object.username:
            self.context_ajax.update({"success": False, "message": "You are not allowed to change this user's data"})
            return JsonResponse(data=self.context_ajax)

        if "personal-image" in self.request.FILES:
            return self.upload_personal_image()
        elif "action" in self.request.POST:
            return self.handle_ajax_post()

        raise Exception(f"Cannot identify the purpose of post request: {self.request}")

    def get(self, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        return self.render_to_response(self.context)

    def handle_ajax_post(self) -> JsonResponse:
        action = self.request.POST.get("action")
        if action == "edit-about":
            return self.edit_about()
    
    def edit_about(self) -> JsonResponse:
        edited_about_text_content = self.request.POST.get("edited-about-text-content")
        self.object.about = edited_about_text_content
        try:
            self.object.save()
        except ...:
            self.context_ajax["success"] = False
            self.context_ajax["message"] = "Failed to save changes"
            self.context_ajax["about-text-content"] = self.object.about
            return JsonResponse(data=self.context_ajax)

        self.context_ajax["success"] = True
        self.context_ajax["about-text-content"] = self.object.about
        return JsonResponse(data=self.context_ajax)

    def upload_personal_image(self) -> HttpResponse:
        in_memory_image: InMemoryUploadedFile = self.request.FILES.get("personal-image")

        self.object.image = in_memory_image
        self.object.save()
        self.crop_personal_image()
        return self.render_to_response(self.context)

    """
    Crops personal raw image after it was saved in media directory
    """
    def crop_personal_image(self) -> None:
        init_path = self.object.image.path
        with Image.open(init_path) as img:
            img = Image.open(init_path)
            width, height = img.size

            crop_size = min(width, height)
            margin_lr = width - crop_size >> 1
            margin_ud = height - crop_size >> 1
            crop_box = (margin_lr, margin_ud, margin_lr + crop_size, margin_ud + crop_size)
            cropped_img = img.crop(crop_box)

            cropped_img.save(init_path)

    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)

        self.object: User = self.get_object()
        self.context = self.get_context_data(**kwargs)
        self.context_ajax = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_user_id"] = kwargs["pk"]
        context["csrf_token"] = get_token(self.request)
        context.update({
            "change_allowed": self.request.session.get("username") == self.object.username,
            "default_image_url": "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg",
            "user_logined": ("remembered" in self.request.session),
            "my_user": get_object_or_404(User.objects, username=self.request.session.get("username")),
            "theme": (self.request.COOKIES["theme"] if "theme" in self.request.COOKIES else "light"),
            "input_fields": [
                {
                    "title": "Имя",
                    "icon_class": "fas fa-user",
                    "content": self.object.first_name,
                },
                {
                    "title": "Фамилия",
                    "icon_class": "fas fa-user",
                    "content": self.object.last_name,
                },
                {
                    "title": "Номер телефона",
                    "icon_class": "fas fa-phone",
                    "content": self.object.phone_number,
                },
                {
                    "title": "Электронная почта",
                    "icon_class": "fas fa-envelope",
                    "content": self.object.email,
                },
                {
                    "title": "Хэндл",
                    "icon_class": "fas fa-user",
                    "content": self.object.username,
                },
            ],
            "about": {
                "content": self.object.about,
            },
        })

        return context
