from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'User' 

urlpatterns = [
    
    path('', views.pagina_inicio, name='pagina_inicio'),
    # register and login 
    path('login/', views.custom_login, name='login'),  # Asegúrate de usar el nombre de la vista correcto
    path('register/', views.register, name='register'),
    # Perfil
    path('dashboard/', views.dashboard, name='dashboard'),
    # Logout whit django.contrib.auth
    path('logout/', views.custom_logout, name='logout'),
    # PerfilCutsom
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    # Cambio de contraseña
    path('recover/', views.password_reset_request, name='password_reset'),
    path('recover/done/', views.password_reset_done, name='password_reset_done'),
    path('recover/confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('recover/complete/', views.password_reset_complete, name='password_reset_complete'),
    
    # ELIMINAR_PUBLICACION
     path('eliminar_publicacion/<int:publicacion_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
     
    #  CREAR GRUPO
    path('create_group/', views.create_group, name='create_group'),
    path('eliminar_publicacion_feed/<int:post_id>/', views.eliminar_publicacion_feed, name='eliminar_publicacion_feed'),

    
    path('eliminar_publicacion_grupo/<int:publicacion_id>/', views.eliminar_publicacion_grupo, name='eliminar_publicacion_grupo'),
    path('editar_grupo/<int:group_id>/', views.editar_grupo, name='editar_grupo'),

    
    # PERFIL DEL GRUPO
    
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    
    # Administrar GRUPO
    path('administrar_grupos/', views.administrar_grupos, name='administrar_grupos'),
    
    path('eliminar_miembro/<int:group_id>/<int:member_id>/', views.eliminar_miembro, name='eliminar_miembro'),
    path('join_request/<int:join_request_id>/aceptar/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('join_request/<int:join_request_id>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
    # ENVIAR INVITACIOENS 

    path('enviar_invitacion_grupo/<int:group_id>/', views.enviar_invitacion_grupo, name='enviar_invitacion_grupo'),

    path('group_members/<int:group_id>/', views.group_members, name='group_members'),


    path('aceptar_invitacion/<int:invitation_id>/', views.aceptar_invitacion, name='aceptar_invitacion'),
    path('rechazar_invitacion/<int:invitation_id>/', views.rechazar_invitacion, name='rechazar_invitacion'),
    path('abandonar_grupo/<int:group_id>/', views.abandonar_grupo, name='abandonar_grupo'),
    
    
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('eliminar_comentario_grupo/<int:comentario_id>/', views.eliminar_comentario_grupo, name='eliminar_comentario_grupo'),
    path('eliminar_comentario_grupo_desde_el_feed/<int:comentario_id>/', views.eliminar_comentario_grupo_desde_el_feed, name='eliminar_comentario_grupo'),
    
    
    path('buscar_grupos/', views.vista_de_busqueda_de_grupos, name='ruta_de_tu_vista_de_busqueda_de_grupos'),
    path('calificar_publicacion_grupo/<int:post_id>/', views.calificar_publicacion_grupo, name='calificar_publicacion_grupo'),
    path('calificar_publicacion_feed/<int:post_id>/', views.calificar_publicacion_grupo_feed, name='calificar_publicacion_grupo_feed'),
    path('perfil/<int:user_id>/', views.perfil, name='perfil'),

    path('inicio/', views.feed, name='feed'),]
