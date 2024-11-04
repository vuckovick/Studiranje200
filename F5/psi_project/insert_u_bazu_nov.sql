-- Place Type Data
INSERT INTO `studiranje200_placetype` (name, picture) VALUES
    ('bar', '/media/location_background/bar.png'),
    ('klub', '/media/location_background/klub.png'),
    ('kafana', '/media/location_background/kafana.png'),
    ('splav', '/media/location_background/splav.png'),
    ('kafic', '/media/location_background/kafic.png');

-- Notification Type Data
INSERT INTO `studiranje200_notificationtype` (name) VALUES
    ('connection_request'),
    ('event_invite'),
    ('event_reminder'),
    ('standard'),
    ('join_organization'),
    ('become_organizer'),
    ('new_event');

-- Event Type Data
INSERT INTO `studiranje200_eventtype` (name) VALUES
    ('Žurka'),
    ('Beer pong'),
    ('Udomi ne kupuj!'),
    ('Sportski turnir'),
    ('200 200'),
    ('Pub kviz');

-- Faculty Data
INSERT INTO `studiranje200_faculty` (name, city, tag) VALUES
    ('Matematički i Informatički Fakultet', 'Beograd', 'MATF'),
    ('Elektrotehnički Fakultet', 'Beograd', 'ETF'),
    ('Ekonomski Fakultet', 'Beograd', 'EKOF'),
    ('Fakultet Organizacionih Nauka', 'Beograd', 'FON'),
    ('Građevinski Fakultet', 'Beograd', 'GRF'),
    ('Mašinski Fakultet', 'Beograd', 'MAF'),
    ('Medicinski Fakultet', 'Beograd', 'MEF'),
    ('Fakultet Politickih Nauka', 'Beograd', 'FPN'),
    ('Fakultet Dramskih Umetnosti', 'Beograd', 'FDU'),
    ('Fakultet Bezbednosti', 'Beograd', 'FB'),
    ('Fakultet Opšte Medicine', 'Beograd', 'FOM'),
    ('Fakultet Tehničkih Nauka', 'Beograd', 'FTN'),
    ('Fakultet Primenjenih Umetnosti', 'Beograd', 'FPU'),
    ('Prirodno-Matematički Fakultet', 'Novi Sad', 'PMF'),
    ('Fakultet Sportskih Nauka', 'Novi Sad', 'FSN'),
    ('Filozofski Fakultet', 'Novi Sad', 'FF'),
    ('Medicinski Fakultet', 'Niš', 'MF'),
    ('Pravni Fakultet', 'Niš', 'PF'),
    ('Pedagoški Fakultet', 'Niš', 'PedF'),
    ('Fakultet Umetnosti', 'Kragujevac', 'FU'),
    ('Tehnološko-Metalurški Fakultet', 'Kragujevac', 'TMF'),
    ('Fakultet Medicinskih Nauka', 'Kragujevac', 'FMN');

