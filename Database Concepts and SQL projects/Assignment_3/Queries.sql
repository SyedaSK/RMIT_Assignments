/* D1*/
SELECT c.country AS 'Country Name (CN)', 
       (v.peopleVaccinated + v.peopleFullyVaccinated 
       + v.totalBoosters) AS 'Total Vaccinations (administered to date)', 
       v.dailyVaccinations AS 'Daily Vaccinations', 
       v.dates AS 'Date'
FROM vaccinations v
JOIN country c 
ON v.iso = c.iso
JOIN (
    SELECT dates, AVG(peopleVaccinated + peopleFullyVaccinated 
    + totalBoosters) AS avg_vaccinations
    FROM vaccinations
    GROUP BY dates
) av ON v.dates = av.dates
WHERE (v.peopleVaccinated + v.peopleFullyVaccinated 
       + v.totalBoosters) > av.avg_vaccinations;


/*D2*/
SELECT c.country AS 'Country Name (CN)', 
       (SUM(v.peopleVaccinated
       + v.peopleFullyVaccinated
       + v.totalBoosters)) 
       AS 'Cumulative Doses'
FROM vaccinations v
JOIN country c 
ON v.iso = c.iso
GROUP BY c.country
HAVING (SUM(v.peopleVaccinated + v.peopleFullyVaccinated + v.totalBoosters)) > (
    SELECT AVG(total_vaccinations) 
    FROM (
        SELECT c.country, (SUM(v.peopleVaccinated 
        + v.peopleFullyVaccinated + v.totalBoosters)) AS total_vaccinations
        FROM vaccinations v
        JOIN country c 
        ON v.iso = c.iso
        GROUP BY c.country
    )
);



/* D3 */
SELECT DISTINCT c.country AS 'Country', 
       vm.vaccines AS 'Vaccine Type'
FROM vaccinationsByManufacturer vm
JOIN country c ON vm.iso = c.iso;


/* D4 */
SELECT c.country AS 'Country', 
       s.sourceName AS 'Source Name (URL)', 
       MAX(v.peopleVaccinated + v.peopleFullyVaccinated 
       + v.totalBoosters) AS 'Biggest total Administered Vaccines'
FROM vaccinations v
JOIN country c ON v.iso = c.iso
JOIN dataFrom d ON v.iso = d.iso
JOIN sources s ON d.url = s.url
GROUP BY c.country, s.sourceName
ORDER BY s.sourceName;


/* D5 */


