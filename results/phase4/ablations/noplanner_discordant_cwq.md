# noplanner-only-correct: cwq (15 cases)

## WebQTrn-1180_d234333cfe0037241bacdcbbc5a74317

**Question:** What County with Wellsville Missouri as downtown has 0.003572302 as its total Industrial CO2 emissions rate?

**Gold:** ['Montgomery County']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Montgomery County is the county with Wellsville as downtown, but the total Industrial CO2 emissions rate of 0.003572302 could not be determined from the facts provided. | Montgomery County. |
| entities | [] | ['Montgomery County'] |
| plan | ablated=False  sub_objectives=['find the county with Wellsville Missouri as downtown', 'find which of #1 has total Industrial CO2 emissions rate 0.003572302'] | ablated=True  sub_objectives=['What County with Wellsville Missouri as downtown has 0.003572302 as its total Industrial CO2 emissions rate?'] |
| backtracks | 1 backtracks: ['dead_end'] | 1 backtracks: ['dead_end'] |
| verifier | grounded | grounded |
| calls/tokens | 12/9685 | 11/7974 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTrn-25_4d68c1f4906c41ef2f0ea4e416e2615b

**Question:** Jack Giarraputo produced what movie that stars Taylor Lautner?

**Gold:** ['Grown Ups 2']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Jack Giarraputo produced Grown Ups, which stars Taylor Lautner could not be determined from the facts provided. | Jack Giarraputo produced Grown Ups 2, which stars Taylor Lautner. |
| entities | [] | ['Grown Ups 2'] |
| plan | ablated=False  sub_objectives=['find the movie that stars Taylor Lautner and was produced by Jack Giarraputo'] | ablated=True  sub_objectives=['Jack Giarraputo produced what movie that stars Taylor Lautner?'] |
| backtracks | 0 backtracks | 3 backtracks: ['evaluator', 'evaluator', 'evaluator'] |
| verifier | grounded | unsupported |
| calls/tokens | 10/7951 | 15/12990 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1260_018dc0c070e53555fa37f63d4b83ca87

**Question:** In what year did mascot Poe's team win the Super Bowl?

**Gold:** ['Super Bowl XXXV']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Poe's team won the Super Bowl in 2001. | Baltimore Ravens won the Super Bowl in 2001 and 2013, corresponding to Super Bowl XXXV and Super Bowl XLVII. |
| entities | ['Baltimore Ravens'] | ['Super Bowl XXXV', 'Super Bowl XLVII'] |
| plan | ablated=False  sub_objectives=['find the team of mascot Poe', 'find the year that #1 won the Super Bowl'] | ablated=True  sub_objectives=["In what year did mascot Poe's team win the Super Bowl?"] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 6/4269 | 5/3317 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-837_c4e06c3a9e4b4f10bd1ae97f1742c198

**Question:** In what year did a team win the superbowl and the 2013 AFC Championship Game ?

**Gold:** ['Super Bowl XLVII', 'Super Bowl XXXV']

