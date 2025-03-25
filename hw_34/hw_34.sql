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
