======================================================
Envio correo electrónico durante la importación de CSV
======================================================

Envia correo electrónico desde plantilla cuando se importa desde ficheros CSV.

Configuración
=============

 * Configure una cuenta de correo electrónico de salida SMTP a través del menú
|menu_server_form| tal y como se indica para el módulo Envío de correo.

 * Cree una plantilla de correo electrónico a través del menú
|menu_email_template| (tal y como se indica para el módulo Plantillas de correo
electrónico), relacionada con la clase de registros que desee importar. En la
pestaña "Informes" añada un informe si lo desea. Finalmente, en la pestaña
"Avanzado" marque la casilla "Permitir importación CSV".

.. |menu_server_form| tryref:: smtp.menu_server_form/complete_name
.. |menu_email_template| tryref:: electronic_mail_template.menu_email_template/complete_name
