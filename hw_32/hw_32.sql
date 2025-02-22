-- 1. Лысые злодеи из девяностых
SELECT name,
    first_appearance,
    appearances
FROM MarvelCharacters
WHERE hair = 'Bald'
    AND align = 'Bad Characters'
    AND year BETWEEN 1990 AND 1999;

-- 2. Герои с тайной идентичностью и необычными глазами
SELECT name,
    first_appearance,
    eye
FROM MarvelCharacters
WHERE identify = 'Secret Identity'
    AND NOT eye IN('Blue Eyes', 'Brown Eyes', 'Green Eyes')
    AND NOT year IS NULL;

-- 3. Персонаж с изменяющимся цветом волос
SELECT name,
    hair
FROM MarvelCharacters
WHERE hair = 'Variable Hair';

-- 4. Женские персонажи с редким цвтом глаз
SELECT name,
    eye
FROM MarvelCharacters
WHERE sex = 'Female Characters'
    AND eye IN ('Gold Eyes', 'Amber Eyes');

-- 5. Персонаж без двойной идентичности, сортированные по году появления
SELECT name,
    first_appearance,
    identify
FROM MarvelCharacters
WHERE identify = 'No Dual Identity'
ORDER BY first_appearance DESC;

-- 6. Герои и злоде с необычными прическами
SELECT name,
    align,
    hair
FROM MarvelCharacters
WHERE NOT hair IN ('Brown Hair', 'Black Hair', 'Blond Hair', 'Red Hair')
    AND align IN ('Good Characters', 'Bad Characters');

--7. Персонажи появившиеся в определенное десятилетие
SELECT name,
    first_appearance
FROM MarvelCharacters
WHERE first_appearance LIKE '%6_';

--8. Персонажи, появившиеся в определенное десятилетие
SELECT name,
    eye,
    hair
FROM MarvelCharacters
WHERE eye = 'Yellow Eyes'
    AND hair = 'Red Hair';

--9. Персонажи с ограниченным количеством появлений
SELECT name,
    appearances
FROM MarvelCharacters
WHERE appearances < 10;

--10. Персонажи с наибольшим количеством появлений
SELECT name,
    appearances
FROM MarvelCharacters
ORDER BY appearances DESC
LIMIT 5