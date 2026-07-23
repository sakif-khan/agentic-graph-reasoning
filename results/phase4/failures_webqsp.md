## WebQTest-86 (wrong)

**Q:** which country does greenland belong to

**gold:** ['Denmark']

**answer:** Greenland belongs to Kingdom of Denmark.

**entities:** ['Kingdom of Denmark']

plan: ['find the country that Greenland belongs to']

explored: ['location.location.containedby', 'location.location.containedby', 'location.country.capital'] (score max 0.514)

verifier: grounded

---

## WebQTest-783 (wrong)

**Q:** what county is houston tx in

**gold:** ['Montgomery County']

**answer:** Houston is in Harris County.

**entities:** ['Harris County']

plan: ['find Houston, TX', 'find the county of #1']

explored: ['location.neighborhood.neighborhood_of', 'location.location.nearby_airports', 'location.location.geolocation'] (score max 0.263)

explored: ['location.location.containedby', 'location.place_with_neighborhoods.neighborhoods', 'location.location.geolocation', 'location.location.containedby', 'location.place_with_neighborhoods.neighborhoods', 'location.neighborhood.neighborhood_of', 'location.location.containedby', 'location.place_with_neighborhoods.neighborhoods', 'location.neighborhood.neighborhood_of', 'location.location.containedby', 'location.place_with_neighborhoods.neighborhoods', 'location.location.geolocation', 'location.location.containedby', 'location.location.contains', 'location.statistical_region.population'] (score max 0.503)

verifier: grounded

---

## WebQTest-118 (wrong)

**Q:** who fought in the gulf war 1991

**gold:** ['France', 'Australia', 'United States of America', 'Argentina', 'Iraq', 'United Kingdom', 'Saudi Arabia']

**answer:** Israel fought in the Gulf War 1991.

**entities:** ['Israel']

plan: ['find the Gulf War in 1991', 'find who fought in #1']

explored: ['time.event.locations', 'location.location.events', 'military.casualties.military_conflict'] (score max 0.394)

explored: ['military.military_combatant_group.combatants', 'military.military_combatant.military_conflicts', 'military.military_combatant.casualties', 'military.military_combatant_group.combatants', 'military.military_combatant.military_conflicts', 'location.location.contains', 'military.military_combatant_group.combatants', 'military.military_combatant.military_conflicts', 'location.statistical_region.size_of_armed_forces', 'location.location.contains', 'location.location.contains', 'location.location.containedby', 'time.event.locations', 'location.location.events', 'event.disaster.areas_affected'] (score max 0.615)

verifier: grounded

---

## WebQTest-1674 (wrong)

**Q:** who is the leader of north korea today

**gold:** ['Kim Jong-un']

**answer:** Kim Il-sung

**entities:** ['Kim Il-sung']

plan: ['find the leader of North Korea today']

explored: ['military.military_command.military_combatant', 'military.military_combatant.military_commanders', 'location.country.national_anthem'] (score max 0.189)

explored: ['military.military_command.military_commander', 'military.military_commander.military_commands', 'military.military_person.participated_in_conflicts', 'military.military_command.military_commander', 'military.military_commander.military_commands', 'military.military_person.participated_in_conflicts', 'military.military_command.military_commander', 'military.military_commander.military_commands', 'people.person.gender', 'military.military_conflict.commanders', 'military.military_person.participated_in_conflicts', 'military.military_command.military_conflict', 'government.national_anthem_of_a_country.anthem', 'government.national_anthem.national_anthem_of', 'music.composition.lyricist'] (score max 0.286)

explored: ['military.military_combatant.military_commanders', 'military.military_command.military_combatant', 'location.country.national_anthem', 'military.military_conflict.commanders', 'military.military_person.participated_in_conflicts', 'military.military_command.military_conflict', 'military.military_conflict.commanders', 'military.military_person.participated_in_conflicts', 'military.military_command.military_conflict', 'military.military_conflict.commanders', 'military.military_command.military_conflict', 'military.military_conflict.combatants', 'military.military_conflict.commanders', 'military.military_command.military_conflict', 'military.military_conflict.combatants'] (score max 0.388)

backtrack: evaluator

explored: ['location.administrative_division.country', 'government.national_anthem_of_a_country.country', 'location.country.form_of_government', 'military.military_conflict.combatants', 'military.military_conflict.military_personnel_involved', 'event.speech_topic.speeches_or_presentations_on_this_topic', 'military.military_conflict.combatants', 'military.military_conflict.casualties', 'military.casualties.military_conflict', 'military.military_combatant_group.conflict', 'location.location.events', 'time.event.locations', 'military.military_combatant_group.conflict', 'location.location.events', 'time.event.locations'] (score max 0.168)

backtrack: evaluator

explored: ['organization.organization_member.member_of', 'language.human_language.main_country', 'location.country.administrative_divisions', 'military.military_conflict.force_strengths', 'event.speech_or_presentation.speech_topic', 'base.argumentmaps.motivated_event.motive', 'military.military_combatant_group.conflict', 'location.location.events', 'time.event.locations', 'base.culturalevent.event.entity_involved', 'time.event.included_in_event', 'time.event.includes_event', 'base.culturalevent.event.entity_involved', 'time.event.included_in_event', 'time.event.includes_event'] (score max 0.148)

backtrack: evaluator

explored: ['language.human_language.countries_spoken_in', 'location.country.first_level_divisions', 'location.country.official_language', 'military.force_strength.military_conflict', 'base.argumentmaps.motivation.motivated_event', 'military.military_combatant_group.conflict', 'media_common.quotation_subject.quotations_about_this_subject', 'base.culturalevent.event.entity_involved', 'media_common.quotation.subjects', 'base.schemastaging.context_name.pronunciation'] (score max 0.131)

verifier: grounded

---

## WebQTest-1330 (wrong)

**Q:** what is the most populated state in united states

**gold:** ['New York']

**answer:** California is the most populated state in the United States.

**entities:** ['California']

plan: ['find the United States', 'find the most populated state in #1']

explored: ['base.locations.countries.continent', 'base.locations.countries.planet', 'location.country.form_of_government'] (score max 0.305)

