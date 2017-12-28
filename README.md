# site_with_parse_another_sites
Простейший сайт. На главной странице есть два <textarea>, в которые выводится информация о парсинге нескольких других сайтах.
В первый блок выводится дата и время запроса, а также статус(успех/неудача). Во второй блок выводится: url-ссылка, заголовок страницы, кодировка, <h1>, если есть, в случае неудачи - только url.

Парсинг сайтов выполняется в фоновом режиме, в виде таймерных потоков, отдельных для каждого url. Данные парсинга загружаются в ту же базу данных. Загрузка потоков выполнена в виде команды (см. my_resource/management/commands/url_parser.py), вызов команды осуществляется в wsgi-файле. При работе потоков с базой данных используется блокировка, для избежания конфликтов.

Обновление данных на странице пользователя осуществляется с помощью ajax-запросов с интервалом в 5с.
Запуск проекта осуществляется командой python3 manage.py runserver