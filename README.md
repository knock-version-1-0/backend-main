# Knock Backend

## Skills

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

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

## Description

Knock main backend is concentrated on how to manage note application.

Note domain is very conceptual and iconic application in knock project. To protect the concistency and make great sensitivity of domain, I should choice the architecture that could test efficiently.

Thanks to https://github.com/sdediego/django-clean-architecture, I can make a draft of the clean architecture based on django rest framework. Additionally, I drive intuitive solutions like below.

1. DI

    Using factory that can access the objects with property(getter) which provide simple testable object.

2. DIP

    To make independency of accessing database in usecase, usecase refers repository interface, not a repository instance. To implement usecase, we should use repository interface that is not implemented. Dependency injection factory can do inject the dependency of repository on usecase.

3. Exception based logic

    To process status of requirement, I use the domain exception. The domain exception name is the same as the Schema in the API Documentation.

<img width="559" alt="image" src="https://user-images.githubusercontent.com/82345753/231099383-a80e29cf-1e2f-4e78-addf-8823531ba7b6.png">
