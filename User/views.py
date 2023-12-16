from django.contrib.auth.views import LoginView
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from User.forms import CustomUserCreationForm
from User.forms import UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView 
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from User.forms import CustomUserCreationForm
from User.forms import UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import login, get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from Post.models import Post
from Post.forms import PostForm
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from Group.forms import EditGroupForm


def pagina_inicio(request):
    # apararecer solo when is_home is false
    is_homepage = True
    return render(request, 'Homepage.html', {'is_homepage': is_homepage})


# Login 
def custom_login(request):
    if request.user.is_authenticated:
        # Si el usuario ya ha iniciado sesión, redirige a la vista de dashboard
        return redirect('User:feed')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('User:feed')  # Redirige a la vista de dashboard después del inicio de sesión
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
from django.db import IntegrityError

# FUNCION DE REGISTRO
def register(request):
    if request.user.is_authenticated:
        return redirect('User:feed')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']

            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                messages.error(request, 'El correo o nombre de usuario ya están registrados.')
            else:
                user = form.save()

                # Crea un perfil de usuario asociado al nuevo usuario
                user_profile = UserProfile.objects.create(user=user)
                user_profile.email = email  # Establece el email en el perfil

                # Establece el nivel_de_dominio en 1
                user_profile.nivel_de_dominio = json.dumps({"ejemplo": 1})

                # Establece el campo de intereses en "ejemplo"
                user_profile.intereses = "ejemplo"

                # Establece el campo de preferencias en "ejemplo"
                user_profile.preferencias = "ejemplo"

                user_profile.save()

                # Enviar correo de bienvenida
                subject = '¡Bienvenido a nuestro sitio AcademyWeb!'
                message = f'¡Hola {username}!\n\n¡Gracias por registrarte en nuestro sitio! Disfruta de tu experiencia y comparte con la comunidad.'
                send_mail(subject, message, None, [email])

                login(request, user)
                return redirect('User:feed')
        else:
            return render(request, 'register.html', {'form': form})

    form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


from Coments.forms import CommentForm
from Post.models import Comment
# FUNCION DE PERFIL
from django.shortcuts import get_object_or_404, redirect


def eliminar_publicacion_feed(request, post_id):
    if request.method == 'POST':
        # Intenta obtener la publicación del modelo Post
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            post = None

        # Si la publicación no se encuentra en el modelo Post, intenta obtenerla del modelo PostGroup
        if not post:
            try:
                post = PostGroup.objects.get(pk=post_id)
            except PostGroup.DoesNotExist:
                post = None

        # Si la publicación se encuentra y el usuario actual es el autor de la publicación, entonces la publicación se eliminará
        if post and request.user == post.autor:
            post.delete()
            messages.success(request, 'La publicación se ha eliminado exitosamente.')
        else:
            messages.error(request, 'No se pudo eliminar la publicación.')

        # Redirige al usuario a la página de inicio (o donde prefieras) después de eliminar la publicación
        return redirect('User:feed')


from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q  # Necesario para consultas OR
from User.forms import SearchGroupForm
from Group.models import JoinRequest

