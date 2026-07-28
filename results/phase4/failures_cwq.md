## WebQTrn-2069_14d783de97238bd1ef6eb28fe7221306 (wrong)

**Q:** Which language is spoken in Chile, its main speaking country is Peru?

**gold:** ['Puquina Language']

**answer:** Spanish Language is spoken in Chile, and its main speaking country is Peru.

**entities:** ['Spanish Language']

- plan: ['find the language spoken in Chile', 'find the main speaking country of #1', 'find which language is spoken in #2']
- explored: ['location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'location.country.official_language', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'location.country.official_language'] (max_score 0.698)
- eval: continue resolved=['Spanish Language', 'Aymara language', 'Puquina Language', 'Mapudungun Language']
- explored: ['language.human_language.main_country', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in'] (max_score 0.755)
- eval: continue resolved=['Spain', 'Peru', 'Chile']
- explored: ['language.human_language.main_country', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in'] (max_score 0.755)
- eval: continue resolved=['Spanish Language', 'Aymara language', 'Puquina Language', 'Mapudungun Language']
- explored: ['location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'language.human_language.main_country'] (max_score 0.653)
- eval: continue resolved=['Spanish Language', 'Aymara language', 'Puquina Language']
- verifier: grounded unsupported=[]

---

## WebQTrn-894_022431f6dfa30cf2e715eb171e0437ec (wrong)

**Q:** What inspired Scott Fitzgerald and was also influenced by Mark Twain?

**gold:** ['Sherwood Anderson']

**answer:** Jazz Age inspired F. Scott Fitzgerald.

**entities:** ['Jazz Age']

- plan: ['find what inspired Scott Fitzgerald', 'find what was influenced by Mark Twain', 'find the overlap between #1 and #2']
- explored: ['book.author.school_or_movement', 'book.written_work.author', 'book.school_or_movement.associated_authors', 'book.written_work.author', 'book.book_subject.works', 'fictional_universe.fictional_character.character_created_by'] (max_score 0.256)
- eval: continue resolved=['Mark Twain']
- explored: ['book.school_or_movement.associated_authors', 'book.author.school_or_movement', 'book.written_work.school_or_movement', 'book.written_work.author', 'media_common.adapted_work.adaptations', 'media_common.adaptation.adapted_from'] (max_score 0.23)
- eval: continue resolved=['Jazz Age']
- explored: ['book.author.works_written', 'book.author.works_written', 'book.author.contributing_author_to', 'book.author.works_written', 'book.school_or_movement.associated_authors', 'book.written_work.author'] (max_score 0.222)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['book.school_or_movement.associated_authors', 'book.author.school_or_movement', 'book.written_work.school_or_movement', 'book.written_work.author', 'media_common.adapted_work.adaptations', 'media_common.adaptation.adapted_from'] (max_score 0.23)
- eval: backtrack resolved=['F. Scott Fitzgerald']
- backtrack: evaluator
- explored: ['book.school_or_movement.associated_works', 'book.book_subject.works', 'book.school_or_movement.associated_period', 'book.written_work.subjects', 'book.book.genre', 'media_common.adapted_work.adaptations'] (max_score 0.191)
- eval: continue resolved=['Jazz Age']
- explored: ['book.book_subject.works', 'book.school_or_movement.associated_works', 'book.written_work.school_or_movement', 'book.book_subject.works', 'book.school_or_movement.associated_works', 'book.written_work.author'] (max_score 0.243)
- eval: continue resolved=['Jazz Age']
- explored: ['base.inspiration.inspiration.inspired_by', 'base.inspiration.inspiration.inspired_by', 'base.inspiration.inspiration.inspiration_for', 'book.school_or_movement.associated_works', 'book.book_subject.works', 'book.school_or_movement.associated_period'] (max_score 0.275)
- eval: continue resolved=['Jazz Age']
- verifier: unsupported unsupported=['Jazz Age was also influenced by Mark Twain']

---

## WebQTrn-3100_d059b24adec4064377b957ca598769be (wrong)

**Q:** What part is the country with the capital named Santo Domingo?

**gold:** ['Greater Antilles', 'Latin America', 'North America', 'Americas', 'País']

**answer:** The country with the capital named Santo Domingo is Dominican Republic.

**entities:** ['Dominican Republic']

- plan: ['find the country with the capital named Santo Domingo', 'find the part of #1']
- explored: ['location.country.capital', 'location.capital_of_administrative_division.capital_of', 'location.administrative_division_capital_relationship.capital'] (max_score 0.675)
- eval: continue resolved=['Dominican Republic']
- explored: ['location.country.administrative_divisions', 'location.country.first_level_divisions', 'location.administrative_division.country'] (max_score 0.553)
- eval: answer resolved=['La Romana Province, Dominican Republic', 'Duarte Province', 'Distrito Nacional', 'Santiago Rodríguez Province']
- verifier: grounded unsupported=[]

---

## WebQTrn-303_2ee96aa7464485d80d214b61773f4a5c (wrong)

**Q:** Who was the literary role model for the "Not Without Laughter (Thrift Edition)" piece poet?

**gold:** ['Walt Whitman']

**answer:** Langston Hughes

**entities:** ['Langston Hughes']

- plan: ['find the literary role model for the poet of "Not Without Laughter (Thrift Edition)"']
- explored: ['book.book_edition.author_editor', 'book.book_edition.book', 'book.author.book_editions_published'] (max_score 0.508)
- eval: continue resolved=['Langston Hughes']
- explored: ['book.written_work.author', 'book.author.works_written', 'book.written_work.subjects', 'book.author.works_written', 'book.author.works_written', 'book.literary_series.author_s'] (max_score 0.545)
- eval: continue resolved=['Langston Hughes']
- explored: ['book.literary_series.author_s', 'book.author.works_written', 'book.author.works_written', 'book.author.works_written', 'book.written_work.author', 'book.written_work.subjects'] (max_score 0.297)
- eval: backtrack resolved=['Langston Hughes']
- backtrack: evaluator
- explored: ['book.book_edition.book', 'book.book_edition.book', 'book.book_edition.author_editor', 'book.written_work.author', 'book.written_work.author', 'book.author.contributing_author_to'] (max_score 0.29)
- eval: backtrack resolved=['Langston Hughes']
- backtrack: evaluator
- explored: ['book.book_edition.contributing_authors', 'book.author.series_written_or_contributed_to', 'book.written_work.subjects', 'book.written_work.original_language', 'book.author.book_editions_published', 'book.book_edition.publisher'] (max_score 0.258)
- eval: backtrack resolved=['Langston Hughes']
- backtrack: evaluator
- explored: ['theater.theatrical_lyricist.play_lyrics_written', 'book.book_edition.author_editor', 'theater.play.lyricist', 'book.book.editions', 'book.book.editions', 'book.book_edition.binding'] (max_score 0.225)
- eval: answer resolved=['Langston Hughes']
- verifier: grounded unsupported=[]

---

## WebQTrn-2292_ea0bc3bb340865025c534c91eca19be9 (wrong)

**Q:** What kind of economy does the country have that breeds Moscow watchdogs?

**gold:** ['Communist state', 'Socialist state', 'Soviet democracy', 'Parliamentary republic']

**answer:** The country is Soviet Union, and it has a Communist state economy.

**entities:** ['Soviet Union']

- plan: ['find the country that breeds Moscow watchdogs', 'find the kind of economy of #1']
- explored: ['biology.breed_origin.breeds_originating_here', 'biology.animal_breed.place_of_origin', 'biology.breed_temperament.breeds'] (max_score 0.55)
- eval: continue resolved=['Soviet Union']
- explored: ['finance.currency.countries_formerly_used', 'government.form_of_government.countries', 'location.country.form_of_government'] (max_score 0.204)
- eval: continue resolved=['Communist state', 'Socialist state']
- explored: ['finance.currency.countries_used', 'finance.currency.countries_formerly_used', 'location.country.currency_used', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.form_of_government.countries'] (max_score 0.222)
- eval: answer resolved=['Socialist state', 'Communist state']
- verifier: grounded unsupported=[]

---

## WebQTrn-2047_3d5f855275265f74d81b862231578e33 (wrong)

**Q:** What is the name of the structure opened in 1997 where the Chicago Cubs play?

**gold:** ['Hohokam Stadium']

**answer:** Wrigley Field

**entities:** ['Wrigley Field']

- plan: ['find where the Chicago Cubs play', 'find the structure opened in 1997 at #1', 'find the name of #2']
- explored: ['sports.sports_team.venue', 'sports.sports_team.arena_stadium', 'sports.sports_team.location'] (max_score 0.61)
- eval: continue resolved=['Wrigley Field']
- explored: ['time.event.locations', 'location.location.events', 'sports.sports_team.arena_stadium'] (max_score 0.429)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['sports.sports_facility.home_venue_for', 'sports.sports_facility.teams', 'base.playball.baseball_stadium.naming_rights'] (max_score 0.279)
- eval: continue resolved=[]
- explored: ['sports.sports_team.arena_stadium', 'sports.sports_team.venue', 'base.schemastaging.sports_team_extra.training_ground', 'sports.sports_team.arena_stadium', 'sports.sports_team.venue', 'sports.sports_facility.teams'] (max_score 0.553)
- eval: continue resolved=['Wrigley Field']
- explored: ['base.schemastaging.sports_facility_extra.training_ground_for', 'sports.sports_team.arena_stadium', 'sports.sports_facility.home_venue_for', 'sports.sports_facility.home_venue_for', 'base.playball.baseball_stadium.naming_rights', 'sports.sports_facility.teams'] (max_score 0.284)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-1677_bdfdca39c58846e51247fd78bc7683eb (wrong)

**Q:** In which films decorated by Karen O'Hara did Adam Sandler appear?

**gold:** ['Paul Blart: Mall Cop 2', 'Blended']

**answer:** The answer could not be verified against the knowledge graph. Spider-Man and The American President are films decorated by Karen O'Hara, but Adam Sandler’s appearance in them is not supported.

**entities:** ['Spider-Man', 'The American President']

- plan: ["find films decorated by Karen O'Hara", 'find which of #1 feature Adam Sandler']
- explored: ['film.film.film_set_decoration_by', 'film.film_set_designer.film_sets_designed', 'award.award_honor.award_winner', 'film.writer.film', 'film.film.written_by', 'film.person_or_entity_appearing_in_film.films'] (max_score 0.637)
- eval: continue resolved=['True Identity', 'Blended', 'License to Wed', 'Spider-Man']
- explored: ['film.film_film_distributor_relationship.film', 'film.film.costume_design_by', 'film.film.directed_by', 'film.film_film_distributor_relationship.film', 'film.film.costume_design_by', 'film.music_contributor.film'] (max_score 0.194)
- eval: continue resolved=['Spider-Man', 'License to Wed']
- explored: ['comic_books.comic_book_creator.characters_created', 'comic_books.comic_book_creator.series_created', 'comic_books.comic_book_character.created_by', 'comic_books.comic_book_creator.characters_created', 'people.marriage.spouse', 'comic_books.comic_book_creator.series_created'] (max_score 0.226)
- eval: continue resolved=['Spider-Man']
- explored: ['fictional_universe.marriage_of_fictional_characters.spouses', 'comic_books.comic_book_creator.characters_created', 'fictional_universe.fictional_character.married_to', 'fictional_universe.marriage_of_fictional_characters.spouses', 'comic_books.comic_book_creator.characters_created', 'fictional_universe.fictional_character.married_to'] (max_score 0.27)
- eval: answer resolved=['Spider-Man']
- verifier: unsupported unsupported=['Adam Sandler appeared in Spider-Man', 'Adam Sandler appeared in The American President']

---

## WebQTrn-1069_3c89af72801c057504e78b3a263a9b77 (wrong)

**Q:** What language is used in Denmark with the abbreviation DE?

**gold:** ['German Language']

**answer:** Danish Language

**entities:** ['Danish Language']

- plan: ['find the entity in Denmark with the abbreviation DE', 'find the language used in #1']
- explored: ['base.aareas.schema.administrative_area_type.iso_country', 'location.country.official_language', 'location.administrative_division.country'] (max_score 0.263)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['base.aareas.schema.earth.sovereign_domain.sovereign_state', 'location.country.internet_tld', 'location.location.contains'] (max_score 0.238)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['location.location.contains', 'base.biblioness.bibs_location.country', 'base.jewlib.judaica_owner.parent_institution'] (max_score 0.23)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['location.country.currency_used', 'location.country.administrative_divisions', 'location.location.containedby'] (max_score 0.21)
- eval: continue resolved=[]
- explored: ['location.administrative_division.country', 'location.location.contains', 'location.country.administrative_divisions', 'location.administrative_division.country', 'location.country.administrative_divisions', 'location.location.containedby'] (max_score 0.256)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-1923_eaeaff16b51e52669edc90501a373c61 (wrong)

**Q:** Which movie did Miley Cyrus appear in and got a nomination for "the entire cast"?

**gold:** ['Sex and the City 2']

**answer:** Miley Cyrus appeared in Hannah Montana: The Movie, which is the movie that got a nomination for "the entire cast".

**entities:** ['Hannah Montana: The Movie']

- plan: ['find movies that Miley Cyrus appeared in', 'find which of #1 got a nomination for "the entire cast"']
- explored: ['film.actor.film', 'film.person_or_entity_appearing_in_film.films', 'film.performance.actor'] (max_score 0.573)
- eval: continue resolved=['The Last Song', 'So Undercover', 'Hannah Montana: The Movie', 'Radio Disney Party Jams: The Concert']
- explored: ['film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack'] (max_score 0.351)
- eval: continue resolved=['Hannah Montana: The Movie', 'Radio Disney Party Jams: The Concert', 'The Last Song', 'So Undercover']
- explored: ['film.film.featured_song', 'film.film_featured_song.performed_by', 'film.film_featured_song.featured_in_film', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack'] (max_score 0.621)
- eval: continue resolved=['Hannah Montana: The Movie']
- explored: ['film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'film.film.featured_song', 'film.film_featured_song.performed_by', 'film.film_featured_song.featured_in_film'] (max_score 0.366)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-1178_09e61020934818b85641a22821e7a455 (wrong)

**Q:** Where is the Strictly 4 My N.I.G.G.A.Z. producer originally from?

**gold:** ['East Harlem']

**answer:** Marin City

**entities:** ['Marin City']

- plan: ['find the producer of Strictly 4 My N.I.G.G.A.Z.', 'find where #1 is originally from']
- explored: ['music.producer.releases_produced', 'music.recording.releases'] (max_score 0.588)
- eval: continue resolved=['Tupac Shakur']
- explored: ['location.location.people_born_here', 'music.artist.origin', 'people.person.places_lived'] (max_score 0.532)
- eval: answer resolved=['Marin City']
- verifier: grounded unsupported=[]

---

## WebQTest-213_024fd6ca0b4cb30927c22e93a552ae6c (wrong)

**Q:** What person notable with the medical condition Attention deficit hyperactivity disorder id Scarlett Johansson date?

**gold:** ['Justin Timberlake']

**answer:** Mary-Kate Olsen is a notable person with Attention deficit hyperactivity disorder.

**entities:** ['Mary-Kate Olsen']

- plan: ['find the person notable with Attention deficit hyperactivity disorder and named Scarlett Johansson', 'find the date associated with #1']
- explored: ['medicine.notable_person_with_medical_condition.condition', 'medicine.disease.notable_people_with_this_condition', 'fictional_universe.medical_condition_in_fiction.characters_with_this_condition', 'tv.tv_guest_personal_appearance.person', 'film.personal_film_appearance.person', 'people.person.gender'] (max_score 0.615)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['fictional_universe.fictional_character.medical_conditions', 'medicine.disease.medical_specialties', 'base.aubreymaturin.affliction.malady', 'film.performance.actor', 'film.person_or_entity_appearing_in_film.films', 'people.person.spouse_s'] (max_score 0.251)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['base.aubreymaturin.malady.sufferers', 'medicine.disease.includes_diseases', 'medicine.disease.includes_diseases', 'people.person.children', 'people.person.children', 'people.person.profession'] (max_score 0.205)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['medicine.symptom.symptom_of', 'medicine.risk_factor.diseases', 'medicine.risk_factor.diseases', 'theater.theater_role.actor', 'celebrities.sexual_orientation_phase.celebrity', 'celebrities.romantic_relationship.celebrity'] (max_score 0.201)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-2569_6b6fb0182356d92873272424688be466 (wrong)

**Q:** The building where the Houston Rockets and Houston Aeros played is now called what?

**gold:** ['Lakewood Church Central Campus']

**answer:** Toyota Center

**entities:** ['Toyota Center']

- plan: ['find the building where the Houston Rockets and Houston Aeros played', 'find what #1 is now called']
- explored: ['sports.sports_team.arena_stadium', 'sports.sports_facility.teams', 'sports.sports_team.venue', 'sports.sports_team.arena_stadium', 'sports.sports_facility.teams', 'sports.sports_team.venue'] (max_score 0.586)
- eval: continue resolved=['Toyota Center', 'Lakewood Church Central Campus']
- explored: ['sports.sports_facility.home_venue_for', 'sports.sports_team.arena_stadium', 'sports.sports_facility.teams', 'sports.sports_facility.home_venue_for', 'sports.sports_team.arena_stadium', 'sports.sports_facility.teams'] (max_score 0.239)
- eval: answer resolved=['Toyota Center', 'Lakewood Church Central Campus']
- verifier: grounded unsupported=[]

---

## WebQTrn-849_fa1fffe7995213b6528da57ea4c8d226 (wrong)

**Q:** Which country, with an army of 101,000, borders Germany?

**gold:** ['Belgium']

**answer:** Poland borders Germany. The claim that Poland has an army of 101,000 could not be verified against the knowledge graph.

**entities:** ['Poland']

- plan: ['find countries that border Germany', 'find which of #1 have an army of 101,000']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'film.film.country', 'film.film_regional_release_date.film', 'base.ontologies.ontology_instance_mapping.freebase_topic'] (max_score 0.309)
- eval: continue resolved=['Germany']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.states_and_provences.continent', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country'] (max_score 0.309)
- eval: continue resolved=['Belgium', 'Luxembourg', 'Poland', 'Austria']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country'] (max_score 0.309)
- eval: continue resolved=['Belgium', 'Liechtenstein']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.states_and_provences.continent', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country'] (max_score 0.309)
- eval: continue resolved=['Belgium', 'Liechtenstein', 'Europe']
- verifier: unsupported unsupported=['Poland has an army of 101,000']

---

## WebQTest-1348_b7598df908bf8cbe941f82e1cefaec28 (wrong)

**Q:** What defunct sports team later known as the Tennessee Oilers did Peyton Manning 's dad play for?

**gold:** ['Houston Oilers']

**answer:** Archie Manning played for Houston Oilers, which later became known as Tennessee Oilers.

**entities:** ['Archie Manning']

- plan: ['find the sports team later known as the Tennessee Oilers', "find the team that Peyton Manning's dad played for that is #1"]
- explored: ['sports.defunct_sports_team.later_known_as', 'sports.defunct_sports_team.later_known_as', 'sports.sports_team.previously_known_as', 'sports.pro_athlete.teams', 'sports.sports_team_roster.player', 'sports.pro_athlete.sports_played_professionally'] (max_score 0.617)
- eval: continue resolved=['Tennessee Oilers']
- explored: ['american_football.football_historical_coach_position.team', 'american_football.football_team.historical_coaching_staff', 'american_football.football_division.teams', 'american_football.football_historical_coach_position.team', 'american_football.football_team.historical_coaching_staff', 'sports.sports_team_season_record.team'] (max_score 0.375)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['american_football.football_team.division', 'sports.sports_team_season_record.team', 'american_football.football_game.home_team', 'sports.sports_team_roster.team', 'sports.sports_team.roster', 'sports.sports_team.season_record'] (max_score 0.308)
- eval: answer resolved=['Houston Oilers']
- verifier: unsupported unsupported=['Peyton Manning dad played for Houston Oilers']
- explored: ['sports.pro_sports_played.athlete', 'sports.sports_team_roster.player', 'sports.sports_award.award_winner'] (max_score 0.228)
- eval: answer resolved=['Archie Manning']
- verifier: grounded unsupported=[]

---

## WebQTrn-2100_faefa67fba5946fa87b438a6df0b8e63 (wrong)

**Q:** What city can the headquarters for Curno Brakes be found?

**gold:** ['Curno']

**answer:** Brembo

**entities:** ['Brembo']

- plan: ['find the headquarters for Curno Brakes', 'find the city where #1 can be found']
- explored: ['location.location.containedby', 'location.mailing_address.citytown', 'location.statistical_region.population'] (max_score 0.218)
- eval: continue resolved=['Curno']
- explored: ['location.administrative_division.country', 'location.administrative_division.capital', 'location.administrative_division_capital_relationship.administrative_division', 'location.administrative_division.country', 'organization.organization.locations', 'location.administrative_division.first_level_division_of'] (max_score 0.3)
- eval: continue resolved=['Brembo']
- explored: ['location.administrative_division.country', 'organization.organization.locations', 'location.administrative_division.first_level_division_of', 'location.administrative_division.country', 'location.administrative_division.second_level_division_of', 'location.location.containedby'] (max_score 0.3)
- eval: continue resolved=['Curno']
- explored: ['location.administrative_division.country', 'location.administrative_division.second_level_division_of', 'location.location.containedby', 'location.administrative_division.country', 'location.administrative_division.second_level_division_of', 'location.location.containedby'] (max_score 0.3)
- eval: backtrack resolved=['Curno']
- verifier: grounded unsupported=[]

---

## WebQTrn-493_cf7833e237b8cda1de396587129515c1 (wrong)

**Q:** Where was the newspaper La Libre Belgique distributed during World War II?

**gold:** ['Europe', 'Eurasia', 'Western Europe']

**answer:** La Libre Belgique during World War II was distributed in Belgium.

**entities:** ['Belgium']

- plan: ['find World War II distribution locations of La Libre Belgique']
- explored: ['periodicals.newspaper_circulation_area.newspapers', 'book.newspaper.circulation_areas'] (max_score 0.459)
- eval: answer resolved=['Belgium']
- verifier: grounded unsupported=[]

---

## WebQTrn-64_08a3071aec88af141fc20ed22cfff0e2 (wrong)

**Q:** What did the person who lived in Marin City once do?

**gold:** ['Bishop']

**answer:** The person who lived in Marin City was Tupac Shakur, and he once recorded California Love.

**entities:** ['Tupac Shakur', 'California Love']

- plan: ['find the person who lived in Marin City', 'find what #1 once did']
- explored: ['people.place_lived.location', 'location.location.people_born_here', 'people.person.place_of_birth', 'book.written_work.author', 'book.author.works_written', 'film.film.story_by'] (max_score 0.626)
- eval: continue resolved=['Tupac Shakur']
- explored: ['music.artist.track_contributions', 'music.recording.artist', 'music.album.artist'] (max_score 0.446)
- eval: continue resolved=['Tupac Shakur']
- explored: ['music.track_contribution.track', 'media_common.quotation.subjects', 'music.artist.track', 'music.track_contribution.role', 'music.recording_contribution.performance_role', 'base.recordingstudios.studio_musician.insturments_played'] (max_score 0.487)
- eval: answer resolved=['Out The Moon', 'Smile', 'Same Song', 'Gangsta Team']
- verifier: grounded unsupported=[]

---

## WebQTrn-3170_8c4cd2a8dd5064dcd1e88389796138c7 (wrong)

**Q:** What does the political appointee, Associate Director, White House Office of Public Liaison, have a degree in?

**gold:** ['Political Science']

**answer:** Kal Penn. The degree could not be determined from the facts provided.

**entities:** ['Kal Penn']

- plan: ['find the degree of the Associate Director of the White House Office of Public Liaison']
- explored: ['government.government_position_held.office_position_or_title', 'government.government_office_or_title.office_holders'] (max_score 0.504)
- eval: continue resolved=['Kal Penn']
- explored: ['government.government_position_held.office_holder', 'people.person.profession', 'award.award_nomination.award_nominee', 'education.honorary_degree.recipient', 'organization.leadership.person', 'business.board_member.leader_of'] (max_score 0.494)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['government.politician.government_positions_held', 'award.award_nominee.award_nominations', 'film.performance.actor', 'education.honorary_degree_recipient.honorary_degrees', 'organization.organization_member.member_of', 'government.us_president.vice_president'] (max_score 0.256)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['film.actor.film', 'tv.tv_actor.starring_roles', 'tv.regular_tv_appearance.actor', 'people.appointment.appointed_by', 'government.political_appointer.appointees', 'business.employment_tenure.person'] (max_score 0.226)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['people.person.gender', 'people.person.languages', 'people.person.nationality', 'government.us_vice_president.to_president', 'government.government_position_held.office_holder', 'government.political_party_tenure.politician'] (max_score 0.211)
- eval: answer resolved=['Kal Penn']
- verifier: grounded unsupported=[]

---

## WebQTrn-1484_1fbd766e1b1bf978da23e8646cadf3a1 (wrong)

**Q:** The person who attended the education institution Colegio AlemÃ¡n Alexander von Humboldt did what kind of paintings?

**gold:** ['Magic realism', 'Modern art', 'Surrealism']

**answer:** Frida Kahlo did paintings such as Self-Portrait, The Two Fridas, Henry Ford Hospital, and Viva la Vida, Watermelons.

**entities:** ['Frida Kahlo']

- plan: ['find the person who attended Colegio AlemÃ¡n Alexander von Humboldt', 'find what kind of paintings #1 did']
- explored: ['education.educational_institution.students_graduates', 'education.education.institution', 'symbols.namesake.named_after'] (max_score 0.416)
- eval: continue resolved=['Frida Kahlo']
- explored: ['visual_art.artwork.artist', 'visual_art.visual_artist.artworks', 'visual_art.artwork.art_subject'] (max_score 0.596)
- eval: answer resolved=['Roots', 'What the Water Gave Me', 'Living Nature', 'Congress of People for Peace']
- verifier: grounded unsupported=[]

---

## WebQTrn-1180_67f5f717564163742ca2588b7e186fd8 (wrong)

**Q:** The city of Wellsville can be found where in the United States?

**gold:** ['Missouri']

**answer:** Wellsville can be found in Montgomery County, United States of America.

**entities:** ['Montgomery County']

- plan: ['find the location of Wellsville in the United States']
- explored: ['location.us_county.hud_county_place', 'location.hud_county_place.place', 'location.hud_county_place.place', 'location.mailing_address.citytown', 'location.location.primarily_containedby', 'location.location.primarily_containedby'] (max_score 0.599)
- eval: continue resolved=['Wellsville', 'Montgomery County']
- explored: ['location.us_county.hud_county_place', 'location.hud_county_place.place', 'location.hud_county_place.place', 'location.us_county.hud_county_place', 'location.us_county.county_seat', 'location.hud_county_place.county'] (max_score 0.599)
- eval: answer resolved=['Montgomery County']
- verifier: grounded unsupported=[]

---

## WebQTest-1923_7084416ab9f72f1f1f8fc3ce7871ee4a (wrong)

**Q:** Which movie has Miley Cyrus starred in that is 102.0 minutes long?

**gold:** ['Hannah Montana: The Movie']

**answer:** The movie is The Last Song.

**entities:** ['The Last Song']

- plan: ['find movies that Miley Cyrus starred in', 'find which of #1 are 102.0 minutes long']
- explored: ['film.actor.film', 'film.performance.actor', 'film.person_or_entity_appearing_in_film.films'] (max_score 0.597)
- eval: continue resolved=['The Last Song', 'So Undercover', 'Hannah Montana: The Movie', 'Radio Disney Party Jams: The Concert']
- explored: ['film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack'] (max_score 0.351)
- eval: continue resolved=[]
- explored: ['film.film.featured_song', 'music.artist.track', 'film.film_featured_song.performed_by', 'film.film.featured_song', 'music.artist.track', 'film.film_featured_song.performed_by'] (max_score 0.351)
- eval: continue resolved=['Hannah Montana: The Movie']
- explored: ['film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack'] (max_score 0.351)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-831_f2d789d28c11bc5b682263b07195d208 (wrong)

**Q:** What is the last movie by the artist who recorded Faster Kill Pussycat?

**gold:** ['Something Wicked']

**answer:** Brittany Murphy. The last movie in the facts is The Dead Girl.

**entities:** ['The Dead Girl']

- plan: ['find the artist who recorded Faster Kill Pussycat', 'find the last movie by #1']
- explored: ['music.recording.artist', 'music.album.artist', 'music.artist.track'] (max_score 0.657)
- eval: continue resolved=['Paul Oakenfold', 'Brittany Murphy']
- explored: ['film.actor.film', 'film.music_contributor.film', 'film.film.music', 'film.actor.film', 'film.performance.actor', 'film.producer.film'] (max_score 0.589)
- eval: continue resolved=['Brittany Murphy']
- explored: ['film.film.starring', 'film.performance.film', 'film.film.country', 'film.film.starring', 'film.performance.film', 'film.producer.film'] (max_score 0.609)
- eval: continue resolved=['Brittany Murphy']
- explored: ['film.actor.film', 'film.performance.actor', 'film.producer.film', 'film.actor.film', 'film.music_contributor.film', 'film.film.music'] (max_score 0.589)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-1297_a0da13a7b70a064b8cffb58007f6739d (wrong)

**Q:** Where did the artist grow up that recorded #Thatpower?

**gold:** ['London']

**answer:** Justin Bieber grew up in Stratford and Canada.

**entities:** ['Stratford', 'Canada']

- plan: ['find the artist that recorded #Thatpower', 'find where #1 grew up']
- explored: ['music.recording.artist', 'music.featured_artist.recordings', 'music.recording.featured_artists'] (max_score 0.645)
- eval: continue resolved=['Will i Am', 'Justin Bieber']
- explored: ['people.place_lived.person', 'people.person.place_of_birth', 'people.person.places_lived', 'people.place_lived.person', 'people.person.place_of_birth', 'people.person.places_lived'] (max_score 0.504)
- eval: answer resolved=['Los Angeles', 'Stratford', 'Canada', 'London']
- verifier: grounded unsupported=[]

---

## WebQTrn-2784_025fdfafd914ff922ab8144f527c06ec (wrong)

**Q:** In what films does the lyracist for "Panther Power" appear?

**gold:** ['Murder Was the Case', 'Poetic Justice', "Gridlock'd", 'Above the Rim', 'Juice', 'Nothing but Trouble', 'Gang Related', 'Bullet']

**answer:** The lyracist for "Panther Power" is Tupac Shakur. Tupac Shakur appears in Tupac: Assassination, Tupac Shakur: Thug Angel: The Life of an Outlaw, R.I.P. II: Eyes on Hip Hop, Tha Westside, Apprenticeship of Tupac Shakur, Tupac: Live at the House of Blues, Tupac: Resurrection, Thug Immortal: The Tupac Shakur Story, Freestyle: The Art of Rhyme, and R.I.P.: Shades of Hip Hop.

**entities:** ['Tupac: Assassination', 'Tupac Shakur: Thug Angel: The Life of an Outlaw', 'R.I.P. II: Eyes on Hip Hop', 'Tha Westside', 'Apprenticeship of Tupac Shakur', 'Tupac: Live at the House of Blues', 'Tupac: Resurrection', 'Thug Immortal: The Tupac Shakur Story', 'Freestyle: The Art of Rhyme', 'R.I.P.: Shades of Hip Hop']

- plan: ['find the lyracist for "Panther Power"', 'find the films that this person appears in']
- explored: ['music.composition.lyricist', 'music.lyricist.lyrics_written'] (max_score 0.358)
- eval: continue resolved=['Tupac Shakur']
- explored: ['film.personal_film_appearance.person', 'film.person_or_entity_appearing_in_film.films', 'film.actor.film'] (max_score 0.806)
- eval: answer resolved=['Apprenticeship of Tupac Shakur', 'Tupac: Resurrection', 'Welcome to Death Row', 'Biggie & Tupac']
- verifier: grounded unsupported=[]

---

## WebQTest-1736_125140bfa1a60527bde6e40dce7fe54a (wrong)

**Q:** Where's the location where the Slavic language is spoken located?

**gold:** ['Europe']

**answer:** The location where the Slavic language is spoken is Holy Roman Empire.

**entities:** ['Holy Roman Empire']

- plan: ['find the location where the Slavic language is spoken', 'find the location of #1']
- explored: ['location.country.official_language', 'language.language_family.languages', 'language.human_language.language_family'] (max_score 0.377)
- eval: backtrack resolved=['Holy Roman Empire']
- backtrack: evaluator
- explored: [] (max_score 0.0)
- eval: backtrack resolved=['Holy Roman Empire']
- backtrack: dead_end
- explored: [] (max_score 0.0)
- eval: backtrack resolved=['Holy Roman Empire']
- backtrack: dead_end
- explored: [] (max_score 0.0)
- eval: continue resolved=['Holy Roman Empire']
- verifier: grounded unsupported=[]

---

## WebQTrn-2570_ff6becc9074132acf2f300dbba1c1e4e (wrong)

**Q:** Who was the president of the United States during World War 2 that started his governmental position after January 2, 1939?

**gold:** ['Franklin D. Roosevelt', 'Harry S. Truman']

**answer:** Dwight D. Eisenhower was the president of the United States during World War 2 that started his governmental position after January 2, 1939.

**entities:** ['Dwight D. Eisenhower']

- plan: ['find the president of the United States during World War 2', 'find which of #1 started his governmental position after January 2, 1939']
- explored: ['government.government_position_held.office_position_or_title', 'government.electoral_college_elected_office.office', 'government.election.office', 'military.military_person.participated_in_conflicts', 'military.military_conflict.commanders', 'military.military_command.military_conflict'] (max_score 0.453)
- eval: continue resolved=['Dwight D. Eisenhower']
- explored: ['organization.role.leaders', 'organization.leadership.role', 'organization.role.governors', 'government.us_president.vice_president', 'government.us_vice_president.to_president', 'military.military_person.participated_in_conflicts'] (max_score 0.454)
- eval: continue resolved=['Dwight D. Eisenhower']
- explored: ['organization.leadership.person', 'business.board_member.leader_of', 'organization.organization.founders', 'organization.leadership.person', 'business.board_member.leader_of', 'organization.leadership.person'] (max_score 0.172)
- eval: continue resolved=['Dwight D. Eisenhower']
- explored: ['people.person.employment_history', 'business.employment_tenure.person', 'government.government_position_held.office_holder'] (max_score 0.411)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-25_2a2de50d3b65cc5d2c88f54e283a4b8a (wrong)

**Q:** What movie featured Taylor Lautner and was released straight to video?

**gold:** ['Shadow Fury', 'Shadow Fury']

**answer:** Abduction

**entities:** ['Abduction']

- plan: ['find the movie that featured Taylor Lautner', 'find which of #1 were released straight to video']
- explored: ['film.actor.film', 'film.performance.actor', 'film.personal_film_appearance.person', 'film.film.film_format', 'film.film_film_distributor_relationship.film_distribution_medium', 'film.film_regional_release_date.film_release_distribution_medium'] (max_score 0.623)
- eval: continue resolved=['Abduction', "Valentine's Day", 'Incarceron', 'Tracers']
- explored: ['film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film_film_distributor_relationship.film', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.story_by'] (max_score 0.319)
- eval: continue resolved=['Abduction', 'Twilight']
- explored: ['film.film_regional_release_date.film_release_distribution_medium', 'base.mediapackage.video_release.consumer_releases', 'base.mediapackage.media_release.video_contents', 'film.film_regional_release_date.film_release_distribution_medium', 'film.film_regional_release_date.film_regional_debut_venue', 'film.film_film_distributor_relationship.film_distribution_medium'] (max_score 0.528)
- eval: continue resolved=['Abduction', 'Twilight']
- explored: ['film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.edited_by', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.edited_by'] (max_score 0.319)
- eval: continue resolved=['Abduction', 'Twilight']
- verifier: grounded unsupported=[]

---

## WebQTrn-64_025fdfafd914ff922ab8144f527c06ec (wrong)

**Q:** What was the name in "Juice" of the lyricist for "Panther Power"?

**gold:** ['Bishop']

**answer:** The lyricist for "Panther Power" in "Juice" was Tupac Shakur.

**entities:** ['Tupac Shakur']

- plan: ['find the lyricist for "Panther Power"', 'find the name used in "Juice" for #1']
- explored: ['music.lyricist.lyrics_written', 'music.composition.lyricist', 'music.lyricist.lyrics_written', 'music.composition.lyricist', 'music.artist.track'] (max_score 0.682)
- eval: continue resolved=['Tupac Shakur']
- explored: ['music.artist.label', 'symbols.name_source.namesakes', 'symbols.name_source.namesakes'] (max_score 0.481)
- eval: backtrack resolved=['Tupac Shakur']
- backtrack: evaluator
- explored: ['symbols.namesake.named_after', 'symbols.namesake.named_after', 'music.record_label.artist'] (max_score 0.176)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['music.artist.origin', 'music.artist.contribution', 'music.artist.track_contributions'] (max_score 0.149)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['base.popstra.celebrity.canoodled', 'music.album.artist', 'music.recording.artist'] (max_score 0.138)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-213_71621b15ae9777fca8c1becaa188a3bb (wrong)

**Q:** Who were the award nominees for the 2003 Boston Society of Film Critics Awards?

**gold:** ['Josh Hartnett']

**answer:** The award nominee was Scarlett Johansson for Lost in Translation.

**entities:** ['Scarlett Johansson']

- plan: ['find the 2003 Boston Society of Film Critics Awards', 'find the award nominees for #1']
- explored: ['award.award_ceremony.awards_presented', 'award.award_ceremony.nominees', 'award.award_nomination.ceremony'] (max_score 0.587)
- eval: continue resolved=['Boston Society of Film Critics Awards 2003']
- explored: ['award.award_category.nominees', 'award.award_nomination.award', 'award.award_category.winners', 'award.award_nominee.award_nominations', 'award.award_nomination.award_nominee', 'award.ranking.item'] (max_score 0.806)
- eval: answer resolved=['Her', "People's Choice Award for Favorite Star Under 35", "People's Choice Award for Favorite Leading Lady", "33rd People's Choice Awards"]
- verifier: grounded unsupported=[]

---

## WebQTrn-2540_1af583970c492fc3682ae363bbfca3d3 (wrong)

**Q:** Who was influenced by Eugene Delacroix and inspired Monet?

**gold:** ['Camille Pissarro', 'Pierre-Auguste Renoir']

**answer:** Claude Monet was influenced by Eugène Delacroix, and Eugène Delacroix influenced Claude Monet.

**entities:** ['Claude Monet']

- plan: ['find people influenced by Eugene Delacroix', 'find which of #1 inspired Monet']
- explored: ['influence.influence_node.influenced_by', 'influence.influence_node.influenced_by', 'influence.influence_node.influenced', 'influence.influence_node.influenced_by', 'influence.influence_node.influenced_by', 'influence.influence_node.influenced'] (max_score 0.581)
- eval: continue resolved=['Vincent van Gogh', 'Purvis Young', 'Pierre-Auguste Renoir', 'Pierre Puvis de Chavannes']
- explored: ['visual_art.artwork.artist', 'visual_art.visual_artist.associated_periods_or_movements', 'visual_art.visual_artist.art_forms', 'visual_art.artwork.artist', 'visual_art.art_series.artist', 'visual_art.art_period_movement.associated_artists'] (max_score 0.324)
- eval: continue resolved=['Vincent van Gogh', 'Pierre-Auguste Renoir']
- explored: ['visual_art.artwork.artist', 'visual_art.artwork.owners', 'visual_art.artwork.art_subject', 'visual_art.artwork.artist', 'visual_art.art_series.artworks', 'visual_art.artwork.art_form'] (max_score 0.309)
- eval: answer resolved=['Vincent van Gogh', 'Pierre-Auguste Renoir']
- verifier: grounded unsupported=[]

---

## WebQTest-1012_73741811f34519b29f7d19ccfd4d9553 (wrong)

**Q:** What structure opened in 1922 in Hollywood, CA?

**gold:** ["Grauman's Egyptian Theatre"]

**answer:** Hollywood Palladium

**entities:** ['Hollywood Palladium']

- plan: ['find the structure in Hollywood, CA that opened in 1922']
- explored: ['film.film_location.featured_in_films', 'film.film.featured_film_locations', 'location.location.containedby'] (max_score 0.329)
- eval: continue resolved=[]
- explored: ['film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.director.film', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film.film_production_design_by'] (max_score 0.314)
- eval: continue resolved=[]
- explored: ['organization.organization.place_founded', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'location.location.containedby'] (max_score 0.47)
- eval: answer resolved=['Hollywood Palladium']
- verifier: unsupported unsupported=['Hollywood Palladium opened in 1922']
- explored: ['time.event.locations', 'location.location.events', 'location.location.containedby'] (max_score 0.388)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-25_f65ceb2f4ef98392b0177705932740a5 (wrong)

**Q:** What other movies has the actor that played the character Eliot Murtaugh play in?

**gold:** ['Run the Tide', 'The Ridiculous Six', "He's a Bully, Charlie Brown", 'Twilight', 'The Twilight Saga: New Moon', "Valentine's Day", 'Cheaper by the Dozen 2', 'The Adventures of Sharkboy and Lavagirl', 'Shadow Fury', 'Eclipse', 'The Twilight Saga: Breaking Dawn - Part 1', 'The Nick and Jessica Variety Hour', 'Northern Lights', 'Abduction', 'The Twilight Saga: Breaking Dawn - Part 2', 'Field of Dreams 2: Lockout', 'Incarceron', 'Grown Ups 2', 'Tracers']

**answer:** Taylor Lautner played Eliott Murtaugh, and other movies he played in include Twilight, The Twilight Saga: New Moon, Eclipse, The Twilight Saga: Breaking Dawn - Part 1, The Twilight Saga: Breaking Dawn - Part 2, Northern Lights, The Ridiculous Six, and Incarceron.

**entities:** ['Taylor Lautner']

- plan: ['find the actor that played the character Eliot Murtaugh', 'find other movies that #1 has played in']
- explored: ['film.film_character.portrayed_in_films', 'film.performance.character'] (max_score 0.589)
- eval: continue resolved=['Taylor Lautner']
- explored: ['film.actor.film', 'film.performance.actor', 'tv.tv_actor.starring_roles'] (max_score 0.631)
- eval: answer resolved=['Abduction', 'Incarceron', 'Tracers', 'Twilight']
- verifier: grounded unsupported=[]

---

## WebQTest-1251_cf6cc4cc9ed790243a390f155ae72256 (wrong)

**Q:** Which country speaks Germanic languages has the nominal GDP of 279500000000.0?

**gold:** ['Austria']

**answer:** Germany speaks a Germanic language. However, the claim that it is the country with a nominal GDP of 279500000000.0 is not verified by the knowledge graph.

**entities:** ['Germany']

- plan: ['find the country that has nominal GDP of 279500000000.0', 'find which of #1 speaks Germanic languages']
- explored: ['location.country.official_language', 'language.human_language.countries_spoken_in', 'language.human_language.main_country'] (max_score 0.239)
- eval: continue resolved=['Germany']
- explored: ['location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_real', 'location.statistical_region.military_expenditure_percent_gdp', 'location.country.currency_used', 'location.country.form_of_government', 'location.country.capital'] (max_score 0.721)
- eval: backtrack resolved=['Switzerland']
- backtrack: evaluator
- explored: ['location.statistical_region.gdp_growth_rate', 'location.country.currency_used', 'location.statistical_region.gross_savings_as_percent_of_gdp', 'location.country.official_language', 'location.location.geolocation', 'location.location.containedby'] (max_score 0.352)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['location.statistical_region.trade_balance_as_percent_of_gdp', 'location.statistical_region.agriculture_as_percent_of_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp', 'location.location.contains', 'location.location.events', 'government.national_anthem_of_a_country.country'] (max_score 0.319)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['location.statistical_region.health_expenditure_as_percent_of_gdp', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'finance.currency.countries_used', 'location.location.contains', 'base.schemastaging.context_name.pronunciation', 'location.location.containedby'] (max_score 0.312)
- eval: continue resolved=['Switzerland']
- explored: ['business.market_size.currency', 'location.country.currency_used', 'location.country.currency_formerly_used', 'location.country.currency_used', 'finance.currency.countries_used', 'measurement_unit.dated_money_value.currency'] (max_score 0.56)
- eval: continue resolved=['Switzerland']
- explored: ['location.statistical_region.gdp_nominal', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_real', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.military_expenditure_percent_gdp', 'location.country.currency_used'] (max_score 0.725)
- eval: backtrack resolved=[]
- verifier: unsupported unsupported=['Germany is the best match for country with nominal GDP of 279500000000.0']

---

## WebQTrn-567_2c5591f1dbe7402405004d7a0836dd3b (wrong)

**Q:** Which animated movies hs Ron Howard done?

**gold:** ['Osmosis Jones']

**answer:** Ron Howard did these animated movies: Willow and Splash. I could not determine any others from the facts provided.

**entities:** ['Willow', 'Splash']

- plan: ['find animated movies associated with Ron Howard']
- explored: ['film.director.film', 'film.film.directed_by', 'film.actor.film'] (max_score 0.567)
- eval: continue resolved=['Cocoon', 'Willow', 'Splash']
- explored: ['film.film.genre', 'film.production_company.films', 'film.film_film_distributor_relationship.film', 'film.film_subject.films', 'film.film.featured_film_locations', 'film.film_art_director.films_art_directed'] (max_score 0.345)
- eval: continue resolved=['Cocoon', 'Willow', 'Backdraft', 'The Missing']
- explored: ['film.film_subject.films', 'film.film.subjects', 'film.film.genre', 'film.film_subject.films', 'film.film.subjects', 'film.film.genre'] (max_score 0.326)
- eval: continue resolved=['Cocoon', 'Willow', 'Backdraft', 'Splash']
- explored: ['film.film_subject.films', 'film.music_contributor.film', 'film.film_subject.films', 'film.film_art_director.films_art_directed', 'film.production_company.films', 'film.film_subject.films'] (max_score 0.326)
- eval: answer resolved=['Cocoon', 'Willow', 'Backdraft', 'The Missing']
- verifier: grounded unsupported=[]

---

## WebQTest-212_7905d5d52ac1a17f68996d4a2245e682 (wrong)

**Q:** What state does the Colorado River run through that has a governmental jurisdiction location symbol adapted the earliest?

**gold:** ['Phoenix']

**answer:** Colorado

**entities:** ['Colorado']

- plan: ['find the states that the Colorado River runs through', 'find which of #1 has the earliest adapted governmental jurisdiction location symbol']
- explored: ['location.location.partially_contains', 'location.location.partially_contained_by', 'location.partial_containment_relationship.partially_contains'] (max_score 0.436)
- eval: continue resolved=['Colorado', 'Arizona', 'California', 'Utah']
- explored: ['government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country'] (max_score 0.647)
- eval: continue resolved=['Colorado', 'Arizona', 'Utah']
- explored: ['location.symbol_of_administrative_division.official_symbol_of', 'location.location_symbol_relationship.symbol', 'biology.organism_classification.lower_classifications', 'location.symbol_of_administrative_division.official_symbol_of', 'location.location_symbol_relationship.symbol', 'location.location_symbol_relationship.Kind_of_symbol'] (max_score 0.31)
- eval: continue resolved=['Colorado', 'Arizona', 'Utah']
- explored: ['government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country'] (max_score 0.674)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-1405_b98a27e21e904173168eb7517b123e51 (wrong)

**Q:** Where did President Kennedy go to school that has less than 2416 postgraduates?

**gold:** ['Stanford Graduate School of Business']

**answer:** Choate Rosemary Hall

**entities:** ['Choate Rosemary Hall']

- plan: ['find the school that President Kennedy went to', 'find which of #1 have less than 2416 postgraduates']
- explored: ['education.education.student', 'people.person.education', 'base.inaugurations.inauguration.president'] (max_score 0.529)
- eval: continue resolved=['Choate Rosemary Hall']
- explored: ['education.educational_institution.students_graduates', 'education.education.institution', 'education.educational_institution.school_type'] (max_score 0.418)
- eval: continue resolved=['Choate Rosemary Hall']
- explored: ['base.jewlib.research_collection.originators', 'base.usnris.nris_listing.significant_person', 'base.kwebbase.kwsentence.kwtopic', 'education.educational_institution.school_type', 'business.industry.companies', 'organization.organization.organization_type'] (max_score 0.129)
- eval: backtrack resolved=[]
- backtrack: low_score
- explored: ['education.educational_institution.students_graduates', 'education.education.institution', 'education.educational_institution.school_type'] (max_score 0.418)
- eval: continue resolved=['Choate Rosemary Hall']
- explored: ['base.reviews.review.mentions', 'visual_art.artwork.owners', 'visual_art.artwork_owner_relationship.artwork', 'book.book_subject.works', 'base.schemastaging.context_name.pronunciation', 'book.written_work.subjects'] (max_score 0.115)
- eval: backtrack resolved=[]
- backtrack: low_score
- explored: ['organization.organization_member.member_of', 'visual_art.artwork.locations', 'organization.organization_membership.member', 'business.employment_tenure.company', 'business.business_operation.industry', 'organization.organization_type.organizations_of_this_type'] (max_score 0.106)
- eval: backtrack resolved=[]
- backtrack: low_score
- explored: ['media_common.dedicatee.dedications', 'visual_art.visual_artist.artworks', 'award.award_nominee.award_nominations', 'business.employer.employees', 'fictional_universe.fictional_organization_type.organizations', 'fictional_universe.fictional_organization.type_of_organization'] (max_score 0.1)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-64_d8e43a02200cfdff82052f8cc5395b27 (wrong)

**Q:** What was the actor's name that played the character Digital Underground Member in "Juice"?

**gold:** ['Bishop']

**answer:** Tupac Shakur played the character Digital Underground member in Juice.

**entities:** ['Tupac Shakur']

- plan: ['find the character Digital Underground Member in Juice', 'find the actor who played #1']
- explored: ['film.film_character.portrayed_in_films', 'film.performance.character', 'film.film.story_by', 'film.film.soundtrack', 'film.film.soundtrack'] (max_score 0.461)
- eval: continue resolved=['Tupac Shakur']
- explored: ['book.book.characters', 'base.popstra.celebrity.friendship', 'base.popstra.friendship.participant', 'film.film.story_by', 'film.film_story_contributor.film_story_credits', 'film.person_or_entity_appearing_in_film.films'] (max_score 0.238)
- eval: continue resolved=['Tupac Shakur']
- explored: ['film.performance.actor', 'film.actor.film', 'film.film_character.portrayed_in_films'] (max_score 0.593)
- eval: answer resolved=['Tupac Shakur']
- verifier: grounded unsupported=[]

---

## WebQTest-1000_7457bb008a1da743b19ff9ce3a5cac63 (wrong)

**Q:** Which countries included in Oceania, had a population of less than 523000?

**gold:** ['Tonga', 'Samoa', 'Northern Mariana Islands', 'Solomon Islands', 'Guam', 'New Caledonia', 'Marshall Islands', 'Vanuatu', 'Kiribati', 'Fiji', 'Cook Islands']

**answer:** The countries included in Oceania that had a population of less than 523000 were Nauru, Tuvalu, and Norfolk Island.

**entities:** ['Nauru', 'Tuvalu', 'Norfolk Island']

- plan: ['find countries included in Oceania', 'find which of #1 had a population of less than 523000']
- explored: ['location.location.contains', 'location.location.contains', 'location.statistical_region.population'] (max_score 0.557)
- eval: continue resolved=['Papua New Guinea', 'Coral Sea Islands', 'French Polynesia', 'Nauru']
- explored: ['location.statistical_region.population', 'location.location.people_born_here', 'language.human_language.countries_spoken_in', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'location.statistical_region.literacy_rate'] (max_score 0.541)
- eval: continue resolved=['Coral Sea Islands']
- explored: ['people.ethnicity.geographic_distribution', 'people.ethnicity.population', 'people.ethnicity.included_in_group', 'people.ethnicity.geographic_distribution', 'people.ethnicity.included_in_group', 'people.ethnicity.languages_spoken'] (max_score 0.217)
- eval: continue resolved=['Coral Sea Islands']
- explored: ['location.statistical_region.population', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'people.ethnicity.geographic_distribution'] (max_score 0.541)
- eval: continue resolved=['Coral Sea Islands', 'Nauru']
- verifier: grounded unsupported=[]

---

## WebQTest-1528_3c737d4a4dbf3b5acb082a4a1e43d792 (wrong)

**Q:** What Cameron Pace Group movie was Logan Lerman in?

**gold:** ['The Three Musketeers']

**answer:** Logan Lerman was in Meet Bill.

**entities:** ['Meet Bill']

- plan: ['find the movie that Logan Lerman was in', 'find the Cameron Pace Group movie among #1']
- explored: ['film.actor.film', 'film.person_or_entity_appearing_in_film.films', 'film.performance.actor', 'film.film_company.films', 'film.production_company.films', 'film.film_film_company_relationship.film_company'] (max_score 0.587)
- eval: continue resolved=['Meet Bill', 'Hoot', 'The Only Living Boy in New York', 'Riding in Cars with Boys']
- explored: ['film.film.starring', 'film.film.genre', 'film.film.country', 'film.film.starring', 'film.film.genre', 'film.film.country'] (max_score 0.298)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['film.film.film_set_decoration_by', 'film.film.music', 'film.director.film', 'film.film.soundtrack', 'film.film.soundtrack', 'film.film_film_distributor_relationship.film'] (max_score 0.278)
- eval: answer resolved=['Life of Pi']
- verifier: grounded unsupported=[]

---

## WebQTrn-1053_4c8649801d197e6eb5377d292c0b6ca8 (wrong)

**Q:** Which actor played the character Henri Ducard in Star Wars?

**gold:** ['Qui-Gon Jinn']

**answer:** Liam Neeson played Henri Ducard.

**entities:** ['Liam Neeson']

- plan: ['find the character Henri Ducard in Star Wars', 'find the actor who played #1']
- explored: ['film.film_character.portrayed_in_films', 'film.performance.character', 'fictional_universe.fictional_character.character_created_by', 'film.film.prequel', 'film.film_art_director.films_art_directed', 'film.director.film'] (max_score 0.587)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['fictional_universe.fictional_character.occupation', 'fictional_universe.fictional_character.species', 'fictional_universe.fictional_character.gender', 'film.film.film_casting_director', 'film.writer.film', 'film.cinematographer.film'] (max_score 0.25)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['fictional_universe.fictional_character_creator.fictional_characters_created', 'fictional_universe.work_of_fiction.setting', 'film.film.starring', 'film.film.film_series'] (max_score 0.194)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['film.film_series.films_in_series', 'film.film.written_by', 'film.film.costume_design_by'] (max_score 0.189)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-1012_131eaad9f6b360a7166467b5784470d4 (hedge)

**Q:** Which building in Hollywood, CA was opened on May 18, 1927, and can be visited this weekend?

**gold:** ['TCL Chinese Theatre']

**answer:** Could not be determined from the provided facts which building in Hollywood, CA was opened on May 18, 1927 and can be visited this weekend.

**entities:** []

- plan: ['find the building in Hollywood, CA that was opened on May 18, 1927', 'find which of #1 can be visited this weekend']
- explored: ['film.film_location.featured_in_films', 'film.film.featured_film_locations', 'tv.tv_program.filming_locations'] (max_score 0.257)
- eval: continue resolved=[]
- explored: ['film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film.starring', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film.release_date_s'] (max_score 0.242)
- eval: continue resolved=[]
- explored: ['film.film_location.featured_in_films', 'film.film.featured_film_locations', 'tv.tv_program.filming_locations', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'location.location.containedby'] (max_score 0.242)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film.starring', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film.release_date_s'] (max_score 0.242)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['base.popstra.hangout.business_location', 'tv.tv_location.tv_shows_filmed_here', 'film.film_regional_release_date.film_release_region', 'location.location.containedby', 'location.location.events', 'location.location.geolocation'] (max_score 0.168)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['film.director.film', 'film.writer.film', 'film.music_contributor.film', 'film.film.film_production_design_by', 'base.wfilmbase.siteid.film', 'film.film_production_designer.films_production_designed'] (max_score 0.197)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-1091_61efa0b17cc53c2187422d88bf670f22 (hedge)

**Q:** Is the religion of which Gautama Buddha is a founding figure also a type of religions are in the united states?

**gold:** ['Buddhism']

**answer:** It could not be determined from the provided facts whether Buddhism is also a type of religions in the United States.

**entities:** []

- plan: ['find the religion of which Gautama Buddha is a founding figure', 'find whether #1 is a type of religions are in the united states']
- explored: ['religion.founding_figure.religion_founded', 'religion.religion.founding_figures', 'people.person.religion', 'religion.religious_leadership_jurisdiction.leader', 'religion.religious_organization_leadership.jurisdiction', 'location.statistical_region.religions'] (max_score 0.659)
- eval: continue resolved=['Buddhism']
- explored: ['people.person.religion', 'location.religion_percentage.religion', 'religion.religion.is_part_of'] (max_score 0.579)
- eval: answer resolved=['United States of America']
- verifier: grounded unsupported=[]

---

## WebQTest-537_e5da8cda32fb1aa37028f9f7f7b1d3a8 (hedge)

**Q:** Which film was nominated for an award with the description, "Outstanding Director - Motion Picture", and Charlie Hunnam was in?

**gold:** ['Children of Men']

**answer:** Nicholas Nickleby could not be determined from the facts provided as the film nominated for an award with the description, "Outstanding Director - Motion Picture", and Charlie Hunnam was in.

**entities:** []

- plan: ['find the award with the description "Outstanding Director - Motion Picture"', 'find the film that was nominated for #1 and that Charlie Hunnam was in']
- explored: ['film.actor.film', 'film.performance.actor', 'tv.tv_actor.starring_roles'] (max_score 0.349)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['tv.tv_actor.guest_roles', 'tv.tv_guest_role.actor', 'tv.regular_tv_appearance.actor'] (max_score 0.168)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['people.person.profession', 'base.popstra.dated.participant', 'people.person.spouse_s'] (max_score 0.132)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['people.person.gender', 'people.person.education', 'base.popstra.friendship.participant'] (max_score 0.098)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-125_003c6a046c47526d922683f22cf0e983 (hedge)

**Q:** The subject of the film King: A Filmed Record... Montgomery to Memphis was shot at what location?

**gold:** ['Memphis']

**answer:** It could not be determined from the provided facts.

**entities:** []

- plan: ['find the subject of the film King: A Filmed Record... Montgomery to Memphis', 'find the location where #1 was shot']
- explored: ['film.film.subjects', 'film.producer.film', 'film.film.music'] (max_score 0.579)
- eval: continue resolved=['Martin Luther King, Jr.']
- explored: ['base.crime.crime_victim.crime_type', 'people.deceased_person.place_of_death', 'base.activism.activist.area_of_activism'] (max_score 0.361)
- eval: continue resolved=['Memphis']
- explored: ['time.event.locations', 'location.location.events', 'location.location.containedby', 'base.activism.activist.area_of_activism', 'people.person.profession', 'people.profession.people_with_this_profession'] (max_score 0.506)
- eval: answer resolved=['Memphis']
- verifier: grounded unsupported=[]

---

## WebQTest-517_e7d8b401e84db19b4965bb23aa43871d (hedge)

**Q:** Which conlang type "Engineered language" is spoken in Canada?

**gold:** ['Lojban']

**answer:** Could not be determined from the provided facts which conlang type "Engineered language" is spoken in Canada.

**entities:** []

- plan: ['find the conlang type "Engineered language" spoken in Canada']
- explored: ['language.conlang.conlang_type', 'language.conlang_purpose.languages_of_this_type', 'language.language_family.languages', 'language.human_language.countries_spoken_in', 'location.country.languages_spoken', 'location.country.official_language'] (max_score 0.428)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['language.human_language.language_family', 'base.schemastaging.context_name.pronunciation', 'language.human_language.main_country', 'food.beer.from_region', 'tv.tv_program.country_of_origin'] (max_score 0.276)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['location.statistical_region.places_imported_from', 'location.statistical_region.foreign_direct_investment_net_inflows', 'location.statistical_region.high_tech_as_percent_of_manufactured_exports'] (max_score 0.173)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['location.imports_and_exports.imported_from', 'internet.localized_uri.location', 'geography.river.origin'] (max_score 0.167)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-849_eba7931ddf28af4dfa20fb099196c91f (hedge)

**Q:** What country bordering Germany that involved in the Gulf War?

**gold:** ['France']

**answer:** Germany borders Europe, and the Gulf War involved Saudi Arabia, Israel, Kuwait, Persian Gulf, Arabian Peninsula, and Iraq. From the facts given, it could not be determined which country bordering Germany was involved in the Gulf War.

**entities:** []

- plan: ['find countries bordering Germany', 'find which of #1 were involved in the Gulf War']
- explored: ['geography.river.basin_countries', 'geography.lake.basin_countries', 'base.locations.continents.countries_within', 'film.film.country', 'film.film_regional_release_date.film', 'base.ontologies.ontology_instance_mapping.freebase_topic'] (max_score 0.562)
- eval: continue resolved=['Europe']
- explored: ['geography.river.basin_countries', 'location.location.containedby', 'location.location.partially_contained_by', 'geography.river.basin_countries', 'location.location.containedby', 'location.location.partially_contained_by'] (max_score 0.277)
- eval: continue resolved=['Germany']
- explored: ['base.locations.countries.cities_within', 'base.locations.continents.countries_within', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.countries.continent', 'location.country.languages_spoken'] (max_score 0.35)
- eval: continue resolved=['Germany']
- explored: ['base.locations.countries.cities_within', 'base.biblioness.bibs_location.country', 'location.administrative_division.country', 'base.locations.continents.countries_within', 'base.locations.countries.continent', 'location.location.geolocation'] (max_score 0.35)
- eval: continue resolved=['Germany']
- verifier: grounded unsupported=[]

---

## WebQTrn-710_e3d40457273785e46c5b71732713a5f4 (hedge)

**Q:** When is the last time the team whose mascot is called Crazy Cab win the World Series?

**gold:** ['2014 World Series']

**answer:** It could not be determined from the provided facts when the San Francisco Giants last won the World Series.

**entities:** []

- plan: ['find the team whose mascot is called Crazy Cab', 'find the last time #1 won the World Series']
- explored: ['sports.mascot.team', 'sports.sports_team.team_mascot'] (max_score 0.702)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: [] (max_score 0.0)
- eval: backtrack resolved=[]
- backtrack: dead_end
- explored: [] (max_score 0.0)
- eval: backtrack resolved=[]
- backtrack: dead_end
- explored: [] (max_score 0.0)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-1785_2fd3a482f02db22067954809fe7b222b (hedge)

**Q:** What Kim Richards films have film netflix_id numbers lower than 70037542?

**gold:** ['No Deposit, No Return', 'Escape to Witch Mountain', 'Tuff Turf', 'Raid on Entebbe', 'Return from Witch Mountain']

**answer:** Could not be determined from the facts provided which of Kim Richards's films have film netflix_id numbers lower than 70037542, because no film netflix_id numbers are given for the films listed.

**entities:** []

- plan: ['find films featuring Kim Richards', 'find which of #1 have netflix_id numbers lower than 70037542']
- explored: ['film.actor.film', 'film.performance.actor', 'tv.tv_actor.starring_roles'] (max_score 0.619)
- eval: continue resolved=['Race to Witch Mountain', 'No Deposit, No Return', 'Black Snake Moan', 'Escape to Witch Mountain']
- explored: ['media_common.netflix_title.netflix_genres', 'film.film.featured_film_locations', 'film.film.starring', 'media_common.netflix_title.netflix_genres', 'film.film.starring', 'film.film_regional_release_date.film'] (max_score 0.326)
- eval: continue resolved=[]
- explored: ['media_common.netflix_genre.titles', 'media_common.netflix_title.netflix_genres', 'media_common.netflix_title.netflix_genres', 'media_common.netflix_title.netflix_genres', 'media_common.netflix_title.netflix_genres', 'media_common.netflix_title.netflix_genres'] (max_score 0.318)
- eval: continue resolved=[]
- explored: ['media_common.netflix_genre.titles', 'media_common.netflix_title.netflix_genres', 'tv.tv_genre.programs', 'media_common.netflix_title.netflix_genres', 'film.film.genre', 'film.film.rating'] (max_score 0.318)
- eval: continue resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-14_f56f0b81a5d0fd41e793f70c0b468455 (hedge)

**Q:** Where is the location of the film, "The Emperor's New Clothes" takes place, on a map?

**gold:** ['Italy', 'Lazio', 'Province of Rome']

**answer:** It could not be determined from the provided facts where The Emperor's New Clothes takes place on a map.

**entities:** []

- plan: ['find the film "The Emperor\'s New Clothes"', 'find the location where #1 takes place']
- explored: ['film.film.costume_design_by', 'film.film_costumer_designer.costume_design_for_film', 'film.director.film'] (max_score 0.358)
- eval: continue resolved=["The Emperor's New Clothes"]
- explored: ['people.person.places_lived', 'people.place_lived.person', 'people.person.sibling_s', 'people.person.place_of_birth', 'film.film.film_production_design_by', 'people.person.gender'] (max_score 0.205)
- eval: continue resolved=['New York City']
- explored: ['location.location.geolocation', 'location.location.partially_contained_by', 'location.location.containedby', 'location.location.partially_contained_by', 'location.location.containedby', 'location.location.containedby'] (max_score 0.656)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['people.person.places_lived', 'people.place_lived.person', 'people.person.sibling_s', 'people.person.place_of_birth', 'film.film.film_production_design_by', 'people.person.gender'] (max_score 0.205)
- eval: continue resolved=['New York City']
- explored: ['location.location.containedby', 'location.location.contains', 'location.location.partially_contains', 'location.location.contains', 'location.location.partially_contains', 'location.location.partially_contains'] (max_score 0.463)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['people.person.places_lived', 'people.place_lived.person', 'people.person.sibling_s', 'people.person.place_of_birth', 'film.film.film_production_design_by', 'people.person.gender'] (max_score 0.205)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['film.film.directed_by', 'people.sibling_relationship.sibling', 'film.director.film', 'award.award_nominee.award_nominations', 'film.film.costume_design_by', 'people.person.profession'] (max_score 0.073)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-1923_a64ef0f5ce397a5e1ef6fcd550ebfcfb (hedge)

**Q:** What movies has Miley Cyrus been in with music by Aaron Zigman?

**gold:** ['Sex and the City 2', 'The Last Song']

**answer:** Miley Cyrus has been in The Last Song, So Undercover, Hannah Montana: The Movie, Radio Disney Party Jams: The Concert, Bolt, Wizards on Deck with Hannah Montana, The World According to Miley Cyrus, and LOL. However, from the facts provided, it could not be determined which of these had music by Aaron Zigman.

**entities:** []

- plan: ['find movies that feature Miley Cyrus', 'find which of #1 have music by Aaron Zigman']
- explored: ['film.actor.film', 'film.person_or_entity_appearing_in_film.films', 'film.performance.actor', 'film.film.music', 'film.music_contributor.film', 'music.artist.track_contributions'] (max_score 0.548)
- eval: continue resolved=['The Last Song', 'So Undercover', 'Hannah Montana: The Movie', 'Radio Disney Party Jams: The Concert']
- explored: ['film.film.music', 'music.track_contribution.track', 'film.film.soundtrack', 'film.film.music', 'film.music_contributor.film', 'film.film_crew_gig.film'] (max_score 0.541)
- eval: answer resolved=['The Last Song']
- verifier: grounded unsupported=[]

---

## WebQTest-576_99c43635b648023af901dc341b3bab6e (hedge)

**Q:** In which of the seven countries making up Central America are there fewer than 1100 people in the country's army?

**gold:** ['Belize']

**answer:** Could not be determined from the provided facts which of Belize, Guatemala, Panama, Costa Rica, El Salvador, and Honduras have fewer than 1100 people in the country's army.

**entities:** []

- plan: ['find the seven countries making up Central America', "find which of #1 have fewer than 1100 people in the country's army"]
- explored: ['location.location.contains', 'organization.organization.geographic_scope', 'location.location.geolocation', 'film.film.country', 'film.film_regional_release_date.film', 'music.genre.subgenre'] (max_score 0.432)
- eval: continue resolved=['Belize', 'Guatemala', 'Panama', 'Costa Rica']
- explored: ['base.locations.continents.countries_within', 'base.locations.countries.continent', 'location.country.form_of_government', 'base.locations.continents.countries_within', 'base.locations.countries.continent', 'location.country.form_of_government'] (max_score 0.616)
- eval: continue resolved=['Belize', 'Guatemala', 'Panama', 'Costa Rica']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.continents.states_provinces_within', 'location.country.form_of_government', 'base.schemastaging.context_name.pronunciation', 'base.ontologies.ontology_instance_mapping.freebase_topic'] (max_score 0.379)
- eval: continue resolved=['Belize', 'Guatemala', 'Panama', 'Costa Rica']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.country.form_of_government', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.country.form_of_government'] (max_score 0.649)
- eval: continue resolved=['Belize', 'Guatemala', 'Panama', 'Costa Rica']
- verifier: grounded unsupported=[]

---

## WebQTrn-567_724a3b769671b1ea52a76af3a90687f4 (hedge)

**Q:** What movie was decorated by Antonio Mateos and made by Ron Howard?

**gold:** ['The Spikes Gang']

**answer:** Patton was decorated by Antonio Mateos and made by Ron Howard could not be determined from the facts provided.

**entities:** []

- plan: ['find the movie decorated by Antonio Mateos', 'find the movie made by Ron Howard', 'find the movie that satisfies both #1 and #2']
- explored: ['film.film.film_set_decoration_by', 'film.film_set_designer.film_sets_designed', 'award.award_honor.award_winner', 'film.film.directed_by', 'film.film.story_by', 'film.actor.film'] (max_score 0.656)
- eval: continue resolved=['Patton', 'The Spikes Gang', 'Custer of the West', 'Krakatoa, East of Java']
- explored: ['film.film.directed_by', 'film.film.starring', 'film.film.story_by', 'film.film.directed_by', 'film.film.starring', 'film.film.story_by'] (max_score 0.659)
- eval: continue resolved=['Cocoon', 'Frost/Nixon', 'Parenthood', 'Willow']
- explored: ['film.film.sequel', 'film.film.film_series', 'film.film.genre', 'film.film.genre', 'film.film.featured_film_locations', 'film.film.starring'] (max_score 0.34)
- eval: continue resolved=['Patton', 'The Spikes Gang', 'Custer of the West', 'Krakatoa, East of Java']
- explored: ['film.film.sequel', 'film.film.film_series', 'film.film.genre', 'film.film.film_series', 'film.film.genre', 'film.film.genre'] (max_score 0.34)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-576_495085ad9dd6274cce483df63474ca21 (hedge)

**Q:** Of the 7 countries in Central America, which has an ISO smaller than 188?

**gold:** ['Belize']

**answer:** It could not be determined from the provided facts which of Belize, Guatemala, Panama, Costa Rica, El Salvador, Honduras, or Nicaragua has an ISO smaller than 188, because no ISO values are given.

**entities:** []

- plan: ['find the 7 countries in Central America', 'find which of #1 have an ISO smaller than 188']
- explored: ['location.location.contains', 'location.location.contains', 'location.location.containedby', 'film.film.country', 'film.film_regional_release_date.film', 'broadcast.radio_station.format'] (max_score 0.478)
- eval: continue resolved=['Belize', 'Guatemala', 'Panama', 'Costa Rica']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.country.capital', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.country.capital'] (max_score 0.654)
- eval: continue resolved=['Belize', 'Guatemala', 'Panama', 'Costa Rica']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.continents.states_provinces_within', 'location.country.capital', 'base.biblioness.bibs_location.country', 'location.statistical_region.population'] (max_score 0.654)
- eval: continue resolved=['Belize', 'Guatemala', 'Panama', 'Costa Rica']
- explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.country.capital', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.country.capital'] (max_score 0.399)
- eval: continue resolved=['Belize', 'Guatemala', 'Panama', 'Costa Rica']
- verifier: grounded unsupported=[]

---

## WebQTrn-3249_0b9c49912f43238136954d463b417194 (hedge)

**Q:** Which program featuring Tamera Mowry has the largest "tvrage_id?"?

**gold:** ['Roommates']

**answer:** Tia & Tamera is the program featuring Tamera Mowry that can be identified from the facts, but the largest tvrage_id could not be determined because no tvrage_id values are provided.

**entities:** []

- plan: ['find programs featuring Tamera Mowry', 'find the program in #1 with the largest tvrage_id']
- explored: ['film.actor.film', 'film.performance.actor', 'tv.tv_personality.tv_regular_appearances'] (max_score 0.423)
- eval: continue resolved=['Tia & Tamera']
- explored: ['tv.tv_program.country_of_origin', 'tv.tv_program.languages', 'tv.tv_program.seasons'] (max_score 0.268)
- eval: continue resolved=['Tia & Tamera']
- explored: ['tv.tv_program.country_of_origin', 'tv.tv_network.areas_served', 'tv.tv_program.filming_locations', 'tv.tv_program.country_of_origin', 'tv.tv_program.languages', 'broadcast.tv_channel.language'] (max_score 0.268)
- eval: continue resolved=['Tia & Tamera']
- explored: ['tv.tv_program.program_creator', 'tv.tv_program.country_of_origin', 'tv.tv_program.languages', 'tv.tv_program.country_of_origin', 'tv.tv_program.languages', 'tv.tv_program.original_network'] (max_score 0.275)
- eval: continue resolved=['Tia & Tamera']
- verifier: grounded unsupported=[]

---

## WebQTest-1528_ac9d054b50d6d55401844da4807076b2 (hedge)

**Q:** Which movie did Logan Lerman act in, that was directed by Guy Barnes?

**gold:** ['My One and Only']

**answer:** Could not be determined from the provided facts. Logan Lerman is listed for several films, but no fact links any of those films to Guy Barnes as director.

**entities:** []

- plan: ['find the movie that was directed by Guy Barnes', 'find the movie from #1 that Logan Lerman acted in']
- explored: ['film.film_art_director.films_art_directed', 'film.film.film_art_direction_by', 'film.film.film_production_design_by', 'film.actor.film', 'tv.tv_actor.starring_roles', 'film.personal_film_appearance.person'] (max_score 0.537)
- eval: continue resolved=['Outlaw Country', 'In the Line of Duty: The F.B.I. Murders', 'American Harvest', 'The Missing']
- explored: ['film.film.country', 'film.film.starring', 'film.writer.film', 'film.film.country', 'film.film.starring', 'film.film.directed_by'] (max_score 0.319)
- eval: continue resolved=['The Patriot']
- explored: ['film.film.country', 'film.film.featured_film_locations', 'film.film_location.featured_in_films', 'film.film.country', 'film.film.featured_film_locations', 'film.film_location.featured_in_films'] (max_score 0.319)
- eval: answer resolved=['The Patriot']
- verifier: grounded unsupported=[]

---

## WebQTest-1923_a90c08a839ac4d0ac22ebbf436bb578b (hedge)

**Q:** What movie featuring Miley Cyrus was directed by Tom Vaughan?

**gold:** ['So Undercover']

**answer:** The movie featuring Miley Cyrus that was directed by Tom Vaughan could not be determined from the facts provided.

**entities:** []

- plan: ['find the movie featuring Miley Cyrus', 'find the movie from #1 that was directed by Tom Vaughan']
- explored: ['film.actor.film', 'film.music_contributor.film', 'film.person_or_entity_appearing_in_film.films', 'film.film.directed_by', 'film.director.film', 'tv.tv_director.episodes_directed'] (max_score 0.565)
- eval: continue resolved=['Hannah Montana and Miley Cyrus: Best of Both Worlds Concert', 'High School Musical 2', 'The Last Song', 'Sex and the City 2']
- explored: ['film.film.featured_song', 'film.film.starring', 'film.film_featured_song.featured_in_film', 'film.film.starring', 'music.soundtrack.film', 'film.film.soundtrack'] (max_score 0.34)
- eval: continue resolved=['The Last Song']
- explored: ['film.film.music', 'film.music_contributor.film', 'music.artist.track', 'music.artist.track', 'music.track_contribution.track', 'music.recording.song'] (max_score 0.285)
- eval: answer resolved=['The Last Song']
- verifier: grounded unsupported=[]

---

## WebQTrn-1294_a4b2006ad5ffa1964eb8aa93149cba5a (hedge)

**Q:** Which actor who portrayed Vito Corleone also played in Joy?

**gold:** ['Robert De Niro']

**answer:** The answer could not be verified against the knowledge graph.

**entities:** []

- plan: ['find the actor who portrayed Vito Corleone', 'find which of #1 also played in Joy']
- explored: ['film.film_character.portrayed_in_films', 'film.performance.character', 'tv.regular_tv_appearance.character', 'film.film_character.portrayed_in_films', 'film.performance.character', 'tv.regular_tv_appearance.character'] (max_score 0.618)
- eval: continue resolved=['Marlon Brando', 'Robert De Niro', 'Oreste Baldini']
- explored: ['film.actor.dubbing_performances', 'film.dubbing_performance.actor', 'film.actor.film', 'film.actor.film', 'film.performance.actor', 'tv.tv_actor.starring_roles'] (max_score 0.545)
- eval: answer resolved=['Robert De Niro']
- verifier: unsupported unsupported=['Marlon Brando also played in Joy']
- explored: ['film.actor.film', 'film.performance.actor', 'film.person_or_entity_appearing_in_film.films'] (max_score 0.581)
- eval: continue resolved=[]
- explored: ['film.film_character.portrayed_in_films', 'film.performance.character', 'theater.theater_role.role', 'film.film.film_casting_director', 'film.film.starring', 'film.director.film'] (max_score 0.296)
- eval: backtrack resolved=[]
- verifier: unsupported unsupported=['Marlon Brando also played in Joy']

---

## WebQTrn-1677_2fe630fbb46b32aa9774a9417e843503 (hedge)

**Q:** Which John Chichester movie starred Adam Sandler?

**gold:** ['The House Bunny']

**answer:** It could not be determined from the provided facts which John Chichester movie starred Adam Sandler.

**entities:** []

- plan: ['find the movie by John Chichester that starred Adam Sandler']
- explored: ['film.actor.film', 'film.performance.actor', 'film.person_or_entity_appearing_in_film.films', 'film.film_crewmember.films_crewed', 'film.film_art_director.films_art_directed', 'film.film.film_art_direction_by'] (max_score 0.58)
- eval: continue resolved=['Dirty Work', 'Click', 'Men, Women & Children', 'Just Go With It']
- explored: ['film.film.starring', 'film.film.directed_by', 'film.director.film', 'film.film.directed_by', 'film.director.film', 'film.film_casting_director.films_casting_directed'] (max_score 0.6)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['film.film_casting_director.films_casting_directed', 'film.writer.film', 'film.film.film_casting_director', 'film.writer.film', 'film.film.film_casting_director', 'film.cinematographer.film'] (max_score 0.284)
- eval: backtrack resolved=[]
- backtrack: evaluator
- explored: ['film.cinematographer.film', 'film.film.written_by', 'film.music_contributor.film', 'film.film.written_by', 'film.music_contributor.film', 'film.film.story_by'] (max_score 0.272)
- eval: continue resolved=['Adam Sandler']
- explored: ['film.film.directed_by', 'film.director.film', 'film.actor.film', 'film.actor.film', 'film.writer.film', 'film.film.written_by'] (max_score 0.329)
- eval: continue resolved=['The Longest Yard']
- explored: ['film.film.prequel', 'film.film.directed_by', 'film.film.starring', 'film.film.directed_by', 'film.film.starring', 'film.director.film'] (max_score 0.346)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTest-1012_872253e47dd6ddaa213ff31eeda8783b (hedge)

**Q:** What is there to do in Hollywood, California in the Eastern Time Zone?

**gold:** ['Universal Studios Hollywood']

**answer:** It could not be determined from the provided facts what there is to do in Hollywood, California in the Eastern Time Zone. The facts only identify Hollywood as being in California and in the Greater Los Angeles Area, but they do not provide activities for Hollywood, California, and the Eastern Time Zone facts do not connect to Hollywood, California.

**entities:** []

- plan: ['find Hollywood, California', 'find things to do in #1', 'find which of #2 are in the Eastern Time Zone']
- explored: ['location.neighborhood.neighborhood_of', 'location.neighborhood.neighborhood_of', 'base.biblioness.bibs_location.state', 'location.location.time_zones', 'base.schemastaging.phone_open_times.time_zone', 'base.schemastaging.context_name.pronunciation'] (max_score 0.494)
- eval: continue resolved=['Hollywood']
- explored: ['location.location.events', 'travel.travel_destination.tourist_attractions', 'location.place_with_neighborhoods.neighborhoods', 'location.location.events', 'travel.travel_destination.tourist_attractions', 'location.place_with_neighborhoods.neighborhoods'] (max_score 0.484)
- eval: continue resolved=['Memphis', 'Portland']
- explored: ['location.location.events', 'base.marchmadness.ncaa_basketball_tournament_stage.games', 'location.location.events', 'location.location.events', 'time.event.locations', 'base.marchmadness.ncaa_basketball_tournament_stage.games'] (max_score 0.199)
- eval: continue resolved=['Memphis Zoo', 'Memphis Brooks Museum of Art', 'Memphis Botanic Garden', 'Graceland']
- explored: ['zoos.zoo_category.zoos', 'travel.travel_destination.tourist_attractions', 'location.location.geolocation', 'film.film.featured_film_locations', 'protected_sites.natural_or_cultural_site_listing.listed_site', 'travel.travel_destination.tourist_attractions'] (max_score 0.349)
- eval: backtrack resolved=[]
- verifier: grounded unsupported=[]

---

## WebQTrn-2871_98925752e1e60abb73dc775f15ee38af (hedge)

**Q:** What is near the Grand Canyon and is where a Wide Receiver Football player was born?

**gold:** ['Phoenix']

**answer:** Grand Canyon National Park Airport is near the Grand Canyon. However, from the facts provided, it could not be determined which Wide Receiver Football player was born there.

**entities:** []

- plan: ['find what is near the Grand Canyon', 'find the birthplace of a Wide Receiver Football player', 'find which of #1 is the same as #2']
- explored: ['location.location.contains', 'location.location.nearby_airports', 'location.location.contains', 'sports.sport.positions', 'american_football.football_player.position_s', 'sports.sports_position.sport'] (max_score 0.484)
- eval: continue resolved=['Grand Canyon Depot', 'Grand Canyon Water Reclamation Plant', "Buckey O'Neill Cabin", 'North Rim, Arizona']
- explored: ['location.location.street_address', 'location.location.contains', 'location.location.geolocation', 'location.location.contains', 'location.location.geolocation', 'location.location.containedby'] (max_score 0.199)
- eval: continue resolved=[]
- explored: ['people.person.place_of_birth', 'sports.sports_team.location', 'sports.sports_team_location.teams', 'location.location.contains', 'location.location.contains', 'location.location.geolocation'] (max_score 0.499)
- eval: continue resolved=['J. J. Nelson', 'Johnny Rodgers', 'Leo Lewis', 'Josh Cribbs']
- explored: ['people.person.place_of_birth', 'sports.pro_sports_played.athlete', 'sports.pro_athlete.sports_played_professionally', 'people.person.place_of_birth', 'people.person.nationality', 'book.written_work.author'] (max_score 0.499)
- eval: continue resolved=['J. J. Nelson', 'Johnny Rodgers', 'Leo Lewis', 'Josh Cribbs']
- verifier: grounded unsupported=[]

---

