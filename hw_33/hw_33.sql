-- 1. Общее количество персонажей по статусу
SELECT ALIVE, COUNT(*)
FROM MarvelCharacters
GROUP BY ALIVE;

-- 2. Среднее количество появлений персонажей с разным цветом глаз
SELECT DISTINCT eye, round(avg(APPEARANCES), 1) AS min_appear
FROM MarvelCharacters
WHERE eye IS NOT NULL
GROUP BY eye;

-- 3. Максимальное количество появлений персонажей с определенным цветом волос
SELECT DISTINCT Hair, max(APPEARANCES) AS max_appear
FROM MarvelCharacters
WHERE Hair IS NOT NULL
GROUP BY Hair;

-- 4. Минимальное количество появлений среди персонажей с известной и публичной личностью
SELECT identify, min(APPEARANCES) AS min_appear
FROM MarvelCharacters
WHERE identify = 'Public Identity'
GROUP BY identify;

-- 5. Общее количество персонажей по полу
SELECT sex, COUNT(*)
FROM MarvelCharacters
WHERE SEX IS NOT NULL
GROUP BY SEX;

-- 6. Средний год первого появления персонажей с различным типом личности
SELECT identify, round(avg(Year), 1) AS avg_year
FROM MarvelCharacters
WHERE identify IS NOT NULL
GROUP BY identify;

-- 7. Количество персонажей с разным цветом глаз среди живых
SELECT eye, COUNT(ALIVE) AS count_living
FROM MarvelCharacters
WHERE eye IS NOT NULL AND ALIVE = 'Living Characters'
GROUP BY eye;

-- 8. Максимальное и минимальное количество появлений среди персонажей с определенным цветом волос
SELECT Hair, max(APPEARANCES) AS max_apear, min(APPEARANCES) AS min_appear
FROM MarvelCharacters
WHERE Hair IS NOT NULL
GROUP BY Hair;

-- 9. Количество персонажей с различным типом личности среди умерших
SELECT identify, COUNT(ALIVE) AS count_deceased
FROM MarvelCharacters
WHERE ALIVE ='Deceased Characters' and identify IS NOT NULL
GROUP BY identify;

-- 10. Средний год появления персонажей с различным цветом глаз
SELECT eye, round(avg(Year), 1) AS avg_year
FROM MarvelCharacters
WHERE eye IS NOT NULL
GROUP BY eye;

-- 11. Персонаж с наибольшим количеством появлений
SELECT name, APPEARANCES
FROM MarvelCharacters
WHERE APPEARANCES = (
    SELECT max(APPEARANCES)
    from MarvelCharacters
);

-- 12. Персонажи, впервые появившиеся в том  же году, что и персонаж с максимальным появлением
SELECT name, Year
FROM MarvelCharacters
WHERE Year = (
    SELECT Year
    FROM MarvelCharacters
    WHERE appearances = (
        SELECT max(appearances)
        FROM MarvelCharacters
    )
);

--13. Персонажи с наименьшим количеством появлений среди живых
SELECT name, APPEARANCES
from MarvelCharacters
WHERE ALIVE = 'Living Characters' AND APPEARANCES = (
    SELECT min(APPEARANCES)
    FROM MarvelCharacters
    WHERE ALIVE = 'Living Characters'
);

--14. Персонажи с определенным цветом волос и максимальными появлениями среди такого цвета
SELECT name, Hair, APPEARANCES
FROM MarvelCharacters
WHERE (Hair, APPEARANCES) IN (
    SELECT Hair, max(APPEARANCES)
    FROM MarvelCharacters
    WHERE Hair IS NOT NULL
    GROUP BY Hair
);

--15. Персонажи с публичной личностью и наименьшим количеством появлений
SELECT name, identify, APPEARANCES
FROM MarvelCharacters
WHERE APPEARANCES = (
    SELECT min(APPEARANCES)
    FROM MarvelCharacters
)
AND identify = "Public Identity";