-- Place Data
INSERT INTO `studiranje200_place` (name, description, working_hours, address, place_type_id, picture, total_rating, count_rating, google_maps_url, website_url)
VALUES
    ('Splav River', 'Odmor na reci sa živom muzikom i odličnim pogledom', '20:00 - 04:00', 'Reka, Novi Sad, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='splav'), 'place_pictures/limun.png', 0, 0, 'https://maps.google.com/maps?q=Splav+River+Novi+Sad', 'https://place_web_site'),
    ('Caffe Lav', 'Udoban kafić sa mirnom atmosferom i odličnom kafom', '07:00 - 22:00', 'Trg Slobode 8, Novi Sad, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='kafic'), 'place_pictures/place2.png', 0, 0, 'https://maps.google.com/maps?q=Caffe+Lav+Novi+Sad', 'https://place_web_site'),
    ('Klub Tunnel', 'Podzemni klub sa alternativnom muzikom i umetničkim performansima', '22:00 - 05:00', 'Miloša Pocerca 10, Niš, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='klub'), 'place_pictures/place1.png', 0, 0, 'https://maps.google.com/maps?q=Klub+Tunnel+Niš', 'https://place_web_site'),
    ('Kafana Zlatibor', 'Tipična srpska kafana sa domaćom hranom i živom svirkom', '12:00 - 01:00', 'Zlatibor, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='kafana'), 'place_pictures/limun.png', 0, 0, 'https://maps.google.com/maps?q=Kafana+Zlatibor+Zlatibor', 'https://place_web_site'),
    ('Bar Havana', 'Karipski bar sa koktelima, salsa plesom i tropskom atmosferom', '18:00 - 03:00', 'Str. Braće Ribnikar 34, Kragujevac, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='bar'), 'place_pictures/place2.png', 0, 0, 'https://maps.google.com/maps?q=Bar+Havana+Kragujevac', 'https://place_web_site'),
    ('Splav Amsterdam', 'Plovni klub sa živom muzikom i dobro poznatom atmosferom', '22:00 - 04:00', 'Kej Oslobodjenja bb, Beograd, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='splav'), 'place_pictures/limun.png', 0, 0, 'https://maps.google.com/maps?q=Splav+Amsterdam+Beograd', 'https://place_web_site'),
    ('Dorćol Platz', 'Kafe i prostor za dogadjaje sa umetnošću, muzikom i kreativnim sadržajem', '08:00 - 01:00', 'Braće Krsmanović 4, Beograd, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='kafic'), 'place_pictures/place1.png', 0, 0, 'https://maps.google.com/maps?q=Dorćol+Platz+Beograd', 'https://place_web_site'),
    ('Klub DOT', 'Klub sa DJ nastupima i tematskim žurkama', '23:00 - 05:00', 'Trg Republike 3, Beograd, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='klub'), 'place_pictures/limun.png', 0, 0, 'https://maps.google.com/maps?q=Klub+DOT+Beograd', 'https://place_web_site'),
    ('Tri Šešira', 'Tradicionalna srpska kafana sa nacionalnom kuhinjom i muzikom uživo', '11:00 - 01:00', 'Skadarska 29, Beograd, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='kafana'), 'place_pictures/place2.png', 0, 0, 'https://maps.google.com/maps?q=Tri+Šešira+Beograd', 'https://place_web_site'),
    ('Bar Central', 'Opušten bar sa širokim izborom pića i prijatnom atmosferom', '10:00 - 02:00', 'Kralja Petra 13, Beograd, Srbija', (SELECT id FROM `studiranje200_placetype` WHERE name='bar'), 'place_pictures/limun.png', 0, 0, 'https://maps.google.com/maps?q=Bar+Central+Beograd', 'https://place_web_site');

INSERT INTO studiranje200_user200 (date_joined, is_superuser, is_staff, is_active, username, password, email, first_name, last_name, full_name, date_birth, gender, city, faculty_id, instagram_link, profile_picture, bio, role, unread_notifications, created_at)
VALUES
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'vanja031', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user1@example.com', 'Vanja', 'Tomic', 'Vanja Tomic', '1992-08-20', 'M', 'Uzice', 2, 'https://www.instagram.com/vanja031', 'profile_pictures/vanja031.jpg', 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem.', 'organizer', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'mihajlo', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user2@example.com', 'Mihajlo', 'Antonijevic', 'Mihajlo Antonijevic', '1992-08-20', 'M', 'Smederevo', 2, 'https://www.instagram.com/mihajlo', 'profile_pictures/mihajlo.png', 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem.', 'regular', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'kole', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user3@example.com', 'Konstantin', 'Vuckovic', 'Konstantin Vuckovic', '1988-03-10', 'M', 'Beograd', 3, 'https://www.instagram.com/kole', 'profile_pictures/kolle.png', 'Ut enim ad minim veniam, quis nostrud exercitation ullamco.', 'admin', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'dovla', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'admin1@example.com', 'Vladimir', 'Bogojevic', 'Vladimir Bogojevic', '1975-12-01', 'M', 'Kraljevo', 1, 'https://www.instagram.com/dovla', 'profile_pictures/dovla.png', 'Duis aute irure dolor in reprehenderit in voluptate velit esse.', 'organizer', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'jana', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user5@example.com', 'Jana', 'Petrovic', 'Jana Petrovic', '1996-02-15', 'F', 'Novi Sad', 2, 'https://www.instagram.com/jana', 'profile_pictures/placeholder.jpg', 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur.', 'regular', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'marko', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user6@example.com', 'Marko', 'Ilic', 'Marko Ilic', '1995-07-20', 'M', 'Subotica', 3, 'https://www.instagram.com/marko', 'profile_pictures/placeholder.jpg', 'Quis autem vel eum iure reprehenderit qui in ea voluptate velit.', 'regular', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'ana', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user7@example.com', 'Ana', 'Savic', 'Ana Savic', '1993-05-25', 'F', 'Kragujevac', 2, 'https://www.instagram.com/ana', 'profile_pictures/placeholder.jpg', 'At vero eos et accusamus et iusto odio dignissimos ducimus.', 'regular', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'stefan', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user8@example.com', 'Stefan', 'Jovanovic', 'Stefan Jovanovic', '1994-11-30', 'M', 'Nis', 1, 'https://www.instagram.com/stefan', 'profile_pictures/placeholder.jpg', 'Et harum quidem rerum facilis est et expedita distinctio.', 'regular', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'jelena', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user9@example.com', 'Jelena', 'Nedic', 'Jelena Nedic', '1991-01-10', 'F', 'Valjevo', 3, 'https://www.instagram.com/jelena', 'profile_pictures/placeholder.jpg', 'Nam libero tempore, cum soluta nobis est eligendi optio cumque.', 'regular', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'uros', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user10@example.com', 'Uros', 'Pavlovic', 'Uros Pavlovic', '1990-09-05', 'M', 'Leskovac', 2, 'https://www.instagram.com/uros', 'profile_pictures/placeholder.jpg', 'Temporibus autem quibusdam et aut officiis debitis aut rerum.', 'regular', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'milica', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user11@example.com', 'Milica', 'Mihailovic', 'Milica Mihailovic', '1998-06-18', 'F', 'Zrenjanin', 1, 'https://www.instagram.com/milica', 'profile_pictures/placeholder.jpg', 'Excepteur sint occaecat cupidatat non proident, sunt in culpa.', 'regular', 0, NOW()),
    ('2024-05-19 15:30:45.123456', 0, 0, 1, 'nikola', 'pbkdf2_sha256$720000$8G0VVfBT6ZpqxCw36NkIcd$ruZZwkMjw7V+m2BOlEj3viP3I9YBcAXHi79EfuzfN40=', 'user12@example.com', 'Nikola', 'Stankovic', 'Nikola Stankovic', '1993-08-22', 'M', 'Loznica', 3, 'https://www.instagram.com/nikola', 'profile_pictures/placeholder.jpg', 'In voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'regular', 0, NOW());


INSERT INTO studiranje200_organization (name, description, picture, total_rating, count_rating, created_at)
VALUES
    ('Asocijacija Studenata Fakulteta Elektrotehnike', 'Studentska organizacija koja okuplja studente elektrotehnike radi unapređenja njihovih interesovanja i aktivnosti.', 'organization_pictures/1.jpg', 0, 0, NOW()),
    ('Studentski Kulturni Centar', 'Organizacija posvećena kulturnim događajima, umetnosti i promociji studentske kulture.', 'organization_pictures/1.jpg', 0, 0, NOW());



INSERT INTO studiranje200_event (name, description, date, time, org_id, status, event_type_id, picture, total_rating, count_rating, created_at, place_id)
VALUES
    ('Elektro žurka', 'Najveća elektro žurka u gradu, sa najboljim DJ-evima i atmosferom koja će vas ostaviti bez daha.', '2024-06-10', '22:00:00', 2, 'published', 1, 'event_pictures/event1.png', 0, 0, NOW(), 3),
    ('Medicinska sestra žurka', 'Tematska žurka na kojoj se svi oblače kao medicinske sestre i doktori. Očekuje vas nezaboravna zabava i puno iznenađenja!', '2024-06-15', '20:00:00', 1, 'published', 1, 'event_pictures/event3.png', 0, 0, NOW(), 5),
    ('Pivska fešta', 'Tradiconalna pivska fešta na kojoj možete probati najbolja piva iz raznih pivara, uz dobru muziku i društvo.', '2024-06-20', '19:30:00', 1, 'published', 1, 'event_pictures/event2.png', 0, 0, NOW(), 7),
    ('Latino noć', 'Vrela latino žurka na kojoj ćete naučiti plesati salse, bachatu i merenge, uz autentičnu latino muziku.', '2024-07-05', '21:00:00', 2, 'published', 1, 'event_pictures/event1.png', 0, 0, NOW(), 6);


INSERT INTO studiranje200_studentorg (org_id, faculty_id) VALUES
    (1, 1),
    (2, 2);


INSERT INTO studiranje200_organizationuser (org_id, user_id, role, join_date) VALUES
    (1, 1, 'member', '2024-01-01'),
    (1, 2, 'member', '2024-01-15'),
    (2, 3, 'member', '2024-02-01'),
    (2, 4, 'member', '2024-02-15');