def feed(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_interests = user_profile.intereses.split(',')  # 
    
    user_posts = Post.objects.filter(autor=user).order_by('-fecha_publicacion')
    grupos_usuario_ids = Group.objects.filter(miembros=user).values_list('id', flat=True)

    grupos_administrados_ids = Group.objects.filter(administrador=user).values_list('id', flat=True)

    grupos_usuario_ids = list(set(list(grupos_usuario_ids) + list(grupos_administrados_ids)))

    group_posts = PostGroup.objects.filter(grupo__id__in=grupos_usuario_ids).order_by('-fecha_publicacion')

    post_form = PostForm()
    comment_form = CommentForm()
    search_form = SearchGroupForm(request.GET)
    grupos_encontrados = Group.objects.none()
    suggested_groups = Group.objects.none()
    for interest in user_interests:
        suggested_groups |= Group.objects.filter(nombre__icontains=interest)


    post_form = PostForm()
    comment_form = CommentForm()
    search_form = SearchGroupForm(request.GET)
    grupos_encontrados = Group.objects.none()
    
    if search_form.is_valid():
        nombre_grupo_query = search_form.cleaned_data.get('nombre')
        grupos_encontrados = Group.objects.filter(nombre__icontains=nombre_grupo_query)

    if request.method == 'POST':
        if 'publicar' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                new_post = post_form.save(commit=False)
                new_post.autor = user

                if 'archivo_adjunto' in request.FILES:
                    archivo_adjunto = request.FILES['archivo_adjunto']
                    allowed_extensions = ['.xlsx', '.xls', '.doc', '.docx', '.pdf', '.pptx', '.mpp']
                    file_extension = os.path.splitext(archivo_adjunto.name)[1]

                    if file_extension not in allowed_extensions:
                        post_form.add_error('archivo_adjunto', "Tipo de archivo no permitido. Solo se permiten archivos de Excel, Word, PDF, PPTX y project")
                    else:
                        new_post.nombre_archivo = archivo_adjunto.name
                        new_post.save()
                        messages.success(request, 'La publicación se ha subido exitosamente.')
                        post_form = PostForm()
                else:
                    pass
            else:
                post_form = PostForm()

        elif 'comentar' in request.POST:
            comment_form = CommentGroupForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                post_id_str = request.POST.get('post_id', '')
            
                if post_id_str.isdigit():
                    post_id = int(post_id_str)
                    post = PostGroup.objects.get(pk=post_id)
                    new_comment.post = post
                    new_comment.author = request.user
                    new_comment.save()
                    messages.success(request, 'El comentario se ha agregado exitosamente.')
                    comment_form = CommentGroupForm()
                else:
                    messages.error(request, 'El ID de la publicación no es válido.')
            else:
                messages.error(request, 'El formulario de comentario no es válido.')
                
        elif 'join_request' in request.POST:
            group_id_str = request.POST.get('group_id', '')
            if group_id_str.isdigit():
                group_id = int(group_id_str)
                group = Group.objects.get(pk=group_id)
                join_request, created = JoinRequest.objects.get_or_create(group=group, sender=user)
                if created:
                    messages.success(request, 'Solicitud de unión enviada.')
                else:
                    messages.info(request, 'Ya has enviado una solicitud de unión a este grupo.')
                    
    context = {
        'user_posts': user_posts,
        'group_posts': group_posts,
        'post_form': post_form,
        'comment_form': comment_form,
        'grupos_encontrados': grupos_encontrados,
        'search_form': search_form,
        'suggested_groups': suggested_groups,  
    }

    return render(request, 'feed.html', context)


def mi_vista(request):
    # Obtiene el valor del campo de búsqueda del formulario
    nombre_grupo_query = request.GET.get('nombre', '')

    # Realiza la búsqueda en la base de datos
    grupos_encontrados = Group.objects.filter(nombre__icontains=nombre_grupo_query)

    # Pasa los resultados de la búsqueda al contexto de la plantilla
    context = {
        'grupos_encontrados': grupos_encontrados,
    }

    # Renderiza la plantilla con el contexto
    return render(request, 'base.html', context)




@login_required
def dashboard(request):
    # Obtener el usuario que hizo la solicitud al iniciar sesión
    user = request.user
    # Obtener el perfil de usuario asociado
    user_profile = user.userprofile

    try:
        # Intenta cargar el nivel de dominio del usuario desde JSON
        dominions = json.loads(user_profile.nivel_de_dominio)
    except (json.JSONDecodeError, TypeError):
        # Si hay un error al cargar JSON, establece un diccionario vacío
        dominions = {}

    # Publicacion formulario
    if request.method == 'POST' and 'publicar' in request.POST:
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            # Si el formulario de publicación es válido
            new_post = post_form.save(commit=False)
            new_post.autor = user

            if 'archivo_adjunto' in request.FILES:
                archivo_adjunto = request.FILES['archivo_adjunto']

                # Validar la extensión del archivo
                allowed_extensions = ['.xlsx', '.xls', '.doc', '.docx', '.pdf','.pptx','.mpp']
                file_extension = os.path.splitext(archivo_adjunto.name)[1]

                if file_extension not in allowed_extensions:
                    # Agrega un mensaje de error al formulario
                    post_form.add_error('archivo_adjunto', "Tipo de archivo no permitido. Solo se permiten archivos de Excel, Word, PDF, PPTX y project")
                else:
                    new_post.nombre_archivo = archivo_adjunto.name
                    new_post.save()
                    messages.success(request, 'La publicación se ha subido exitosamente.')
                    post_form = PostForm()
            else:
                pass
        else:
            pass  # Hacer algo si el formulario no es válido, como mostrar un mensaje de error

    else:
        post_form = PostForm()

    # Filtrar las publicaciones del usuario actual
    posts = Post.objects.filter(autor=user).order_by('-fecha_publicacion')

    # Comentario formulario
    if request.method == 'POST' and 'comentar' in request.POST:
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            # Si el formulario de comentario es válido
            new_comment = comment_form.save(commit=False)
            post_id_str = request.POST.get('post_id', '')
            if post_id_str.isdigit():
                post_id = int(post_id_str)
                post = Post.objects.get(pk=post_id)
                new_comment.post = post
                new_comment.author = user
                new_comment.save()
                messages.success(request, 'El comentario se ha agregado exitosamente.')
                comment_form = CommentForm()
            else:
                messages.error(request, 'El ID del post no es válido.')
        else:
            messages.error(request, 'El formulario de comentario no es válido')

    else:
        comment_form = CommentForm()

    # Preparar el contexto para la plantilla
    context = {
        'user': user,
        'dominions': dominions,
        'post_form': post_form,
        'comment_form': comment_form,
        'posts': posts,
    }

    # Renderizar la plantilla 'dashboard.html' con el contexto y devolver la respuesta
    return render(request, 'dashboard.html', context)



from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages

def eliminar_publicacion(request, publicacion_id):
    # Obtén la publicación que deseas eliminar
    publicacion = get_object_or_404(Post, id=publicacion_id)

    # Verifica si el usuario actual es el autor de la publicación o tiene permisos adecuados
    if request.user == publicacion.autor:
        # Elimina la publicación
        publicacion.delete()

        # Agrega un mensaje de éxito
        messages.success(request, 'Publicación eliminada correctamente.')

        # Redirige a la página de perfil o a donde desees después de eliminar
        return redirect('User:dashboard')  # Reemplaza 'User:perfil' con la URL correcta
    else:
        # Maneja el caso en el que el usuario no está autorizado para eliminar la publicación
        return redirect('User:dashboard')  # Puedes redirigir a la página de perfil o mostrar un mensaje de error
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from PostGroup.models import PostGroup

def eliminar_publicacion_grupo(request, publicacion_id):
    # Obtén la publicación que deseas eliminar
    publicacion = get_object_or_404(PostGroup, id=publicacion_id)
    
    # Obten el ID del grupo al que pertenece la publicación
    group_id = publicacion.grupo.id

    # Verifica si el usuario actual es el autor de la publicación o un administrador del grupo
    if request.user == publicacion.autor or request.user == publicacion.grupo.administrador:
        # Elimina la publicación
        publicacion.delete()

        # Agrega un mensaje de éxito
        messages.success(request, 'Publicación eliminada correctamente.')

        # Redirige al grupo desde el que se eliminó la publicación
        return redirect('User:group_detail', group_id=group_id)
    else:
        # Maneja el caso en el que el usuario no está autorizado para eliminar la publicación
        return redirect('User:dashboard')   # Puedes redirigir a la página de perfil o mostrar un mensaje de error


# Logout cutomizado con contrib.auth 
from django.contrib.auth import logout
def custom_logout(request):
    logout(request)
    return redirect('User:login') 

from .forms import UserProfileForm 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
import json
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from Post.models import Comment  # Asegúrate de importar el modelo correcto

@login_required

# En tu archivo views.py





def eliminar_comentario(request, comentario_id):
    # Obtén el comentario que deseas eliminar
    comentario = get_object_or_404(Comment, id=comentario_id)

    # Verifica si el usuario actual es el autor del comentario o tiene permisos adecuados
    if request.user == comentario.author:
        # Elimina el comentario
        comentario.delete()

        # Agrega un mensaje de éxito
        messages.success(request, 'Comentario eliminado correctamente.')

        # Redirige a la página de perfil o a donde desees después de eliminar
        return redirect('User:dashboard')  # Reemplaza 'User:dashboard' con la URL correcta
    else:
        # Maneja el caso en el que el usuario no está autorizado para eliminar el comentario
        messages.error(request, 'No estás autorizado para eliminar este comentario.')
        return redirect('User:dashboard')  # Puedes redirigir a la página de perfil o mostrar un mensaje de error

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from PostGroup.models import CommentGroup

def eliminar_comentario_grupo(request, comentario_id):
    # Obtén el comentario que deseas eliminar
    comentario = get_object_or_404(CommentGroup, id=comentario_id)

    # Verifica si el usuario actual es el autor del comentario
    if request.user == comentario.author:
        # Elimina el comentario
        comentario.delete()

        # Agrega un mensaje de éxito
        messages.success(request, 'Comentario eliminado correctamente.')

        # Redirige a la página del grupo o a donde desees después de eliminar
        return redirect('User:group_detail', group_id=comentario.post.grupo.id)
    else:
        # Maneja el caso en el que el usuario no está autorizado para eliminar el comentario
        messages.error(request, 'No estás autorizado para eliminar este comentario.')
        return redirect('User:group_detail', group_id=comentario.post.grupo.id)

def eliminar_comentario_grupo_desde_el_feed(request, comentario_id):
    # Obtén el comentario que deseas eliminar
    comentario = get_object_or_404(CommentGroup, id=comentario_id)

    # Verifica si el usuario actual es el autor del comentario
    if request.user == comentario.author:
        # Elimina el comentario
        comentario.delete()

        # Agrega un mensaje de éxito
        messages.success(request, 'Comentario eliminado correctamente.')

        # Redirige a la página del grupo o a donde desees después de eliminar
        return redirect('User:feed')
    else:
        # Maneja el caso en el que el usuario no está autorizado para eliminar el comentario
        messages.error(request, 'No estás autorizado para eliminar este comentario.')
        return redirect('User:feed')


def edit_profile(request):
    user_profile = request.user.userprofile
    user_interests = user_profile.intereses.split(',') if user_profile.intereses else []

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.intereses = ','.join(request.POST.getlist('interests'))

            interests_and_dominions = {}

            for idx, interest in enumerate(request.POST.getlist('interests')):
                dominion = request.POST.get(f"dominion_{idx + 1}")
                interests_and_dominions[interest] = dominion

            user_profile.nivel_de_dominio = json.dumps(interests_and_dominions)
            user_profile.save()

            # Procesa los nuevos intereses y dominios
            new_interests = request.POST.getlist('newInterest')
            new_dominions = request.POST.getlist('newDominion')

            for interest, dominion in zip(new_interests, new_dominions):
                interests_and_dominions[interest] = dominion

            user_profile.nivel_de_dominio = json.dumps(interests_and_dominions)
            user_profile.save()

            # Muestra un mensaje de éxito
            messages.success(request, 'Cambios guardados con éxito.')

            return redirect('User:dashboard')
        else:
            # Muestra un mensaje de error si el formulario no es válido
            messages.error(request, 'Error al guardar cambios. Por favor, verifica tus datos.')

    else:
        form = UserProfileForm(instance=user_profile)

    interests = [
        'Matemáticas', 'Física', 'Química', 'Biología', 'Historia', 'Literatura',
        # Añade más intereses aquí
    ]

    dominions = json.loads(user_profile.nivel_de_dominio) if user_profile.nivel_de_dominio else {}

    return render(request, 'edit_profile.html', {'form': form, 'interests': interests, 'dominions': dominions, 'user_interests': user_interests})
# vistas de recuperar contraseña
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_model = get_user_model()
            email = form.cleaned_data['email']
            try:
                user = user_model.objects.get(email=email)
            except user_model.DoesNotExist:
             
                return render(request, 'recover.html', {'form': form, 'success_message': True})
            
            # Genera un token único para el usuario
            token = default_token_generator.make_token(user)

            # Crea el enlace de restablecimiento de contraseña
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            reset_url = f'http://{domain}/recover/confirm/{uidb64}/{token}/'


            # Construye el mensaje de correo electrónico
            subject = 'Restablecer contraseña'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'reset_url': reset_url,
                
            })
