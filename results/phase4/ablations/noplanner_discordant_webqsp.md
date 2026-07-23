# noplanner-only-correct: webqsp (21 cases)

## WebQTest-397

**Question:** what are the school colors for harvard university

**Gold:** ['Crimson']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Harvard University school colors could not be determined from the provided facts. | Harvard University's school colors are Crimson. |
| entities | [] | ['Crimson'] |
| plan | ablated=False  sub_objectives=['find Harvard University', 'find the school colors of #1'] | ablated=True  sub_objectives=['what are the school colors for harvard university'] |
| backtracks | 1 backtracks: ['evaluator'] | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/8170 | 3/1329 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-336

**Question:** what currency should you take to morocco

**Gold:** ['Moroccan dirham']

| | full (with planner) | noplanner |
|---|---|---|
| answer | The currency used in Morocco could not be determined from the provided facts. | You should take Moroccan dirham to Morocco. |
| entities | [] | ['Moroccan dirham'] |
| plan | ablated=False  sub_objectives=['find the country Morocco', 'find the currency used in #1'] | ablated=True  sub_objectives=['what currency should you take to morocco'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 8/6218 | 3/1323 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1679

**Question:** what kind of government does the united states have currently

**Gold:** ['Presidential system', 'Federal republic', 'Constitutional republic']

| | full (with planner) | noplanner |
|---|---|---|
| answer | The United States of America has the Federal government of the United States. | The United States of America has a Federal republic, a Presidential system, and a Constitutional republic. |
| entities | ['Federal government of the United States'] | ['Federal republic', 'Presidential system', 'Constitutional republic'] |
| plan | ablated=False  sub_objectives=['find the current government of the United States'] | ablated=True  sub_objectives=['what kind of government does the united states have currently'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 4/2308 | 3/1645 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-16

**Question:** what countries are part of the uk

**Gold:** ['Wales', 'Northern Ireland', 'Scotland', 'England']

| | full (with planner) | noplanner |
|---|---|---|
| answer | The United Kingdom is part of Europe. The facts do not determine any countries that are part of the UK. | England, Scotland, Wales, and Northern Ireland are part of the United Kingdom. |
| entities | [] | ['England', 'Scotland', 'Wales', 'Northern Ireland'] |
| plan | ablated=False  sub_objectives=['find the UK', 'find countries that are part of #1'] | ablated=True  sub_objectives=['what countries are part of the uk'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 6/3907 | 5/3623 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1233

**Question:** what are the colors of the ny giants

**Gold:** ['Red', 'Grey', 'Blue', 'White']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Could not be determined from the provided facts. | The New York Giants colors are Grey, White, Blue, and Red. |
| entities | [] | ['Grey', 'White', 'Blue', 'Red'] |
| plan | ablated=False  sub_objectives=['find the New York Giants', 'find the colors of #1'] | ablated=True  sub_objectives=['what are the colors of the ny giants'] |
| backtracks | 3 backtracks: ['low_score', 'low_score', 'low_score'] | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 12/13466 | 3/3789 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-567

**Question:** what is the zip code for nogales az

**Gold:** ['85621', '85628', '85662']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Nogales is contained by United States of America and Arizona, but the specific zip code for Nogales AZ could not be determined from the facts provided. | Nogales has postal codes 85621, 85628, and 85662. |
| entities | [] | ['85621', '85628', '85662'] |
| plan | ablated=False  sub_objectives=['find Nogales, AZ', 'find the zip code for #1'] | ablated=True  sub_objectives=['what is the zip code for nogales az'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/7127 | 3/3150 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1674

**Question:** who is the leader of north korea today

**Gold:** ['Kim Jong-un']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Kim Il-sung | Kim Jong-un |
| entities | ['Kim Il-sung'] | ['Kim Jong-un'] |
| plan | ablated=False  sub_objectives=['find the leader of North Korea today'] | ablated=True  sub_objectives=['who is the leader of north korea today'] |
| backtracks | 3 backtracks: ['evaluator', 'evaluator', 'evaluator'] | 3 backtracks: ['evaluator', 'evaluator', 'evaluator'] |
| verifier | grounded | grounded |
| calls/tokens | 14/12327 | 13/11961 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1353

**Question:** what are the four nations of the united kingdom

**Gold:** ['Wales', 'Northern Ireland', 'Scotland', 'England']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Could not be determined from the provided facts. The facts mention United Kingdom and United Kingdom, with Dependencies and Territories, but do not identify the four nations of the United Kingdom. | The four nations of the United Kingdom are Wales, England, Northern Ireland, and Scotland. |
| entities | [] | ['Wales', 'England', 'Northern Ireland', 'Scotland'] |
| plan | ablated=False  sub_objectives=['find the nations of the United Kingdom'] | ablated=True  sub_objectives=['what are the four nations of the united kingdom'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 6/5264 | 3/1679 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-329

**Question:** what type of government was formed when italy unified

**Gold:** ['Unitary state', 'Parliamentary republic', 'Constitutional republic']

| | full (with planner) | noplanner |
|---|---|---|
| answer | It could not be determined from the provided facts what type of government was formed when Italy unified. | Italy was formed as a Constitutional republic, and it is also listed as a Parliamentary republic and a Unitary state. |
| entities | [] | ['Constitutional republic', 'Parliamentary republic', 'Unitary state'] |
| plan | ablated=False  sub_objectives=['find the event of Italy unifying', 'find the type of government formed in #1'] | ablated=True  sub_objectives=['what type of government was formed when italy unified'] |
| backtracks | 3 backtracks: ['low_score', 'dead_end', 'dead_end'] | 2 backtracks: ['evaluator', 'evaluator'] |
| verifier | grounded | grounded |
| calls/tokens | 12/6095 | 7/5797 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-788

**Question:** what is the holy book of the buddhist religion

**Gold:** ['Gangōji Garan Engi', 'Longchen Nyingthig', 'Chinese Buddhist canon', 'Nīlakaṇṭha Dhāraṇī', 'Mahāvastu', 'Pāli Canon', 'Dhammapada', 'Āgama', 'Amitabha Sutra', 'Uṣṇīṣa Vijaya Dhāraṇī Sūtra', 'Vimalakirti Sutra', 'Śrīmālādevī Siṃhanāda Sūtra', 'Mahāyāna sūtras', 'Tibetan Buddhist canon']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Buddhism has several holy texts, including Pāli Canon, Mahāyāna sūtras, Tibetan Buddhist canon, Chinese Buddhist canon, Dhammapada, and Amitabha Sutra. If you mean a single holy book, it could not be determined from the facts provided. | Pāli Canon, Chinese Buddhist canon, Tibetan Buddhist canon, Dhammapada, and Mahāyāna sūtras are listed as religious texts of Buddhism. |
| entities | [] | ['Pāli Canon', 'Chinese Buddhist canon', 'Tibetan Buddhist canon', 'Dhammapada', 'Mahāyāna sūtras'] |
| plan | ablated=False  sub_objectives=['find the buddhist religion', 'find the holy book of #1'] | ablated=True  sub_objectives=['what is the holy book of the buddhist religion'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/7148 | 3/2601 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-284

**Question:** where did the latin language originate from

**Gold:** ['Indo-European languages', 'Italic languages']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Latin Language originated in Europe. | Latin Language originated in Europe and is part of the Italic languages and Indo-European languages. |
| entities | ['Europe'] | ['Europe', 'Italic languages', 'Indo-European languages'] |
| plan | ablated=False  sub_objectives=['find where the Latin language originated from'] | ablated=True  sub_objectives=['where did the latin language originate from'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/6462 | 5/3504 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1289

**Question:** what type of music did mozart composed

**Gold:** ['Classical music', 'Opera', 'Chamber music', 'Ballet', 'Art song']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Wolfgang Amadeus Mozart composed works including opera, symphony, concerto, chamber music, piano sonata, and songs. Examples from the facts include Don Giovanni, The Magic Flute, Symphony No. 37, Piano Concerto No.24 in C minor, String Quartet No. 17, Piano Sonata No. 6, and Songs. | Wolfgang Amadeus Mozart composed Opera and Classical music. |
| entities | ['Don Giovanni', 'The Magic Flute', 'Symphony No. 37', 'Piano Concerto No.24 in C minor', 'String Quartet No. 17', 'Piano Sonata No. 6', 'Songs'] | ['Opera', 'Classical music'] |
| plan | ablated=False  sub_objectives=['find the music composed by Mozart', 'find the type of #1'] | ablated=True  sub_objectives=['what type of music did mozart composed'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/8870 | 3/3091 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-2006

**Question:** what race is vanessa carlton

**Gold:** ['Scandinavians', 'Russian']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Could not be determined from the provided facts. | Vanessa Carlton is listed as Russian and Scandinavians. |
| entities | [] | ['Russian', 'Scandinavians'] |
| plan | ablated=False  sub_objectives=["find Vanessa Carlton's race"] | ablated=True  sub_objectives=['what race is vanessa carlton'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/7645 | 3/1394 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1309

**Question:** what art did wassily kandinsky do

**Gold:** ['Painting']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Wassily Kandinsky did works including Composition VIII, Painting with Green Center, Painting with Troika, Park im Herbst, Improvisation No. 30 (Cannons), Houses at Murnau, Succession, Autumn II, On the Points, Landscape with Two Poplars, Picture with an Archer, and Munich-Schwabing with the Church of St. Ursula. He is also associated with Abstract art, German Expressionism, and Der Blaue Reiter. | Wassily Kandinsky did Painting. The facts also list many artworks by Wassily Kandinsky, including Composition VIII, Painting with Green Center, and The White Dot. |
| entities | ['Composition VIII', 'Painting with Green Center', 'Painting with Troika', 'Park im Herbst', 'Improvisation No. 30 (Cannons)', 'Houses at Murnau', 'Succession', 'Autumn II', 'On the Points', 'Landscape with Two Poplars', 'Picture with an Archer', 'Munich-Schwabing with the Church of St. Ursula'] | ['Painting'] |
| plan | ablated=False  sub_objectives=['find the art that Wassily Kandinsky did'] | ablated=True  sub_objectives=['what art did wassily kandinsky do'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 4/4097 | 3/2987 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-869

**Question:** where is ancient phoenician

**Gold:** ['Lebanon']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Phoenicia. | Ancient Phoenicia was in Lebanon. |
| entities | ['Phoenicia'] | ['Lebanon'] |
| plan | ablated=False  sub_objectives=['find ancient Phoenician'] | ablated=True  sub_objectives=['where is ancient phoenician'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 6/3861 | 3/1166 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-893

**Question:** what is the zip code for azle texas

**Gold:** ['76098', '76020']

| | full (with planner) | noplanner |
|---|---|---|
| answer | The zip code for Azle, Texas could not be determined from the provided facts. | Azle has postal codes 76098 and 76020. |
| entities | [] | ['76098', '76020'] |
| plan | ablated=False  sub_objectives=['find Azle, Texas', 'find the zip code for #1'] | ablated=True  sub_objectives=['what is the zip code for azle texas'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/6466 | 3/1098 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-923

**Question:** what countries does england border

**Gold:** ['Wales', 'Scotland']

| | full (with planner) | noplanner |
|---|---|---|
| answer | England borders United Kingdom. The facts provided do not determine any other countries that England borders. | England borders Scotland and Wales. It is part of the United Kingdom. |
| entities | ['United Kingdom'] | ['Scotland', 'United Kingdom', 'Wales'] |
| plan | ablated=False  sub_objectives=['find countries that border England'] | ablated=True  sub_objectives=['what countries does england border'] |
| backtracks | 3 backtracks: ['evaluator', 'evaluator', 'evaluator'] | 0 backtracks |
| verifier | grounded | unsupported |
| calls/tokens | 14/8802 | 11/7502 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-118

**Question:** who fought in the gulf war 1991

**Gold:** ['France', 'Australia', 'United States of America', 'Argentina', 'Iraq', 'United Kingdom', 'Saudi Arabia']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Israel fought in the Gulf War 1991. | Iraq, Saudi Arabia, France, Australia, United States of America, and United Kingdom fought in the Gulf War. Several people also participated, including Colin Powell, Chuck Horner, and James Mattis. |
| entities | ['Israel'] | ['Iraq', 'Saudi Arabia', 'France', 'Australia', 'United States of America', 'United Kingdom', 'Colin Powell', 'Chuck Horner', 'James Mattis'] |
| plan | ablated=False  sub_objectives=['find the Gulf War in 1991', 'find who fought in #1'] | ablated=True  sub_objectives=['who fought in the gulf war 1991'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 6/5129 | 3/3455 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1362

**Question:** who is the state governor of florida

**Gold:** ['Rick Scott']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Francis P. Fleming is the state governor of Florida. | Rick Scott is the Governor of Florida. |
| entities | ['Francis P. Fleming'] | ['Rick Scott'] |
| plan | ablated=False  sub_objectives=['find the state governor of Florida'] | ablated=True  sub_objectives=['who is the state governor of florida'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/10114 | 9/9433 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1829

**Question:** what type of religion did massachusetts have

**Gold:** ['United Church of Christ', 'Buddhism', 'Churches of Christ', 'Methodism', 'Christianity', "Jehovah's Witnesses", 'Pentecostalism', 'Protestantism', 'Judaism', 'Baptists', 'Catholicism', 'Presbyterianism', 'Lutheranism', 'Episcopal Church']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Massachusetts is in the United States of America, and the retrieved facts do not determine a specific religion for Massachusetts. The only promising candidate mentioned is Christianity, but it is not supported directly by the facts above, so it could not be determined. | Massachusetts had Christianity, including Protestantism, Catholicism, Judaism, Buddhism, Pentecostalism, Lutheranism, Baptists, Presbyterianism, Churches of Christ, Jehovah's Witnesses, Episcopal Church, United Church of Christ, and Methodism. |
| entities | [] | ['Christianity', 'Protestantism', 'Catholicism', 'Judaism', 'Buddhism', 'Pentecostalism', 'Lutheranism', 'Baptists', 'Presbyterianism', 'Churches of Christ', "Jehovah's Witnesses", 'Episcopal Church', 'United Church of Christ', 'Methodism'] |
| plan | ablated=False  sub_objectives=['find Massachusetts', 'find the religion type associated with #1'] | ablated=True  sub_objectives=['what type of religion did massachusetts have'] |
| backtracks | 3 backtracks: ['evaluator', 'evaluator', 'evaluator'] | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 14/11986 | 3/2309 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-701

**Question:** what team is reggie bush on 2011

**Gold:** ['Miami Dolphins', 'New Orleans Saints']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Reggie Bush was on the Detroit Lions in 2011. | Reggie Bush was on Miami Dolphins in 2011. |
| entities | ['Detroit Lions'] | ['Miami Dolphins'] |
| plan | ablated=False  sub_objectives=['find the team Reggie Bush was on in 2011'] | ablated=True  sub_objectives=['what team is reggie bush on 2011'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 4/2415 | 3/3476 |

**category:** _(fill in)_

**note:** _(fill in)_

---

