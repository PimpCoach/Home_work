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

CREATE TABLE IF NOT EXISTS Status_id (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT NOT NULL UNIQUE
);

ALTER TABLE RecordingClient ADD COLUMN status_id INTEGER REFERENCES AppointmentServices(status_id);
ALTER TABLE RecordingClient DROP COLUMN record_status;

COMMIT;

-- 2. Новые таблицы

-- Статус записи
CREATE TABLE IF NOT EXISTS StatusDictionary(
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT NOT NULL UNIQUE,
    status_description TEXT
);

-- Отзывы
CREATE TABLE IF NOT EXISTS Reviews(
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Расписание мастера
CREATE TABLE IF NOT EXISTS MasterShedule(
    shedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    status_id INTEGER NOT NULL,
    comment TEXT
);