# Construye el mensaje de correo electrónico
        subject = 'Restablecer contraseña'
        message = '''
    <html>
    <body>
        <p>Hola {0},</p>
        <p>Recibiste este correo electrónico porque solicitaste restablecer tu contraseña en nuestro sitio web.</p>
        <p>Para cambiar tu contraseña, haz clic en el siguiente enlace:</p>
        <p><a href="{1}">Restablecer Contraseña</a></p>
        <p>Si no solicitaste este restablecimiento, puedes ignorar este correo electrónico y tu contraseña seguirá siendo la misma.</p>
        <p>Gracias,<br>El equipo de nuestro sitio web</p>
    </body>
    </html>
    '''.format(user.username, reset_url)

            # Envía el correo electrónico
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], html_message=message)

            # Puedes mostrar un mensaje de éxito o redirigir a una página de éxito
        return render(request, 'recover_done.html')


    else:
        form = PasswordResetForm()

    return render(request, 'recover.html', {'form': form})
  
def password_reset_done(request):
    
    return render(request, 'recover_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                # Actualizar la contraseña del usuario
                form.save()

               # Redirigir a la página de éxito después de restablecer la contraseña
                return render(request, 'recover_complete.html')
        else:
            form = SetPasswordForm(user)

        return render(request, 'recover_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
    else:
        return render(request, 'recover_confirm_invalid.html')

def password_reset_complete(request):
   
    return render(request, 'recover_complete.html')

# Vistas de Creacion de grupo

from django.shortcuts import render, redirect
from Group.forms import GroupCreationForm
from Group.models import Group


# CREACION DE GRUPOS

def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.administrador = request.user  # Asignar el administrador del grupo
            group.save()
            form.save_m2m()  # Guardar los miembros del grupo
            return redirect('Group:group_detail', group_id=group.pk)  # Redirigir a la página de detalles del grupo
    else:
        form = GroupCreationForm()

    return render(request, 'create_group.html', {'form': form})

# PERFIL DEL
from django.shortcuts import render, get_object_or_404
from PostGroup.models import PostGroup
from PostGroup.forms import PostGroupForm



from django.shortcuts import render, get_object_or_404
from django.contrib import messages


from commentsgroup.forms import CommentGroupForm  # Asegúrate de importar el formulario CommentGroupForm
# views.py


from django.contrib import messages
from django.shortcuts import render, get_object_or_404

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    posts = PostGroup.objects.filter(grupo=group)
    user = request.user
    is_member = user in group.miembros.all() or user == group.administrador

    post_form = PostGroupForm()
    comment_form = CommentGroupForm()

    if request.method == 'POST' and is_member:
        if 'publicar' in request.POST:
            post_form = PostGroupForm(request.POST, request.FILES)
            if post_form.is_valid():
                new_post = post_form.save(commit=False)
                new_post.autor = user
                new_post.grupo = group

                if 'archivo_adjunto' in request.FILES:
                    archivo_adjunto = request.FILES['archivo_adjunto']
                    new_post.archivo_adjunto = archivo_adjunto
                    new_post.nombre_archivo = archivo_adjunto.name

                new_post.save()
                messages.success(request, 'La publicación se ha subido exitosamente.')
                post_form = PostGroupForm()
        elif 'comentar' in request.POST:
            comment_form = CommentGroupForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                post_id_str = request.POST.get('post_id', '')
                
                if post_id_str.isdigit():
                    post_id = int(post_id_str)
                    post = PostGroup.objects.get(pk=post_id)
                    new_comment.post = post
                    new_comment.author = request.user
                    new_comment.save()
                    messages.success(request, 'El comentario se ha agregado exitosamente.')
                    comment_form = CommentGroupForm()
                else:
                    messages.error(request, 'El ID de la publicación no es válido.')
            else:
                messages.error(request, 'El formulario de comentario no es válido')

    context = {
        'group': group,
        'post_form': post_form if is_member else None,
        'comment_form': comment_form if is_member else None,
        'posts': posts,
        'is_member': is_member,
    }

    return render(request, 'group_detail.html', context)

from PostGroup.models import Calificacion
from django.db.models import Sum
def calificar_publicacion_grupo(request, post_id):
    if request.method == 'POST':
        calificacion = request.POST.get('calificacion')
        post = get_object_or_404(PostGroup, pk=post_id)
        calificacion_obj, created = Calificacion.objects.get_or_create(usuario=request.user, post=post)
        calificacion_obj.calificacion = int(calificacion)
        calificacion_obj.save()
        post.total_calificaciones = Calificacion.objects.filter(post=post).aggregate(Sum('calificacion'))['calificacion__sum']
        post.save()
        messages.success(request, 'La calificación se ha guardado exitosamente.')
    return redirect('User:group_detail', group_id=post.grupo.id)

def calificar_publicacion_grupo_feed(request, post_id):
    if request.method == 'POST':
        calificacion = request.POST.get('calificacion')
        post = get_object_or_404(PostGroup, pk=post_id)
        calificacion_obj, created = Calificacion.objects.get_or_create(usuario=request.user, post=post)
        calificacion_obj.calificacion = int(calificacion)
        calificacion_obj.save()
        post.total_calificaciones = Calificacion.objects.filter(post=post).aggregate(Sum('calificacion'))['calificacion__sum']
        post.save()
        messages.success(request, 'La calificación se ha guardado exitosamente.')
    return redirect('User:feed')

# ADMINISTRACION DE GRUPOS 

from django.shortcuts import render, redirect
from Group.models import Group
from django.db.models import Q


from django.shortcuts import render, redirect
from Group.models import Group, GroupInvitation

def administrar_grupos(request):
    # Obtener grupos que el usuario administra
    grupos_administrados = Group.objects.filter(administrador=request.user)

    # Obtener grupos a los que el usuario pertenece y no administra
    grupos_pertenecientes = Group.objects.filter(miembros=request.user).exclude(administrador=request.user)

    # Obtener las invitaciones pendientes del usuario
    invitations = GroupInvitation.objects.filter(nombre_de_usuario=request.user, accepted=False)

    if request.method == 'POST':
        buscar_grupo = request.POST.get('buscar_grupo', None)
        if buscar_grupo:
            # Realizar la búsqueda de grupos por nombre
            grupos_encontrados = Group.objects.filter(nombre__icontains=buscar_grupo)
        else:
            grupos_encontrados = None
    else:
        grupos_encontrados = None

    return render(request, 'administrar_grupos.html', {
        'grupos_administrados': grupos_administrados,
        'grupos_pertenecientes': grupos_pertenecientes,
        'grupos_encontrados': grupos_encontrados,
        'invitations': invitations,  # Agrega las invitaciones pendientes al contexto
    })


# Invitaciones

from django import forms
from Group.models import GroupInvitation
from Group.forms import GroupInvitationForm


from django.shortcuts import render, redirect, get_object_or_404
from Group.models import Group
from Group.forms import GroupInvitationForm

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from Group.models import Group, GroupInvitation

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from Group.models import Group, GroupInvitation

def enviar_invitacion_grupo(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if request.method == 'POST':
        form = GroupInvitationForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_de_usuario']
            try:
                user_to_invite = User.objects.get(username=nombre_usuario)

                if user_to_invite in group.miembros.all():
                    messages.error(request, 'El usuario ya es miembro del grupo.', extra_tags='alert-danger')
                else:
                    if user_to_invite == group.administrador:
                        messages.error(request, 'No puedes invitarte a ti mismo, ya eres el administrador del grupo.', extra_tags='alert-danger')
                    else:
                        existing_invitation = GroupInvitation.objects.filter(
                            group=group, nombre_de_usuario=nombre_usuario, accepted=False
                        )
                        if existing_invitation.exists():
                            messages.error(request, 'Ya existe una invitación pendiente para este usuario en el grupo.', extra_tags='alert-danger')
                        else:
                            invitation = form.save(commit=False)
                            invitation.group = group
                            invitation.sender = request.user
                            invitation.nombre_de_usuario = user_to_invite
                            invitation.save()
                            messages.success(request, 'Invitación enviada correctamente.')

                return redirect('User:group_detail', group_id)
            except User.DoesNotExist:
                form.add_error('nombre_de_usuario', 'Usuario no encontrado')

    else:
        form = GroupInvitationForm()

    return render(request, 'enviar_invitacion_grupo.html', {'form': form, 'group': group})




from django.contrib import messages

def aceptar_invitacion(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, pk=invitation_id)
    group = invitation.group

    # Agregar al usuario al grupo
    group.miembros.add(request.user)
    invitation.accepted = True
    invitation.save()

    # Agregar un mensaje de éxito con el nombre del grupo
    messages.success(request, f'Te has unido al grupo "{group.nombre}" correctamente.')

    return redirect('User:group_detail', group_id=group.id)



def rechazar_invitacion(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, pk=invitation_id)
    invitation.delete()  # Elimina la invitación de la base de datos
    messages.success(request, 'Invitación rechazada correctamente.')  # Agrega un mensaje de éxito
    return redirect('User:administrar_grupos')  # Redirige al usuario a donde prefieras

def abandonar_grupo(request, group_id):
    # Obtén el grupo al que el usuario desea salir
    group = get_object_or_404(Group, pk=group_id)

    # Verifica si el usuario es un miembro del grupo
    if request.user in group.miembros.all():
        # Quita al usuario del grupo
        group.miembros.remove(request.user)
        messages.success(request, f'Te has retirado del grupo "{group.nombre}" correctamente.')
    else:
        messages.error(request, 'No eres miembro de este grupo.')

    return redirect('User:administrar_grupos')

def group_members(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    members = group.miembros.all()
    join_requests = group.join_requests.all()  # Nuevas solicitudes de unión
    return render(request, 'group_members.html', {'group': group, 'members': members, 'join_requests': join_requests})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from Group.models import JoinRequest

def aceptar_solicitud(request, join_request_id):
    join_request = get_object_or_404(JoinRequest, pk=join_request_id)
    group = join_request.group
    user = join_request.sender

    if request.method == 'POST':
        group.miembros.add(user)
        join_request.delete()
        messages.success(request, f'Se ha aceptado la solicitud de {user.username} para unirse al grupo {group.nombre}.')

    return redirect('User:group_members', group_id=group.id)

def rechazar_solicitud(request, join_request_id):
    join_request = get_object_or_404(JoinRequest, pk=join_request_id)
    group = join_request.group
    user = join_request.sender

    if request.method == 'POST':
        join_request.delete()
        messages.success(request, f'Se ha rechazado la solicitud de {user.username} para unirse al grupo {group.nombre}.')

    return redirect('User:group_members', group_id=group.id)


@login_required
def eliminar_miembro(request, group_id, member_id):
    group = Group.objects.get(id=group_id)
    member = group.miembros.get(id=member_id)
    
    if request.user == group.administrador:
        # Verificar que el usuario actual sea el administrador del grupo
        group.miembros.remove(member)
        return redirect('User:group_members', group_id=group_id)
    else:
        # Manejar el caso en el que el usuario no esté autorizado para eliminar al miembro
        return redirect('User:dashboard')


@login_required
def editar_grupo(request, group_id):
    group = Group.objects.get(id=group_id)

    if request.method == 'POST':
        form = EditGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo actualizado correctamente.')
            return redirect('User:group_detail', group_id=group.id)
    else:
        form = EditGroupForm(instance=group)

    return render(request, 'editar_grupo.html', {'form': form})


# FEED
from django.shortcuts import render


def vista_de_busqueda_de_grupos(request):
    grupos_encontrados = []
    if 'nombre_grupo' in request.GET:
        nombre_grupo = request.GET['nombre_grupo']
        grupos_encontrados = Group.objects.filter(nombre__icontains=nombre_grupo)

    return render(request, 'feed.html', {'grupos_encontrados': grupos_encontrados})

from User.forms import SearchUserProfileForm

from django.shortcuts import render, get_object_or_404


def perfil(request, user_id):
    perfil = get_object_or_404(UserProfile, user__id=user_id)
    return render(request, 'perfil.html', {'perfil': perfil})



# views.py



