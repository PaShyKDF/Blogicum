import debug_toolbar
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.conf.urls.static import static
from django.conf import settings
from user.forms import CustomUserCreationForm


User = get_user_model()

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/',
         CreateView.as_view(
             template_name='registration/registration_form.html',
             form_class=CustomUserCreationForm,
             success_url=reverse_lazy('blog:index'),
         ),
         name='registration',
         ),
    path('__debug__/', include(debug_toolbar.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.internal_sever_error'
