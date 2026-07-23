## WebQTrn-1484_1fbd766e1b1bf978da23e8646cadf3a1 (wrong)

**Q:** The person who attended the education institution Colegio AlemÃ¡n Alexander von Humboldt did what kind of paintings?

**gold:** ['Magic realism', 'Modern art', 'Surrealism']

**answer:** Frida Kahlo did paintings such as Self-Portrait, The Two Fridas, Henry Ford Hospital, and Viva la Vida, Watermelons.

**entities:** ['Frida Kahlo']

plan: ['find the person who attended Colegio AlemÃ¡n Alexander von Humboldt', 'find what kind of paintings #1 did']

explored: ['education.educational_institution.students_graduates', 'education.education.institution', 'symbols.namesake.named_after'] (score max 0.416)

explored: ['visual_art.artwork.artist', 'visual_art.visual_artist.artworks', 'visual_art.artwork.art_subject'] (score max 0.596)

verifier: grounded

---

## WebQTest-1000_7457bb008a1da743b19ff9ce3a5cac63 (wrong)

**Q:** Which countries included in Oceania, had a population of less than 523000?

**gold:** ['Tonga', 'Samoa', 'Northern Mariana Islands', 'Solomon Islands', 'Guam', 'New Caledonia', 'Marshall Islands', 'Vanuatu', 'Kiribati', 'Fiji', 'Cook Islands']

**answer:** The countries included in Oceania that had a population of less than 523000 were Nauru, Tuvalu, and Norfolk Island.

**entities:** ['Nauru', 'Tuvalu', 'Norfolk Island']

plan: ['find countries included in Oceania', 'find which of #1 had a population of less than 523000']

explored: ['location.location.contains', 'location.location.contains', 'location.statistical_region.population'] (score max 0.557)

explored: ['location.statistical_region.population', 'location.location.people_born_here', 'language.human_language.countries_spoken_in', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'location.statistical_region.literacy_rate', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'location.statistical_region.official_development_assistance', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'people.ethnicity.geographic_distribution', 'location.country.administrative_divisions', 'location.location.containedby', 'location.administrative_division.country'] (score max 0.541)

explored: ['people.ethnicity.geographic_distribution', 'people.ethnicity.population', 'people.ethnicity.included_in_group', 'people.ethnicity.geographic_distribution', 'people.ethnicity.included_in_group', 'people.ethnicity.languages_spoken', 'people.ethnicity.geographic_distribution', 'people.ethnicity.included_in_group', 'people.ethnicity.languages_spoken', 'people.ethnicity.geographic_distribution', 'people.ethnicity.population', 'people.ethnicity.included_in_group', 'measurement_unit.dated_percentage.source'] (score max 0.217)

explored: ['location.statistical_region.population', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'people.ethnicity.geographic_distribution', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'people.ethnicity.geographic_distribution', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'people.ethnicity.geographic_distribution', 'location.statistical_region.internet_users_percent_population', 'location.statistical_region.renewable_freshwater_per_capita', 'people.ethnicity.geographic_distribution'] (score max 0.541)

verifier: grounded

---

## WebQTrn-2871_4c5dc1332d9eba8fde58e7b9561d4ae3 (wrong)

**Q:** Which state has the position title of Mayor is near the Grand Canyon?

**gold:** ['Phoenix', 'Phoenix']

**answer:** Arizona

**entities:** ['Arizona']

plan: ['find the place near the Grand Canyon', 'find the state of #1', 'find the position title of Mayor in #2']

explored: ['location.location.geolocation', 'location.location.nearby_airports', 'location.location.containedby', 'fictional_universe.fictional_character.places_lived', 'fictional_universe.fictional_setting.characters_that_have_lived_here', 'base.fictionaluniverse.deceased_fictional_character.place_of_death'] (score max 0.573)

explored: ['location.location.nearby_airports', 'location.location.geolocation', 'location.location.containedby', 'location.location.geolocation', 'travel.tourist_attraction.near_travel_destination', 'location.location.containedby', 'location.location.geolocation', 'location.location.partiallycontains', 'base.popstra.vacation_choice.location', 'location.location.geolocation', 'location.location.primarily_containedby', 'location.location.primarily_containedby', 'location.location.contains', 'fictional_universe.fictional_universe.locations', 'fictional_universe.fictional_character.places_lived'] (score max 0.509)

explored: ['location.location.geolocation', 'location.location.nearby_airports', 'location.location.containedby', 'location.location.geolocation', 'location.location.nearby_airports', 'location.location.containedby'] (score max 0.504)

explored: ['government.government_office_or_title.jurisdiction', 'government.governmental_jurisdiction.government_positions', 'government.government_position_held.district_represented'] (score max 0.318)

verifier: grounded

---

## WebQTest-965_e91a95bd503f0704b9cc40c6f2139524 (wrong)

**Q:** "Laziness may appear attractive but work gives satisfaction," was said by a person who went to what school?

**gold:** ['Montessori Lyceum Amsterdam', 'Jewish Lyceum']

**answer:** Anne Frank went to Montessori Lyceum Amsterdam and Jewish Lyceum.

**entities:** ['Anne Frank']

plan: ['find the person who said "Laziness may appear attractive but work gives satisfaction"', 'find the school attended by #1']

explored: ['media_common.quotation.author', 'people.person.quotations', 'media_common.quotation.subjects'] (score max 0.501)

explored: ['education.education.student', 'people.person.education', 'people.place_of_interment.interred_here'] (score max 0.504)

verifier: grounded

---

## WebQTest-12_7b54b31f3e5a6273f4fd2a20e565ec6d (wrong)

**Q:** Who was the Governor of Ohio that held his position from before 1-10-2011?

**gold:** ['Return J. Meigs, Jr.', 'Ted Strickland', 'John Kasich']

**answer:** James Rudolph Garfield was the Governor of Ohio before 1-10-2011.

**entities:** ['James Rudolph Garfield']

plan: ['find the Governor of Ohio who held the position before 1-10-2011']

explored: ['organization.role.governors', 'government.government_position_held.office_position_or_title', 'government.government_office_or_title.office_holders', 'government.government_position_held.jurisdiction_of_office', 'government.government_position_held.district_represented', 'government.election.district'] (score max 0.564)

verifier: grounded

---

## WebQTrn-683_7584ba13fff133af09542211fd90a33d (wrong)

**Q:** Who is the actor tha tplayed Hawkeye in the film starred by Katarzyna Ancuta?

**gold:** ['Jeremy Renner']

**answer:** Chris Hemsworth played Hawkeye in The Avengers.

**entities:** ['Chris Hemsworth']

plan: ['find the film starred by Katarzyna Ancuta', 'find the actor who played Hawkeye in #1']

explored: ['film.film_crewmember.films_crewed', 'film.film_crew_gig.crewmember', 'film.film_character.portrayed_in_films', 'film.performance.character', 'tv.tv_character.appeared_in_tv_program'] (score max 0.469)

explored: ['film.film.starring', 'film.film.film_casting_director', 'film.film.personal_appearances'] (score max 0.489)

verifier: grounded

---

## WebQTrn-1812_82e069064d66663276c549f47e5e179d (wrong)

**Q:** What countries are in the Atlantic Time Zone in the Caribbean?

**gold:** ['British Virgin Islands', 'Netherlands Antilles']

**answer:** The countries in the Atlantic Time Zone in the Caribbean that could be determined from the facts are Dominican Republic, Trinidad and Tobago, and Bermuda. The facts also mention Netherlands and Canada, but they are not Caribbean countries.

**entities:** ['Dominican Republic', 'Trinidad and Tobago', 'Bermuda']

plan: ['find countries in the Atlantic Time Zone', 'find which of #1 are in the Caribbean']

explored: ['location.location.time_zones', 'time.time_zone.day_dst_begins', 'time.time_zone.day_dst_ends', 'time.event.locations', 'location.location.geolocation', 'organization.organization.geographic_scope', 'film.film.country', 'film.film_regional_release_date.film', 'broadcast.radio_station.format'] (score max 0.749)

