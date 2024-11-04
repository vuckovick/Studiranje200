-- Inserting data into 'faculties'
INSERT INTO faculties (name, city, tag) VALUES ('Engineering', 'New York', 'eng');
INSERT INTO faculties (name, city, tag) VALUES ('Arts', 'Los Angeles', 'arts');
INSERT INTO faculties (name, city, tag) VALUES ('Science', 'Chicago', 'sci');

-- Inserting data into 'users'
INSERT INTO users (username, email, password, full_name, date_birth, gender, city, faculty_id, instagram_link, profile_picture, bio, role, unread_notifications) 
VALUES ('user', 'john@example.com', '123', 'John Doe', NULL, 'M', 'New York', 1, 'http://instagram.com/johndoe', 'profile_pic.jpg', 'Bio of John', 'regular', 0);

INSERT INTO users (username, email, password, full_name, date_birth, gender, city, faculty_id, instagram_link, profile_picture, bio, role, unread_notifications) 
VALUES ('org', 'jane@example.com', '123', 'Jane Smith', NULL, 'F', 'Los Angeles', 2, 'http://instagram.com/janesmith', 'profile_pic2.jpg', 'Bio of Jane', 'organizer', 0);

-- Inserting data into 'organizations'
INSERT INTO organizations (name, description, picture, total_rating, count_rating)
VALUES ('Tech Club', 'A club for tech enthusiasts.', 'tech_club.jpg', 0, 0);

INSERT INTO organizations (name, description, picture, total_rating, count_rating)
VALUES ('Art Society', 'A society for art lovers.', 'art_society.jpg', 0, 0);

-- Inserting data into 'places'
INSERT INTO places (name, description, working_hours, address, type, picture, total_rating, count_rating, google_maps_url)
VALUES ('Cool Bar', 'A cool bar in town.', '9AM - 11PM', '123 Main St', 'bar', 'cool_bar.jpg', 0, 0, 'http://maps.google.com/coolbar');

INSERT INTO places (name, description, working_hours, address, type, picture, total_rating, count_rating, google_maps_url)
VALUES ('Awesome Klub', 'An awesome klub.', '10AM - 2AM', '456 Klub St', 'klub', 'awesome_klub.jpg', 0, 0, 'http://maps.google.com/awesomeklub');

-- Inserting data into 'events'
INSERT INTO events (name, description, date, time, org_id, status, type, picture, total_rating, count_rating, place_id)
VALUES ('Tech Meetup', 'A meetup for tech enthusiasts.', '2024-06-15', '18:00:00', 1, 'published', 'party', 'tech_meetup.jpg', 0, 0, 1);

INSERT INTO events (name, description, date, time, org_id, status, type, picture, total_rating, count_rating, place_id)
VALUES ('Art Exhibition', 'An exhibition for art lovers.', '2024-06-20', '19:00:00', 2, 'published', 'party', 'art_exhibition.jpg', 0, 0,  2);

-- Inserting data into 'connections'
INSERT INTO connections (follower_id, followee_id, status)
VALUES (1, 2,  'active');

INSERT INTO connections (follower_id, followee_id,  status)
VALUES (2, 1,  'active');

-- Inserting data into 'event_reviews'
INSERT INTO event_reviews (event_id, user_id, comment,  count_id)
VALUES (1, 1, 'Great event!', 1);

INSERT INTO event_reviews (event_id, user_id, comment, count_id)
VALUES (2, 2, 'Amazing exhibition!',  1);

-- Inserting data into 'event_user'
INSERT INTO event_user (event_id, user_id, status,  rating)
VALUES (1, 1, 'going',  5);

INSERT INTO event_user (event_id, user_id, status,  rating)
VALUES (2, 2, 'going',  4);

-- Inserting data into 'notifications'
INSERT INTO notifications (user_id, from_id, from_type, message, type, status)
VALUES (1, 2, 'user', 'You have a new connection request.', 'connection_request', 'unread');

INSERT INTO notifications (user_id, from_id, from_type, message, type, status)
VALUES (2, 1, 'user', 'You have a new event invite.', 'event_invite', 'unread');

-- Inserting data into 'organization_user'
INSERT INTO organization_user (org_id, user_id, role)
VALUES (1, 1, 'admin');

INSERT INTO organization_user (org_id, user_id, role)
VALUES (2, 2, 'member');

-- Inserting data into 'student_org'
INSERT INTO student_org (org_id, faculty_id)
VALUES (1, 1);

INSERT INTO student_org (org_id, faculty_id)
VALUES (2, 2);
