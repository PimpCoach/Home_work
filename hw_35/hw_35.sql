-- HW_34
-- 1. Создание таблиц и связей

-- Запись на услуги
CREATE TABLE IF NOT EXISTS RecordingClient(
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    client_phone INTEGER NOT NULL,
    record_data TEXT DEFAULT CURRENT_TIMESTAMP,
    master_id INTEGER,
    record_status TEXT,
    FOREIGN KEY (master_id) REFERENCES Masters(master_id)
);

-- Мастера
CREATE TABLE IF NOT EXISTS Masters(
    master_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    master_phone INTEGER NOT NULL
);

-- Услуги
CREATE TABLE IF NOT EXISTS Services(
    services_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE,
    services_description TEXT NOT NULL,
    price INTEGER NOT NULL
);

-- Связующая таблица местеров и услуг
CREATE TABLE IF NOT EXISTS MastersServices(
    master_id INTEGER NOT NULL,
    services_id INTEGER NOT NULL,
    FOREIGN KEY (master_id) REFERENCES Masters(master_id),
    FOREIGN KEY (services_id) REFERENCES Services(services_id),
    UNIQUE (master_id, services_id)
);

-- Связующая таблица записи и услуг
CREATE TABLE IF NOT EXISTS AppointmentServices(
    client_id INTEGER NOT NULL,
    services_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES RecordingClient(client_id),
    FOREIGN KEY (services_id) REFERENCES Services(services_id),
    UNIQUE (client_id, services_id)
);

-- 2. Внесение данных

-- Данные о мастерах
INSERT INTO Masters(`first_name`, `last_name`, `middle_name`, `master_phone`)
VALUES("Джагорид", "Варахов", "Ахарович", "89991234567"),
    ("Андрей", "Козлов", "Андреевич", "89991254567");

-- Данные об услугах
INSERT INTO Services(`title`, `services_description`, `price`)
VALUES("Брутал", "Мужская стрижка + уход за бородой", 2000),
    ("Батя и сын", "Мусжкая стрижка взрослого и ребенка", 1600),
    ("Борода ДА", "Моделирование бороды", 600),
    ("Кайфули", "Мытье и массаж головы + укладка", 800),
    ("ВолосOFF", "Удалени волос из носа и ушей", 500);

-- Связывание мастеров и услуг
INSERT INTO MastersServices(`master_id`, `services_id`)
VALUES(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3);

-- Добавление записи
INSERT INTO RecordingClient(`client_name`, `client_phone`, `master_id`, `record_status`)
VALUES("Андрей", "89991234567", 1, "Подтверждена"),
    ("Василий", "89991234567", 2, "В ожидании"),
    ("Макар", "89991234567", 2, "Отменена"),
    ("Валерий", "89991234567", 1, "В ожидании");

-- Связывание записи и услуг
INSERT INTO AppointmentServices(`client_id`, `services_id`)
VALUES(1, 1), (1, 5), (2, 2), (3, 1), (3, 3), (4, 4), (4, 5);

-- HW 35
-- 1. Изменений в существующих таблицах
BEGIN TRANSACTION;

-- Модификация таблицы MastersServices
ALTER TABLE MastersServices ADD COLUMN price REAL;
ALTER TABLE MastersServices ADD COLUMN duration_minutes REAL;
-- Модификация таблицы Services
ALTER TABLE Services ADD COLUMN duration_minutes INTEGER NOT NULL DEFAULT 60;
-- Модификация таблицы RecordingClient
ALTER TABLE RecordingClient ADD COLUMN start_time TEXT NOT NULL DEFAULT '10:00';
ALTER TABLE RecordingClient ADD COLUMN end_time TEXT NOT NULL DEFAULT '22:00';




ALTER TABLE RecordingClient ADD COLUMN status_id INTEGER REFERENCES AppointmentServices(status_id);
ALTER TABLE RecordingClient DROP COLUMN record_status;

COMMIT;

-- 2. Новые таблицы

-- Статус записи
CREATE TABLE IF NOT EXISTS StatusDictionary (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT NOT NULL UNIQUE
);

ALTER TABLE Status_id RENAME TO StatusDictionary;
ALTER TABLE StatusDictionary ADD COLUMN status_description TEXT;

-- Отзывы
CREATE TABLE IF NOT EXISTS Reviews(
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(id)
);

-- Расписание мастера
CREATE TABLE IF NOT EXISTS MasterSchedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL CHECK(day_of_week BETWEEN 1 AND 7),
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    status_id INTEGER NOT NULL,
    comment TEXT,
    FOREIGN KEY (master_id) REFERENCES Masters(master_id),
    FOREIGN KEY (status_id) REFERENCES ScheduleStatus(status_id)
);

CREATE TABLE IF NOT EXISTS ScheduleStatus (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT NOT NULL UNIQUE
);

-- Серия запросов в БД

-- 1. Новая запись на услугу 
BEGIN TRANSACTION;

    INSERT INTO RecordingClient('client_name', 'client_phone', 'master_id', 'start_time', 'end_time', 'status_id')
    VALUES("Евгений", "89991234567", 1, "21:00", "22:00", 1);

    SELECT RecordingClient.*, StatusDictionary.status_name FROM RecordingClient
    JOIN StatusDictionary ON RecordingClient.status_id = StatusDictionary.status_id;

