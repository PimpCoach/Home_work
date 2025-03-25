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


-- 3. Вывод данных

-- Вывод мастера и услуг, которые они предоставляют
SELECT 
    Masters.first_name,
    Masters.last_name,
    Services.title
FROM MastersServices
JOIN Masters ON MastersServices.master_id = Masters.master_id
JOIN Services ON MastersServices.services_id = Services.services_id;

-- Вывод имя клиента и услуг, которые он заказал
SELECT
    RecordingClient.client_name,
    Services.title,
    RecordingClient.record_status
FROM AppointmentServices
JOIN RecordingClient ON AppointmentServices.client_id = RecordingClient.client_id
JOIN Services ON AppointmentServices.services_id = Services.services_id;