| | full (with planner) | noplanner |
|---|---|---|
| answer | 2012 NFL season | Baltimore Ravens won Super Bowl XLVII and the 2013 AFC Championship Game, so the year was 2013. |
| entities | ['2012 NFL season'] | ['Baltimore Ravens', 'Super Bowl XLVII'] |
| plan | ablated=False  sub_objectives=['find the team that won the Super Bowl and the 2013 AFC Championship Game', 'find the year of #1'] | ablated=True  sub_objectives=['In what year did a team win the superbowl and the 2013 AFC Championship Game ?'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/8336 | 3/2975 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1797_dece4ddacc57788e31bf70edc99f1f37

**Question:** What Government position holder fought in the battle of Vicksburg?

**Gold:** ['Ulysses S. Grant']

| | full (with planner) | noplanner |
|---|---|---|
| answer | John C. Pemberton fought in the Siege of Vicksburg. | Ulysses S. Grant fought in the Siege of Vicksburg. |
| entities | ['John C. Pemberton'] | ['Ulysses S. Grant'] |
| plan | ablated=False  sub_objectives=['find the battle of Vicksburg', 'find the Government position holder who fought in #1'] | ablated=True  sub_objectives=['What Government position holder fought in the battle of Vicksburg?'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/9420 | 3/2401 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTrn-1001_33d9f1ae3911d4f69a9993902924107d

**Question:** Which Super Bowl did the Giants win against the Denver Broncos?

**Gold:** ['Super Bowl XXI']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Super Bowl XXXII | The Giants won against the Denver Broncos in Super Bowl XXI. |
| entities | ['Super Bowl XXXII'] | ['Super Bowl XXI'] |
| plan | ablated=False  sub_objectives=['find the Super Bowl that the Giants won against the Denver Broncos'] | ablated=True  sub_objectives=['Which Super Bowl did the Giants win against the Denver Broncos?'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/10550 | 3/3536 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-538_485b6c9f1bd7bd7972f3dd4fcc11b1e9

**Question:** What film was Taylor Swift in that Shelby Young was a crew member on?

**Gold:** ['Jonas Brothers: The Concert Experience']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Taylor Swift was in Hannah Montana: The Movie. | Taylor Swift was in Jonas Brothers: The Concert Experience, and Shelby Young was a crew member on Jonas Brothers: The Concert Experience. |
| entities | ['Hannah Montana: The Movie'] | ['Jonas Brothers: The Concert Experience'] |
| plan | ablated=False  sub_objectives=['find the film that Taylor Swift was in', 'find films where Shelby Young was a crew member', 'find the film from #1 that is also in #2'] | ablated=True  sub_objectives=['What film was Taylor Swift in that Shelby Young was a crew member on?'] |
| backtracks | 0 backtracks | 1 backtracks: ['evaluator'] |
| verifier | grounded | grounded |
| calls/tokens | 8/7247 | 11/8682 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTrn-2615_48a6ac5681b2e67e07d84708115db614

**Question:** What instruments does the author of Fela! play?

**Gold:** ['Drums', 'Guitar', 'Keyboard', 'Saxophone', 'Trumpet']

| | full (with planner) | noplanner |
|---|---|---|
| answer | It could not be determined from the provided facts what instruments Bill T. Jones or Jim Lewis play. | Fela Kuti plays Keyboard, Trumpet, Saxophone, Drums, and Guitar. |
| entities | [] | ['Keyboard', 'Trumpet', 'Saxophone', 'Drums', 'Guitar'] |
| plan | ablated=False  sub_objectives=['find the author of Fela!', 'find the instruments played by #1'] | ablated=True  sub_objectives=['What instruments does the author of Fela! play?'] |
| backtracks | 3 backtracks: ['evaluator', 'evaluator', 'evaluator'] | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 12/8432 | 5/3230 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1797_5a1c66f408118c6342c4a0eb350b58de

**Question:** Who was president during the battle of Vicksburg?

**Gold:** ['Ulysses S. Grant']

| | full (with planner) | noplanner |
|---|---|---|
| answer | The answer could not be verified against the knowledge graph. | Ulysses S. Grant was president during the battle of Vicksburg. |
| entities | [] | ['Ulysses S. Grant'] |
| plan | ablated=False  sub_objectives=['find the battle of Vicksburg', 'find the president during #1'] | ablated=True  sub_objectives=['Who was president during the battle of Vicksburg?'] |
| backtracks | 1 backtracks: ['evaluator'] | 0 backtracks |
| verifier | unsupported | grounded |
| calls/tokens | 14/15231 | 3/3267 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTrn-2570_ac52c51debd358141a23acc7ae7ec938

**Question:** Which WW2 US President had a political appointer that was White House Chief of Staff?

**Gold:** ['Harry S. Truman']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Dwight D. Eisenhower | Harry S. Truman, because White House Chief of Staff is shown as the political appointer for Harry S. Truman. |
| entities | ['Dwight D. Eisenhower'] | ['Harry S. Truman'] |
| plan | ablated=False  sub_objectives=['find the US President during World War II', 'find the political appointer of #1', 'find which of #2 was White House Chief of Staff'] | ablated=True  sub_objectives=['Which WW2 US President had a political appointer that was White House Chief of Staff?'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/9872 | 3/4471 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTrn-2570_d63877a40200d18c7c4e39215a3c7019

**Question:** This 33rd president was the nation's leader during WW2.?

**Gold:** ['Harry S. Truman']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Woodrow Wilson | Harry S. Truman was the nation's leader during World War II. |
| entities | ['Woodrow Wilson'] | ['Harry S. Truman'] |
| plan | ablated=False  sub_objectives=['find the 33rd president', "find the nation's leader during WW2"] | ablated=True  sub_objectives=["This 33rd president was the nation's leader during WW2.?"] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 10/9358 | 3/3375 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTrn-1597_8adc06ba12a3254370bdb3ff8e8820af

**Question:** Which character voiced by Seth MacFarlane was born in Thundera?

**Gold:** ['Lion-O']

| | full (with planner) | noplanner |
|---|---|---|
| answer | The answer could not be verified against the knowledge graph. | Lion-O was born in Thundera. |
| entities | [] | ['Lion-O'] |
| plan | ablated=False  sub_objectives=['find the character voiced by Seth MacFarlane', 'find which of #1 was born in Thundera'] | ablated=True  sub_objectives=['Which character voiced by Seth MacFarlane was born in Thundera?'] |
| backtracks | 1 backtracks: ['evaluator'] | 0 backtracks |
| verifier | unsupported | grounded |
| calls/tokens | 16/15311 | 3/3828 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-1348_3f44e0c4fd23a8334a972ebb812e0e35

**Question:** What Minneapolis sports team had Peyton Manning's father on their roster?

**Gold:** ['Minnesota Vikings']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Archie Manning was on the Minnesota Vikings roster. | Minnesota Vikings had Peyton Manning's father, Archie Manning, on their roster. |
| entities | ['Archie Manning'] | ['Minnesota Vikings'] |
| plan | ablated=False  sub_objectives=["find Peyton Manning's father", 'find the sports team that had #1 on their roster and is based in Minneapolis'] | ablated=True  sub_objectives=["What Minneapolis sports team had Peyton Manning's father on their roster?"] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 6/5260 | 5/4870 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-634_4f2c0d9eb022ed67ec2cc356d4d5113a

**Question:** What county does the place with San Antonio City Council located in?

**Gold:** ['Comal County']

| | full (with planner) | noplanner |
|---|---|---|
| answer | San Antonio City Council is located in San Antonio, which is in Bexar County. | San Antonio City Council is located in San Antonio, and San Antonio is in Comal County. |
| entities | ['Bexar County'] | ['Comal County'] |
| plan | ablated=False  sub_objectives=['find the place where the San Antonio City Council is located', 'find the county of #1'] | ablated=True  sub_objectives=['What county does the place with San Antonio City Council located in?'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 8/6547 | 5/4456 |

**category:** _(fill in)_

**note:** _(fill in)_

---

## WebQTest-965_e91a95bd503f0704b9cc40c6f2139524

**Question:** "Laziness may appear attractive but work gives satisfaction," was said by a person who went to what school?

**Gold:** ['Montessori Lyceum Amsterdam', 'Jewish Lyceum']

| | full (with planner) | noplanner |
|---|---|---|
| answer | Anne Frank went to Montessori Lyceum Amsterdam and Jewish Lyceum. | Anne Frank went to Montessori Lyceum Amsterdam. |
| entities | ['Anne Frank'] | ['Montessori Lyceum Amsterdam'] |
| plan | ablated=False  sub_objectives=['find the person who said "Laziness may appear attractive but work gives satisfaction"', 'find the school attended by #1'] | ablated=True  sub_objectives=['"Laziness may appear attractive but work gives satisfaction," was said by a person who went to what school?'] |
| backtracks | 0 backtracks | 0 backtracks |
| verifier | grounded | grounded |
| calls/tokens | 6/3283 | 5/5967 |

**category:** _(fill in)_

**note:** _(fill in)_

---

