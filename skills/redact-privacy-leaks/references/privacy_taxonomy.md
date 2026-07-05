# Strict Privacy Taxonomy

Use this reference to widen the scan beyond obvious PII. The working rule is: if a value can identify, contact, locate, authenticate, profile, single out, track, or re-identify a person alone or in combination, surface it for user choice.

## Source-Informed Baseline

- NIST SP 800-122 treats PII as information that can distinguish or trace identity, or can identify a person when linked with other information: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf
- GDPR Article 4 includes names, ID numbers, location data, online identifiers, and factors specific to physical, physiological, genetic, mental, economic, cultural, or social identity: https://gdpr-info.eu/art-4-gdpr/
- FTC business guidance emphasizes minimizing, protecting, and safely disposing of personal information collected or stored by organizations: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business

## Always Flag

- Names and aliases: legal names, preferred names, nicknames, initials with context, romanized names, handles.
- Contact information: email, phone, messaging IDs, social profiles, home/work/school addresses.
- Government, school, work, and account identifiers: national IDs, passport, driver license, student ID, employee ID, customer ID, usernames.
- Authentication and secrets: passwords, recovery answers, API keys, tokens, session IDs, private keys, cookies.
- Location: precise address, dorm/building, GPS, commute route, neighborhood, hometown, school city, workplace city.
- Time-linked routines: class schedule, shift schedule, commute time, event attendance, check-in history.
- Demographics: age, birth date, gender, sex, nationality, ethnicity, race, religion, language, marital/family status.
- Education and work: school, grade, major, class, thesis topic, employer, role, team, manager, salary.
- Health and biometrics: health status, disability, medication, diagnosis, genetics, face, fingerprint, voiceprint.
- Financial and legal: bank/payment accounts, income, tax, debt, legal cases, insurance.
- Children/minors: anything identifying or describing a minor or student, even if otherwise mundane.

## Also Flag Profiling Clues

- Personality and psychology: MBTI, Big Five traits, introversion, anxiety, habits, temperament.
- Preferences and interests: favorite apps, games, music, food, shopping habits, hobbies, fandoms, political views.
- Behavioral data: browsing, search history, device use, sleep, exercise, spending, travel, attendance.
- Relationship graph: family, friends, roommates, teachers, coworkers, social circles.
- Free-text self descriptions: "I am a...", "my hometown...", "I like...", "I usually...".

## Combination Risk

Flag otherwise ordinary facts when several appear together. Examples:

- Age + school + city.
- Hobby + rare major + grade.
- First name + workplace/team.
- Region + commute route + schedule.
- Writing style + personal story + date.

When in doubt, list the item and let the user decide.