COMMIT;

-- 2. Изменение статуса записи
BEGIN TRANSACTION;

INSERT INTO StatusDictionary(status_name) VALUES("Подверждена");
INSERT INTO StatusDictionary(status_name) VALUES("Отмена");
INSERT INTO StatusDictionary(status_name) VALUES("В ожидании");
INSERT INTO StatusDictionary(status_name) VALUES("Завершена");

COMMIT;

SELECT * FROM StatusDictionary
-- Изменение только что добавленной записи статуса
BEGIN TRANSACTION;

UPDATE StatusDictionary SET status_name = "Отменена" WHERE status_id = 2;

COMMIT;

-- Изменение статуса записи 
BEGIN TRANSACTION;

UPDATE RecordingClient SET status_id = 2 WHERE client_id = 5;

COMMIT;

-- 3. Корректировка цены на услуги
BEGIN TRANSACTION;

-- Обновление цены в таблце Services 
UPDATE Services SET price = "1800 - 2200" where services_id = 1;
UPDATE Services SET price = "1600 - 1800" where services_id = 2;

-- Обновление индивидуальной цены в таблице MastersServices
UPDATE MastersServices SET price = 2200 where services_id = 1 and master_id = 1;
UPDATE MastersServices SET price = 1800 where services_id = 2 and master_id = 1;
UPDATE MastersServices SET price = 600 where services_id = 3;
UPDATE MastersServices SET price = 800 where services_id = 4;
UPDATE MastersServices SET price = 500 where services_id = 5;
UPDATE MastersServices SET price = 1800 where services_id = 1 and master_id = 2;
UPDATE MastersServices SET price = 1600 where services_id = 2 and master_id = 2;

COMMIT;

-- 4. Обновление расписания мастера

-- Обновление статуса расписания
INSERT INTO ScheduleStatus (status_name) VALUES ('Рабочий день');
INSERT INTO ScheduleStatus (status_name) VALUES ('Выходной');

-- Добавление нового расписания
INSERT INTO MasterSchedule (master_id, day_of_week, start_time, end_time, status_id, comment)
VALUES (1, 1, '10:00', '15:00', 1, "Работает"),
    (1, 2, '10:00', '18:00', 2, "Заболел"),
    (1, 3, '10:00', '18:00', 1, "Работает"),
    (1, 4, '10:00', '18:00', 2, "В отпуске"),
    (1, 5, '15:00', '22:00', 1, "Работает"),
    (1, 6, '15:00', '22:00', 1, "Работает"),
    (1, 7, '10:00', '18:00', 2, "На учебе"),
    (2, 1, '15:00', '22:00', 1, "Работает"),
    (2, 2, '10:00', '18:00', 1, "Работает"),
    (2, 3, '10:00', '18:00', 2, "Заболел"),
    (2,4, '15:00', '22:00', 1, "Работает"),
    (2,5, '10:00', '18:00', 2, "Забухал"),
    (2,6, '15:00', '22:00', 1, "Работает"),
    (2,7, '10:00', '18:00', 2, "Уволен");

SELECT MasterSchedule.*, ScheduleStatus.status_name FROM MasterSchedule
JOIN ScheduleStatus ON MasterSchedule.status_id = ScheduleStatus.status_id;

-- Обновить расписание мастера
BEGIN TRANSACTION;

UPDATE MasterSchedule SET start_time = '12:00', end_time = '18:00' WHERE master_id = 1 AND day_of_week = 1;

COMMIT;

-- 5. Добавление нового статуса (Уже сделано в 2. Изменение статуса записи)

BEGIN TRANSACTION;

INSERT INTO StatusDictionary(status_name) VALUES("Подверждена");
INSERT INTO StatusDictionary(status_name) VALUES("Отменена");
INSERT INTO StatusDictionary(status_name) VALUES("В ожидании");
INSERT INTO StatusDictionary(status_name) VALUES("Завершена");

COMMIT;

-- 6. Добавление отзыва
BEGIN TRANSACTION;

INSERT INTO Reviews (appointment_id, rating, comment)
VALUES (1, 5, 'Отличная работа! Спасибо!'),
    (2, 4, 'Хороший мастер, но дорого'),
    (3, 5, 'Очень доволен работой мастера'),
    (4, 3, 'Нормально, но дорого');

ROLLBACK;
    SELECT "Статусы уже существуют" AS Error;

-- 7. Массовая вставка новых услуг
BEGIN TRANSACTION;

INSERT INTO Services(`title`, `services_description`, `price`, `duration_minutes`)
VALUES ('Дед', "Окрас волос и бороды в седой цвет", 2500, 120),
    ("Х", "Бритье наголо", 100, 30);

SELECT * FROM Services

COMMIT;

-- 8. Отмена записи на услугу

SELECT * FROM StatusDictionary;

    SELECT RecordingClient.*, StatusDictionary.status_name FROM RecordingClient
    JOIN StatusDictionary ON RecordingClient.status_id = StatusDictionary.status_id;

BEGIN TRANSACTION;
-- Изменение статуса записи
UPDATE RecordingClient SET status_id = 2 WHERE client_id = 3;

-- Удаление связанных  записей из таблицы AppointmentServices
DELETE FROM RecordingClient WHERE status_id = 2;

COMMIT;