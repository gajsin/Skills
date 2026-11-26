# Optional editing examples

Read only the relevant language and task. The pairs below are authored teaching
examples, not collected private correspondence, copied source passages, or proof of
human authorship. Their listed facts are the complete factual basis. Instruction
text is English; Russian passages are sample data. No specific wording is mandatory.

## Russian: choose from context, without a questionnaire

### Session summary, no recipient specified

Facts: duplicate form submissions were fixed; double-click was checked; no server
deployment was made. The user requests a short summary of the session.

Before: «В рамках сессии было реализовано исправление повторной отправки формы.
Выполнена проверка сценария двойного нажатия. Деплой не производился».

After: «Исправили повторную отправку формы и проверили двойное нажатие.
На сервер не выкладывали».

Keep the deployment limit; omit greetings and an invented addressee.

### Client message, no established familiarity

Facts: the writer made changes to a form, checked submission, and wants the client
to look at the result. The source establishes a male singular speaker.

Before: «Внесение правок в форму завершено. Проверка отправки выполнена.
Просьба ознакомиться с результатом и сообщить, подходит ли он».

After: «Внёс правки в форму и проверил отправку. Посмотрите, всё ли подходит».

Use polite «вы» here, not because all human writing must be formal. Do not transfer
the user's familiar address to the agent onto the client.

### Familiar colleague, established «ты»

Facts: a male writer updated the document; Oleg is asked to review its payment
section. The supplied correspondence uses «ты».

Before: «Олег, документ мною обновлён. Прошу тебя осуществить ознакомление
с разделом, касающимся оплаты».

After: «Олег, я обновил документ. Посмотри раздел об оплате».

Do not impose formal address on an established relationship.

### Short report with an unperformed check

Facts: the bug fix was made; unit tests passed; the integration test was not run
because database access was unavailable.

Before: «Было реализовано исправление ошибки, после чего был выполнен прогон
модульных тестов с положительным результатом. Интеграционный тест не был запущен
по причине отсутствия доступа к базе данных».

After: «Исправили ошибку, модульные тесты прошли. Интеграционный тест
не запускали: нет доступа к базе данных».

Do not compress this into «Всё проверили» or «Готово к выпуску».

### Explicit no-dash request

Source: «Сначала готовим ТЗ — потом пишем код. Проверка занимает 10–12 минут».
The user asks to remove long rhetorical dashes while preserving numeric ranges.

After: «Сначала готовим ТЗ, потом пишем код. Проверка занимает 10–12 минут».

Restructure prose; do not substitute a spaced hyphen. Exact quotations, commands
such as `git diff --stat`, identifiers, and ranges are not rhetorical punctuation.

### Already natural

Source: «Анна, пришлите, пожалуйста, таблицу с ценами. Она нужна для расчёта».

Keep it. Do not add a greeting, deadline, emotion, promise, or a different register
just to demonstrate editing. The name is fictional sample data.

## English: shared editorial checks

## Staging and repeated conclusions

Before: "This is not just a database, but the foundation of digital transformation."
After: "The database stores project data." Use that edit only if the source supports it.

Before: "The system keeps history. This is very important. It allows a previous version
to be restored. That is its main value."
After: "The system keeps history and allows a previous version to be restored."

Keep a real contrast: "Version A supports export; version B does not yet support it."
Both halves contain information.

## Rhythm and grammar

Before: "She opened the file. She checked the date. She sent the document."
After: "She opened the file, checked the date, and sent the document."
Keep deliberate repetition from a supplied writing sample.

Keep three real requirements: "We need search, export, and a change log."
Preserve grammatical punctuation in the source language. Keep ranges, units, and
symbols: "2025–2026", "10–12 ms", and `git diff --stat`. Do not rotate established
terms through synonyms just to vary vocabulary.

## Evidence and uncertainty

Before: "It may possibly, in some circumstances, be able to reduce latency."
After: "It may reduce latency." Keep the uncertainty.

Source: "After the update, latency fell from 120 to 90 ms on one test environment."
Safe edit: "On one test environment, latency fell from 120 to 90 ms after the update."
Unsafe edit: "The update makes the system 25% faster in all conditions."
The unsafe edit invents causality and generalises beyond the observation.

Source: "Experts say the service is reliable", without an identified source.
Do not invent an expert or endorse reliability. Flag unsupported attribution when
material, or retain it as an attributed claim. Do not silently erase a material
claim from a requested faithful rewrite.

## Formatting and protected content

Remove decorative labels only when their information survives. A comparison table
or requested checklist is useful structure. Preserve quotations, identifiers, URL
targets, and code when editing surrounding prose. For example, retain
`tool_choice="required"`, `C:/data/raw.json`, and `https://example.com/report?version=2`
exactly when supplied.

## Draft residue and history

Before: "Great question! Of course, here is the description. The service handles
imports. I hope that helps!"
After: "The service handles imports."

Keep a real limitation: "The interface was not checked in Antigravity."
Keep actual change history: "Version 2 fixed duplicate event delivery."

## Reader context

For a reader who already described the bug, lead with the decision and the fact
that affects it. Keep source pointers needed to act; avoid restating their diagnosis
merely to demonstrate that it was read.

A requested detailed report or standalone specification still needs its evidence
and background. Brevity does not authorize deleting requirements, negative results,
limitations, or requested decisions.