explored: ['base.locations.countries.planet', 'base.locations.countries.states_provinces_within', 'base.locations.countries.continent', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.country.languages_spoken'] (score max 0.307)

explored: ['base.locations.countries.planet', 'base.locations.planets.countries_within', 'base.locations.continents.planet', 'base.locations.countries.states_provinces_within', 'base.biblioness.bibs_location.country', 'base.locations.states_and_provences.country', 'base.locations.countries.states_provinces_within', 'base.biblioness.bibs_location.country', 'base.locations.states_and_provences.country', 'base.locations.countries.states_provinces_within', 'base.biblioness.bibs_location.country', 'base.locations.states_and_provences.country', 'base.locations.countries.states_provinces_within', 'base.biblioness.bibs_location.country', 'base.locations.states_and_provences.country'] (score max 0.307)

verifier: grounded

---

## WebQTrn-25_2a2de50d3b65cc5d2c88f54e283a4b8a (wrong)

**Q:** What movie featured Taylor Lautner and was released straight to video?

**gold:** ['Shadow Fury', 'Shadow Fury']

**answer:** Abduction

**entities:** ['Abduction']

plan: ['find the movie that featured Taylor Lautner', 'find which of #1 were released straight to video']

explored: ['film.actor.film', 'film.performance.actor', 'film.personal_film_appearance.person', 'film.film.film_format', 'film.film_film_distributor_relationship.film_distribution_medium', 'film.film_regional_release_date.film_release_distribution_medium'] (score max 0.623)

explored: ['film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film_film_distributor_relationship.film', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.story_by', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.story_by', 'film.film.edited_by', 'film.film.written_by', 'film.film.produced_by', 'film.film.produced_by', 'film.film.starring', 'film.producer.film'] (score max 0.319)

explored: ['film.film_regional_release_date.film_release_distribution_medium', 'base.mediapackage.video_release.consumer_releases', 'base.mediapackage.media_release.video_contents', 'film.film_regional_release_date.film_release_distribution_medium', 'film.film_regional_release_date.film_regional_debut_venue', 'film.film_film_distributor_relationship.film_distribution_medium', 'film.film.story_by', 'music.music_video_subject.subject_in_these_music_videos', 'film.film.featured_film_locations', 'film.film.featured_film_locations', 'tv.tv_program.filming_locations', 'film.film_regional_release_date.film_release_region', 'film.film_regional_release_date.film_release_region', 'film.film.produced_by', 'time.event.locations'] (score max 0.528)

explored: ['film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.edited_by', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.edited_by', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.story_by', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film.story_by', 'film.film.release_date_s', 'film.film_regional_release_date.film', 'film.film_film_distributor_relationship.film'] (score max 0.319)

verifier: grounded

---

## WebQTest-212_7905d5d52ac1a17f68996d4a2245e682 (wrong)

**Q:** What state does the Colorado River run through that has a governmental jurisdiction location symbol adapted the earliest?

**gold:** ['Phoenix']

**answer:** Colorado

**entities:** ['Colorado']

plan: ['find the states that the Colorado River runs through', 'find which of #1 has the earliest adapted governmental jurisdiction location symbol']

explored: ['location.location.partially_contains', 'location.location.partially_contained_by', 'location.partial_containment_relationship.partially_contains'] (score max 0.436)

explored: ['government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country'] (score max 0.647)

explored: ['location.symbol_of_administrative_division.official_symbol_of', 'location.location_symbol_relationship.symbol', 'biology.organism_classification.lower_classifications', 'location.symbol_of_administrative_division.official_symbol_of', 'location.location_symbol_relationship.symbol', 'location.location_symbol_relationship.Kind_of_symbol', 'location.offical_symbol_variety.symbols_of_this_kind', 'location.location_symbol_relationship.Kind_of_symbol', 'location.offical_symbol_variety.symbols_of_this_kind', 'location.location_symbol_relationship.Kind_of_symbol', 'location.offical_symbol_variety.symbols_of_this_kind'] (score max 0.31)

explored: ['government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'government.governmental_jurisdiction.official_symbols', 'location.us_state.capital', 'base.locations.states_and_provences.country', 'location.location_symbol_relationship.Kind_of_symbol', 'location.offical_symbol_variety.symbols_of_this_kind', 'location.location_symbol_relationship.Kind_of_symbol', 'location.offical_symbol_variety.symbols_of_this_kind'] (score max 0.674)

verifier: grounded

---

## WebQTrn-493_590fff78c30981ef9566ad54a453d002 (wrong)

**Q:** Where does the breed Schipperke originated from?

**gold:** ['Europe', 'Eurasia', 'Western Europe']

**answer:** Schipperke originated from Belgium.

**entities:** ['Belgium']

plan: ['find the origin of the breed Schipperke']

explored: ['biology.animal_breed.place_of_origin', 'biology.breed_origin.breeds_originating_here', 'biology.breed_registration.breed'] (score max 0.742)

verifier: grounded

---

## WebQTest-1178_09e61020934818b85641a22821e7a455 (wrong)

**Q:** Where is the Strictly 4 My N.I.G.G.A.Z. producer originally from?

**gold:** ['East Harlem']

**answer:** Marin City

**entities:** ['Marin City']

plan: ['find the producer of Strictly 4 My N.I.G.G.A.Z.', 'find where #1 is originally from']

explored: ['music.producer.releases_produced', 'music.recording.releases'] (score max 0.588)

explored: ['location.location.people_born_here', 'music.artist.origin', 'people.person.places_lived'] (score max 0.532)

verifier: grounded

---

## WebQTrn-1297_a0da13a7b70a064b8cffb58007f6739d (wrong)

**Q:** Where did the artist grow up that recorded #Thatpower?

**gold:** ['London']

**answer:** Justin Bieber grew up in Stratford and Canada.

**entities:** ['Stratford', 'Canada']

plan: ['find the artist that recorded #Thatpower', 'find where #1 grew up']

explored: ['music.recording.artist', 'music.featured_artist.recordings', 'music.recording.featured_artists'] (score max 0.645)

explored: ['people.place_lived.person', 'people.person.place_of_birth', 'people.person.places_lived', 'people.place_lived.person', 'people.person.place_of_birth', 'people.person.places_lived'] (score max 0.504)

verifier: grounded

---

## WebQTrn-2006_7993a79baca778d4e8e6cb2b1882bca4 (wrong)

**Q:** What magazine, published in 1841, once employed Edgar Allen Poe?

**gold:** ["Burton's Gentleman's Magazine"]

**answer:** Graham's Magazine

**entities:** ["Graham's Magazine"]

plan: ['find the magazine published in 1841 that once employed Edgar Allan Poe']

explored: ['book.periodical_editor.periodicals_edited', 'book.editorial_tenure.editor', 'book.author.book_editions_published'] (score max 0.526)

explored: ['book.periodical_subject.periodicals', 'book.periodical.subjects', 'book.periodical.editorial_staff', 'book.periodical.editorial_staff', 'book.editorial_tenure.periodical', 'book.periodical.editorial_staff', 'book.editorial_tenure.periodical', 'book.written_work.subjects', 'book.book_subject.works', 'book.editorial_tenure.title', 'book.editorial_tenure.title', 'fictional_universe.fictional_character.occupation', 'fictional_universe.character_occupation.characters_with_this_occupation'] (score max 0.562)

verifier: grounded

---

## WebQTrn-1841_5d1cba94c816bec220b9f98e97493b0f (wrong)

**Q:** What nominee of the Laureus World Sports Award for Team of the Year represents a popular sport in Spain?

**gold:** ['Spain national football team', 'Spain national football team', 'Spain national football team']

**answer:** FC Barcelona represents a popular sport in Spain.

**entities:** ['FC Barcelona']

plan: ['find nominees of the Laureus World Sports Award for Team of the Year', 'find which of #1 represent a popular sport in Spain']

explored: ['award.award_category.nominees', 'award.award_category.winners', 'award.award_nomination.award', 'sports.sport_country.athletes', 'sports.competitor_competition_relationship.country', 'olympics.olympic_athlete_affiliation.country'] (score max 0.696)

explored: ['award.award_ceremony.nominees', 'award.award_nomination.ceremony', 'award.award_ceremony.awards_presented', 'award.award_ceremony.nominees', 'award.award_nomination.ceremony', 'award.award_ceremony.awards_presented', 'award.award_nominee.award_nominations', 'award.award_nomination.award_nominee', 'sports.sports_team.sport', 'award.award_nominee.award_nominations', 'award.award_nomination.award_nominee', 'base.formula1.formula_1_season.constructors_champion'] (score max 0.7)

explored: ['award.award_category.nominees', 'award.award_category.winners', 'award.award_nomination.award', 'sports.sports_award.team', 'award.award_nominee.award_nominations', 'award.award_honor.award_winner', 'sports.sports_award_winner.awards', 'sports.sports_award.award_winner', 'award.award_nominee.award_nominations', 'sports.sports_award_winner.awards', 'sports.sports_award.award_winner', 'award.award_nominee.award_nominations'] (score max 0.696)

explored: ['award.award_ceremony.nominees', 'award.award_nomination.ceremony', 'award.award_ceremony.awards_presented', 'award.award_ceremony.nominees', 'award.award_nomination.ceremony', 'award.award_ceremony.awards_presented', 'award.award_nominee.award_nominations', 'award.award_nomination.award_nominee', 'sports.sports_team.sport', 'award.award_nominee.award_nominations', 'award.award_nomination.award_nominee', 'base.formula1.formula_1_season.constructors_champion'] (score max 0.7)

verifier: grounded

---

## WebQTrn-3100_d059b24adec4064377b957ca598769be (wrong)

**Q:** What part is the country with the capital named Santo Domingo?

**gold:** ['Greater Antilles', 'Latin America', 'North America', 'Americas', 'País']

**answer:** The country with the capital named Santo Domingo is Dominican Republic.

**entities:** ['Dominican Republic']

plan: ['find the country with the capital named Santo Domingo', 'find the part of #1']

explored: ['location.country.capital', 'location.capital_of_administrative_division.capital_of', 'location.administrative_division_capital_relationship.capital'] (score max 0.675)

explored: ['location.country.administrative_divisions', 'location.country.first_level_divisions', 'location.administrative_division.country'] (score max 0.553)

verifier: grounded

---

## WebQTrn-2784_025fdfafd914ff922ab8144f527c06ec (wrong)

**Q:** In what films does the lyracist for "Panther Power" appear?

**gold:** ['Murder Was the Case', 'Poetic Justice', "Gridlock'd", 'Above the Rim', 'Juice', 'Nothing but Trouble', 'Gang Related', 'Bullet']

**answer:** The lyracist for "Panther Power" is Tupac Shakur. Tupac Shakur appears in Tupac: Assassination, Tupac Shakur: Thug Angel: The Life of an Outlaw, R.I.P. II: Eyes on Hip Hop, Tha Westside, Apprenticeship of Tupac Shakur, Tupac: Live at the House of Blues, Tupac: Resurrection, Thug Immortal: The Tupac Shakur Story, Freestyle: The Art of Rhyme, and R.I.P.: Shades of Hip Hop.

**entities:** ['Tupac: Assassination', 'Tupac Shakur: Thug Angel: The Life of an Outlaw', 'R.I.P. II: Eyes on Hip Hop', 'Tha Westside', 'Apprenticeship of Tupac Shakur', 'Tupac: Live at the House of Blues', 'Tupac: Resurrection', 'Thug Immortal: The Tupac Shakur Story', 'Freestyle: The Art of Rhyme', 'R.I.P.: Shades of Hip Hop']

plan: ['find the lyracist for "Panther Power"', 'find the films that this person appears in']

explored: ['music.composition.lyricist', 'music.lyricist.lyrics_written'] (score max 0.358)

explored: ['film.personal_film_appearance.person', 'film.person_or_entity_appearing_in_film.films', 'film.actor.film'] (score max 0.806)

verifier: grounded

---

## WebQTest-1797_dece4ddacc57788e31bf70edc99f1f37 (wrong)

**Q:** What Government position holder fought in the battle of Vicksburg?

**gold:** ['Ulysses S. Grant']

**answer:** John C. Pemberton fought in the Siege of Vicksburg.

**entities:** ['John C. Pemberton']

plan: ['find the battle of Vicksburg', 'find the Government position holder who fought in #1']

explored: ['base.americancivilwar.battle.military_units_involved_in_this_conflict', 'base.americancivilwar.military_unit.conflicts_participated_in', 'military.military_conflict.combatants'] (score max 0.51)

explored: ['base.americancivilwar.military_unit.conflicts_participated_in', 'military.military_unit.place_of_origin', 'military.military_unit.armed_force', 'base.americancivilwar.military_unit.conflicts_participated_in', 'military.military_unit.place_of_origin', 'military.military_unit.armed_force', 'base.americancivilwar.military_unit.conflicts_participated_in', 'military.military_unit.place_of_origin', 'military.military_unit.armed_force', 'base.americancivilwar.military_unit.conflicts_participated_in', 'military.military_unit.place_of_origin', 'military.military_unit.armed_force', 'base.americancivilwar.military_unit.conflicts_participated_in', 'military.military_unit.place_of_origin', 'military.military_unit.armed_force'] (score max 0.233)

explored: ['military.military_person.participated_in_conflicts', 'military.military_conflict.military_personnel_involved', 'base.americancivilwar.military_unit.conflicts_participated_in', 'military.military_person.participated_in_conflicts', 'military.military_conflict.military_personnel_involved', 'base.americancivilwar.military_unit.conflicts_participated_in', 'military.military_person.participated_in_conflicts', 'military.military_conflict.combatants', 'military.military_conflict.commanders', 'military.military_person.participated_in_conflicts', 'military.military_conflict.combatants', 'military.military_conflict.commanders', 'base.americancivilwar.military_unit.conflicts_participated_in', 'base.americancivilwar.battle.military_units_involved_in_this_conflict', 'base.culturalevent.event.entity_involved'] (score max 0.618)

explored: ['government.government_position_held.office_holder', 'government.politician.government_positions_held', 'military.military_person.participated_in_conflicts', 'military.military_person.participated_in_conflicts', 'military.military_conflict.military_personnel_involved', 'military.military_service.military_person', 'military.military_person.participated_in_conflicts', 'military.military_conflict.military_personnel_involved', 'military.military_service.military_person', 'military.military_person.participated_in_conflicts', 'military.military_conflict.military_personnel_involved', 'military.military_service.military_person', 'military.military_person.participated_in_conflicts', 'military.military_conflict.military_personnel_involved', 'military.military_service.military_person'] (score max 0.725)

verifier: grounded

---

## WebQTest-1736_125140bfa1a60527bde6e40dce7fe54a (wrong)

**Q:** Where's the location where the Slavic language is spoken located?

**gold:** ['Europe']

**answer:** The location where the Slavic language is spoken is Holy Roman Empire.

**entities:** ['Holy Roman Empire']

plan: ['find the location where the Slavic language is spoken', 'find the location of #1']

explored: ['location.country.official_language', 'language.language_family.languages', 'language.human_language.language_family'] (score max 0.377)

backtrack: evaluator

explored: [] (score max 0.0)

backtrack: dead_end

explored: [] (score max 0.0)

backtrack: dead_end

explored: [] (score max 0.0)

verifier: grounded

---

## WebQTest-1513_5422fa602469c38418171ad342583759 (wrong)

**Q:** What is there to do in downtown Sacramento, where there is an organization headquarters, located in the city of Sacramento County?

**gold:** ['California State Capitol Museum']

**answer:** Downtown Sacramento is in Sacramento, which is the capital of California. One organization headquarters there is Superior Pest Control of Sacramento, and Sacramento also has organizations such as Andersen Corporation and US Notary Public Association. If you meant specific things to do in downtown Sacramento, that could not be determined from the facts provided.

**entities:** ['Sacramento']

plan: ['find the organization headquarters located in the city of Sacramento County', 'find downtown Sacramento']

explored: ['organization.organization.locations', 'organization.organization.place_founded', 'base.aareas.schema.administrative_area.capital', 'location.administrative_division.capital', 'location.us_county.hud_county_place', 'location.hud_county_place.county'] (score max 0.44)

explored: ['organization.organization.headquarters', 'organization.organization.locations', 'organization.organization.place_founded', 'organization.organization.headquarters', 'organization.organization.place_founded', 'organization.organization_founder.organizations_founded', 'organization.organization.headquarters', 'organization.organization.locations', 'organization.organization.place_founded', 'organization.organization.headquarters', 'organization.organization.locations', 'organization.organization.place_founded', 'organization.organization.place_founded', 'organization.organization.operates_government_service', 'government.government_agency.government'] (score max 0.755)

explored: ['organization.organization.locations', 'organization.organization.place_founded', 'organization.organization_founder.organizations_founded', 'organization.organization.locations', 'organization.organization.place_founded', 'location.administrative_division.capital', 'organization.organization.locations', 'location.us_county.hud_county_place', 'location.hud_county_place.county', 'organization.organization.locations', 'organization.organization.place_founded', 'base.sportbase.sport_sport_club.location', 'business.business_location.parent_company', 'base.schemastaging.context_name.pronunciation', 'book.book_subject.works'] (score max 0.434)

explored: ['business.business_location.hours', 'business.business_location.address', 'business.business_location.phone_number'] (score max 0.185)

verifier: grounded

---

## WebQTrn-2047_3d5f855275265f74d81b862231578e33 (wrong)

**Q:** What is the name of the structure opened in 1997 where the Chicago Cubs play?

**gold:** ['Hohokam Stadium']

**answer:** Wrigley Field

**entities:** ['Wrigley Field']

plan: ['find where the Chicago Cubs play', 'find the structure opened in 1997 at #1', 'find the name of #2']

explored: ['sports.sports_team.venue', 'sports.sports_team.arena_stadium', 'sports.sports_team.location'] (score max 0.61)

explored: ['time.event.locations', 'location.location.events', 'sports.sports_team.arena_stadium'] (score max 0.429)

backtrack: evaluator

explored: ['sports.sports_facility.home_venue_for', 'sports.sports_facility.teams', 'base.playball.baseball_stadium.naming_rights'] (score max 0.279)

explored: ['sports.sports_team.arena_stadium', 'sports.sports_team.venue', 'base.schemastaging.sports_team_extra.training_ground', 'sports.sports_team.arena_stadium', 'sports.sports_team.venue', 'sports.sports_facility.teams', 'sports.sports_team.arena_stadium', 'sports.sports_team.venue', 'sports.sports_facility.teams'] (score max 0.553)

explored: ['base.schemastaging.sports_facility_extra.training_ground_for', 'sports.sports_team.arena_stadium', 'sports.sports_facility.home_venue_for', 'sports.sports_facility.home_venue_for', 'base.playball.baseball_stadium.naming_rights', 'sports.sports_facility.teams', 'sports.sports_team.arena_stadium', 'sports.sports_facility.teams', 'architecture.structure.architecture_firm', 'sports.sports_team.arena_stadium', 'sports.sports_facility.home_venue_for', 'sports.sports_facility.teams'] (score max 0.284)

verifier: grounded

---

## WebQTrn-2784_abedc8acd0fdcd2e595d7ec6d58d6058 (wrong)

**Q:** In which movies does Tupac act in, that was edited by Malcolm Campbell?

**gold:** ['Nothing but Trouble']

**answer:** Gang Related is a movie Tupac acted in, but the claim that it was edited by Malcolm Campbell could not be verified against the knowledge graph.

**entities:** ['Gang Related']

plan: ['find movies that Tupac acts in', 'find which of #1 were edited by Malcolm Campbell']

explored: ['film.actor.film', 'film.performance.actor', 'film.personal_film_appearance.person', 'film.editor.film', 'film.personal_film_appearance.person', 'film.film.edited_by'] (score max 0.616)

explored: ['film.film.edited_by', 'book.written_work.part_of_series', 'book.written_work.previous_in_series', 'film.film.edited_by', 'film.film.story_by', 'film.film.written_by', 'film.film.edited_by', 'film.film.written_by', 'film.writer.film', 'film.film.edited_by', 'film.film.written_by', 'film.film.film_art_direction_by', 'film.film.written_by', 'film.film.soundtrack', 'film.film.soundtrack'] (score max 0.565)

explored: ['film.film.edited_by', 'film.editor.film', 'film.person_or_entity_appearing_in_film.films', 'film.film.edited_by', 'film.editor.film', 'people.person.place_of_birth', 'film.film.edited_by', 'film.film.edited_by', 'film.editor.film', 'film.film.executive_produced_by', 'film.film.edited_by', 'film.editor.film', 'people.person.profession'] (score max 0.565)

explored: ['film.film.edited_by', 'film.film.story_by', 'film.film.written_by', 'film.film.edited_by', 'film.film.story_by', 'film.film.written_by', 'film.film.edited_by', 'film.film.film_art_direction_by', 'film.film.music', 'film.film.edited_by', 'film.film.story_by', 'film.film.written_by', 'film.film.edited_by', 'film.film.story_by', 'film.film.written_by'] (score max 0.265)

verifier: unsupported

---

## WebQTrn-962_f69b9d7b30f2ef81193ae7b0a39c78c5 (wrong)

**Q:** Who played in a movie that included a young Ray O Hardesty as a crew membner?

**gold:** ['Michael Connor Humphreys']

**answer:** Tom Hanks played in Forrest Gump, which included Ray O. Hardesty as a crew member.

**entities:** ['Tom Hanks']

plan: ['find the movie that included a young Ray O Hardesty as a crew member', 'find who played in #1']

explored: ['film.film_crewmember.films_crewed', 'film.film_crew_gig.crewmember', 'film.film.other_crew', 'film.film_crew_gig.film', 'film.director.film'] (score max 0.672)

explored: ['film.film_character.portrayed_in_films', 'film.performance.character', 'film.film.film_casting_director'] (score max 0.589)

verifier: grounded

---

## WebQTrn-3057_5a7cd2677ed97e520a124ba9c2da6ad4 (wrong)

**Q:** When prior to October 30, 2014 did the Giants win the world series?

**gold:** ['Songwriter']

**answer:** The Giants won the World Series in 2010 and 2012 prior to October 30, 2014.

**entities:** ['2010 World Series', '2012 World Series']

plan: ['find the World Series wins by the Giants', 'find when #1 occurred prior to October 30, 2014']

explored: ['sports.sports_team.championships', 'baseball.baseball_team.division', 'baseball.baseball_division.teams'] (score max 0.552)

explored: ['sports.sports_championship_event.season', 'time.event.locations', 'location.location.events', 'sports.sports_championship_event.season', 'time.event.locations', 'sports.sports_championship_event.runner_up', 'sports.sports_championship_event.runner_up', 'sports.sports_championship_event.championship', 'sports.sports_team.championships'] (score max 0.335)

explored: ['sports.sports_championship_event.season', 'sports.sports_league_season.championship', 'time.event.previous_in_series', 'sports.sports_championship_event.season', 'sports.sports_league.seasons', 'sports.sports_league_season.championship', 'time.event.locations', 'location.location.events', 'sports.sports_facility.teams', 'time.event.locations', 'location.location.events', 'sports.sports_facility.teams', 'time.event.locations', 'location.location.events', 'location.location.time_zones'] (score max 0.605)

verifier: grounded

---

## WebQTest-1923_7084416ab9f72f1f1f8fc3ce7871ee4a (wrong)

**Q:** Which movie has Miley Cyrus starred in that is 102.0 minutes long?

**gold:** ['Hannah Montana: The Movie']

**answer:** The movie is The Last Song.

**entities:** ['The Last Song']

plan: ['find movies that Miley Cyrus starred in', 'find which of #1 are 102.0 minutes long']

explored: ['film.actor.film', 'film.performance.actor', 'film.person_or_entity_appearing_in_film.films'] (score max 0.597)

explored: ['film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'music.track_contribution.track', 'film.film.soundtrack', 'film.film.soundtrack', 'film.film.music', 'film.film_crew_gig.film', 'film.music_contributor.film', 'film.film.starring', 'film.film.country', 'media_common.netflix_title.netflix_genres'] (score max 0.351)

explored: ['film.film.featured_song', 'music.artist.track', 'film.film_featured_song.performed_by', 'film.film.featured_song', 'music.artist.track', 'film.film_featured_song.performed_by', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'music.music_video.directed_by', 'film.film.music', 'music.artist.track_contributions', 'music.track_contribution.role', 'music.group_member.instruments_played', 'music.group_membership.role'] (score max 0.351)

explored: ['film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.soundtrack', 'film.film.featured_song', 'music.artist.track', 'film.film_featured_song.performed_by', 'music.artist.track', 'music.featured_artist.recordings', 'music.recording.featured_artists', 'music.artist.track', 'music.recording.artist', 'music.record_label.artist'] (score max 0.351)

verifier: grounded

---

## WebQTrn-124_0782789f35ce79d56102e26e54e5b700 (wrong)

**Q:** What was directed by the actor who played Corneila Wallace?

**gold:** ['By the Sea', 'In the Land of Blood and Honey', 'A Place in Time', 'Unbroken']

**answer:** Angelina Jolie directed Unbroken, In the Land of Blood and Honey, A Place in Time, and By the Sea.

**entities:** ['Angelina Jolie']

plan: ['find the actor who played Corneila Wallace', 'find what was directed by #1']

explored: ['film.film_character.portrayed_in_films', 'film.performance.character'] (score max 0.672)

explored: ['film.film.directed_by', 'film.director.film', 'film.editor.film'] (score max 0.614)

verifier: grounded

---

## WebQTest-1348_3f44e0c4fd23a8334a972ebb812e0e35 (wrong)

**Q:** What Minneapolis sports team had Peyton Manning's father on their roster?

**gold:** ['Minnesota Vikings']

**answer:** Archie Manning was on the Minnesota Vikings roster.

**entities:** ['Archie Manning']

plan: ["find Peyton Manning's father", 'find the sports team that had #1 on their roster and is based in Minneapolis']

explored: ['people.person.parents', 'people.person.parents', 'american_football.football_player.rushing', 'people.person.place_of_birth', 'sports.sports_team.location', 'base.wikipedia_infobox.settlement.area_code', 'fictional_universe.fictional_character.place_of_birth', 'base.thoroughbredracing.thoroughbred_racehorse.sex', 'base.givennames.given_name.gender'] (score max 0.446)

explored: ['sports.sports_team_roster.player', 'sports.pro_athlete.teams', 'sports.pro_sports_played.athlete'] (score max 0.629)

verifier: grounded

---

## WebQTest-1251_cf6cc4cc9ed790243a390f155ae72256 (wrong)

**Q:** Which country speaks Germanic languages has the nominal GDP of 279500000000.0?

**gold:** ['Austria']

**answer:** Germany speaks a Germanic language. However, the claim that it is the country with a nominal GDP of 279500000000.0 is not verified by the knowledge graph.

**entities:** ['Germany']

plan: ['find the country that has nominal GDP of 279500000000.0', 'find which of #1 speaks Germanic languages']

explored: ['location.country.official_language', 'language.human_language.countries_spoken_in', 'language.human_language.main_country'] (score max 0.239)

explored: ['location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_real', 'location.statistical_region.military_expenditure_percent_gdp', 'location.country.currency_used', 'location.country.form_of_government', 'location.country.capital', 'location.country.currency_used', 'finance.currency.countries_used', 'location.country.form_of_government', 'location.country.form_of_government', 'location.country.capital', 'government.form_of_government.countries', 'location.country.official_language', 'location.location.containedby', 'location.location.contains'] (score max 0.721)

backtrack: evaluator

explored: ['location.statistical_region.gdp_growth_rate', 'location.country.currency_used', 'location.statistical_region.gross_savings_as_percent_of_gdp', 'location.country.official_language', 'location.location.geolocation', 'location.location.containedby', 'location.country.capital', 'government.form_of_government.countries', 'location.country.official_language', 'location.country.official_language', 'language.human_language.countries_spoken_in', 'location.country.languages_spoken', 'location.location.people_born_here', 'base.culturalevent.event.entity_involved', 'people.person.place_of_birth'] (score max 0.352)

backtrack: evaluator

explored: ['location.statistical_region.trade_balance_as_percent_of_gdp', 'location.statistical_region.agriculture_as_percent_of_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp', 'location.location.contains', 'location.location.events', 'government.national_anthem_of_a_country.country', 'location.country.national_anthem', 'location.location.containedby', 'people.family.country', 'government.governmental_jurisdiction.governing_officials', 'location.location.containedby', 'military.military_combatant.military_conflicts', 'location.location.events', 'distilled_spirits.spirit_producing_region.distilleries'] (score max 0.319)

backtrack: evaluator

explored: ['location.statistical_region.health_expenditure_as_percent_of_gdp', 'location.statistical_region.gni_per_capita_in_ppp_dollars', 'finance.currency.countries_used', 'location.location.contains', 'base.schemastaging.context_name.pronunciation', 'location.location.containedby', 'people.person.nationality', 'royalty.system_rank_relationship.system', 'military.military_combatant_group.combatants'] (score max 0.312)

explored: ['business.market_size.currency', 'location.country.currency_used', 'location.country.currency_formerly_used', 'location.country.currency_used', 'finance.currency.countries_used', 'measurement_unit.dated_money_value.currency', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'location.statistical_region.population', 'measurement_unit.dated_money_value.source', 'people.person.nationality', 'location.location.people_born_here', 'people.deceased_person.place_of_death'] (score max 0.56)

explored: ['location.statistical_region.gdp_nominal', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_real', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.military_expenditure_percent_gdp', 'location.country.currency_used', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.military_expenditure_percent_gdp', 'location.country.currency_used', 'location.country.currency_used', 'finance.currency.countries_used', 'location.country.internet_tld', 'base.ontologies.ontology_instance_mapping.freebase_topic', 'base.ontologies.ontology_instance.equivalent_instances', 'business.competitive_space.market_size'] (score max 0.725)

verifier: unsupported

---

## WebQTrn-2570_ac52c51debd358141a23acc7ae7ec938 (wrong)

**Q:** Which WW2 US President had a political appointer that was White House Chief of Staff?

**gold:** ['Harry S. Truman']

**answer:** Dwight D. Eisenhower

**entities:** ['Dwight D. Eisenhower']

plan: ['find the US President during World War II', 'find the political appointer of #1', 'find which of #2 was White House Chief of Staff']

explored: ['military.military_conflict.commanders', 'military.military_command.military_conflict', 'military.military_person.participated_in_conflicts', 'government.government_office_or_title.office_holders', 'government.government_position_held.office_position_or_title', 'government.electoral_college_elected_office.office', 'government.government_position_held.office_position_or_title', 'base.obamabase.possible_cabinet_member.cabinet_position', 'government.government_office_or_title.governmental_body_if_any'] (score max 0.496)

explored: ['military.military_person.participated_in_conflicts', 'military.military_command.military_commander', 'military.military_commander.military_commands', 'military.military_person.participated_in_conflicts', 'military.military_command.military_commander', 'military.military_commander.military_commands', 'military.military_command.military_commander', 'military.military_commander.military_commands', 'government.government_position_held.office_holder', 'military.military_combatant.includes_allies', 'military.military_command.military_combatant', 'military.military_combatant.military_commanders', 'military.military_command.military_combatant', 'military.military_combatant.military_commanders', 'military.armed_force.military_combatant'] (score max 0.253)

explored: ['military.military_person.participated_in_conflicts', 'military.military_conflict.commanders', 'military.military_command.military_conflict', 'military.military_person.participated_in_conflicts', 'military.military_conflict.commanders', 'military.military_conflict.military_personnel_involved', 'military.military_person.participated_in_conflicts', 'military.military_conflict.commanders', 'military.military_conflict.military_personnel_involved', 'military.military_person.participated_in_conflicts', 'military.military_conflict.military_personnel_involved', 'time.event.included_in_event', 'military.military_person.participated_in_conflicts', 'military.military_conflict.commanders', 'military.military_command.military_conflict'] (score max 0.253)

explored: ['government.political_appointer.appointees', 'people.appointer.appointment_made', 'people.appointment.appointed_by'] (score max 0.679)

verifier: grounded

---

## WebQTrn-1812_04dbed66ba17d35bf79f72e04bbcc776 (wrong)

**Q:** What country in the Caribbean appointed Elizabeth II to a governmental position?

**gold:** ['British Virgin Islands']

**answer:** Anguilla appointed Elizabeth II to a governmental position.

**entities:** ['Anguilla']

plan: ['find the Caribbean country that appointed Elizabeth II to a governmental position']

explored: ['government.government_position_held.appointed_by', 'people.appointment.appointed_by', 'people.appointer.appointment_made', 'film.film.country', 'organization.organization.geographic_scope', 'base.popstra.vacation_choice.location', 'film.film.country', 'award.award_nomination.nominated_for', 'film.director.film'] (score max 0.552)

verifier: grounded

---

## WebQTest-1348_b7598df908bf8cbe941f82e1cefaec28 (wrong)

**Q:** What defunct sports team later known as the Tennessee Oilers did Peyton Manning 's dad play for?

**gold:** ['Houston Oilers']

**answer:** Archie Manning played for Houston Oilers, which later became known as Tennessee Oilers.

**entities:** ['Archie Manning']

plan: ['find the sports team later known as the Tennessee Oilers', "find the team that Peyton Manning's dad played for that is #1"]

explored: ['sports.defunct_sports_team.later_known_as', 'sports.defunct_sports_team.later_known_as', 'sports.sports_team.previously_known_as', 'sports.pro_athlete.teams', 'sports.sports_team_roster.player', 'sports.pro_athlete.sports_played_professionally', 'sports.sports_gender.sports_teams', 'sports.sports_team.gender', 'base.marchmadness.ncaa_basketball_team.team_gender'] (score max 0.617)

explored: ['american_football.football_historical_coach_position.team', 'american_football.football_team.historical_coaching_staff', 'american_football.football_division.teams', 'american_football.football_historical_coach_position.team', 'american_football.football_team.historical_coaching_staff', 'sports.sports_team_season_record.team', 'music.artist.track', 'music.recording.artist', 'music.record_label.artist', 'base.technologyofdoing.knowledge_worker_practice.scopelevel'] (score max 0.375)

backtrack: evaluator

explored: ['american_football.football_team.division', 'sports.sports_team_season_record.team', 'american_football.football_game.home_team', 'sports.sports_team_roster.team', 'sports.sports_team.roster', 'sports.sports_team.season_record', 'music.artist.label', 'people.profession.specialization_of', 'film.film.genre'] (score max 0.308)

verifier: unsupported

explored: ['sports.pro_sports_played.athlete', 'sports.sports_team_roster.player', 'sports.sports_award.award_winner'] (score max 0.228)

verifier: grounded

---

## WebQTrn-1706_97097ed7f8b2c898c800e8717998cb4c (wrong)

**Q:** What controls the second level division Kuna de Madugandi?

**gold:** ['Ricardo Martinelli']

**answer:** Panama controls Kuna de Madugandí.

**entities:** ['Panama']

plan: ['find the second level division Kuna de Madugandi', 'find what controls #1']

explored: ['location.country.second_level_divisions', 'location.administrative_division.second_level_division_of', 'location.location.contains', 'government.government_office_or_title.jurisdiction', 'government.governmental_jurisdiction.government_positions', 'government.government_position_held.office_position_or_title'] (score max 0.652)

explored: ['location.country.form_of_government', 'government.form_of_government.countries', 'base.locations.countries.continent'] (score max 0.236)

explored: ['location.country.form_of_government', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.form_of_government.countries', 'base.schemastaging.context_name.pronunciation', 'location.country.form_of_government', 'government.form_of_government.countries', 'base.schemastaging.context_name.pronunciation', 'base.locations.countries.continent', 'base.locations.continents.states_provinces_within', 'base.locations.continents.countries_within'] (score max 0.236)

verifier: grounded

---

## WebQTest-213_024fd6ca0b4cb30927c22e93a552ae6c (wrong)

**Q:** What person notable with the medical condition Attention deficit hyperactivity disorder id Scarlett Johansson date?

**gold:** ['Justin Timberlake']

**answer:** Mary-Kate Olsen is a notable person with Attention deficit hyperactivity disorder.

**entities:** ['Mary-Kate Olsen']

plan: ['find the person notable with Attention deficit hyperactivity disorder and named Scarlett Johansson', 'find the date associated with #1']

explored: ['medicine.notable_person_with_medical_condition.condition', 'medicine.disease.notable_people_with_this_condition', 'fictional_universe.medical_condition_in_fiction.characters_with_this_condition', 'tv.tv_guest_personal_appearance.person', 'film.personal_film_appearance.person', 'people.person.gender'] (score max 0.615)

backtrack: evaluator

explored: ['fictional_universe.fictional_character.medical_conditions', 'medicine.disease.medical_specialties', 'base.aubreymaturin.affliction.malady', 'film.performance.actor', 'film.person_or_entity_appearing_in_film.films', 'people.person.spouse_s'] (score max 0.251)

backtrack: evaluator

explored: ['base.aubreymaturin.malady.sufferers', 'medicine.disease.includes_diseases', 'medicine.disease.includes_diseases', 'people.person.children', 'people.person.children', 'people.person.profession'] (score max 0.205)

backtrack: evaluator

explored: ['medicine.symptom.symptom_of', 'medicine.risk_factor.diseases', 'medicine.risk_factor.diseases', 'theater.theater_role.actor', 'celebrities.sexual_orientation_phase.celebrity', 'celebrities.romantic_relationship.celebrity'] (score max 0.201)

verifier: grounded

---

## WebQTest-1923_b10bde702bb6c68ce3cdced85d5aff02 (wrong)

**Q:** Which movie that was cast by Cathy Sandrich was Miley Cyrus in?

**gold:** ['The Last Song']

**answer:** Miley Cyrus was in So Undercover.

**entities:** ['So Undercover']

plan: ['find the movie cast by Cathy Sandrich that Miley Cyrus was in']

explored: ['film.actor.film', 'film.person_or_entity_appearing_in_film.films', 'film.performance.actor', 'film.film.film_casting_director', 'film.film_casting_director.films_casting_directed', 'people.person.parents'] (score max 0.575)

explored: ['film.film.starring', 'film.film.film_casting_director', 'film.film_casting_director.films_casting_directed', 'film.film.starring', 'film.personal_film_appearance.film', 'film.film.personal_appearances', 'film.film.starring', 'film.film_character.portrayed_in_films', 'tv.tv_program.regular_cast', 'film.film_character.portrayed_in_films', 'tv.tv_program.regular_cast', 'film.performance.character', 'film.film_character.portrayed_in_films', 'film.performance.character'] (score max 0.565)

explored: ['film.actor.film', 'film.performance.actor', 'people.person.gender', 'film.actor.film', 'film.performance.actor', 'people.person.gender', 'film.film_character.portrayed_in_films', 'film.performance.character', 'film.film_character.portrayed_in_films', 'film.performance.character', 'film.film_character.portrayed_in_films', 'film.performance.character'] (score max 0.29)

backtrack: evaluator

explored: ['film.film.starring', 'film.film.film_casting_director', 'film.film_casting_director.films_casting_directed', 'film.film.starring', 'film.personal_film_appearance.film', 'film.film.personal_appearances', 'film.film.starring', 'film.film_character.portrayed_in_films', 'tv.tv_program.regular_cast', 'film.film_character.portrayed_in_films', 'tv.tv_program.regular_cast', 'film.performance.character', 'film.film_character.portrayed_in_films', 'film.performance.character'] (score max 0.565)

explored: ['people.person.profession', 'people.person.profession'] (score max 0.06)

explored: ['film.film_character.portrayed_in_films', 'film.director.film', 'film.performance.character'] (score max 0.277)

verifier: unsupported

---

## WebQTrn-64_d8e43a02200cfdff82052f8cc5395b27 (wrong)

**Q:** What was the actor's name that played the character Digital Underground Member in "Juice"?

**gold:** ['Bishop']

**answer:** Tupac Shakur played the character Digital Underground member in Juice.

**entities:** ['Tupac Shakur']

plan: ['find the character Digital Underground Member in Juice', 'find the actor who played #1']

explored: ['film.film_character.portrayed_in_films', 'film.performance.character', 'film.film.story_by', 'film.film.soundtrack', 'film.film.soundtrack'] (score max 0.461)

explored: ['book.book.characters', 'base.popstra.celebrity.friendship', 'base.popstra.friendship.participant', 'film.film.story_by', 'film.film_story_contributor.film_story_credits', 'film.person_or_entity_appearing_in_film.films', 'film.film.story_by', 'film.film.soundtrack', 'film.film.soundtrack', 'film.film.starring', 'film.director.film', 'film.music_contributor.film'] (score max 0.238)

explored: ['film.performance.actor', 'film.actor.film', 'film.film_character.portrayed_in_films'] (score max 0.593)

verifier: grounded

---

## WebQTest-837_c4e06c3a9e4b4f10bd1ae97f1742c198 (wrong)

**Q:** In what year did a team win the superbowl and the 2013 AFC Championship Game ?

**gold:** ['Super Bowl XLVII', 'Super Bowl XXXV']

**answer:** 2012 NFL season

**entities:** ['2012 NFL season']

plan: ['find the team that won the Super Bowl and the 2013 AFC Championship Game', 'find the year of #1']

explored: ['sports.sports_team.championships', 'sports.sports_championship_event.championship', 'sports.sports_league_season.championship', 'sports.sports_league.championship', 'sports.sports_championship_event.championship', 'sports.sports_championship.events'] (score max 0.589)

explored: ['sports.sports_team.championships', 'american_football.football_conference.teams', 'american_football.football_division.teams', 'sports.sports_league.championship', 'sports.sports_championship_event.championship', 'sports.sports_championship.events', 'sports.sports_team.championships', 'sports.sports_championship_event.championship', 'sports.sports_league_season.championship', 'sports.sports_team.championships', 'sports.sports_championship_event.championship', 'sports.sports_league_season.championship', 'american_football.football_conference.league', 'sports.sports_league.championship', 'sports.sports_championship.league'] (score max 0.589)

explored: ['sports.sports_team.championships', 'sports.sports_championship_event.championship', 'sports.sports_league_season.championship', 'sports.sports_team.championships', 'sports.sports_championship_event.championship', 'sports.sports_league_season.championship', 'sports.sports_team.championships', 'sports.sports_championship_event.championship', 'sports.sports_league_season.championship', 'american_football.football_conference.teams', 'american_football.football_team.conference', 'american_football.football_division.conference', 'sports.sports_team.championships', 'sports.sports_championship_event.championship', 'sports.sports_league_season.championship'] (score max 0.604)

explored: ['sports.sports_championship_event.season', 'sports.sports_team.championships', 'sports.sports_league_season.championship', 'sports.sports_team.championships', 'sports.sports_team.season_record', 'sports.sports_team_season_record.team'] (score max 0.569)

verifier: grounded

---

## WebQTrn-1677_bdfdca39c58846e51247fd78bc7683eb (wrong)

**Q:** In which films decorated by Karen O'Hara did Adam Sandler appear?

**gold:** ['Paul Blart: Mall Cop 2', 'Blended']

**answer:** The answer could not be verified against the knowledge graph. Spider-Man and The American President are films decorated by Karen O'Hara, but Adam Sandler’s appearance in them is not supported.

**entities:** ['Spider-Man', 'The American President']

plan: ["find films decorated by Karen O'Hara", 'find which of #1 feature Adam Sandler']

explored: ['film.film.film_set_decoration_by', 'film.film_set_designer.film_sets_designed', 'award.award_honor.award_winner', 'film.writer.film', 'film.film.written_by', 'film.person_or_entity_appearing_in_film.films'] (score max 0.637)

explored: ['film.film_film_distributor_relationship.film', 'film.film.costume_design_by', 'film.film.directed_by', 'film.film_film_distributor_relationship.film', 'film.film.costume_design_by', 'film.music_contributor.film', 'film.film_film_distributor_relationship.film', 'film.film_story_contributor.film_story_credits', 'film.film.costume_design_by', 'tv.tv_program.program_creator', 'film.film_story_contributor.film_story_credits', 'tv.tv_program_creator.programs_created', 'film.film.costume_design_by', 'film.film.story_by', 'film.film.film_production_design_by'] (score max 0.194)

explored: ['comic_books.comic_book_creator.characters_created', 'comic_books.comic_book_creator.series_created', 'comic_books.comic_book_character.created_by', 'comic_books.comic_book_creator.characters_created', 'people.marriage.spouse', 'comic_books.comic_book_creator.series_created', 'film.film_film_distributor_relationship.distributor', 'organization.organization.founders', 'cvg.cvg_publisher.games_published', 'film.film_film_distributor_relationship.distributor', 'internet.website_ownership.owner', 'internet.website.owner', 'film.film_film_distributor_relationship.distributor', 'amusement_parks.ride.designer', 'amusement_parks.ride_designer.rides'] (score max 0.226)

explored: ['fictional_universe.marriage_of_fictional_characters.spouses', 'comic_books.comic_book_creator.characters_created', 'fictional_universe.fictional_character.married_to', 'fictional_universe.marriage_of_fictional_characters.spouses', 'comic_books.comic_book_creator.characters_created', 'fictional_universe.fictional_character.married_to', 'comic_books.comic_book_creator.characters_created', 'comic_books.comic_book_character.created_by', 'fictional_universe.fictional_character.character_created_by', 'comic_books.comic_book_creator.characters_created', 'comic_books.comic_book_character.created_by', 'comic_books.comic_book_character.story_specific_appearances', 'comic_books.comic_book_creator.characters_created', 'comic_books.comic_book_character.created_by', 'comic_books.comic_book_character.story_specific_appearances'] (score max 0.27)

verifier: unsupported

---

## WebQTrn-1677_15a55e684b4c9a686e6865cfcad59905 (wrong)

**Q:** What movie produced by Chris Columbus did Adam Sandler play in?

**gold:** ['Pixels']

**answer:** Nine Months

**entities:** ['Nine Months']

plan: ['find movies produced by Chris Columbus', 'find which of #1 Adam Sandler played in']

explored: ['film.producer.film', 'film.film.produced_by', 'film.producer.films_executive_produced', 'film.producer.film', 'film.film.produced_by', 'film.producer.films_executive_produced'] (score max 0.582)

explored: ['film.film.soundtrack', 'film.film.soundtrack', 'film.music_contributor.film', 'film.film.soundtrack', 'film.film.soundtrack', 'music.soundtrack.film', 'film.film.soundtrack', 'film.film.music', 'film.film.story_by', 'film.film.soundtrack', 'film.film.soundtrack', 'music.soundtrack.film', 'film.film.music', 'film.film.story_by', 'film.film_crew_gig.film'] (score max 0.269)

explored: ['film.film.soundtrack', 'film.film.soundtrack', 'film.music_contributor.film', 'film.film.soundtrack', 'film.film.soundtrack', 'music.soundtrack.film', 'film.film.soundtrack', 'film.film.soundtrack', 'film.film.soundtrack', 'music.soundtrack.film', 'film.music_contributor.film', 'film.film.music', 'film.film.story_by'] (score max 0.269)

explored: ['film.film.soundtrack', 'film.film.soundtrack', 'film.music_contributor.film', 'film.film.soundtrack', 'film.film.soundtrack', 'music.soundtrack.film', 'film.film.soundtrack', 'film.film.music', 'film.film.story_by', 'film.film.soundtrack', 'film.film.soundtrack', 'music.soundtrack.film', 'film.music_contributor.film', 'film.film.music', 'film.film.story_by'] (score max 0.269)

verifier: grounded

---

## WebQTest-1012_73741811f34519b29f7d19ccfd4d9553 (wrong)

**Q:** What structure opened in 1922 in Hollywood, CA?

**gold:** ["Grauman's Egyptian Theatre"]

**answer:** Hollywood Palladium

**entities:** ['Hollywood Palladium']

plan: ['find the structure in Hollywood, CA that opened in 1922']

explored: ['film.film_location.featured_in_films', 'film.film.featured_film_locations', 'location.location.containedby'] (score max 0.329)

explored: ['film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.director.film', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film.film_production_design_by', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film.film_production_design_by', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film_festival_event.films', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film.film_production_design_by'] (score max 0.314)

explored: ['organization.organization.place_founded', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'location.location.containedby', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'location.location.containedby', 'film.film.film_production_design_by', 'film.film_set_designer.film_sets_designed', 'film.film.film_set_decoration_by', 'film.film.film_production_design_by', 'film.film_production_designer.films_production_designed', 'film.film_art_director.films_art_directed'] (score max 0.47)

verifier: unsupported

explored: ['time.event.locations', 'location.location.events', 'location.location.containedby'] (score max 0.388)

verifier: grounded

---

## WebQTrn-2292_ea0bc3bb340865025c534c91eca19be9 (wrong)

**Q:** What kind of economy does the country have that breeds Moscow watchdogs?

**gold:** ['Communist state', 'Socialist state', 'Soviet democracy', 'Parliamentary republic']

**answer:** The country is Soviet Union, and it has a Communist state economy.

**entities:** ['Soviet Union']

plan: ['find the country that breeds Moscow watchdogs', 'find the kind of economy of #1']

explored: ['biology.breed_origin.breeds_originating_here', 'biology.animal_breed.place_of_origin', 'biology.breed_temperament.breeds'] (score max 0.55)

explored: ['finance.currency.countries_formerly_used', 'government.form_of_government.countries', 'location.country.form_of_government'] (score max 0.204)

explored: ['finance.currency.countries_used', 'finance.currency.countries_formerly_used', 'location.country.currency_used', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.government.government_for', 'government.form_of_government.countries', 'location.country.form_of_government', 'government.form_of_government.countries', 'location.country.form_of_government'] (score max 0.222)

verifier: grounded

---

## WebQTrn-3170_8c4cd2a8dd5064dcd1e88389796138c7 (wrong)

**Q:** What does the political appointee, Associate Director, White House Office of Public Liaison, have a degree in?

**gold:** ['Political Science']

**answer:** Kal Penn. The degree could not be determined from the facts provided.

**entities:** ['Kal Penn']

plan: ['find the degree of the Associate Director of the White House Office of Public Liaison']

explored: ['government.government_position_held.office_position_or_title', 'government.government_office_or_title.office_holders'] (score max 0.504)

explored: ['government.government_position_held.office_holder', 'people.person.profession', 'award.award_nomination.award_nominee', 'education.honorary_degree.recipient', 'organization.leadership.person', 'business.board_member.leader_of', 'government.government_office_or_title.governmental_body_if_any', 'government.governmental_body.offices_positions', 'government.government_agency.jurisdiction'] (score max 0.494)

backtrack: evaluator

explored: ['government.politician.government_positions_held', 'award.award_nominee.award_nominations', 'film.performance.actor', 'education.honorary_degree_recipient.honorary_degrees', 'organization.organization_member.member_of', 'government.us_president.vice_president', 'business.employment_tenure.company', 'government.governmental_body.members', 'business.employer.employees'] (score max 0.256)

backtrack: evaluator

explored: ['film.actor.film', 'tv.tv_actor.starring_roles', 'tv.regular_tv_appearance.actor', 'people.appointment.appointed_by', 'government.political_appointer.appointees', 'business.employment_tenure.person', 'government.governmental_jurisdiction.government_bodies', 'government.government_position_held.governmental_body', 'government.governmental_body.jurisdiction'] (score max 0.226)

backtrack: evaluator

explored: ['people.person.gender', 'people.person.languages', 'people.person.nationality', 'government.us_vice_president.to_president', 'government.government_position_held.office_holder', 'government.political_party_tenure.politician', 'base.schemastaging.context_name.pronunciation'] (score max 0.211)

verifier: grounded

---

## WebQTrn-1677_c006ead7cde93a8aff111388eaa455c1 (hedge)

**Q:** Which movie is about baseball and featured Adam Sandler?

**gold:** ['The Benchwarmers']

**answer:** It could not be determined from the provided facts which baseball movie featured Adam Sandler. The baseball-related films listed do not overlap with the Adam Sandler film facts given.

**entities:** []

plan: ['find movies about baseball', 'find which of #1 featured Adam Sandler']

explored: ['film.film_subject.films', 'film.film.subjects', 'sports.sports_league.sport', 'film.film.story_by', 'film.writer.film', 'film.actor.film'] (score max 0.596)

explored: ['film.film.starring', 'media_common.netflix_genre.titles', 'film.writer.film', 'film.film.starring', 'media_common.netflix_genre.titles', 'film.film.sequel', 'film.film.starring', 'film.writer.film', 'film.film.written_by', 'film.film.starring', 'film.production_company.films', 'film.film.genre', 'film.film.starring', 'film.film.genre', 'film.producer.film'] (score max 0.446)

explored: ['film.film.story_by', 'award.hall_of_fame_inductee.hall_of_fame_inductions', 'award.hall_of_fame_induction.inductee', 'film.film.directed_by', 'film.actor.film', 'film.director.film', 'film.actor.film', 'film.performance.actor', 'people.person.sibling_s', 'film.performance.character', 'film.film_character.portrayed_in_films', 'film.performance.character', 'film.film_character.portrayed_in_films'] (score max 0.199)

backtrack: evaluator

explored: ['film.film.starring', 'media_common.netflix_genre.titles', 'film.writer.film', 'film.film.starring', 'media_common.netflix_genre.titles', 'film.film.sequel', 'film.film.starring', 'film.writer.film', 'film.film.written_by', 'film.film.starring', 'film.production_company.films', 'film.film.genre', 'film.film.starring', 'film.film.genre', 'film.producer.film'] (score max 0.446)

explored: ['film.writer.film', 'film.film_story_contributor.film_story_credits', 'film.film.written_by', 'tv.tv_program.program_creator', 'film.performance.actor', 'tv.tv_program_creator.programs_created', 'people.person.place_of_birth', 'people.sibling_relationship.sibling', 'people.person.parents'] (score max 0.141)

explored: ['film.film.story_by', 'film.film.starring', 'film.writer.film', 'film.film.story_by', 'film.film.starring', 'film.writer.film', 'film.film.starring', 'media_common.netflix_genre.titles', 'film.writer.film', 'film.writer.film', 'film.film.written_by', 'film.film.genre', 'tv.tv_program.original_network', 'tv.tv_program.regular_cast', 'tv.tv_program.genre'] (score max 0.199)

verifier: grounded

---

## WebQTrn-849_f0ffa14797f7486fb0510a740e1cc8d6 (hedge)

**Q:** Of the countries that border Germany, which country has an iso alpha 3 of CHE?

**gold:** ['Switzerland']

**answer:** Switzerland could not be determined from the provided facts as a country that borders Germany, because the facts list neighboring countries only indirectly and do not explicitly state Germany's borders or Switzerland's iso alpha 3 code.

**entities:** []

plan: ['find countries that border Germany', 'find which of #1 has iso alpha 3 CHE']

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'film.film.country', 'film.film_regional_release_date.film', 'base.ontologies.ontology_instance_mapping.freebase_topic'] (score max 0.309)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.states_and_provences.continent', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country', 'base.biblioness.bibs_location.country', 'location.location.containedby', 'base.biblioness.bibs_location.state', 'base.biblioness.bibs_location.country', 'location.location.containedby', 'base.biblioness.bibs_location.state', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country'] (score max 0.309)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country'] (score max 0.309)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.states_and_provences.continent', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country', 'base.biblioness.bibs_location.country', 'location.location.containedby', 'base.biblioness.bibs_location.state', 'base.biblioness.bibs_location.country', 'location.location.containedby', 'base.biblioness.bibs_location.state', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country'] (score max 0.309)

verifier: grounded

---

## WebQTest-1686_554811ebe1463287ee640a214683ea57 (hedge)

**Q:** Who held his governmental position from before Janaury 6, 2003 and was the 2009 Governor of Arizona?

**gold:** ['Janet Napolitano']

**answer:** Jan Brewer was the 2009 Governor of Arizona, but it could not be determined from the provided facts who held his governmental position from before Janaury 6, 2003.

**entities:** []

plan: ['find the 2009 Governor of Arizona', 'find who held the same governmental position as #1 from before January 6, 2003']

explored: ['government.government_office_or_title.office_holders', 'government.government_position_held.office_position_or_title', 'organization.role.governors', 'government.governmental_jurisdiction.governing_officials', 'government.political_district.representatives', 'government.governmental_jurisdiction.government_positions'] (score max 0.428)

explored: ['organization.role.governors', 'organization.role.leaders', 'government.government_office_or_title.office_holders', 'government.politician.government_positions_held', 'government.government_position_held.office_holder', 'people.person.profession', 'government.politician.government_positions_held', 'government.government_position_held.office_holder', 'people.person.profession', 'government.politician.government_positions_held', 'government.government_position_held.office_holder', 'people.person.place_of_birth', 'base.braziliangovt.state.politicians', 'government.governmental_jurisdiction.agencies', 'government.government_agency.jurisdiction'] (score max 0.556)

explored: ['government.political_appointer.appointees', 'government.government_position_held.appointed_by', 'organization.organization.founders', 'organization.leadership.person', 'business.board_member.leader_of', 'people.person.employment_history', 'organization.organization.board_members', 'business.employment_tenure.company', 'organization.organization_board_membership.organization', 'organization.organization.board_members', 'organization.organization_board_membership.organization', 'organization.organization_board_membership.member', 'people.person.profession', 'people.person.gender'] (score max 0.223)

explored: ['government.politician.government_positions_held', 'government.government_position_held.office_holder', 'people.person.employment_history', 'government.governmental_jurisdiction.governing_officials', 'government.government_position_held.jurisdiction_of_office', 'government.governmental_jurisdiction.governing_officials', 'government.government_position_held.jurisdiction_of_office', 'location.country.form_of_government', 'organization.role.leaders', 'government.government_position_held.basic_title', 'organization.leadership.role', 'government.government_office_or_title.office_holders', 'government.government_position_held.office_position_or_title', 'government.government_office_or_title.category'] (score max 0.24)

verifier: grounded

---

## WebQTrn-3543_3f03848605c6758ff2230a955cd92d65 (hedge)

**Q:** Which countries does Japan export that that have a GDP deflator change of rate -0.61?

**gold:** ['Kiribati']

**answer:** Could not be determined from the provided facts which of Japan's export destinations have a GDP deflator change rate of -0.61.

**entities:** []

plan: ['find countries that Japan exports to', 'find which of #1 have a GDP deflator change of rate -0.61']

explored: ['location.imports_and_exports.exported_to', 'location.statistical_region.places_exported_to', 'location.imports_and_exports.imported_from'] (score max 0.677)

explored: ['location.statistical_region.gdp_growth_rate', 'location.statistical_region.gdp_nominal', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_growth_rate', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_real', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.military_expenditure_percent_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.military_expenditure_percent_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp', 'location.statistical_region.gdp_real', 'location.statistical_region.military_expenditure_percent_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp'] (score max 0.464)

explored: ['location.country.currency_used', 'location.country.currency_formerly_used', 'finance.currency.countries_used', 'location.country.currency_used', 'finance.currency.countries_used', 'measurement_unit.dated_money_value.currency', 'measurement_unit.dated_percentage.source', 'measurement_unit.dated_money_value.source', 'measurement_unit.dated_money_value.source', 'measurement_unit.dated_money_value.source', 'measurement_unit.adjusted_money_value.source'] (score max 0.302)

backtrack: evaluator

explored: ['location.statistical_region.gdp_growth_rate', 'location.statistical_region.gdp_nominal', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_growth_rate', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_real', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.military_expenditure_percent_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.military_expenditure_percent_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp', 'location.statistical_region.gdp_real', 'location.statistical_region.military_expenditure_percent_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp'] (score max 0.464)

explored: ['finance.currency.countries_formerly_used', 'location.imports_exports_by_industry.currency', 'location.imports_and_exports.currency', 'finance.exchange_rate.target_of_exchange', 'finance.currency.target_of_exchange'] (score max 0.259)

explored: ['location.statistical_region.gdp_deflator_change', 'location.statistical_region.gdp_growth_rate', 'location.statistical_region.gdp_nominal', 'location.statistical_region.gdp_growth_rate', 'location.statistical_region.gdp_nominal', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.gdp_nominal', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.major_exports', 'location.statistical_region.gdp_nominal_per_capita', 'location.statistical_region.military_expenditure_percent_gdp', 'location.statistical_region.merchandise_trade_percent_of_gdp', 'location.imports_exports_by_industry.industry', 'organization.organization.sectors', 'organization.organization_sector.organizations_in_this_sector'] (score max 0.434)

verifier: grounded

---

## WebQTrn-1770_6325ee890e333f0d4fe222c15a95906f (hedge)

**Q:** What is the name of the daughter of the actor that played the character Etta James?

**gold:** ['Blue Ivy']

**answer:** The daughter of the actor that played Etta James could not be determined from the facts provided.

**entities:** []

plan: ['find the actor that played the character Etta James', 'find the daughter of #1', 'find the name of #2']

explored: ['tv.tv_actor.starring_roles', 'film.film_character.portrayed_in_films', 'tv.tv_guest_role.actor'] (score max 0.388)

explored: ['people.sibling_relationship.sibling', 'base.popstra.celebrity.infidelity_victim', 'celebrities.romantic_relationship.celebrity'] (score max 0.426)

backtrack: evaluator

explored: ['celebrities.celebrity.sexual_relationships', 'base.popstra.celebrity.infidelity_perpetrator', 'base.popstra.infidelity.victim'] (score max 0.166)

backtrack: evaluator

explored: ['celebrities.sexual_orientation_phase.celebrity', 'base.popstra.celebrity.friendship', 'base.popstra.celebrity.dated'] (score max 0.161)

backtrack: evaluator

explored: ['celebrities.celebrity.sexual_orientation', 'celebrities.celebrity.celebrity_friends', 'base.popstra.celebrity.operation'] (score max 0.149)

verifier: grounded

---

## WebQTrn-125_003c6a046c47526d922683f22cf0e983 (hedge)

**Q:** The subject of the film King: A Filmed Record... Montgomery to Memphis was shot at what location?

**gold:** ['Memphis']

**answer:** It could not be determined from the provided facts.

**entities:** []

plan: ['find the subject of the film King: A Filmed Record... Montgomery to Memphis', 'find the location where #1 was shot']

explored: ['film.film.subjects', 'film.producer.film', 'film.film.music'] (score max 0.579)

explored: ['base.crime.crime_victim.crime_type', 'people.deceased_person.place_of_death', 'base.activism.activist.area_of_activism'] (score max 0.361)

explored: ['time.event.locations', 'location.location.events', 'location.location.containedby', 'base.activism.activist.area_of_activism', 'people.person.profession', 'people.profession.people_with_this_profession', 'base.activism.activist.area_of_activism', 'base.activism.organization.area_of_activism', 'base.activism.activism_issue.activist_organizations', 'base.activism.activist.area_of_activism', 'base.activism.activism_issue.activists', 'base.activism.activism_issue.includes_issues', 'base.crime.crime.crime_type', 'base.crime.crime_victim.crime_type', 'media_common.quotation_subject.quotations_about_this_subject'] (score max 0.506)

verifier: grounded

---

## WebQTrn-25_62939f05e216712e4700e993437a980a (hedge)

**Q:** What was the latest film that Taylor Lautner played in?

**gold:** ['Grown Ups 2']

**answer:** The latest film that Taylor Lautner played in could not be determined from the facts provided.

**entities:** []

plan: ['find the films Taylor Lautner played in', 'find the latest film in #1']

explored: ['film.actor.film', 'film.performance.actor', 'tv.tv_actor.starring_roles'] (score max 0.67)

explored: ['film.film_regional_release_date.film', 'film.film.release_date_s', 'film.film.starring', 'film.film_regional_release_date.film', 'film.film.release_date_s', 'film.film.story_by', 'film.film_regional_release_date.film', 'film.film.release_date_s', 'film.film.story_by', 'film.film.starring', 'film.film.genre', 'film.producer.film', 'film.film.starring', 'film.film.directed_by', 'film.writer.film'] (score max 0.665)

explored: ['film.film.story_by', 'film.film.starring', 'film.film.featured_film_locations', 'film.film.featured_film_locations', 'film.film_location.featured_in_films', 'film.film_subject.films', 'film.film.featured_film_locations', 'film.film_location.featured_in_films', 'film.film_regional_release_date.film_release_region', 'film.film_regional_release_date.film_regional_debut_venue', 'film.film_regional_release_date.film_release_distribution_medium', 'film.film_film_distributor_relationship.film_distribution_medium', 'film.film_regional_release_date.film_release_distribution_medium', 'film.film.film_format', 'film.film_film_distributor_relationship.film_distribution_medium'] (score max 0.352)

explored: ['film.film.story_by', 'film.film.directed_by', 'film.writer.film', 'film.film.featured_film_locations', 'film.film.directed_by', 'film.film_location.featured_in_films', 'film.film.featured_film_locations', 'film.film_location.featured_in_films', 'film.film.genre', 'film.actor.film', 'film.producer.film', 'film.film.produced_by', 'film.film_character.portrayed_in_films', 'film.performance.character'] (score max 0.352)

verifier: grounded

---

## WebQTrn-3515_76ac752ffcee1b2759600cbec55107c7 (hedge)

**Q:** Which college attended by Paul Ryan was founded after 1809?

**gold:** ['American University']

**answer:** The answer could not be verified against the knowledge graph.

**entities:** []

plan: ['find colleges attended by Paul Ryan', 'find which of #1 were founded after 1809']

explored: ['education.education.student', 'people.person.education', 'award.award_nominee.award_nominations', 'base.descriptive_names.names.descriptive_name'] (score max 0.492)

explored: ['education.university.number_of_undergraduates', 'education.educational_institution.campuses', 'education.educational_institution.campuses', 'education.university.number_of_undergraduates', 'education.educational_institution.campuses', 'education.educational_institution.campuses'] (score max 0.261)

explored: ['education.university.number_of_undergraduates', 'education.educational_institution.campuses', 'education.educational_institution.campuses', 'education.university.number_of_undergraduates', 'education.educational_institution.campuses', 'education.educational_institution.campuses'] (score max 0.261)

explored: ['education.university.number_of_undergraduates', 'education.educational_institution.campuses', 'education.educational_institution.campuses', 'education.university.number_of_undergraduates', 'education.educational_institution.campuses', 'education.educational_institution.campuses'] (score max 0.261)

verifier: unsupported

---

## WebQTrn-849_8bb131f101e71d906d4a6dd2dbed06f7 (hedge)

**Q:** What countries border German and which one has a nominal GDP per capita of 36,000?

**gold:** ['Austria']

**answer:** Germany borders Denmark, Poland, Austria, Belgium, Netherlands, and Liechtenstein. From the provided facts, it could not be determined which one has a nominal GDP per capita of 36,000.

**entities:** []

plan: ['find countries that border Germany', 'find which of #1 has a nominal GDP per capita of 36,000']

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'film.film.country', 'film.film_regional_release_date.film', 'base.ontologies.ontology_instance_mapping.freebase_topic'] (score max 0.309)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.states_and_provences.continent', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country', 'base.biblioness.bibs_location.country', 'location.location.containedby', 'base.biblioness.bibs_location.state', 'base.biblioness.bibs_location.country', 'location.location.containedby', 'base.biblioness.bibs_location.state', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country'] (score max 0.309)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country', 'base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.biblioness.bibs_location.country'] (score max 0.309)

explored: ['base.locations.countries.continent', 'base.locations.continents.countries_within', 'base.locations.states_and_provences.continent', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country', 'base.biblioness.bibs_location.country', 'location.location.containedby', 'base.biblioness.bibs_location.state', 'base.biblioness.bibs_location.country', 'location.location.containedby', 'base.biblioness.bibs_location.state', 'base.biblioness.bibs_location.country', 'location.country.administrative_divisions', 'location.administrative_division.country'] (score max 0.309)

verifier: grounded

---

## WebQTrn-1484_256d41885c1839681311ca57f4d7b6c4 (hedge)

**Q:** What kind of paintings, that influenced Miguel Angel Asturias, did that Frida Kahola do?

**gold:** ['Surrealism']

**answer:** It could not be determined from the provided facts what kind of paintings Frida Kahola did that influenced Miguel Ángel Asturias. The facts only show that Miguel Ángel Asturias was influenced by Surrealism.

**entities:** []

plan: ['find what influenced Miguel Angel Asturias', 'find paintings by Frida Kahola that match #1']

explored: ['influence.influence_node.influenced_by', 'influence.influence_node.influenced', 'book.written_work.author', 'influence.influence_node.influenced', 'influence.influence_node.influenced', 'influence.influence_node.influenced_by'] (score max 0.518)

explored: ['visual_art.visual_artist.associated_periods_or_movements', 'visual_art.artwork.period_or_movement', 'visual_art.artwork.art_subject'] (score max 0.587)

verifier: grounded

---

## WebQTest-1797_2fb9e2823ccf35d2103fa8846d6f2ca8 (hedge)

**Q:** Of the people who fought in the Battle of Vicksburg, who has the earliest date of death?

**gold:** ['John C. Pemberton']

**answer:** Could not be determined from the provided facts, because no dates of death are given for the people who fought in the Siege of Vicksburg.

**entities:** []

plan: ['find the people who fought in the Battle of Vicksburg', 'find which of #1 has the earliest date of death']

explored: ['military.military_person.participated_in_conflicts', 'military.military_conflict.military_personnel_involved', 'base.americancivilwar.battle.military_units_involved_in_this_conflict'] (score max 0.571)

explored: ['people.deceased_person.place_of_death', 'people.person.place_of_birth', 'military.military_person.participated_in_conflicts', 'people.deceased_person.place_of_death', 'people.deceased_person.place_of_burial', 'people.person.place_of_birth', 'people.deceased_person.place_of_death', 'people.deceased_person.place_of_burial', 'people.person.place_of_birth', 'people.deceased_person.place_of_death', 'people.deceased_person.place_of_burial', 'government.political_party_tenure.politician', 'people.person.place_of_birth', 'award.award_honor.award_winner', 'military.military_person.participated_in_conflicts'] (score max 0.281)

explored: ['people.deceased_person.place_of_death', 'film.film_character.portrayed_in_films', 'location.hud_county_place.place', 'people.deceased_person.place_of_death', 'time.event.locations', 'film.film_festival.location', 'people.deceased_person.place_of_death', 'people.person.place_of_birth', 'time.event.locations', 'people.deceased_person.place_of_death', 'people.person.place_of_birth', 'fictional_universe.fictional_character.place_of_birth', 'people.deceased_person.place_of_death', 'people.deceased_person.place_of_burial', 'base.popstra.party.celebrities'] (score max 0.266)

explored: ['people.deceased_person.place_of_death', 'people.person.place_of_birth', 'military.military_person.participated_in_conflicts', 'people.deceased_person.place_of_death', 'people.deceased_person.cause_of_death', 'military.military_person.participated_in_conflicts', 'people.deceased_person.place_of_death', 'people.deceased_person.place_of_burial', 'people.person.places_lived', 'people.deceased_person.place_of_death', 'people.deceased_person.cause_of_death', 'people.cause_of_death.people', 'people.deceased_person.place_of_death', 'people.person.places_lived', 'people.place_lived.person'] (score max 0.266)

verifier: grounded

---

## WebQTrn-831_c191674d835a2284701f16d70a146360 (hedge)

**Q:** What is the last movie recorded by Faster Kill Pussycat (club mix)?

**gold:** ['Brooklyn']

**answer:** It could not be determined from the provided facts.

**entities:** []

plan: ['find the movie recorded by Faster Kill Pussycat (club mix)', 'find the last movie in #1']

explored: ['music.recording.song', 'music.artist.track', 'music.recording.tracks'] (score max 0.353)

explored: ['music.recording.song', 'music.artist.track', 'music.recording.tracks', 'music.recording.song', 'music.recording.song', 'music.artist.track', 'music.artist.track', 'film.producer.film', 'film.film.produced_by'] (score max 0.608)

explored: ['film.film.starring', 'film.film.release_date_s', 'film.film_regional_release_date.film'] (score max 0.276)

explored: ['film.film.starring', 'film.film_subject.films', 'film.film.subjects', 'film.film_subject.films', 'film.film.featured_film_locations', 'film.film.subjects', 'film.film.featured_film_locations', 'film.film.country', 'film.film.country', 'film.film_character.portrayed_in_films', 'film.actor.film', 'film.producer.film', 'film.actor.film', 'film.performance.actor', 'music.artist.track'] (score max 0.291)

verifier: grounded

---

## WebQTrn-2653_ea8442cb2c503dcbd06d9b7a77fed60d (hedge)

**Q:** What war did France participate in where it's fighting force was the smallest?

**gold:** ['Battle of Bailén']

**answer:** It could not be determined from the provided facts which war France participated in where its fighting force was the smallest.

**entities:** []

plan: ['find wars that France participated in', "find which of #1 had France's fighting force as the smallest"]

explored: ['military.military_combatant.includes_allies', 'military.military_combatant_group.combatants', 'military.military_combatant.belongs_to_combatant_group'] (score max 0.575)

explored: ['military.casualties.military_conflict', 'military.force_strength.military_conflict', 'military.military_combatant_group.conflict', 'military.force_strength.military_conflict', 'military.military_combatant_group.conflict', 'military.military_command.military_conflict', 'military.military_combatant_group.conflict', 'military.military_conflict.combatants', 'time.event.locations', 'military.military_combatant_group.conflict', 'military.military_command.military_conflict', 'military.military_conflict.combatants', 'military.military_combatant_group.conflict', 'military.military_conflict.combatants', 'time.event.locations'] (score max 0.555)

explored: ['military.military_combatant.military_conflicts', 'military.military_combatant.force_deployments', 'military.military_combatant.armed_forces', 'military.military_combatant.military_conflicts', 'military.military_combatant.force_deployments', 'location.statistical_region.size_of_armed_forces', 'military.military_combatant.force_deployments', 'military.military_combatant.includes_allies', 'military.military_combatant.armed_forces', 'military.military_combatant.force_deployments', 'military.military_combatant.armed_forces', 'military.military_combatant.casualties', 'military.casualties.type_of_casualties'] (score max 0.295)

explored: ['military.military_combatant_group.conflict', 'military.military_conflict.combatants', 'time.event.locations', 'military.military_combatant_group.conflict', 'military.military_conflict.combatants', 'time.event.included_in_event', 'military.military_combatant_group.conflict', 'military.military_command.military_conflict', 'military.military_conflict.combatants', 'military.military_combatant_group.conflict', 'military.military_conflict.combatants', 'military.military_conflict.military_personnel_involved', 'military.military_combatant_group.conflict', 'military.military_conflict.combatants', 'time.event.locations'] (score max 0.261)

verifier: grounded

---

## WebQTrn-452_f79ffe93341047ed2d8a39e5bb7d9156 (hedge)

**Q:** What city has a located ID less than 1783503 and is home to Lala Anthony?

**gold:** ['Baltimore']

**answer:** New York City is the city that fits the clue, but the located ID condition could not be determined from the facts provided.

**entities:** []

plan: ['find the city that is home to Lala Anthony', 'find which of #1 have a located ID less than 1783503']

explored: ['location.location.people_born_here', 'people.person.places_lived', 'people.place_lived.person'] (score max 0.198)

backtrack: evaluator

explored: ['people.person.place_of_birth', 'film.actor.film', 'people.person.sibling_s'] (score max 0.138)

explored: ['location.neighborhood.neighborhood_of', 'location.place_with_neighborhoods.neighborhoods', 'location.location.contains', 'film.film.featured_film_locations', 'film.film_location.featured_in_films', 'film.film.country', 'film.film.country', 'film.film.starring', 'film.film.personal_appearances', 'music.album.artist', 'film.film.starring', 'music.artist.album', 'film.film_character.portrayed_in_films', 'film.personal_film_appearance.type_of_appearance', 'tv.tv_guest_personal_appearance.appearance_type'] (score max 0.304)

explored: ['people.place_lived.location', 'location.neighborhood.neighborhood_of', 'location.location.nearby_airports', 'people.place_lived.location', 'location.neighborhood.neighborhood_of', 'location.neighborhood.neighborhood_of', 'people.place_lived.location', 'location.neighborhood.neighborhood_of', 'location.location.nearby_airports', 'location.neighborhood.neighborhood_of', 'location.location.nearby_airports', 'location.location.contains', 'location.location.contains', 'location.location.containedby'] (score max 0.507)

backtrack: evaluator

explored: ['location.location.contains', 'base.petbreeds.dog_city_relationship.cities', 'travel.travel_destination.local_transportation', 'location.place_with_neighborhoods.neighborhoods', 'location.place_with_neighborhoods.neighborhoods', 'location.location.contains', 'location.location.contains', 'base.petbreeds.dog_city_relationship.cities', 'travel.travel_destination.accommodation', 'location.location.geolocation', 'location.location.containedby', 'location.location.containedby'] (score max 0.293)

backtrack: evaluator

explored: ['travel.transportation.travel_destination', 'base.meedan.arabic_language_media_source.city', 'travel.travel_destination.how_to_get_here', 'location.location.contains', 'travel.tourist_attraction.near_travel_destination', 'location.location.people_born_here', 'travel.travel_destination.local_transportation', 'travel.transportation.travel_destination', 'base.biblioness.bibs_location.city', 'sports.sports_team.location', 'sports.sports_team_location.teams', 'aviation.airport.serves'] (score max 0.257)

verifier: grounded

---

## WebQTrn-3249_6dbfa476f0510018f470c29993293e68 (hedge)

**Q:** What tv show features Tamera Mowry and has a program "tvrage_id" lower than 5379?

**gold:** ['Sister, Sister', 'Detention']

**answer:** Tia & Tamera, The Real Talk Show, Sister, Sister, Detention, Strong Medicine, The Look for Less, and Roommates all feature Tamera Mowry, but the program tvrage_id is not provided in the facts, so it could not be determined which of these has a tvrage_id lower than 5379.

**entities:** []

plan: ['find tv shows that feature Tamera Mowry', 'find which of #1 have a program "tvrage_id" lower than 5379']

explored: ['tv.tv_personality.tv_regular_appearances', 'tv.regular_tv_appearance.actor', 'tv.tv_regular_personal_appearance.person'] (score max 0.594)

explored: ['tv.tv_program.episodes', 'tv.tv_program.regular_cast', 'tv.tv_program.genre', 'tv.tv_program.regular_cast', 'tv.tv_program.genre', 'tv.regular_tv_appearance.series', 'tv.tv_program.regular_cast', 'tv.tv_program.genre', 'tv.regular_tv_appearance.series', 'tv.tv_program.regular_personal_appearances', 'tv.tv_program.languages', 'tv.tv_regular_personal_appearance.program', 'tv.tv_program.regular_personal_appearances', 'tv.tv_program.seasons', 'tv.tv_program.languages'] (score max 0.35)

explored: ['tv.tv_program.episodes', 'tv.tv_program.original_network', 'tv.tv_program.regular_cast', 'tv.tv_program.episodes', 'tv.tv_program.original_network', 'tv.tv_program.regular_cast', 'tv.tv_character.appeared_in_tv_program', 'tv.regular_tv_appearance.character', 'tv.tv_personality.tv_regular_appearances', 'tv.tv_regular_personal_appearance.person', 'tv.regular_tv_appearance.actor', 'tv.tv_personality.tv_regular_appearances', 'tv.tv_regular_personal_appearance.person', 'tv.tv_producer.programs_produced'] (score max 0.335)

explored: ['tv.tv_program.episodes', 'tv.tv_program.episodes', 'tv.tv_program.episodes', 'tv.tv_program.episodes', 'tv.tv_program.episodes'] (score max 0.338)

verifier: grounded

---

## WebQTest-1923_a64ef0f5ce397a5e1ef6fcd550ebfcfb (hedge)

**Q:** What movies has Miley Cyrus been in with music by Aaron Zigman?

**gold:** ['Sex and the City 2', 'The Last Song']

**answer:** Miley Cyrus has been in The Last Song, So Undercover, Hannah Montana: The Movie, Radio Disney Party Jams: The Concert, Bolt, Wizards on Deck with Hannah Montana, The World According to Miley Cyrus, and LOL. However, from the facts provided, it could not be determined which of these had music by Aaron Zigman.

**entities:** []

plan: ['find movies that feature Miley Cyrus', 'find which of #1 have music by Aaron Zigman']

explored: ['film.actor.film', 'film.person_or_entity_appearing_in_film.films', 'film.performance.actor', 'film.film.music', 'film.music_contributor.film', 'music.artist.track_contributions'] (score max 0.548)

explored: ['film.film.music', 'music.track_contribution.track', 'film.film.soundtrack', 'film.film.music', 'film.music_contributor.film', 'film.film_crew_gig.film', 'film.film.music', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'film.film.music', 'film.film.featured_song', 'film.film_featured_song.featured_in_film', 'media_common.netflix_title.netflix_genres', 'film.film.starring', 'film.film.country'] (score max 0.541)

verifier: grounded

---

## WebQTest-1168_1591d6a0e6cef93c6863edb2eb0e198f (hedge)

**Q:** What kind of guitar did the author who published Kurt Cobain's journals play?

**gold:** ['Fender Jag-Stang']

**answer:** It could not be determined from the provided facts what kind of guitar the author who published Kurt Cobain's journals played.

**entities:** []

plan: ["find the author who published Kurt Cobain's journals", 'find the kind of guitar played by #1']

explored: ['book.book_edition.author_editor', 'book.author.book_editions_published', 'book.book_edition.publisher'] (score max 0.526)

backtrack: evaluator

explored: ['book.book_edition.book', 'book.book.editions', 'book.book_edition.binding'] (score max 0.158)

explored: ['book.book_edition.publisher', 'book.publishing_company.imprints', 'book.publisher_imprint_tenure.imprints'] (score max 0.076)

backtrack: low_score

explored: ['book.book_edition.binding', 'book.book.editions', 'book.book_edition.isbn'] (score max 0.131)

backtrack: low_score

explored: [] (score max 0.0)

verifier: grounded

---

## WebQTest-1301_5714a7a5f1feec1348045800b0c0c28c (hedge)

**Q:** Which amusement park in Sacramento California, was first opened in 1986?

**gold:** ['Raging Waters Sacramento']

**answer:** The answer could not be verified against the knowledge graph.

**entities:** []

plan: ['find amusement parks in Sacramento, California', 'find which of #1 was first opened in 1986']

explored: ['travel.travel_destination.tourist_attractions', 'travel.tourist_attraction.near_travel_destination', 'location.location.events'] (score max 0.562)

backtrack: evaluator

explored: ['film.film_festival.location', 'time.event.locations', 'location.place_with_neighborhoods.neighborhoods'] (score max 0.266)

explored: ['location.location.events', 'time.event.locations', 'base.peleton.road_bicycle_racing_event.start_location', 'location.location.events', 'film.film_festival_event.festival', 'time.event.locations', 'location.location.events', 'film.film_festival_event.festival', 'time.event.locations', 'location.location.events', 'film.film_festival_event.festival', 'time.event.locations', 'film.film_festival.location', 'film.film_festival.individual_festivals', 'film.film_festival_event.festival'] (score max 0.272)

backtrack: evaluator

explored: ['film.film_festival.location', 'time.event.locations', 'location.place_with_neighborhoods.neighborhoods'] (score max 0.266)

explored: ['base.peleton.road_bicycle_racing_event.finish_location', 'base.peleton.road_bicycle_racing_event.teams_participating_uci_protour', 'base.peleton.road_bicycle_racing_event.stages_held', 'time.event.instance_of_recurring_event', 'time.event.instance_of_recurring_event', 'base.events.festival_series.type_of_festival', 'film.film_festival_focus.festivals_with_this_focus', 'film.film_festival.focus'] (score max 0.2)

explored: ['location.location.events', 'time.event.locations', 'film.film_festival_focus.festivals_with_this_focus', 'location.location.events', 'time.event.locations', 'base.peleton.road_bicycle_racing_event.finish_location', 'base.events.type_of_festival.included_in_type', 'base.events.type_of_festival.includes_type_of_celebration', 'base.events.festival_series.type_of_festival', 'base.events.festival_series.type_of_festival', 'base.events.subject_of_festival.festivals_of_this_type', 'sports.sports_team_location.teams', 'sports.sports_team.location', 'base.peleton.road_bicycle_racing_event.teams_participating_uci_protour'] (score max 0.272)

explored: ['location.location.events', 'film.film_festival_event.festival', 'time.event.locations', 'base.peleton.road_bicycle_racing_event.finish_location', 'base.peleton.road_bicycle_racing_event.teams_participating_uci_protour', 'base.peleton.road_bicycle_racing_event.stages_held', 'base.events.type_of_festival.included_in_type', 'base.events.type_of_festival.includes_type_of_celebration', 'base.events.festival_series.type_of_festival', 'base.events.type_of_festival.includes_type_of_celebration', 'base.events.subject_of_festival.festivals_of_this_type', 'base.events.type_of_festival.includes_type_of_celebration', 'base.events.festival_series.type_of_festival', 'base.events.subject_of_festival.festivals_of_this_type'] (score max 0.272)

verifier: unsupported

---

## WebQTest-759_33c0a2138ef3f4a4f61dbee8dc9714e5 (hedge)

**Q:** Who has Brad Pitt dated in the past, and was into Buddhism?

**gold:** ['Thandie Newton']

**answer:** Brad Pitt dated Sinitta, Sonita Henry, Jill Schoelen, Shalane McCall, Katja von Garnier, Juliette Lewis, Nicole Appleton, Robin Givens, Julia Ormond, Claire Forlani, Felicitas Woll, and Christina Applegate. However, from the facts provided, it could not be determined who among these was into Buddhism.

**entities:** []

plan: ['find people Brad Pitt has dated in the past', 'find which of #1 were into Buddhism']

explored: ['celebrities.romantic_relationship.celebrity', 'base.popstra.celebrity.dated', 'celebrities.celebrity.sexual_relationships', 'celebrities.romantic_relationship.relationship_type', 'media_common.quotation.subjects', 'media_common.quotation_subject.quotations_about_this_subject', 'film.film.subjects'] (score max 0.62)

explored: ['people.person.religion', 'celebrities.romantic_relationship.celebrity', 'people.person.place_of_birth', 'celebrities.romantic_relationship.celebrity', 'celebrities.celebrity.sexual_relationships', 'music.artist.origin', 'celebrities.romantic_relationship.celebrity', 'celebrities.celebrity.sexual_relationships', 'people.person.profession', 'people.person.profession', 'people.person.gender', 'base.popstra.celebrity.dated', 'people.person.profession', 'people.person.nationality', 'people.person.gender'] (score max 0.461)

backtrack: evaluator

explored: ['celebrities.celebrity.sexual_relationships', 'film.actor.film', 'people.person.profession', 'people.person.profession', 'music.record_label.artist', 'people.person.nationality', 'people.person.nationality', 'people.person.gender', 'base.popstra.celebrity.dated', 'base.popstra.dated.participant', 'base.popstra.celebrity.dated', 'base.popstra.dated.participant'] (score max 0.135)

backtrack: evaluator

explored: ['film.performance.actor', 'base.popstra.lived_with.participant', 'people.person.nationality', 'people.person.gender', 'base.popstra.celebrity.dated', 'people.person.ethnicity', 'base.popstra.dated.participant'] (score max 0.091)

explored: ['celebrities.celebrity.legal_entanglements', 'book.written_work.subjects', 'people.person.religion', 'book.written_work.subjects', 'fictional_universe.fictional_character.gender', 'book.author.works_written', 'film.film.subjects', 'film.film.film_casting_director', 'film.film_casting_director.films_casting_directed', 'film.film.film_casting_director', 'film.film_casting_director.films_casting_directed', 'film.writer.film', 'media_common.adapted_work.adaptations', 'film.writer.film', 'film.film.written_by'] (score max 0.167)

backtrack: evaluator

explored: ['film.performance.actor', 'base.popstra.lived_with.participant', 'people.person.nationality', 'people.person.gender', 'base.popstra.celebrity.dated', 'people.person.ethnicity', 'base.popstra.dated.participant'] (score max 0.091)

explored: ['celebrities.legal_entanglement.celebrity', 'celebrities.romantic_relationship.celebrity', 'people.person.employment_history', 'book.written_work.previous_in_series', 'film.film.story_by', 'film.film.film_set_decoration_by', 'media_common.adapted_work.adaptations', 'media_common.adapted_work.adaptations', 'film.film.story_by', 'film.film.film_set_decoration_by', 'film.film.written_by', 'film.film.starring', 'film.film.starring', 'film.film_film_distributor_relationship.film', 'film.production_company.films'] (score max 0.154)

explored: ['celebrities.romantic_relationship.relationship_type', 'book.written_work.subjects', 'celebrities.romantic_relationship.celebrity', 'film.personal_film_appearance.person', 'celebrities.romantic_relationship.celebrity', 'people.person.place_of_birth', 'celebrities.celebrity.sexual_relationships', 'base.popstra.dated.participant', 'celebrities.legal_entanglement.offense', 'celebrities.reason_for_arrest.celebrities_charged_or_arrested'] (score max 0.166)

verifier: grounded

---

## WebQTest-389_27f6987805010183edbeba6b91a3cafd (hedge)

**Q:** What type of music was created by Claude Bebussy and in the Album Epica?

**gold:** ['Classical music']

**answer:** Claude Debussy created music compositions such as Jeux. Epica is a Classical music album by Audiomachine. The specific music type created by Claude Debussy in the Album Epica could not be determined from the facts provided.

**entities:** []

plan: ['find the music created by Claude Bebussy', 'find the music in the album Epica']

explored: ['music.composition.composer', 'film.film.music', 'music.artist.track_contributions', 'music.album.artist', 'music.artist.album', 'music.album.genre'] (score max 0.625)

explored: ['music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composer.compositions', 'music.composition.composer', 'music.composition.lyricist', 'music.composition.form', 'music.composition.composer', 'music.composition.composer', 'music.composition.composer', 'media_common.dedication.work_dedicated', 'media_common.dedicated_work.dedication'] (score max 0.344)

explored: ['music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composer.compositions', 'music.composition.lyricist', 'music.lyricist.lyrics_written', 'base.catalog.cataloged_composer.music_catalog', 'music.artist.track_contributions', 'music.composition.composer', 'music.composition.form', 'music.artist.genre', 'music.genre.artists', 'media_common.dedicatee.dedications', 'media_common.dedication.dedicated_to', 'people.person.gender'] (score max 0.359)

explored: ['music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composition.part_of', 'music.composition.includes', 'music.composition.composer', 'music.composer.compositions', 'music.composition.composer', 'music.composition.lyricist'] (score max 0.629)

verifier: grounded

---

