# Knock Backend

## Skills

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![django-channels](https://img.shields.io/badge/-django--channels-blue)
![Clean architecture](https://img.shields.io/badge/-clean--architecture-orange)

## Project description

[https://tangible-velvet-8ec.notion.site/86e56bc3eca64e098925de8b2e6736ee?pvs=4](https://tangible-velvet-8ec.notion.site/86e56bc3eca64e098925de8b2e6736ee?pvs=4)

<img width="1440" alt="screen" src="https://github.com/knock-version-1-0/backend-main/assets/82345753/eb604005-dc32-4057-9507-683ede9458b9">

## ERD

[https://www.erdcloud.com/d/iwavjgkhiMCfbwSPq](https://www.erdcloud.com/d/iwavjgkhiMCfbwSPq)
<a href="https://www.erdcloud.com/d/iwavjgkhiMCfbwSPq">
    <img width="100%" alt="ERD" src="https://user-images.githubusercontent.com/82345753/230279648-be3b9384-d17a-46a7-95dc-aec7b259894c.png">
</a>

## API document

[https://app.swaggerhub.com/apis-docs/jinhyeok15/knock_api/1.0.0#](https://app.swaggerhub.com/apis-docs/jinhyeok15/knock_api/1.0.0#)
<a href="https://app.swaggerhub.com/apis-docs/jinhyeok15/knock_api/1.0.0#">
    <img width="100%" alt="swagger" src="https://user-images.githubusercontent.com/82345753/230279427-95f81f89-b5bd-4897-998f-4bc64e3cad7d.png">
</a>

## Figma

[https://www.figma.com/file/MhShAIR9PU5TMyKFEDGbtN/Knock-Figma?type=design&node-id=0%3A1&t=sdE1jPsdUBE39h9R-1](https://www.figma.com/file/MhShAIR9PU5TMyKFEDGbtN/Knock-Figma?type=design&node-id=0%3A1&t=sdE1jPsdUBE39h9R-1)
<a href="https://www.figma.com/file/MhShAIR9PU5TMyKFEDGbtN/Knock-Figma?type=design&node-id=0%3A1&t=sdE1jPsdUBE39h9R-1">
    <img width="1428" alt="스크린샷 2023-06-16 오전 1 12 03" src="https://github.com/knock-version-1-0/backend-main/assets/82345753/95d04681-044f-4465-a1cf-43e4c6c95d43">
</a>

## Deploy

1. Set .env file in ./src/
2. Set logs/app.log in ./src/knock/
3. [Command] make up-prod

## Clean

1. [Command] make clean
2. [Command] docker volume rm $(docker volume ls -q)