explored: ['base.locations.states_and_provences.continent', 'base.locations.continents.states_provinces_within', 'base.locations.countries.continent', 'location.country.form_of_government', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.form_of_government.countries', 'base.schemastaging.context_name.pronunciation', 'location.country.form_of_government', 'government.form_of_government.countries', 'base.ontologies.ontology_instance_mapping.freebase_topic', 'location.location.events', 'base.conservationaction.documented_priority_species.location', 'base.locations.countries.planet'] (score max 0.554)

explored: ['base.locations.states_and_provences.country', 'location.statistical_region.religions', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'location.statistical_region.religions', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'location.statistical_region.religions', 'location.us_state.capital', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.literacy_rate', 'location.statistical_region.poverty_rate_2dollars_per_day', 'location.location.contains', 'people.ethnicity.geographic_distribution', 'location.country.form_of_government'] (score max 0.311)

explored: ['base.locations.states_and_provences.country', 'base.locations.countries.states_provinces_within', 'location.statistical_region.religions', 'location.religion_percentage.religion', 'religion.religion.places_of_worship', 'religion.place_of_worship.religion', 'location.religion_percentage.religion', 'religion.religion.places_of_worship', 'religion.place_of_worship.religion', 'location.religion_percentage.religion', 'people.person.religion', 'location.religion_percentage.religion', 'religion.religion.number_of_adherents', 'religion.religion.founding_figures'] (score max 0.59)

verifier: grounded

---

## WebQTest-59 (wrong)

**Q:** when did annie open

**gold:** ['1976-08-10']

**answer:** Annie opened in New York City and Los Angeles, with regional release information also pointing to the United States of America.

**entities:** ['New York City', 'Los Angeles', 'United States of America']

plan: ['find the opening date of Annie']

explored: ['film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.story_by'] (score max 0.529)

explored: ['film.film_regional_release_date.film_regional_debut_venue', 'film.film_regional_release_date.film_release_region', 'time.event.locations', 'film.film_regional_release_date.film_regional_debut_venue', 'film.film_regional_release_date.film_release_region', 'time.event.locations', 'film.film_regional_release_date.film_release_region', 'time.event.locations', 'base.datedlocationtest.dated_location_test.preceded_by', 'film.film.story_by', 'film.film_story_contributor.film_story_credits', 'people.person.gender', 'film.film.story_by', 'award.award_honor.award_winner', 'film.film.written_by'] (score max 0.451)

explored: ['film.film.release_date_s', 'film.film.story_by', 'film.film_regional_release_date.film', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.starring', 'film.film.release_date_s', 'film.film.story_by', 'film.film_regional_release_date.film', 'time.event.locations', 'base.datedlocationtest.dated_location_test.preceded_by', 'base.datedlocationtest.dated_location_test.joined_by', 'film.film_regional_release_date.film_regional_debut_venue', 'film.film_regional_release_date.film_release_distribution_medium', 'film.film_film_distributor_relationship.film_distribution_medium'] (score max 0.244)

verifier: grounded

---

## WebQTest-665 (wrong)

**Q:** what government does new zealand have

**gold:** ['Parliamentary system', 'Unitary state', 'Constitutional monarchy']

**answer:** Government of New Zealand

**entities:** ['Government of New Zealand']

plan: ['find the government of New Zealand']

explored: ['government.government_agency.government', 'government.government.agency', 'government.governmental_jurisdiction.government'] (score max 0.638)

verifier: grounded

---

## WebQTest-1555 (wrong)

**Q:** what is the parliament of nepal called

**gold:** ['Parliament of Nepal']

**answer:** The Parliament of Nepal is composed of the National Assembly and the House of Representatives.

**entities:** ['National Assembly', 'House of Representatives']

plan: ['find the parliament of Nepal']

explored: ['government.governmental_jurisdiction.government_bodies', 'government.governmental_body.body_this_is_a_component_of', 'government.governmental_body.component_bodies'] (score max 0.219)

verifier: grounded

---

## WebQTest-1416 (wrong)

**Q:** what was franklin pierce famous for

**gold:** ['US President']

**answer:** Franklin Pierce was famous for being the president in Franklin Pierce 1853 presidential inauguration and for his participation in the Mexican–American War, including the Battle of Molino del Rey, Battle of Churubusco, Battle of Chapultepec, Battle for Mexico City, and Battle of Contreras.

**entities:** ['Franklin Pierce 1853 presidential inauguration', 'Mexican–American War', 'Battle of Molino del Rey', 'Battle of Churubusco', 'Battle of Chapultepec', 'Battle for Mexico City', 'Battle of Contreras']

plan: ['find what Franklin Pierce was famous for']

explored: ['military.military_person.participated_in_conflicts', 'base.inaugurations.inauguration.president', 'media_common.quotation.author'] (score max 0.377)

verifier: grounded

---

## WebQTest-1003 (wrong)

**Q:** who was the prime minister of pakistan in 1999

**gold:** ['Nawaz Sharif', 'Moeenuddin Ahmad Qureshi']

**answer:** Muhammad Mian Soomro was the prime minister of Pakistan in 1999.

**entities:** ['Muhammad Mian Soomro']

plan: ['find the prime minister of Pakistan in 1999']

explored: ['government.government_position_held.office_position_or_title', 'government.government_office_or_title.office_holders', 'government.government_office_or_title.category'] (score max 0.398)

explored: ['government.politician.government_positions_held', 'government.government_position_held.office_holder', 'people.person.nationality', 'government.politician.government_positions_held', 'government.government_position_held.office_holder', 'people.person.nationality', 'cricket.cricket_team.country', 'location.country.form_of_government', 'government.form_of_government.countries', 'government.government_position_held.basic_title', 'government.government_office_or_title.category', 'base.ontologies.ontology_instance_mapping.freebase_topic'] (score max 0.439)

verifier: grounded

---

## WebQTest-701 (wrong)

**Q:** what team is reggie bush on 2011

**gold:** ['Miami Dolphins', 'New Orleans Saints']

**answer:** Reggie Bush was on the Detroit Lions in 2011.

**entities:** ['Detroit Lions']

plan: ['find the team Reggie Bush was on in 2011']

explored: ['sports.sports_team_roster.player', 'sports.pro_athlete.teams', 'american_football.football_player.position_s'] (score max 0.588)

verifier: grounded

---

## WebQTest-704 (wrong)

**Q:** who is thor heyerdahl

**gold:** ['Ethnographer', 'Film director', 'Scientist', 'Film Producer', 'Cinematographer', 'Adventurer']

**answer:** Thor Heyerdahl was a Film director, Cinematographer, Scientist, Ethnographer, Film Producer, and Adventurer. He was also the author of works including Kon-Tiki: Across the Pacific in a Raft, Fatu Hiva, and Aku Aku.

**entities:** ['Thor Heyerdahl']

plan: ['find who Thor Heyerdahl is']

explored: ['people.person.profession', 'book.written_work.author', 'book.written_work.author'] (score max 0.38)

verifier: grounded

---

## WebQTest-301 (wrong)

**Q:** what were amelia earhart 's achievements

**gold:** ['Pilot', 'Writer']

**answer:** Amelia Earhart was inducted into the National Women's Hall of Fame.

**entities:** ["National Women's Hall of Fame"]

plan: ['find achievements of Amelia Earhart']

explored: ['award.award_nomination.nominated_for', 'award.hall_of_fame_inductee.hall_of_fame_inductions', 'award.hall_of_fame_induction.inductee'] (score max 0.454)

explored: ['award.hall_of_fame_induction.hall_of_fame'] (score max 0.364)

verifier: grounded

---

## WebQTest-316 (wrong)

**Q:** what did shakespeare become famous for

**gold:** ['Author', 'Actor', 'Playwright', 'Lyricist', 'Poet']

**answer:** William Shakespeare became famous for writing plays such as Macbeth, Antony and Cleopatra, A Midsummer Night's Dream, Romeo and Juliet, The Taming of the Shrew, The Comedy of Errors, Titus Andronicus, and The Two Gentlemen of Verona.

**entities:** ['William Shakespeare']

plan: ['find what Shakespeare became famous for']

explored: ['theater.play.lyricist', 'theater.theatrical_lyricist.play_lyrics_written', 'music.composition.lyricist'] (score max 0.551)

explored: ['theater.theater_role.play', 'theater.play.lyricist', 'theater.play.characters', 'theater.theater_role.play', 'theater.play.lyricist', 'theater.play.genre', 'theater.theater_role.play', 'theater.play.lyricist', 'theater.play.genre', 'theater.theater_character.portrayed_by', 'theater.play.lyricist', 'theater.theater_role.role', 'theater.play.lyricist', 'theater.play.genre', 'theater.play.characters'] (score max 0.253)

explored: ['theater.theater_role.actor', 'theater.theater_actor.theater_roles', 'media_common.quotation.author', 'theater.theater_character.portrayed_by', 'theater.theater_role.role', 'theater.play.characters', 'theater.theater_character.portrayed_by', 'theater.theater_role.role', 'theater.play.characters', 'theater.theater_character.portrayed_by', 'theater.theater_role.role', 'theater.play.characters', 'theater.theater_character.portrayed_by', 'theater.theater_role.role', 'theater.play.characters'] (score max 0.26)

explored: ['theater.theater_role.play', 'theater.theater_production.cast', 'theater.theater_role.play', 'theater.theater_production.cast', 'book.author.works_written', 'theater.theater_role.play', 'theater.theater_production.cast', 'theater.theater_director.plays_directed', 'theater.theater_role.play', 'theater.play.lyricist', 'theater.play.genre', 'theater.theater_role.play', 'theater.play.lyricist', 'theater.play.genre'] (score max 0.253)

verifier: grounded

---

## WebQTest-1937 (wrong)

**Q:** who is captain james cook facts

**gold:** ['Explorer', 'Sailor']

**answer:** Captain James Cook was a person who served in the Royal Navy and had nationality in the Kingdom of Great Britain and the United Kingdom.

**entities:** ['James Cook']

plan: ['find facts about Captain James Cook']

explored: ['military.military_service.military_person', 'military.military_person.service', 'people.person.nationality'] (score max 0.415)

explored: ['military.military_combatant.military_commanders', 'base.schemastaging.military_person_extra.allegiance', 'military.casualties.combatant', 'military.military_combatant.military_commanders', 'dining.cuisine.region_of_origin', 'book.written_work.subjects', 'book.author.works_written', 'book.written_work.subjects', 'book.book_subject.works'] (score max 0.403)

explored: ['book.author.works_written', 'military.military_command.military_commander', 'military.military_service.military_person', 'military.military_conflict.commanders', 'military.military_person.participated_in_conflicts', 'base.americancivilwar.campaign.battle', 'military.military_conflict.commanders', 'military.military_person.participated_in_conflicts', 'military.military_command.military_conflict', 'military.military_conflict.commanders', 'military.military_person.participated_in_conflicts', 'military.military_command.military_conflict', 'military.military_command.military_commander', 'military.military_commander.military_commands', 'people.person.nationality'] (score max 0.185)

explored: ['book.author.works_written', 'book.author.works_written', 'fictional_universe.person_in_fiction.representations_in_fiction', 'military.military_command.military_commander', 'military.military_command.military_commander', 'military.military_commander.military_commands', 'military.military_person.participated_in_conflicts', 'military.military_combatant.military_commanders', 'military.military_command.military_combatant', 'royalty.kingdom.rulers', 'military.military_combatant.military_commanders', 'base.schemastaging.military_person_extra.allegiance', 'military.casualties.combatant'] (score max 0.185)

verifier: grounded

---

## WebQTest-1679 (wrong)

**Q:** what kind of government does the united states have currently

**gold:** ['Presidential system', 'Federal republic', 'Constitutional republic']

**answer:** The United States of America has the Federal government of the United States.

**entities:** ['Federal government of the United States']

plan: ['find the current government of the United States']

explored: ['government.governmental_jurisdiction.government', 'government.government.government_for', 'government.governmental_jurisdiction.government_positions'] (score max 0.649)

verifier: grounded

---

## WebQTest-1620 (wrong)

**Q:** when was president wilson in office

**gold:** ['1913-03-04']

**answer:** Woodrow Wilson was in office in 1913 and 1917, based on the 1913 presidential inauguration and the 1917 presidential inauguration.

**entities:** ['Woodrow Wilson 1913 presidential inauguration', 'Woodrow Wilson 1917 presidential inauguration']

plan: ['find president Wilson', 'find when #1 was in office']

explored: ['government.us_president.vice_president', 'government.us_vice_president.to_president', 'base.inaugurations.inauguration.president'] (score max 0.568)

explored: ['government.us_president.vice_president', 'government.government_position_held.office_holder', 'government.politician.government_positions_held', 'time.event.locations', 'base.inaugurations.inauguration.president', 'base.inaugurations.inauguration.inaugural_address', 'time.event.locations', 'base.inaugurations.inauguration.president', 'base.inaugurations.inauguration.inaugural_address'] (score max 0.485)

verifier: grounded

---

## WebQTest-1898 (wrong)

**Q:** what voices does seth macfarlane play on family guy

**gold:** ['Glenn Quagmire', 'Kevin Swanson', 'Jasper', 'Mickey McFinnegan', 'Peter Griffin', 'Tom Tucker', 'Brian Griffin', 'Stewie Griffin', 'God', 'Seamus', 'Dr. Elmer Hartman', 'Jake Tucker', 'Nate Griffin', 'Carter Pewterschmidt', 'Kool-aid Guy']

**answer:** Seth MacFarlane.

**entities:** ['Seth MacFarlane']

plan: ['find the characters Seth MacFarlane voices on Family Guy']

explored: ['tv.tv_program.regular_cast', 'tv.regular_tv_appearance.series', 'tv.tv_regular_personal_appearance.program'] (score max 0.258)

explored: ['tv.regular_tv_appearance.actor', 'tv.tv_actor.starring_roles', 'tv.tv_writer.tv_programs', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.episodes', 'tv.tv_program.seasons', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.episodes', 'tv.tv_program.seasons', 'fictional_universe.fictional_character.gender', 'fictional_universe.fictional_character_creator.fictional_characters_created', 'fictional_universe.fictional_character.character_created_by'] (score max 0.238)

explored: ['tv.tv_program.regular_cast', 'tv.regular_tv_appearance.series', 'tv.tv_regular_personal_appearance.program', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.episodes', 'tv.tv_program.seasons', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.episodes', 'tv.tv_program.seasons', 'fictional_universe.fictional_character.gender', 'fictional_universe.fictional_character_creator.fictional_characters_created', 'fictional_universe.fictional_character.character_created_by'] (score max 0.528)

explored: ['tv.regular_tv_appearance.actor', 'tv.tv_actor.starring_roles', 'tv.tv_writer.tv_programs', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.episodes', 'tv.tv_program.seasons', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.episodes', 'tv.tv_program.seasons', 'fictional_universe.fictional_character.gender', 'fictional_universe.fictional_character_creator.fictional_characters_created', 'fictional_universe.fictional_character.character_created_by'] (score max 0.238)

verifier: grounded

---

## WebQTest-1178 (wrong)

**Q:** where is tupac from originally

**gold:** ['East Harlem']

**answer:** Tupac Shakur is originally from Marin City.

**entities:** ['Marin City']

plan: ['find where Tupac is originally from']

explored: ['music.artist.origin', 'location.location.people_born_here', 'people.person.places_lived'] (score max 0.535)

verifier: grounded

---

## WebQTest-958 (wrong)

**Q:** what are some famous people from el salvador

**gold:** ['Mario Wilfredo Contreras', 'William López', 'Fausto Omar Vásquez', 'Francisco Menéndez', 'Jose B. Gonzalez', 'Camilo Minero', 'Santiago \\"Jimmy\\" Mellado', 'Manuel Enrique Araujo', 'Erwin McManus', 'Américo González', 'Rene Moran', 'Mauricio Alonso Rodríguez', 'Saturnino Osorio', 'Jose Solis', 'Damaris Quéles', 'Jorge Búcaro', 'Rafael Menjívar Ochoa', 'Doroteo Vasconcelos', 'Selvin González', 'Claudia Lars', 'Jaime Portillo', 'Joel Aguilar', 'Xenia Estrada', 'Jorge Rivera', 'Miguel Cañizalez', 'José Luis Rugamas', 'Ricardo López Tenorio', 'Raúl Cicero', 'Mario Montoya', 'Carlos Barrios', 'Elena Diaz', 'Steve Montenegro', 'Elmer Acevedo', 'Laura Molina', 'Ernesto Aparicio', 'Gerardo Barrios', 'Pedro José Escalón', 'Isaías Choto', 'Rutilio Grande', 'Carlos Linares', 'Juan Rafael Bustillo', 'Melvin Barrera', 'Enrique Álvarez Córdova', 'Miguel Cruz', 'Roberto Carlos Martinez', 'Armando Chacón', 'Richard Oriani', 'Jorge Meléndez', 'Francisco Gavidia', 'Edwin Ramos', 'José Francisco Valiente', 'José María Cañas', 'Prudencia Ayala', 'Julio Adalberto Rivera Carballo', 'Guillermo García', 'Francisca González', 'Alexander Méndoza', 'Alfredo Ruano', 'Eduardo Hernández', 'José Castellanos Contreras', 'Consuelo de Saint Exupéry', 'Norman Quijano', 'Roberto Rivas', 'Mauricio Alvarenga', 'Patricia Chica', 'Emilio Guardado', 'Paula Heredia', 'Robert Renderos', 'Johnny Lopez', 'Papa A.P.', 'José Inocencio Alas', 'Takeshi Fujiwara', 'William Renderos Iraheta', 'Eduardo \\"Volkswagen\\" Hernández', 'Wilfredo Iraheta', 'José Manfredi Portillo', 'Jose Orlando Martinez', 'Tomás Medina', 'Víctor Ramírez', 'Rubén Zamora', 'Gualberto Fernández', 'Marlon Menjívar', 'Pedro Geoffroy Rivas', 'Arturo Rivera y Damas', 'Francisco Funes', 'DJ Quest', 'Andrés Eduardo Menéndez', 'Keoki', 'Nicolas F. Shi', 'Mauricio Alfaro', 'Sarah Ramos', 'g.11b8058v7j', 'Rafael Campo', 'Malin Arvidsson', 'Diego Velázquez', 'Francisco Dueñas', 'Arturo Armando Molina', 'William Armando', 'Pedro Chavarria', 'Salvador Castaneda Castro', 'Alexander Campos', 'Victor Lopez', 'Milton Palacios', 'Ana Sol Gutierrez', 'Ángel Orellana', 'Genaro Sermeño', 'Victor Manuel Ochoa', 'Óscar Antonio Ulloa', 'Bernard Lewinsky', 'Bobby Rivas', 'Miguel Angel Deras', 'Eva Dimas', 'Ana Maria de Martinez', 'Ruben Cedillos', 'Félix Pineda', 'Juan Ramón Sánchez']

**answer:** Some famous people from El Salvador include José Napoleón Duarte, Salvador Sánchez Cerén, Antonio Saca, Óscar Ortiz, Mauricio Funes, and Pamela Benítez.

**entities:** ['José Napoleón Duarte', 'Salvador Sánchez Cerén', 'Antonio Saca', 'Óscar Ortiz', 'Mauricio Funes', 'Pamela Benítez']

plan: ['find people from El Salvador', 'find which of #1 are famous']

explored: ['people.person.nationality', 'people.person.place_of_birth', 'location.country.languages_spoken'] (score max 0.534)

explored: ['people.person.nationality', 'people.person.place_of_birth', 'olympics.olympic_athlete.country', 'people.person.nationality', 'location.location.people_born_here', 'people.person.place_of_birth', 'people.person.nationality', 'people.person.place_of_birth', 'government.government_position_held.office_holder', 'people.person.nationality', 'people.person.place_of_birth', 'government.government_position_held.office_holder', 'people.person.nationality', 'people.person.place_of_birth', 'olympics.olympic_athlete.country'] (score max 0.519)

explored: ['people.person.nationality', 'people.person.place_of_birth', 'government.politician.government_positions_held', 'people.person.nationality', 'people.person.place_of_birth', 'government.politician.government_positions_held', 'people.person.nationality', 'olympics.olympic_athlete_affiliation.athlete', 'people.person.place_of_birth', 'people.person.nationality', 'people.person.place_of_birth', 'location.location.people_born_here', 'people.person.nationality', 'olympics.olympic_athlete_affiliation.athlete', 'people.person.place_of_birth'] (score max 0.448)

explored: ['base.aubreymaturin.place.mentions', 'base.aubreymaturin.place_mention.place', 'location.location.contains', 'sports.sport.pro_athletes', 'sports.pro_sports_played.sport', 'olympics.olympic_athlete_affiliation.sport', 'music.recording.artist', 'sports.competitor_country_relationship.sports', 'interests.hobbyist.hobbies', 'people.person.nationality', 'organization.organization.founders', 'location.location.contains', 'organization.organization_partnership.members', 'sports.competitor_country_relationship.tournament', 'award.award_nominated_work.award_nominations'] (score max 0.52)

verifier: grounded

---

## WebQTest-1061 (wrong)

**Q:** where does greek language come from

**gold:** ['Attic Group']

**answer:** Greek Language comes from Hellenic languages and Indo-European languages.

**entities:** ['Hellenic languages', 'Indo-European languages']

plan: ['find the origin of the Greek language']

explored: ['language.language_family.languages', 'language.human_language.language_family', 'language.human_language.main_country'] (score max 0.65)

explored: ['language.human_language.language_family', 'language.language_family.sub_families', 'language.language_family.languages', 'language.human_language.language_family', 'language.language_family.member_of_language_families', 'language.language_family.member_of_language_families', 'language.language_family.languages', 'language.human_language.language_family', 'base.schemastaging.context_name.pronunciation', 'language.human_language.main_country', 'language.human_language.countries_spoken_in', 'location.country.languages_spoken'] (score max 0.628)

explored: ['language.language_family.sub_families', 'language.human_language.language_family', 'language.language_family.languages', 'people.ethnicity.languages_spoken', 'language.human_language.language_family', 'language.language_family.languages', 'language.language_writing_system.languages', 'language.human_language.language_family', 'language.language_family.languages', 'language.human_language.region', 'language.language_family.languages', 'language.human_language.language_family', 'language.human_language.region'] (score max 0.555)

explored: ['language.human_language.language_family', 'language.language_family.member_of_language_families', 'language.language_family.member_of_language_families', 'language.human_language.language_family', 'language.language_family.languages', 'language.language_family.sub_families', 'language.language_family.languages', 'language.human_language.language_family', 'base.schemastaging.context_name.pronunciation', 'language.language_family.languages', 'language.language_family.member_of_language_families', 'language.language_family.member_of_language_families', 'language.language_family.member_of_language_families', 'language.language_family.member_of_language_families', 'language.human_language.language_family'] (score max 0.628)

verifier: grounded

---

## WebQTest-1940 (wrong)

**Q:** who do islamic people follow

**gold:** ['Ramdev Pir', 'God', 'Allah']

**answer:** Islamic people follow Muslims. Could not be determined from the provided facts whether any specific person is meant beyond Muslims.

**entities:** ['Muslims']

plan: ['find who Islamic people follow']

explored: ['religion.adherents.religion', 'religion.religion.number_of_adherents', 'religion.religion.collective_term_for_adherents'] (score max 0.324)

backtrack: evaluator

explored: ['people.person.religion', 'location.religion_percentage.religion', 'religion.religious_organization.associated_with'] (score max 0.286)

verifier: grounded

---

## WebQTest-1707 (wrong)

**Q:** who plays lex luthor on smallville

**gold:** ['Michael Rosenbaum']

**answer:** John Glover plays Lionel Luthor on Smallville. The facts provided do not determine who plays Lex Luthor on Smallville.

**entities:** ['John Glover']

plan: ['find the actor who plays Lex Luthor on Smallville']

explored: ['tv.tv_program.regular_cast', 'tv.regular_tv_appearance.series', 'tv.tv_series_season.series'] (score max 0.542)

explored: ['tv.tv_actor.starring_roles', 'tv.regular_tv_appearance.actor', 'people.person.nationality', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.regular_tv_appearance.character', 'tv.tv_character.appeared_in_tv_program'] (score max 0.317)

explored: ['tv.tv_program.regular_cast', 'tv.regular_tv_appearance.series', 'tv.tv_series_season.series', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.regular_tv_appearance.character', 'tv.tv_character.appeared_in_tv_program'] (score max 0.317)

explored: ['tv.tv_actor.starring_roles', 'tv.regular_tv_appearance.actor', 'people.person.nationality', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.tv_series_season.regular_cast', 'tv.tv_series_season.series', 'tv.tv_series_season.episodes', 'tv.regular_tv_appearance.character', 'tv.tv_character.appeared_in_tv_program'] (score max 0.317)

verifier: grounded

---

## WebQTest-164 (wrong)

**Q:** what did stephen hawking become famous for

**gold:** ['Cosmologist', 'Mathematician', 'Author', 'Physicist', 'Writer', 'Astronomer', 'Science writer', 'Astrophysicist', 'Professor', 'Scientist']

**answer:** Stephen Hawking became famous for A Brief History of Time.

**entities:** ['Stephen Hawking']

plan: ['find what Stephen Hawking became famous for']

explored: ['medicine.notable_person_with_medical_condition.condition', 'award.award_honor.award_winner', 'book.author.works_written'] (score max 0.415)

explored: ['medicine.notable_person_with_medical_condition.condition', 'book.book_subject.works', 'medicine.disease.medical_specialties', 'award.award_category.winners', 'award.award_honor.award', 'medicine.notable_person_with_medical_condition.condition', 'book.book_subject.works', 'base.qualia.disabled_person.type_of_disability', 'award.award_honor.award', 'award.award_category.category_of', 'award.award_category.category_of'] (score max 0.43)

verifier: unsupported

explored: ['people.person.employment_history', 'fictional_universe.person_in_fiction.representations_in_fiction', 'fictional_universe.person_in_fiction.representations_in_fiction'] (score max 0.41)

verifier: unsupported

---

## WebQTest-703 (wrong)

**Q:** what currency should i take to mexico

**gold:** ['Mexican peso']

**answer:** United States Dollar

**entities:** ['United States Dollar']

plan: ['find Mexico', 'find the currency used in #1']

explored: ['location.location.contains', 'base.locations.countries.continent', 'location.country.languages_spoken'] (score max 0.258)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.continents.planet', 'location.location.contains', 'location.location.contains', 'base.ontologies.ontology_instance.equivalent_instances', 'location.location.contains', 'location.location.containedby', 'location.location.geolocation', 'location.location.contains', 'location.location.contains', 'base.ontologies.ontology_instance.equivalent_instances', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'location.country.languages_spoken'] (score max 0.192)

explored: ['location.country.currency_used', 'finance.currency.countries_used', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'location.country.currency_used', 'finance.currency.countries_used', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'location.country.currency_used', 'finance.currency.countries_used', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'location.country.currency_used', 'finance.currency.countries_used', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'base.locations.countries.continent', 'location.country.first_level_divisions', 'base.locations.continents.countries_within'] (score max 0.746)

verifier: grounded

---

## WebQTest-114 (wrong)

**Q:** who did the voice of darth vader in episode 3

**gold:** ['Hayden Christensen']

**answer:** Matt Lanter voiced Darth Vader in Episode 3.

**entities:** ['Matt Lanter']

plan: ['find episode 3', 'find who did the voice of Darth Vader in #1']

explored: ['tv.tv_character.appeared_in_tv_program', 'tv.regular_tv_appearance.character', 'book.book.characters'] (score max 0.26)

explored: ['tv.tv_series_season.episodes', 'tv.tv_series_season.series', 'tv.tv_program.seasons', 'tv.tv_series_season.episodes', 'tv.tv_series_season.series', 'tv.tv_program.seasons', 'tv.tv_series_season.series', 'tv.multipart_tv_episode.episodes', 'tv.tv_program.multipart_episodes', 'film.actor.film', 'tv.regular_tv_appearance.actor', 'tv.tv_actor.starring_roles', 'tv.special_tv_performance_type.segment_performances', 'music.artist.album', 'tv.tv_guest_role.special_performance_type'] (score max 0.7)

explored: ['tv.tv_series_season.episodes', 'tv.tv_series_season.episodes', 'tv.tv_program.episodes', 'tv.tv_writer.episodes_written', 'tv.tv_series_season.episodes', 'film.film_crew_gig.film', 'film.producer.film', 'tv.tv_series_season.episodes', 'tv.tv_director.episodes_directed', 'tv.regular_tv_appearance.series', 'tv.tv_series_season.episodes'] (score max 0.691)

explored: ['tv.tv_series_season.episodes', 'tv.tv_series_season.series', 'tv.tv_program.seasons', 'tv.tv_series_season.episodes', 'tv.tv_series_season.series', 'tv.tv_program.seasons', 'tv.tv_program.episodes', 'tv.tv_program.seasons', 'tv.regular_tv_appearance.series', 'tv.tv_director.episodes_directed', 'film.film.directed_by', 'film.director.film', 'tv.tv_director.episodes_directed', 'tv.tv_guest_role.actor', 'tv.tv_actor.guest_roles'] (score max 0.706)

verifier: grounded

---

## WebQTest-1215 (wrong)

**Q:** who was stephen r covey

**gold:** ['Author', 'Manager', 'Writer', 'Consultant', 'Professor', 'Motivational speaker']

**answer:** Stephen Covey was a Writer, Motivational speaker, Author, Consultant, Professor, and Manager. He wrote works including The 8th Habit, First Things First, The Leader in Me, The SPEED of Trust, and The 3rd Alternative.

**entities:** ['Stephen Covey']

plan: ['find who Stephen R. Covey was']

explored: ['people.person.profession', 'book.written_work.author', 'book.author.works_written'] (score max 0.354)

verifier: grounded

---

## WebQTest-923 (wrong)

**Q:** what countries does england border

**gold:** ['Wales', 'Scotland']

**answer:** England borders United Kingdom. The facts provided do not determine any other countries that England borders.

**entities:** ['United Kingdom']

plan: ['find countries that border England']

explored: ['location.location.containedby', 'location.location.containedby', 'geography.river.basin_countries'] (score max 0.512)

explored: ['location.location.geolocation', 'location.location.containedby', 'location.location.contains', 'location.location.containedby', 'location.location.contains', 'location.location.containedby', 'location.location.contains', 'education.educational_institution.campuses', 'location.location.containedby', 'location.location.contains', 'location.location.containedby', 'location.location.containedby', 'location.location.contains'] (score max 0.235)

explored: ['base.locations.countries.continent', 'location.country.internet_tld', 'base.locations.continents.countries_within', 'location.country.internet_tld', 'location.country.languages_spoken', 'geography.river.basin_countries', 'location.country.capital', 'location.administrative_division.country', 'base.biblioness.bibs_location.country', 'location.country.capital', 'base.biblioness.bibs_location.country', 'location.location.geolocation', 'location.location.containedby', 'location.location.containedby', 'location.location.contains'] (score max 0.331)

backtrack: evaluator

explored: ['location.location.geolocation', 'location.location.containedby', 'location.location.contains', 'location.location.containedby', 'location.location.contains', 'location.location.containedby', 'location.location.contains', 'education.educational_institution.campuses', 'location.location.containedby', 'location.location.contains', 'location.location.containedby', 'location.location.containedby', 'location.location.contains'] (score max 0.235)

backtrack: evaluator

explored: ['education.educational_institution.campuses', 'education.educational_institution_campus.educational_institution', 'education.educational_institution_campus.educational_institution', 'location.location.contains', 'location.location.time_zones'] (score max 0.205)

backtrack: evaluator

explored: ['base.locations.continents.counties_within', 'royalty.royal_line.kingdom_s_ruled', 'location.country.languages_spoken', 'location.country.form_of_government', 'location.country.capital', 'location.country.administrative_divisions', 'location.location.geolocation', 'location.location.containedby', 'location.location.containedby', 'location.location.containedby', 'location.location.containedby', 'location.location.contains', 'travel.travel_destination.tourist_attractions', 'location.location.events', 'time.event.locations'] (score max 0.302)

verifier: grounded

---

## WebQTest-209 (wrong)

**Q:** where is laos in world map

**gold:** ['Southeast Asia']

**answer:** Laos is in Asia.

**entities:** ['Laos']

plan: ['find Laos', 'find where #1 is located on the world map']

explored: ['location.country.languages_spoken', 'location.country.internet_tld', 'location.country.form_of_government'] (score max 0.263)

explored: ['location.country.internet_tld', 'base.rosetta.languoid.geolocation', 'base.rosetta.languoid.geolocation', 'location.country.languages_spoken', 'location.country.form_of_government', 'government.form_of_government.countries', 'location.country.languages_spoken', 'location.country.official_language', 'language.human_language.countries_spoken_in', 'location.country.languages_spoken', 'location.country.official_language', 'base.militaryinfiction.location_in_fiction.languages'] (score max 0.286)

backtrack: evaluator

explored: ['location.country.official_language', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'language.human_language.main_country', 'language.human_language.region', 'base.rosetta.languoid.local_name', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'tv.tv_program.country_of_origin'] (score max 0.203)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.location.geolocation', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.location.geolocation', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.location.containedby', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.location.geolocation', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.location.containedby'] (score max 0.652)

backtrack: evaluator

explored: ['location.country.official_language', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'language.human_language.main_country', 'language.human_language.region', 'base.rosetta.languoid.local_name', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'tv.tv_program.country_of_origin'] (score max 0.203)

backtrack: evaluator

explored: ['language.human_language.region', 'fictional_universe.fictional_setting.languages', 'fictional_universe.fictional_language.where_spoken', 'base.rosetta.local_name.languoid', 'base.rosetta.languoid.parent', 'base.rosetta.languoid.document', 'fictional_universe.fictional_setting.languages', 'fictional_universe.fictional_language.where_spoken', 'organization.organization.sectors'] (score max 0.148)

verifier: grounded

---

## WebQTest-245 (wrong)

**Q:** what year was the first miss america pageant held

**gold:** ['1921-09']

**answer:** The first Miss America pageant was held in 1921, corresponding to Miss America 1921.

**entities:** ['Miss America 1921']

plan: ['find the first Miss America pageant', 'find the year it was held']

explored: ['award.recurring_competition.individual_competitions', 'award.competition.instance_of_recurring_competition', 'time.event.instance_of_recurring_event'] (score max 0.438)

explored: ['time.event.instance_of_recurring_event', 'time.recurring_event.instances', 'award.recurring_competition.individual_competitions'] (score max 0.529)

explored: ['time.event.instance_of_recurring_event', 'time.recurring_event.instances', 'award.competition.instance_of_recurring_competition'] (score max 0.529)

verifier: grounded

---

## WebQTest-108 (wrong)

**Q:** what was the book written by charles darwin

**gold:** ['On evolution', 'The Autobiography of Charles Darwin, and selected letters', 'The Voyage of the Beagle', 'The Voyage of the Beagle (Great Minds Series)', "Théorie de l'évolution", 'To the members of the Down Friendly Club', 'The Correspondence of Charles Darwin, Volume 3: 1844-1846', 'Descent of Man and Selection in Relation to Sex (Barnes & Noble Library of Essential Reading)', 'Origin of Species', 'The Origin Of Species', 'The Voyage of the Beagle (Classics of World Literature) (Classics of World Literature)', 'Proiskhozhdenie vidov', 'Darwin and Henslow', 'Resa kring jorden', 'Darwinism stated by Darwin himself', 'The Voyage of the Beagle (Unabridged Classics)', 'The zoology of the voyage of H.M.S. Beagle during the years 1832-1836', 'Darwin', 'The Darwin Reader First Edition', 'The Origin of Species', 'From So Simple a Beginning', 'Diary of the voyage of H.M.S. Beagle', "Journal of researches into the natural history and geology of the countries visited during the voyage round the world of the H. M. S. 'Beagle' under the command of Captain Fitz Roy, R. N", 'The Origin of Species', 'Voyage of the Beagle (NG Adventure Classics)', "Charles Darwin's letters", "Origin of Species (Everyman's University Paperbacks)", 'The Origin of Species', 'The Expression Of The Emotions In Man And Animals', 'The Expression of the Emotions in Man and Animals', 'The Structure and Distribution of Coral Reefs', 'The Formation of Vegetable Mould through the Action of Worms', 'Gesammelte kleinere Schriften', 'Het uitdrukken van emoties bij mens en dier', 'Evolution and natural selection', 'The Correspondence of Charles Darwin, Volume 12: 1864', 'Voyage of the Beagle (Harvard Classics, Part 29)', 'On the tendency of species to form varieties', 'The descent of man, and selection in relation to sex', 'The Correspondence of Charles Darwin, Volume 15: 1867', 'The origin of species', "Darwin's journal", 'The Expression of the Emotions in Man and Animals', 'The Descent of Man, and Selection in Relation to Sex', "The Origin of Species (Collector's Library)", 'Die verschiedenen Blütenformen an Pflanzen der nämlichen Art', 'Darwin-Wallace', 'Part I: Contributions to the Theory of Natural Selection / Part II', 'Charles Darwin', 'Darwin for Today', 'The Origin of Species (Barnes & Noble Classics Series) (Barnes & Noble Classics)', 'The Correspondence of Charles Darwin, Volume 16: 1868', "A student's introduction to Charles Darwin", 'The Expression of the Emotions in Man And Animals', 'The autobiography of Charles Darwin', 'From so simple a beginning', 'The Darwin Reader First Edition', 'Les mouvements et les habitudes des plantes grimpantes', "Charles Darwin's marginalia", 'The Correspondence of Charles Darwin, Volume 8: 1860', 'The Origin of Species', 'The Voyage of the Beagle', 'The Correspondence of Charles Darwin, Volume 2: 1837-1843', 'Autobiography of Charles Darwin', 'The Origin of Species', 'The expression of the emotions in man and animals', 'A Darwin Selection', 'The expression of the emotions in man and animals', "Charles Darwin's zoology notes & specimen lists from H.M.S. Beagle", 'red notebook of Charles Darwin', 'The Origin of Species (Great Books : Learning Channel)', 'The Correspondence of Charles Darwin, Volume 4', 'Questions about the breeding of animals', 'The voyage of Charles Darwin', 'The Correspondence of Charles Darwin, Volume 6', 'Tesakneri tsagumě', 'Cartas de Darwin 18251859', "Un mémoire inédit de Charles Darwin sur l'instinct", 'The Voyage of the Beagle (Unabridged Classics)', 'Works', 'The Correspondence of Charles Darwin, Volume 9: 1861', 'The Origin of Species (Variorum Reprint)', 'On Natural Selection', 'The Correspondence of Charles Darwin, Volume 4: 1847-1850', 'The expression of the emotions in man and animals.', 'Les récifs de corail, leur structure et leur distribution', "Les moyens d'expression chez les animaux", 'The Autobiography of Charles Darwin (Great Minds Series)', 'The Expression of the Emotions in Man and Animals', 'The Correspondence of Charles Darwin, Volume 14', 'The autobiography of Charles Darwin, 1809-1882', 'The Correspondence of Charles Darwin, Volume 8', 'La faculté motrice dans les plantes', 'The Origin of Species (Enriched Classics)', 'The Correspondence of Charles Darwin, Volume 5: 1851-1855', 'Notebooks on transmutation of species', 'The Autobiography of Charles Darwin', 'Opshṭamung fun menshen', 'Fertilisation of Orchids', 'Autobiography of Charles Darwin', 'The Expression of the Emotions in Man And Animals', 'The Correspondence of Charles Darwin, Volume 2', 'Voyage of the Beagle', 'The Voyage of the \\"Beagle\\" (Everyman\'s Classics)', "Darwin's insects", 'Charles Darwin on the routes of male humble bees', 'Reise eines Naturforschers um die Welt', 'Seul celui qui change reste fidèle à lui-même', 'The Correspondence of Charles Darwin, Volume 1', "Human nature, Darwin's view", 'Voyage Of The Beagle', 'The structure and distribution of coral reefs.', 'The descent of man, and selection in relation to sex.', 'The Origin Of Species', 'Das Variiren der Thiere und Pflanzen im Zustande der Domestication', 'The Life of Erasmus Darwin', 'The Correspondence of Charles Darwin, Volume 15', 'geneseōs tōn eidōn', 'The Correspondence of Charles Darwin, Volume 11: 1863', 'Origin of Species', 'The Descent of Man and Selection in Relation to Sex', 'Evolution by natural selection', 'The collected papers of Charles Darwin', 'Insectivorous Plants', 'The Effects of Cross and Self Fertilisation in the Vegetable Kingdom', 'The Correspondence of Charles Darwin, Volume 5', 'Memorias y epistolario íntimo', 'El Origin De Las Especies', 'H.M.S. Beagle in South America', 'The Expression of the Emotions in Man and Animals', 'THE ORIGIN OF SPECIES (Wordsworth Collection) (Wordsworth Collection)', 'Die fundamente zur entstehung der arten', 'The Origin of Species', 'On the Movements and Habits of Climbing Plants', 'The Origin of Species', 'variëeren der huisdieren en cultuurplanten', 'Darwin Compendium', 'Origin of Species', 'Origin of Species (Harvard Classics, Part 11)', 'The portable Darwin', 'The Correspondence of Charles Darwin, Volume 10: 1862', 'The structure and distribution of coral reefs', 'The foundations of the Origin of species', 'The education of Darwin', 'Origin of Species', 'ontstaan der soorten door natuurlijke teeltkeus', 'The Voyage of the Beagle', 'The expression of the emotions in man and animals', 'The expression of the emotions in man and animals', 'The origin of species', 'The Expression of the Emotions in Man and Animals', 'Metaphysics, Materialism, & the evolution of mind', 'Der Ausdruck der Gemüthsbewegungen bei dem Menschen und den Thieren', 'The Origin of Species', 'The Origin of Species', 'The Correspondence of Charles Darwin, Volume 13: 1865', 'monograph on the sub-class Cirripedia', 'La vie et la correspondance de Charles Darwin', 'The voyage of the Beagle.', 'The Origin of Species (Great Minds Series)', 'The Darwin Reader Second Edition', 'The Origin of Species', 'The geology of the voyage of H.M.S. Beagle', 'The Correspondence of Charles Darwin, Volume 11', 'The Autobiography of Charles Darwin (Dodo Press)', 'The Origin of Species', "The Origin of Species (Oxford World's Classics)", "From Darwin's unpublished notebooks", 'The Autobiography of Charles Darwin [EasyRead Edition]', "Charles Darwin's letters", 'Darwin on humus and the earthworm', "A student's introduction to Charles Darwin", 'The Autobiography of Charles Darwin', 'The descent of man, and selection in relation to sex.', 'From so simple a beginning', 'The Voyage of the Beagle (Adventure Classics)', 'The Correspondence of Charles Darwin, Volume 14: 1866', 'The Correspondence of Charles Darwin, Volume 17: 1869', 'The descent of man and selection in relation to sex.', 'The Correspondence of Charles Darwin, Volume 13', 'Origin of Species', 'The Expression of the Emotions in Man and Animals', 'The Autobiography of Charles Darwin [EasyRead Large Edition]', 'Reise um die Welt 1831 - 36', "The Descent Of Man And Selection In Relation To Sex (Kessinger Publishing's Rare Reprints)", 'The Origin Of Species', 'Viaje de Un Naturalista Alrededor del Mundo 2 Vol', 'The Origin of Species', 'Diario del Viaje de Un Naturalista Alrededor', 'The Origin of Species', "Charles Darwin's natural selection", 'On evolution', 'The Origin of Species (Mentor)', 'The living thoughts of Darwin', 'The principal works', 'Über den Bau und die Verbreitung der Corallen-Riffe', 'The origin of species : complete and fully illustrated', 'Notes on the fertilization of orchids', 'The Correspondence of Charles Darwin, Volume 18: 1870', 'Evolution', 'The origin of species', 'The Autobiography Of Charles Darwin', 'The Descent of Man and Selection in Relation to Sex', 'The origin of species : complete and fully illustrated', 'Monographs of the fossil Lepadidae and the fossil Balanidae', 'On a remarkable bar of sandstone off Pernambuco', 'The Correspondence of Charles Darwin, Volume 7: 1858-1859', 'The Correspondence of Charles Darwin, Volume 3', "Charles Darwin's natural selection", 'The Voyage of the Beagle (Unabridged Classics)', "La descendance de l'homme et la s©Øelection sexuelle", 'Darwin en Patagonia', 'Del Plata a Tierra del Fuego', 'The Voyage of the Beagle', "Geological observations on the volcanic islands and parts of South America visited during the voyage of H.M.S. 'Beagle", 'The Structure And Distribution of Coral Reefs', 'The Power of Movement in Plants', 'The Voyage of the Beagle', 'Origins', 'Kleinere geologische Abhandlungen', 'The Correspondence of Charles Darwin, Volume 1: 1821-1836', 'Letters from C. Darwin, Esq., to A. Hancock, Esq', 'The Orgin of Species', 'Die Entstehung der Arten durch natürliche Zuchtwahl', 'The action of carbonate of ammonia on the roots of certain plants', 'The Autobiography of Charles Darwin [EasyRead Comfort Edition]', 'The Voyage of the Beagle (Everyman Paperbacks)', 'The origin of species', 'The Expression of the Emotions in Man and Animals', 'More Letters of Charles Darwin', 'The Expression of the Emotions in Man and Animals (Large Print Edition): The Expression of the Emotions in Man and Animals (Large Print Edition)', 'Beagle letters', 'The Correspondence of Charles Darwin, Volume 10', 'The Correspondence of Charles Darwin, Volume 7', 'Rejse om jorden', 'The Different Forms of Flowers on Plants of the Same Species', "Darwin's notebooks on transmutation of species", 'The Structure and Distribution of Coral Reefs', 'Vospominanii︠a︡ o razvitii moego uma i kharaktera', 'The Origin of Species (Mentor)', 'The Descent of Man and Selection in Relation to Sex', 'The Essential Darwin', 'The Autobiography of Charles Darwin (Large Print)', 'The Descent of Man and Selection in Relation to Sex', 'The Darwin Reader Second Edition', 'Leben und Briefe von Charles Darwin', 'Voyage of the Beagle', 'Die Bewegungen und Lebensweise der kletternden Pflanzen', "Voyage d'un naturaliste autour du monde", 'Über die Wege der Hummel-Männchen', 'The autobiography of Charles Darwin, 1809-1882', 'Darwin Darwin', "The Origin of Species (World's Classics)", 'Motsa ha-minim', 'The Variation of Animals and Plants under Domestication', 'Die geschlechtliche Zuchtwahl', "Darwin's Ornithological notes", 'Wu zhong qi yuan', 'The origin of species by means of natural selection, or, The preservation of favored races in the struggle for life', 'The origin of species', 'Voyage of the Beagle (Dover Value Editions)', 'On Natural Selection', 'The Origin of Species', 'The Correspondence of Charles Darwin, Volume 9', "Charles Darwin's zoology notes & specimen lists from H.M.S. Beagle", 'The Autobiography of Charles Darwin', 'On the origin of species by means of natural selection', 'Geological Observations on South America', 'The Voyage of the Beagle (Mentor)', 'The Origin of Species', 'Die Wirkungen der Kreuz- und Selbst-Befruchtung im Pflanzenreich', 'The Correspondence of Charles Darwin, Volume 6: 1856-1857', 'The Correspondence of Charles Darwin, Volume 12', 'Volcanic Islands', 'Charles Darwin, 1809-1882--Anton Dohrn, 1840-1909']

**answer:** Grant Allen

**entities:** ['Grant Allen']

plan: ['find the book written by Charles Darwin']

explored: ['book.author.works_written', 'book.written_work.author', 'book.book_subject.works'] (score max 0.633)

verifier: grounded

---

## WebQTest-186 (wrong)

**Q:** who rules denmark right now

**gold:** ['Helle Thorning-Schmidt', 'Margrethe II of Denmark', 'Margrethe Vestager']

**answer:** Christian X of Denmark rules Denmark right now.

**entities:** ['Christian X of Denmark']

plan: ['find who rules Denmark right now']

explored: ['royalty.royal_line.kingdom_s_ruled', 'royalty.kingdom.rulers', 'royalty.monarch.kingdom'] (score max 0.535)

explored: ['royalty.royal_line.kingdom_s_ruled', 'royalty.monarch.royal_line', 'people.family.country', 'royalty.royal_line.kingdom_s_ruled', 'royalty.monarch.royal_line', 'people.family.country', 'royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'royalty.monarch.royal_line', 'royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'royalty.monarch.royal_line', 'royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'location.location.people_born_here'] (score max 0.535)

explored: ['royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'government.governmental_jurisdiction.governing_officials', 'royalty.monarch.kingdom', 'royalty.royal_line.kingdom_s_ruled', 'royalty.kingdom.rulers', 'royalty.royal_line.kingdom_s_ruled', 'location.country.form_of_government', 'location.country.official_language', 'royalty.royal_line.kingdom_s_ruled', 'royalty.monarch.royal_line', 'royalty.royal_line.monarchs_from_this_line', 'people.family_member.family'] (score max 0.521)

explored: ['royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'royalty.monarch.royal_line', 'royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'base.culturalevent.event.entity_involved', 'royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'location.location.people_born_here', 'royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'base.culturalevent.event.entity_involved', 'royalty.kingdom.rulers', 'royalty.monarch.kingdom', 'people.person.nationality'] (score max 0.251)

verifier: grounded

---

## WebQTest-749 (wrong)

**Q:** who was president in 1988 in the united states

**gold:** ['Ronald Reagan']

**answer:** George H. W. Bush was president in 1988 in the United States.

**entities:** ['George H. W. Bush']

plan: ['find the president of the United States in 1988']

explored: ['government.election.office', 'government.government_position_held.office_position_or_title', 'government.government_office_or_title.office_holders'] (score max 0.514)

explored: ['government.election.office', 'government.election.winner', 'government.election_campaign.election', 'government.election.office', 'government.election.winner', 'government.election.general_election', 'government.election.office', 'government.election.winner', 'government.election.general_election', 'government.election.office', 'government.election.winner', 'government.election_campaign.election', 'government.election.office', 'government.election.winner', 'time.event.locations'] (score max 0.229)

explored: ['government.us_president.vice_president', 'government.us_vice_president.to_president', 'base.politicalconventions.presidential_nominee.nominated_at', 'government.us_president.vice_president', 'government.us_vice_president.to_president', 'base.presidentialpets.first_family.president', 'government.us_president.vice_president', 'government.us_president.vice_president', 'government.us_vice_president.to_president', 'government.us_president.vice_president', 'government.us_vice_president.to_president', 'base.politicalconventions.presidential_nominee.nominated_at', 'government.electoral_college_elected_office.office', 'government.election.office', 'government.government_position_held.office_position_or_title'] (score max 0.385)

explored: ['government.us_president.vice_president', 'government.us_vice_president.to_president', 'base.politicalconventions.presidential_nominee.nominated_at', 'government.us_president.vice_president', 'government.us_vice_president.to_president', 'government.government_position_held.office_holder', 'government.us_president.vice_president', 'government.us_vice_president.to_president', 'government.government_position_held.office_holder', 'government.us_president.vice_president', 'government.us_vice_president.to_president', 'government.government_position_held.office_holder', 'government.us_president.vice_president', 'government.us_president.vice_president', 'government.us_vice_president.to_president'] (score max 0.385)

verifier: grounded

---

## WebQTest-1170 (wrong)

**Q:** who is the governor of virginia 2011

**gold:** ['Bob McDonnell']

**answer:** Governor of Virginia

**entities:** ['Governor of Virginia']

plan: ['find the governor of Virginia in 2011']

explored: ['government.government_position_held.jurisdiction_of_office', 'government.election.district', 'government.political_district.representatives'] (score max 0.278)

explored: ['government.political_party_tenure.politician', 'government.politician.government_positions_held', 'government.politician.party', 'government.politician.government_positions_held', 'government.government_position_held.office_holder', 'location.location.people_born_here', 'government.government_position_held.office_position_or_title', 'government.government_office_or_title.office_holders', 'government.government_position_held.governmental_body', 'government.governmental_body.members', 'government.governmental_jurisdiction.government_bodies'] (score max 0.263)

backtrack: evaluator

explored: ['government.government_position_held.office_holder', 'education.education.student', 'location.location.people_born_here', 'people.person.place_of_birth', 'people.person.profession', 'people.deceased_person.place_of_death', 'government.governmental_body.jurisdiction', 'government.governmental_body.component_bodies', 'government.governmental_body.body_this_is_a_component_of'] (score max 0.191)

backtrack: evaluator

explored: ['people.person.education', 'people.person.place_of_birth', 'people.person.profession', 'people.person.gender', 'people.person.nationality'] (score max 0.095)

backtrack: evaluator

explored: ['people.deceased_person.place_of_death', 'military.military_person.participated_in_conflicts', 'people.person.gender'] (score max 0.069)

verifier: grounded

---

## WebQTest-1047 (wrong)

**Q:** who does amy stiller play in dodgeball

**gold:** ['Keno Waitress']

**answer:** Amy Stiller plays Pam Bailey in DodgeBall: A True Underdog Story.

**entities:** ['Pam Bailey']

plan: ['find the character Amy Stiller plays in Dodgeball']

explored: ['film.film.starring', 'film.film_costumer_designer.costume_design_for_film', 'film.film_subject.films', 'film.actor.film', 'film.performance.actor', 'tv.tv_actor.starring_roles'] (score max 0.476)

verifier: grounded

---

## WebQTest-1794 (wrong)

**Q:** where is mitt romney 's family from

**gold:** ['Detroit']

**answer:** Mitt Romney's family is from Bloomfield Hills and Massachusetts.

**entities:** ['Bloomfield Hills', 'Massachusetts']

plan: ['find the family of Mitt Romney', 'find where #1 is from']

explored: ['people.person.spouse_s', 'people.person.parents', 'people.person.parents'] (score max 0.469)

explored: ['people.person.places_lived', 'people.person.place_of_birth', 'people.place_lived.person', 'people.person.places_lived', 'people.person.place_of_birth', 'people.place_lived.person', 'people.person.nationality', 'people.person.sibling_s', 'people.person.parents', 'people.person.nationality', 'people.person.spouse_s', 'people.person.sibling_s', 'people.person.nationality', 'people.person.sibling_s', 'people.person.parents'] (score max 0.457)

explored: ['location.location.people_born_here', 'location.location.contains', 'location.location.contains', 'base.biblioness.bibs_location.country', 'location.location.contains', 'people.place_lived.location', 'base.biblioness.bibs_location.country', 'location.location.contains', 'people.place_lived.location', 'base.biblioness.bibs_location.country', 'location.location.contains', 'people.place_lived.location', 'location.location.contains', 'location.location.contains', 'people.place_lived.location'] (score max 0.238)

explored: ['location.location.people_born_here', 'location.location.people_born_here', 'location.location.people_born_here', 'location.location.people_born_here', 'people.person.place_of_birth', 'people.person.nationality', 'location.location.people_born_here', 'people.person.spouse_s', 'people.person.place_of_birth'] (score max 0.238)

verifier: grounded

---

## WebQTest-1477 (wrong)

**Q:** what episode of how i met your mother is carrie underwood on

**gold:** ['Hooked']

**answer:** Carrie Underwood appears on Peyton Manning/Carrie Underwood.

**entities:** ['Peyton Manning/Carrie Underwood']

plan: ['find the episode of How I Met Your Mother that Carrie Underwood appears in']

explored: ['tv.tv_guest_role.actor', 'base.saturdaynightlive.snl_episode.musical_guest', 'base.realitytv.reality_tv_contestant.season'] (score max 0.393)

explored: ['tv.tv_guest_role.episodes_appeared_in', 'tv.tv_guest_personal_appearance.episode', 'tv.tv_series_season.episodes', 'tv.tv_guest_role.episodes_appeared_in', 'tv.tv_guest_role.episodes_appeared_in', 'tv.tv_guest_role.episodes_appeared_in', 'tv.tv_guest_role.episodes_appeared_in'] (score max 0.486)

explored: ['tv.tv_guest_personal_appearance.episode', 'base.saturdaynightlive.snl_episode.musical_guest', 'tv.tv_program_guest.appeared_on', 'tv.tv_guest_personal_appearance.episode', 'tv.tv_program_guest.appeared_on', 'tv.tv_guest_personal_appearance.person', 'tv.tv_guest_personal_appearance.episode', 'tv.tv_series_season.episodes', 'tv.tv_program_guest.appeared_on', 'tv.non_character_role.episode_segment_appearances', 'tv.tv_segment_personal_appearance.appearance_type', 'tv.tv_guest_personal_appearance.appearance_type', 'base.saturdaynightlive.snl_episode.musical_guest', 'base.realitytv.reality_tv_contestant.season', 'base.saturdaynightlive.snl_musical_guest.episodes_as_musical_guest'] (score max 0.322)

backtrack: evaluator

explored: ['tv.tv_guest_role.episodes_appeared_in', 'tv.tv_guest_personal_appearance.episode', 'tv.tv_series_season.episodes', 'tv.tv_guest_role.episodes_appeared_in', 'tv.tv_guest_role.episodes_appeared_in', 'tv.tv_guest_role.episodes_appeared_in', 'tv.tv_guest_role.episodes_appeared_in'] (score max 0.486)

explored: ['base.saturdaynightlive.snl_episode.host', 'base.saturdaynightlive.snl_host.episodes_hosted', 'tv.tv_guest_personal_appearance.person', 'base.saturdaynightlive.snl_character.impression_of', 'base.saturdaynightlive.person_impersonated_on_snl.snl_impersonations', 'people.person.parents', 'tv.tv_guest_personal_appearance.person', 'tv.tv_director.episodes_directed', 'film.film_featured_song.performed_by', 'film.personal_film_appearance.type_of_appearance', 'music.special_music_video_performance_type.special_music_video_performances', 'tv.tv_regular_personal_appearance.appearance_type', 'base.saturdaynightlive.snl_musical_guest.musical_performance', 'base.saturdaynightlive.snl_musical_performance.musical_guest', 'people.person.parents'] (score max 0.197)

backtrack: evaluator

explored: ['base.saturdaynightlive.snl_musical_guest.episodes_as_musical_guest', 'base.saturdaynightlive.snl_musical_guest.musical_performance', 'base.saturdaynightlive.snl_musical_performance.musical_guest', 'people.person.parents', 'event.public_speaker.speeches_or_presentations', 'tv.tv_personality.tv_regular_appearances', 'people.person.parents', 'tv.tv_personality.tv_regular_appearances', 'broadcast.artist.content', 'tv.special_tv_performance_type.segment_performances', 'music.music_video_performance.special_music_video_performance_type', 'film.film_character.portrayed_in_films', 'base.realitytv.reality_tv_season.contestants', 'tv.tv_personality.tv_regular_appearances', 'broadcast.artist.content'] (score max 0.164)

explored: ['tv.tv_guest_personal_appearance.episode', 'tv.tv_program_guest.appeared_on', 'tv.tv_guest_role.episodes_appeared_in', 'base.saturdaynightlive.snl_musical_performance.episode', 'base.saturdaynightlive.snl_episode.season', 'base.saturdaynightlive.snl_season.episodes', 'people.person.parents', 'people.family.members', 'people.family_member.family', 'people.person.parents', 'people.family.members', 'people.family_member.family', 'people.person.parents', 'people.place_lived.person', 'film.personal_film_appearance.person'] (score max 0.337)

verifier: grounded

---

## WebQTest-284 (wrong)

**Q:** where did the latin language originate from

**gold:** ['Indo-European languages', 'Italic languages']

**answer:** Latin Language originated in Europe.

**entities:** ['Europe']

plan: ['find where the Latin language originated from']

explored: ['language.human_language.region', 'language.human_language.main_country', 'location.country.languages_spoken'] (score max 0.522)

explored: ['language.language_family.geographic_distribution', 'language.human_language.region', 'biology.breed_origin.breeds_originating_here', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'base.schemastaging.context_name.pronunciation', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'base.schemastaging.context_name.pronunciation', 'location.country.languages_spoken', 'language.human_language.countries_spoken_in', 'base.schemastaging.context_name.pronunciation'] (score max 0.306)

explored: ['language.language_family.member_of_language_families', 'language.language_family.languages', 'language.language_family.geographic_distribution', 'language.language_family.languages', 'location.country.languages_spoken', 'people.ethnicity.languages_spoken', 'language.language_family.languages', 'location.country.languages_spoken', 'people.ethnicity.languages_spoken', 'language.language_family.languages', 'location.country.languages_spoken', 'people.ethnicity.languages_spoken', 'location.country.languages_spoken', 'people.ethnicity.languages_spoken', 'location.country.official_language'] (score max 0.316)

explored: ['language.language_family.member_of_language_families', 'language.language_family.member_of_language_families', 'language.language_family.languages', 'language.language_family.member_of_language_families', 'language.language_family.member_of_language_families', 'language.human_language.language_family', 'language.language_family.member_of_language_families', 'language.language_family.member_of_language_families', 'language.language_family.languages', 'language.language_family.languages', 'language.human_language.language_family', 'language.human_language.main_country', 'language.language_family.languages', 'language.human_language.language_family', 'base.rosetta.languoid.languoid_class'] (score max 0.316)

verifier: grounded

---

## WebQTest-1289 (wrong)

**Q:** what type of music did mozart composed

**gold:** ['Classical music', 'Opera', 'Chamber music', 'Ballet', 'Art song']

**answer:** Wolfgang Amadeus Mozart composed works including opera, symphony, concerto, chamber music, piano sonata, and songs. Examples from the facts include Don Giovanni, The Magic Flute, Symphony No. 37, Piano Concerto No.24 in C minor, String Quartet No. 17, Piano Sonata No. 6, and Songs.

**entities:** ['Don Giovanni', 'The Magic Flute', 'Symphony No. 37', 'Piano Concerto No.24 in C minor', 'String Quartet No. 17', 'Piano Sonata No. 6', 'Songs']

plan: ['find the music composed by Mozart', 'find the type of #1']

explored: ['music.composition.composer', 'theater.theatrical_composer.plays_composed', 'theater.play.composer'] (score max 0.7)

explored: ['music.composition.composer', 'music.composition.language', 'opera.opera.language', 'music.composition.composer', 'music.composition.form', 'base.catalog.music_catalog_entry.cataloged_composition', 'music.composition.composer', 'music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composer.compositions', 'music.composition.form'] (score max 0.7)

explored: ['music.composition.composer', 'theater.theatrical_composer.plays_composed', 'theater.play.composer', 'music.composer.compositions', 'music.composition.composer', 'music.composition.lyricist', 'music.composer.compositions', 'music.composition.composer', 'music.composition.lyricist', 'music.composition.composer', 'music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composition.part_of', 'music.composition.form'] (score max 0.7)

explored: ['music.composition.form', 'music.composition.composer', 'base.catalog.music_catalog_entry.cataloged_composition', 'music.composition.composer', 'music.composition.includes', 'music.composition.part_of', 'music.composition.composer', 'music.composition.includes', 'base.catalog.music_catalog_entry.cataloged_composition', 'music.composition.composer', 'media_common.dedicated_work.dedication', 'media_common.dedication.work_dedicated', 'music.composition.composer', 'music.composition.place_composed', 'music.composition.includes'] (score max 0.46)

verifier: grounded

---

## WebQTest-873 (wrong)

**Q:** where does toronto get its water from

**gold:** ['Ashbridges Bay Wastewater Treatment Plant']

**answer:** Toronto gets its water from Lake Ontario.

**entities:** ['Lake Ontario']

plan: ['find the water source of Toronto']

explored: ['location.location.containedby', 'location.location.containedby', 'base.infrastructure.sewage_treatment_plant.serves_location_s'] (score max 0.467)

explored: ['location.location.containedby', 'location.location.contains', 'architecture.building.building_function', 'location.location.containedby', 'location.location.geolocation', 'travel.tourist_attraction.near_travel_destination', 'location.location.containedby', 'location.location.geolocation', 'location.location.street_address', 'location.location.containedby', 'metropolitan_transit.transit_line.stops', 'metropolitan_transit.transit_stop.transit_lines', 'location.location.containedby', 'location.location.geolocation', 'film.film.featured_film_locations'] (score max 0.197)

explored: ['geography.lake.cities', 'base.infrastructure.sewage_treatment_plant.serves_location_s', 'location.province.capital', 'location.statistical_region.renewable_freshwater_per_capita', 'location.location.primarily_containedby', 'location.location.primarily_containedby', 'geography.river.cities', 'location.location.primarily_containedby', 'location.location.partially_contained_by', 'location.location.containedby', 'location.location.containedby', 'location.location.contains', 'location.location.containedby', 'location.location.containedby', 'location.location.contains'] (score max 0.49)

verifier: grounded

---

## WebQTest-579 (hedge)

**Q:** where are the new orleans hornets moving to

**gold:** ['Charlotte']

**answer:** The answer could not be verified against the knowledge graph.

**entities:** []

plan: ['find the destination the New Orleans Hornets are moving to']

explored: ['sports.sports_team_location.teams', 'sports.sports_team.location', 'sports.sports_league_draft_pick.team'] (score max 0.334)

explored: ['sports.sports_team_location.teams', 'sports.sports_team.location', 'tv.tv_location.tv_shows_filmed_here', 'sports.sports_league_draft_pick.school', 'sports.school_sports_team.school', 'location.location.contains', 'sports.pro_athlete.teams', 'sports.sports_league_draft_pick.player', 'sports.sports_team_roster.player', 'sports.pro_athlete.teams', 'basketball.basketball_position.players', 'sports.sports_league_draft_pick.player', 'sports.sports_league_draft.picks', 'sports.sports_league_draft_pick.draft'] (score max 0.349)

explored: ['sports.sports_team_location.teams', 'sports.sports_team.location', 'sports.sports_facility.teams', 'sports.sports_team_location.teams', 'sports.sports_team.location', 'sports.sports_facility.teams', 'sports.sports_team_location.teams', 'sports.sports_team.location', 'sports.sports_team.sport', 'sports.sports_team_location.teams', 'sports.sports_team.location', 'sports.sports_league_draft_pick.team', 'tv.tv_location.tv_shows_filmed_here', 'tv.tv_program.filming_locations', 'tv.tv_program.original_network'] (score max 0.634)

backtrack: evaluator

explored: ['sports.sports_team_location.teams', 'sports.sports_team.location', 'tv.tv_location.tv_shows_filmed_here', 'sports.sports_league_draft_pick.school', 'sports.school_sports_team.school', 'location.location.contains', 'sports.pro_athlete.teams', 'sports.sports_league_draft_pick.player', 'sports.sports_team_roster.player', 'sports.pro_athlete.teams', 'basketball.basketball_position.players', 'sports.sports_league_draft_pick.player', 'sports.sports_league_draft.picks', 'sports.sports_league_draft_pick.draft'] (score max 0.349)

backtrack: evaluator

explored: ['location.place_with_neighborhoods.neighborhoods', 'location.location.nearby_airports', 'location.neighborhood.neighborhood_of', 'location.location.contains', 'location.location.geolocation', 'location.location.containedby', 'basketball.basketball_player.position_s', 'sports.drafted_athlete.drafted', 'people.person.profession', 'base.popstra.restaurant_choice.diner', 'sports.sports_team_roster.player', 'basketball.basketball_player.position_s'] (score max 0.241)

backtrack: evaluator

explored: ['sports.sports_team.venue', 'sports.sports_league_draft_pick.team', 'basketball.basketball_conference.teams', 'sports.sports_team.venue', 'basketball.basketball_conference.teams', 'sports.sports_team_roster.team', 'sports.sports_facility.teams', 'sports.sports_team.venue', 'sports.sports_league_participation.team', 'tv.tv_network_duration.program', 'tv.tv_program.spin_offs', 'tv.tv_program.country_of_origin'] (score max 0.531)

explored: ['sports.sports_facility.teams', 'location.location.events', 'location.location.geolocation', 'location.location.containedby', 'education.educational_institution.sports_teams', 'education.school_mascot.school', 'people.person.gender', 'people.person.ethnicity', 'people.person.nationality'] (score max 0.242)

verifier: unsupported

---

## WebQTest-172 (hedge)

**Q:** what do you call members of the senate

**gold:** ['Senator', 'Senate majority leader', 'President pro tempore', 'President of the Senate', 'Chief of staff', 'State Senator']

**answer:** William O'Connell Bradley, John B. Allen, and Randy Scheunemann are the only promising candidates provided, but from the facts above it could not be determined which one is the correct answer to what members of the senate are called.

**entities:** []

plan: ['find members of the senate', 'find what members of #1 are called']

explored: ['base.government2.legislative_position_held.legislative_body', 'government.government_position_held.governmental_body', 'business.employer.employees'] (score max 0.514)

explored: ['government.legislative_committee_membership.member', 'government.politician.legislative_committees_served_on', 'base.government2.legislator.legislative_positions_held', 'government.legislative_committee_membership.session', 'base.government2.legislative_position_held.legislative_sessions', 'government.government_position_held.legislative_sessions', 'base.government2.legislative_position_held.legislative_sessions', 'government.government_position_held.legislative_sessions', 'government.legislative_session.legislature', 'base.government2.legislative_position_held.legislative_sessions', 'government.government_position_held.legislative_sessions', 'government.legislative_session.legislature', 'base.government2.legislative_position_held.legislative_sessions', 'government.government_position_held.legislative_sessions', 'government.legislative_session.legislature'] (score max 0.364)

explored: ['government.legislative_committee.members', 'government.legislative_committee_membership.committee', 'government.legislative_committee.members', 'government.legislative_committee_membership.committee', 'government.legislative_committee.legislature', 'government.legislative_committee.members', 'government.legislative_committee_membership.committee', 'government.legislative_committee.members', 'government.legislative_committee_membership.committee', 'government.legislative_committee_membership.title', 'organization.organization_committee_title.members_with_this_title', 'organization.organization_committee_membership.title'] (score max 0.414)

explored: ['government.legislative_committee_membership.member', 'government.politician.legislative_committees_served_on', 'government.politician.government_positions_held', 'government.legislative_committee_membership.member', 'government.politician.legislative_committees_served_on', 'base.government2.legislator.legislative_positions_held', 'government.legislative_committee_membership.member', 'government.politician.legislative_committees_served_on', 'people.person.nationality', 'government.legislative_committee.members', 'government.legislative_committee_membership.committee', 'government.legislative_committee_membership.title', 'organization.organization_committee_title.members_with_this_title', 'organization.organization_committee_membership.title'] (score max 0.649)

verifier: grounded

---

## WebQTest-1233 (hedge)

**Q:** what are the colors of the ny giants

**gold:** ['Red', 'Grey', 'Blue', 'White']

**answer:** Could not be determined from the provided facts.

**entities:** []

plan: ['find the New York Giants', 'find the colors of #1']

explored: ['american_football.football_team.away_games', 'american_football.football_game.away_team', 'american_football.football_team.home_games'] (score max 0.565)

explored: ['american_football.game_passing_statistics.game', 'american_football.football_game.passing', 'american_football.football_game.receiving', 'american_football.game_passing_statistics.game', 'american_football.football_game.passing', 'american_football.football_game.receiving', 'american_football.game_passing_statistics.game', 'american_football.football_game.passing', 'american_football.football_game.receiving', 'american_football.game_passing_statistics.game', 'american_football.football_game.passing', 'american_football.football_game.receiving', 'american_football.game_passing_statistics.game', 'american_football.football_game.passing', 'american_football.football_game.receiving'] (score max 0.102)

backtrack: low_score

explored: ['american_football.game_receiving_statistics.game', 'american_football.football_game.home_team', 'american_football.game_rushing_statistics.game', 'american_football.game_receiving_statistics.game', 'american_football.football_game.home_team', 'american_football.game_rushing_statistics.game', 'american_football.game_receiving_statistics.game', 'american_football.football_game.home_team', 'american_football.game_rushing_statistics.game', 'american_football.game_receiving_statistics.game', 'american_football.football_game.home_team', 'american_football.game_rushing_statistics.game', 'american_football.game_receiving_statistics.game', 'american_football.football_game.home_team', 'american_football.game_rushing_statistics.game'] (score max 0.078)

backtrack: low_score

explored: ['american_football.football_game.season', 'american_football.football_team.home_games', 'american_football.football_game.away_team', 'american_football.football_game.season', 'american_football.football_team.home_games', 'american_football.football_game.away_team', 'american_football.football_game.season', 'american_football.football_team.home_games', 'american_football.football_game.away_team', 'american_football.football_game.season', 'american_football.football_team.home_games', 'american_football.football_game.away_team', 'american_football.football_game.season', 'american_football.football_team.home_games', 'american_football.football_game.away_team'] (score max 0.064)

backtrack: low_score

explored: ['american_football.football_game.rushing', 'american_football.football_team.away_games', 'american_football.football_game.rushing', 'american_football.football_team.away_games', 'american_football.football_game.rushing', 'american_football.football_team.away_games', 'american_football.football_game.rushing', 'american_football.football_team.away_games', 'american_football.football_game.rushing', 'american_football.football_team.away_games'] (score max 0.049)

verifier: grounded

---

## WebQTest-314 (hedge)

**Q:** what kind of government is sweden

**gold:** ['Parliamentary system', 'Hereditary monarchy', 'Unitary state', 'Constitutional monarchy', 'Representative democracy']

**answer:** It could not be determined from the provided facts what kind of government Sweden has.

**entities:** []

plan: ['find Sweden', 'find the kind of government of #1']

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.location.contains'] (score max 0.27)

explored: ['government.governmental_jurisdiction.governing_officials', 'government.government_position_held.jurisdiction_of_office', 'base.locations.states_and_provences.continent'] (score max 0.557)

backtrack: evaluator

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.continents.states_provinces_within'] (score max 0.209)

explored: ['government.form_of_government.countries', 'location.country.form_of_government', 'government.governmental_jurisdiction.government', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.governmental_jurisdiction.governing_officials', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.political_party.country', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.governmental_jurisdiction.governing_officials', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.governmental_jurisdiction.government'] (score max 0.731)

backtrack: evaluator

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.continents.states_provinces_within'] (score max 0.209)

backtrack: evaluator

explored: ['government.government.government_for', 'government.governmental_jurisdiction.governing_officials', 'government.governmental_jurisdiction.government_bodies', 'government.governmental_jurisdiction.government_bodies', 'government.governmental_jurisdiction.government_positions', 'base.aareas.schema.administrative_area_type.sovereignty', 'government.governmental_jurisdiction.government', 'government.government.government_for', 'government.governmental_jurisdiction.government_bodies', 'government.governmental_jurisdiction.government_bodies', 'government.governmental_jurisdiction.government_positions', 'base.aareas.schema.administrative_area_type.sovereignty', 'government.government.government_for', 'government.governmental_jurisdiction.governing_officials', 'government.governmental_jurisdiction.government_bodies'] (score max 0.302)

verifier: grounded

---

## WebQTest-1791 (hedge)

**Q:** when was the printing press invented by gutenberg

**gold:** ['1440']

**answer:** It could not be determined from the provided facts when the Printing press was invented by Johannes Gutenberg.

**entities:** []

plan: ['find the printing press invented by Gutenberg', 'find when #1 was invented']

explored: ['law.invention.inventor', 'law.inventor.inventions', 'base.ontologies.ontology_instance.equivalent_instances'] (score max 0.501)

explored: ['law.inventor.inventions', 'law.invention.inventor', 'base.argumentmaps.innovator.original_ideas', 'base.ontologies.ontology_instance_mapping.ontology', 'base.ontologies.ontology_class_mapping.ontology', 'base.ontologies.ontology.equivalent_classes'] (score max 0.572)

explored: ['law.invention.inventor', 'law.inventor.inventions', 'base.ontologies.ontology_instance.equivalent_instances', 'base.argumentmaps.innovator.original_ideas', 'tv.tv_program.country_of_origin', 'time.event.locations', 'location.location.contains', 'time.event.locations', 'symbols.namesake.named_after', 'location.location.contains', 'book.book_subject.works', 'base.ontologies.ontology_instance.equivalent_instances', 'base.ontologies.ontology_instance_mapping.freebase_topic'] (score max 0.579)

verifier: grounded

---

## WebQTest-1133 (hedge)

**Q:** what does wh smith stand for

**gold:** ['WHSmith']

**answer:** The answer could not be verified against the knowledge graph.

**entities:** []

plan: ['find what WH Smith stands for']

explored: ['people.person.spouse_s', 'government.political_party_tenure.politician', 'government.politician.party'] (score max 0.089)

backtrack: low_score

explored: ['people.marriage.spouse', 'people.person.gender', 'people.person.nationality'] (score max 0.06)

backtrack: low_score

explored: ['people.person.place_of_birth'] (score max 0.021)

backtrack: low_score

explored: [] (score max 0.0)

verifier: unsupported

explored: [] (score max 0.0)

verifier: unsupported

---

## WebQTest-893 (hedge)

**Q:** what is the zip code for azle texas

**gold:** ['76098', '76020']

**answer:** The zip code for Azle, Texas could not be determined from the provided facts.

**entities:** []

plan: ['find Azle, Texas', 'find the zip code for #1']

explored: ['location.location.containedby', 'location.location.contains', 'location.location.people_born_here'] (score max 0.506)

explored: ['location.mailing_address.postal_code', 'location.postal_code.country', 'location.administrative_division.first_level_division_of', 'location.statistical_region.rent50_1', 'location.statistical_region.rent50_3', 'location.statistical_region.rent50_2', 'location.statistical_region.rent50_1', 'location.statistical_region.rent50_3', 'location.statistical_region.rent50_2', 'location.administrative_division.first_level_division_of', 'location.location.containedby', 'location.location.containedby', 'location.location.people_born_here', 'people.person.place_of_birth', 'people.person.gender'] (score max 0.349)

explored: ['location.administrative_division.first_level_division_of', 'location.location.containedby', 'location.location.containedby', 'business.business_location.parent_company', 'book.book_subject.works', 'base.schemastaging.context_name.pronunciation', 'broadcast.tv_station.affiliations', 'broadcast.tv_station.former_callsign', 'organization.organization.headquarters'] (score max 0.243)

explored: ['location.mailing_address.postal_code', 'location.postal_code.country', 'location.mailing_address.citytown', 'base.wikipedia_infobox.settlement.area_code', 'location.location.containedby', 'location.location.time_zones', 'location.location.containedby', 'education.educational_institution.phone_number', 'organization.organization.headquarters', 'location.location.containedby', 'location.location.contains', 'education.educational_institution.campuses', 'location.location.containedby', 'location.location.contains', 'geography.mountain.mountain_range'] (score max 0.349)

verifier: grounded

---

## WebQTest-1353 (hedge)

**Q:** what are the four nations of the united kingdom

**gold:** ['Wales', 'Northern Ireland', 'Scotland', 'England']

**answer:** Could not be determined from the provided facts. The facts mention United Kingdom and United Kingdom, with Dependencies and Territories, but do not identify the four nations of the United Kingdom.

**entities:** []

plan: ['find the nations of the United Kingdom']

explored: ['base.unitednations.united_nations_member_state.member_of', 'base.aareas.schema.earth.sovereign_domain.sovereign_state', 'royalty.royal_line.kingdom_s_ruled'] (score max 0.586)

explored: ['location.country.first_level_divisions', 'location.country.administrative_divisions', 'location.administrative_division.country', 'royalty.royal_line.kingdom_s_ruled', 'royalty.monarch.royal_line', 'royalty.royal_line.succeeded_by', 'royalty.royal_line.kingdom_s_ruled', 'royalty.monarch.royal_line', 'royalty.royal_line.succeeded_by', 'base.unitednations.united_nations_body.members', 'base.unitednations.united_nations_body_membership.body', 'base.unitednations.united_nations_body.head'] (score max 0.542)

verifier: grounded

---

## WebQTest-336 (hedge)

**Q:** what currency should you take to morocco

**gold:** ['Moroccan dirham']

**answer:** The currency used in Morocco could not be determined from the provided facts.

**entities:** []

plan: ['find the country Morocco', 'find the currency used in #1']

explored: ['location.country.capital', 'base.locations.countries.continent', 'location.country.languages_spoken'] (score max 0.338)

explored: ['base.locations.countries.continent', 'base.locations.continents.planet', 'base.locations.continents.countries_within', 'base.givennames.given_name.language', 'location.country.official_language', 'language.human_language.countries_spoken_in', 'location.country.capital', 'location.location.contains', 'location.location.contains', 'location.country.official_language', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'language.human_language.countries_spoken_in', 'language.human_language.main_country', 'language.human_language.region'] (score max 0.177)

explored: ['finance.currency.countries_used', 'location.country.currency_used', 'location.statistical_region.military_expenditure_percent_gdp', 'finance.currency.countries_used', 'location.country.currency_used', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'finance.currency.countries_used', 'location.country.currency_used', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'location.country.currency_used', 'location.country.currency_formerly_used', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'base.mystery.cryptid_area_of_occurrence.cryptid_s_found_here', 'base.locations.countries.continent', 'base.mystery.cryptid.area_of_occurrence'] (score max 0.751)

verifier: grounded

---

## WebQTest-1399 (hedge)

**Q:** what products does the united states export

**gold:** ['Pharmaceutical Preparation', 'Automotive industry', 'Food Manufacturing', 'Industrial Organic Chemicals, NEC']

**answer:** The answer could not be verified against the knowledge graph.

**entities:** []

plan: ['find products exported by the United States']

explored: ['location.statistical_region.major_exports', 'location.statistical_region.major_imports', 'location.statistical_region.high_tech_as_percent_of_manufactured_exports'] (score max 0.696)

explored: ['location.imports_exports_by_industry.industry', 'business.product_category.products', 'business.business_operation.industry'] (score max 0.751)

explored: ['location.statistical_region.major_exports', 'location.statistical_region.major_imports', 'location.statistical_region.places_exported_to', 'location.statistical_region.major_exports', 'base.biblioness.bibs_location.country', 'travel.travel_destination.how_to_get_here', 'location.statistical_region.major_exports', 'base.biblioness.bibs_location.country', 'travel.travel_destination.how_to_get_here', 'business.product_category.products', 'business.consumer_company.brands', 'business.business_operation.industry', 'business.company_brand_relationship.company'] (score max 0.711)

explored: ['business.product_category.products', 'location.imports_exports_by_industry.industry', 'business.business_operation.industry', 'location.statistical_region.major_imports', 'location.statistical_region.major_exports', 'location.imports_and_exports.imported_from', 'location.imports_exports_by_industry.currency', 'location.imports_and_exports.currency', 'base.bioventurist.sales.currency', 'location.statistical_region.high_tech_as_percent_of_manufactured_exports', 'location.imports_and_exports.imported_from', 'location.imports_and_exports.exported_to', 'location.statistical_region.high_tech_as_percent_of_manufactured_exports', 'location.imports_and_exports.imported_from', 'location.imports_and_exports.exported_to'] (score max 0.588)

verifier: unsupported

---

## WebQTest-996 (hedge)

**Q:** where do ireland play rugby union

**gold:** ['Aviva Stadium']

**answer:** Could not be determined from the provided facts. The facts identify Ireland national rugby union team and its sport, but do not give a place where Ireland play rugby union.

**entities:** []

plan: ['find the rugby union team Ireland', 'find where #1 play']

explored: ['sports.sports_team.sport', 'base.rugby.rugby_club.coaches_of_this_team', 'base.rugby.rugby_coaching_tenure.team'] (score max 0.557)

explored: ['sports.sport.positions', 'sports.sports_position.sport', 'cvg.computer_game_subject.games', 'base.rugby.rugby_coach.coached_team_s', 'base.rugby.rugby_coach.type_of_rugby', 'base.rugby.rugby_coaching_tenure.coach'] (score max 0.264)

explored: ['sports.sports_position.sport', 'sports.sport.positions', 'american_football.football_player.position_s', 'sports.sports_position.sport', 'sports.sport.positions', 'sports.sports_team_roster.position', 'sports.sports_position.sport', 'sports.sport.positions', 'sports.sports_team_roster.position', 'sports.sports_position.sport', 'sports.sport.positions', 'sports.sports_team_roster.position', 'sports.sport.positions'] (score max 0.532)

explored: ['american_football.football_player.position_s', 'american_football.football_player.games', 'american_football.player_game_statistics.player', 'sports.sports_position.sport', 'sports.sport.positions', 'cvg.computer_game_subject.games', 'sports.sports_position.sport', 'sports.sports_team.sport', 'sports.sports_position.sport', 'sports.sport.positions', 'cvg.computer_game_subject.games', 'sports.sports_position.sport', 'sports.sport.positions', 'cvg.computer_game_subject.games'] (score max 0.515)

verifier: grounded

---

## WebQTest-462 (hedge)

**Q:** what time is it in texas houston right now

**gold:** ['Central Time Zone']

**answer:** Could not be determined from the provided facts.

**entities:** []

plan: ['find Houston in Texas', 'find the current time in #1']

explored: ['base.biblioness.bibs_location.state', 'location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods'] (score max 0.453)

explored: ['location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.location.geolocation', 'location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.location.geolocation', 'location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.location.geolocation', 'location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.location.geolocation', 'location.location.contains', 'location.location.geolocation', 'base.locations.states_and_provences.country'] (score max 0.513)

explored: ['location.hud_county_place.county', 'location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.location.nearby_airports', 'location.location.nearby_airports', 'location.location.geolocation', 'location.us_county.hud_county_place', 'location.location.nearby_airports', 'location.location.geolocation', 'location.us_county.hud_county_place', 'location.location.contains_major_portion_of', 'location.location.contains', 'location.location.contains'] (score max 0.486)

explored: ['location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.location.geolocation', 'location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.location.geolocation', 'location.location.geolocation', 'location.location.nearby_airports', 'location.us_county.hud_county_place', 'location.us_county.hud_county_place', 'location.hud_county_place.county', 'location.us_county.county_seat', 'location.us_county.hud_county_place', 'location.hud_county_place.county', 'location.us_county.county_seat'] (score max 0.243)

verifier: grounded

---

## WebQTest-379 (hedge)

**Q:** what year does hitler die

**gold:** ['1945-04-30']

**answer:** It could not be determined from the provided facts what year Adolf Hitler died.

**entities:** []

plan: ['find the year Hitler died']

explored: ['people.deceased_person.place_of_death', 'people.deceased_person.cause_of_death', 'base.jewlib.research_collection.originators'] (score max 0.472)

explored: ['people.deceased_person.cause_of_death', 'people.cause_of_death.includes_causes_of_death', 'base.fictionaluniverse.deceased_fictional_character.cause_of_death', 'people.deceased_person.cause_of_death', 'people.cause_of_death.includes_causes_of_death', 'base.fictionaluniverse.deceased_fictional_character.cause_of_death', 'people.deceased_person.place_of_death', 'people.deceased_person.place_of_burial', 'time.event.locations', 'base.jewlib.research_collection.collection_held_by', 'base.jewlib.research_collection.online_catalogs', 'base.jewlib.research_collection.originators'] (score max 0.497)

verifier: unsupported

explored: ['people.deceased_person.cause_of_death', 'people.deceased_person.place_of_death', 'base.jewlib.research_collection.originators'] (score max 0.463)

verifier: grounded

---

## WebQTest-788 (hedge)

**Q:** what is the holy book of the buddhist religion

**gold:** ['Gangōji Garan Engi', 'Longchen Nyingthig', 'Chinese Buddhist canon', 'Nīlakaṇṭha Dhāraṇī', 'Mahāvastu', 'Pāli Canon', 'Dhammapada', 'Āgama', 'Amitabha Sutra', 'Uṣṇīṣa Vijaya Dhāraṇī Sūtra', 'Vimalakirti Sutra', 'Śrīmālādevī Siṃhanāda Sūtra', 'Mahāyāna sūtras', 'Tibetan Buddhist canon']

**answer:** Buddhism has several holy texts, including Pāli Canon, Mahāyāna sūtras, Tibetan Buddhist canon, Chinese Buddhist canon, Dhammapada, and Amitabha Sutra. If you mean a single holy book, it could not be determined from the facts provided.

**entities:** []

plan: ['find the buddhist religion', 'find the holy book of #1']

explored: ['religion.religion.includes', 'religion.religion.includes', 'religion.monastery.religion'] (score max 0.687)

explored: ['religion.religion.texts', 'religion.religious_text.religious_text_of', 'religion.religion.branched_from', 'religion.religion.texts', 'religion.religious_text.religious_text_of', 'religion.religion.branched_from', 'religion.religion.includes', 'religion.religion.is_part_of', 'base.schemastaging.context_name.pronunciation', 'religion.religion.includes', 'religion.religion.places_of_worship', 'religion.place_of_worship.religion', 'religion.religion.includes', 'religion.religion.is_part_of'] (score max 0.66)

explored: ['religion.religion.texts', 'religion.religion.texts', 'religion.religion.texts', 'religion.religious_text.religious_text_of', 'base.schemastaging.context_name.pronunciation', 'religion.religion.texts', 'religion.religion.texts', 'religion.religious_text.religious_text_of', 'book.author.works_written'] (score max 0.66)

explored: ['religion.religion.texts', 'religion.religious_text.religious_text_of', 'religion.religion.branched_from', 'religion.religion.texts', 'religion.religious_text.religious_text_of', 'religion.monastery.religious_order', 'religion.religion.texts', 'religion.religious_text.religious_text_of', 'religion.religion.branched_from', 'religion.religion.texts', 'religion.religion.branched_from', 'religion.religion.branched_from', 'religion.religious_text.religious_text_of', 'religion.religion.branched_into', 'religion.religion.includes'] (score max 0.66)

verifier: grounded

---

## WebQTest-16 (hedge)

**Q:** what countries are part of the uk

**gold:** ['Wales', 'Northern Ireland', 'Scotland', 'England']

**answer:** The United Kingdom is part of Europe. The facts do not determine any countries that are part of the UK.

**entities:** []

plan: ['find the UK', 'find countries that are part of #1']

explored: ['location.country.internet_tld', 'base.locations.countries.continent', 'location.country.form_of_government'] (score max 0.312)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.location.partially_contains', 'location.country.form_of_government', 'base.ontologies.ontology_instance_mapping.freebase_topic', 'base.ontologies.ontology_instance.equivalent_instances', 'location.country.internet_tld', 'internet.top_level_domain_status.domains', 'internet.top_level_domain.status', 'location.country.internet_tld', 'internet.top_level_domain.status', 'internet.top_level_domain.domain_type', 'location.country.internet_tld', 'internet.top_level_domain.status', 'internet.top_level_domain.domain_type'] (score max 0.661)

verifier: grounded

---

## WebQTest-231 (hedge)

**Q:** when did florida marlins join mlb

**gold:** ['1994 Major League Baseball Season']

**answer:** Could not be determined from the provided facts. The facts only show that Miami Marlins are in the National League and list historical managers, but they do not give when Florida Marlins joined MLB.

**entities:** []

plan: ['find when the Florida Marlins joined MLB']

explored: ['baseball.baseball_team.historical_managers', 'baseball.baseball_historical_managerial_position.team', 'baseball.baseball_league.teams'] (score max 0.348)

explored: ['baseball.baseball_manager.former_teams_managed', 'baseball.baseball_historical_managerial_position.manager', 'baseball.baseball_player.position_s', 'baseball.baseball_manager.former_teams_managed', 'baseball.baseball_historical_managerial_position.manager', 'baseball.baseball_player.position_s', 'baseball.baseball_manager.former_teams_managed', 'baseball.baseball_manager.current_team_managed', 'baseball.baseball_team.current_manager', 'baseball.baseball_manager.former_teams_managed', 'baseball.baseball_manager.current_team_managed', 'baseball.baseball_team.current_manager', 'baseball.baseball_league.teams', 'baseball.baseball_team.league', 'baseball.baseball_league.sports_league'] (score max 0.365)

explored: ['baseball.baseball_team.historical_managers', 'baseball.baseball_historical_managerial_position.team', 'baseball.baseball_league.teams', 'baseball.baseball_team.historical_managers', 'baseball.baseball_historical_managerial_position.team', 'baseball.baseball_league.teams', 'baseball.baseball_team.historical_managers', 'baseball.baseball_historical_managerial_position.team', 'baseball.baseball_league.teams', 'baseball.baseball_team.historical_managers', 'baseball.baseball_historical_managerial_position.team', 'baseball.baseball_league.teams', 'baseball.baseball_team.historical_managers', 'baseball.baseball_historical_managerial_position.team', 'baseball.baseball_league.teams'] (score max 0.348)

explored: ['baseball.baseball_manager.former_teams_managed', 'baseball.baseball_historical_managerial_position.manager', 'baseball.baseball_player.position_s', 'baseball.baseball_manager.former_teams_managed', 'baseball.baseball_historical_managerial_position.manager', 'baseball.baseball_player.position_s', 'baseball.baseball_manager.former_teams_managed', 'baseball.baseball_manager.current_team_managed', 'baseball.baseball_team.current_manager', 'baseball.baseball_manager.former_teams_managed', 'baseball.baseball_manager.current_team_managed', 'baseball.baseball_team.current_manager', 'baseball.baseball_manager.former_teams_managed', 'baseball.baseball_historical_managerial_position.manager', 'baseball.baseball_player.position_s'] (score max 0.365)

verifier: grounded

---

## WebQTest-329 (hedge)

**Q:** what type of government was formed when italy unified

**gold:** ['Unitary state', 'Parliamentary republic', 'Constitutional republic']

**answer:** It could not be determined from the provided facts what type of government was formed when Italy unified.

**entities:** []

plan: ['find the event of Italy unifying', 'find the type of government formed in #1']

explored: ['base.culturalevent.event.entity_involved', 'time.event.locations', 'sports.multi_event_tournament.participating_countries'] (score max 0.31)

explored: ['time.event.locations'] (score max 0.01)

backtrack: low_score

explored: [] (score max 0.0)

backtrack: dead_end

explored: [] (score max 0.0)

backtrack: dead_end

explored: [] (score max 0.0)

verifier: grounded

---

## WebQTest-663 (hedge)

**Q:** what age did william penn get married

**gold:** ['1672-04-04']

**answer:** It could not be determined from the provided facts what age William Penn got married.

**entities:** []

plan: ['find when William Penn got married', 'find the age of William Penn at #1']

explored: ['people.marriage.spouse', 'people.person.spouse_s', 'people.person.employment_history'] (score max 0.526)

explored: ['people.marriage.spouse', 'people.person.spouse_s', 'people.person.place_of_birth', 'people.marriage.spouse', 'people.person.spouse_s', 'people.marriage.type_of_union', 'book.author.works_written', 'media_common.quotation.subjects', 'book.author.works_written', 'organization.organization_relationship.child', 'book.book_subject.works'] (score max 0.526)

explored: ['people.marriage.spouse', 'people.person.spouse_s', 'people.person.employment_history', 'people.marriage.spouse', 'people.person.spouse_s', 'book.author.works_written', 'people.marriage.spouse', 'people.person.spouse_s', 'government.political_party_tenure.politician', 'people.marriage.spouse', 'people.person.spouse_s', 'award.award_honor.award_winner', 'people.marriage.type_of_union', 'book.author.works_written', 'media_common.quotation.subjects'] (score max 0.541)

explored: ['people.marriage.spouse', 'people.person.spouse_s', 'people.person.place_of_birth', 'people.marriage.spouse', 'people.person.spouse_s', 'people.marriage.spouse', 'people.person.spouse_s', 'book.author.works_written', 'people.marriage.type_of_union', 'book.author.works_written', 'media_common.quotation.subjects'] (score max 0.241)

verifier: grounded

---

## WebQTest-1226 (hedge)

**Q:** what form of government does australia use

**gold:** ['Parliamentary system', 'Federal monarchy', 'Constitutional monarchy']

**answer:** Could not be determined from the provided facts.

**entities:** []

plan: ['find Australia', 'find the form of government used by #1']

explored: ['location.country.internet_tld', 'cricket.cricket_team.country', 'location.country.capital'] (score max 0.291)

explored: ['organization.organization.geographic_scope', 'location.administrative_division_capital_relationship.capital', 'base.ontologies.ontology_instance.equivalent_instances', 'location.country.internet_tld', 'internet.top_level_domain.status', 'cricket.cricket_team.country', 'award.award_nominee.award_nominations', 'award.award_nomination.award_nominee', 'cricket.cricket_team.country', 'sports.sports_team.sport', 'sports.sports_team_roster.team'] (score max 0.156)

explored: ['organization.organization.legal_structure', 'organization.organization.geographic_scope', 'organization.organization.sectors', 'organization.organization.geographic_scope', 'organization.organization_scope.organizations_with_this_scope', 'organization.organization.headquarters', 'organization.organization.geographic_scope', 'organization.organization_scope.organizations_with_this_scope', 'organization.organization.headquarters', 'organization.organization.geographic_scope', 'organization.organization_scope.organizations_with_this_scope', 'organization.organization.geographic_scope', 'organization.organization.sectors', 'organization.organization_scope.organizations_with_this_scope'] (score max 0.451)

backtrack: evaluator

explored: ['organization.organization.geographic_scope', 'location.administrative_division_capital_relationship.capital', 'base.ontologies.ontology_instance.equivalent_instances', 'location.country.internet_tld', 'internet.top_level_domain.status', 'cricket.cricket_team.country', 'award.award_nominee.award_nominations', 'award.award_nomination.award_nominee', 'cricket.cricket_team.country', 'sports.sports_team.sport', 'sports.sports_team_roster.team'] (score max 0.156)

backtrack: evaluator

explored: ['base.aareas.schema.administrative_area.capital', 'location.capital_of_administrative_division.capital_of', 'organization.organization_scope.organizations_with_this_scope', 'sports.sports_team.sport', 'sports.sports_team.championships', 'sports.sports_team_location.teams', 'sports.sports_team.roster', 'sports.sports_team_location.teams', 'sports.team_venue_relationship.team'] (score max 0.145)

backtrack: evaluator

explored: ['organization.organization.founders', 'organization.organization_scope.organizations_with_this_scope', 'organization.organization_sector.organizations_in_this_sector', 'organization.organization.email', 'organization.organization.phone_number', 'business.employer.number_of_employees', 'organization.organization.email', 'organization.organization_sector.organizations_in_this_sector', 'base.services.insurance_service.insurance_type', 'organization.organization.headquarters'] (score max 0.147)

verifier: grounded

---

## WebQTest-38 (hedge)

**Q:** who did george w. bush run against for the second term

**gold:** ['John Kerry', 'Ralph Nader', 'Michael Peroutka', 'Gene Amondson']

**answer:** The answer could not be verified against the knowledge graph.

**entities:** []

plan: ['find the second-term election that George W. Bush ran in', 'find who George W. Bush ran against in #1']

explored: ['government.election_campaign.candidate', 'government.politician.election_campaigns', 'government.election.winner'] (score max 0.595)

explored: ['government.election_campaign.candidate', 'government.election_campaign.election', 'government.politician.election_campaigns'] (score max 0.629)

explored: ['government.election.campaigns', 'government.election_campaign.election', 'government.general_election.contests', 'government.election_campaign.candidate', 'government.politician.election_campaigns', 'base.politicalconventions.presidential_nominee.nominated_at'] (score max 0.602)

verifier: unsupported

explored: ['government.election_campaign.candidate', 'government.politician.election_campaigns', 'base.politicalconventions.presidential_nominee.nominated_at'] (score max 0.609)

verifier: unsupported

---

