/* country(iso, country)*/
CREATE TABLE country(
    iso VARCHAR(10) NOT NULL,
    country VARCHAR(30), 
    PRIMARY KEY (iso)
    );
    
/* sources(url, sourceName) */
CREATE TABLE sources(
    url TEXT NOT NULL,
    sourceName TEXT,
    PRIMARY KEY (url)
    );
    
/*manufacturer(vaccines)*/
CREATE TABLE manufacturer(
    vaccines TEXT NOT NULL,
    PRIMARY KEY (vaccines)
    );
    
/*ageGroup(ageGroup)*/
CREATE TABLE ageGroup(
    ageGroup TEXT NOT NULL,
    PRIMARY KEY (ageGroup)
    );

/*states(iso*, stateName)*/
CREATE TABLE states(
    iso VARCHAR(10) NOT NULL,
    stateName TEXT NOT NULL, 
    PRIMARY KEY (iso, stateName),
    FOREIGN KEY (iso) REFERENCES country(iso)
    );
    
/*vaccinations(iso*, dates, peopleVaccinated, peopleFullyVaccinated, totalBoosters, 
dailyVaccinationsRaw, dailyVaccinations, peopleVaccinatedPerHundred, peopleFullyVaccinatedPerHundred, 
totalBoostersPerHundred, dailyVaccinationsPerMillion, dailyPeopleVaccinated, dailyPeopleVaccinatedPerHundred)*/
CREATE TABLE vaccinations(
    iso VARCHAR(10) NOT NULL, 
    dates TEXT NOT NULL, 
    peopleVaccinated INTEGER, 
    peopleFullyVaccinated INTEGER, 
    totalBoosters INTEGER, 
    dailyVaccinationsRaw INTEGER, 
    dailyVaccinations INTEGER, 
    peopleVaccinatedPerHundred REAL, 
    peopleFullyVaccinatedPerHundred REAL, 
    totalBoostersPerHundred REAL, 
    dailyVaccinationsPerMillion REAL, 
    dailyPeopleVaccinated INTEGER, 
    dailyPeopleVaccinatedPerHundred REAL,
    PRIMARY KEY (iso, dates),
    FOREIGN KEY (iso) REFERENCES country(iso)
);

/*peopleVaccinatedByCountry(iso*, dates, peopleVaccinated, 
peopleFullyVaccinated, totalBoosters)*/
CREATE TABLE peopleVaccinatedByCountry(
    iso VARCHAR(10) NOT NULL,
    dates TEXT NOT NULL, 
    peopleVaccinated INTEGER, 
    peopleFullyVaccinated INTEGER, 
    totalBoosters INTEGER,
    PRIMARY KEY (iso, dates),
    FOREIGN KEY (iso) REFERENCES country(iso)
    );

/*peopleVaccinatedByCountryWithStates(iso*, state*, date, 
totalDistributed, peopleVaccinated, peopleFullyVaccinatedPerHundred, 
peopleFullyVaccinated, peopleVaccinatedPerHundred, distributedPerHundred, 
dailyVaccinationsRaw, dailyVaccinations, dailyVaccinationsPerMillion, 
shareDosesUsed, totalBoosters, totalBoostersPerHundred)
*/
CREATE TABLE peopleVaccinatedByCountryWithStates(
    iso VARCHAR(10) NOT NULL, 
    state TEXT NOT NULL,
    date TEXT NOT NULL, 
    totalDistributed INTEGER, 
    peopleVaccinated INTEGER,
    peopleFullyVaccinatedPerHundred REAL, 
    peopleFullyVaccinated INTEGER, 
    peopleVaccinatedPerHundred REAL, 
    distributedPerHundred REAL, 
    dailyVaccinationsRaw INTEGER, 
    dailyVaccinations INTEGER, 
    dailyVaccinationsPerMillion REAL, 
    shareDosesUsed INTEGER, 
    totalBoosters INTEGER, 
    totalBoostersPerHundred REAL,
    PRIMARY KEY (iso, state, date),
    FOREIGN KEY (iso) REFERENCES country(iso),
    FOREIGN KEY (state) References states(stateName)
    );

/*vaccinationsByAgeGroup(iso*, ageGroup*, dates, 
peopleVaccinatedPerHundred, peopleFullyVaccinatedPerHundred, 
peopleWithBoosterPerHundred)
*/
CREATE TABLE vaccinationsByAgeGroup(
    iso VARCHAR(10) NOT NULL, 
    ageGroup TEXT NOT NULL, 
    dates TEXT NOT NULL, 
    peopleVaccinatedPerHundred INTEGER, 
    peopleFullyVaccinatedPerHundred INTEGER, 
    peopleWithBoosterPerHundred INTEGER,
    PRIMARY KEY (iso, ageGroup, dates),
    FOREIGN KEY (iso) REFERENCES country(iso),
    FOREIGN KEY (ageGroup) REFERENCES ageGroup(ageGroup)
    );

/*vaccinationsByManufacturer(iso*, vaccines*, date, totalVaccinations)
*/
CREATE TABLE vaccinationsByManufacturer(
    iso VARCHAR(10) NOT NULL, 
    vaccines TEXT NOT NULL, 
    date TEXT NOT NULL, 
    totalVaccinations INTEGER,
    PRIMARY KEY (iso, vaccines, date),
    FOREIGN KEY (iso) REFERENCES country(iso),
    FOREIGN KEY (vaccines) REFERENCES manufacturer(vaccines)
    );

/*dataFrom(iso*, url*, lastObservationDate)*/
CREATE TABLE dataFrom(
    iso VARCHAR(10) NOT NULL, 
    url TEXT NOT NULL, 
    lastObservationDate TEXT,
    PRIMARY KEY (iso, url),
    FOREIGN KEY (iso) REFERENCES country(iso),
    FOREIGN KEY (url) REFERENCES sources(url)
    );
    
    
SELECT *
FROM country;

SELECT *
FROM sources;

SELECT *
FROM manufacturer;

SELECT *
FROM vaccinations;

SELECT *
FROM peopleVaccinatedByCountry;

SELECT *
FROM states;

