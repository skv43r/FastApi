from models import Service, Trainer, TimeSlot, Branch, TrainerService, GroupClass, TrainerGroup
from database import db
from sqlmodel import Session, select
from typing import Annotated
from fastapi import Depends
from datetime import datetime, timedelta, time
import random

SessionDep = Annotated[Session, Depends(db.get_session)]

services_data = [
    {
        "name": "Хатха йога",
        "duration": "1",
        "description": """
            Персональные тренировки- это как костюм сшитый на заказ.
            В чем преимущества персоналок перед групповыми тренировками?

            - я работаю с вашим персональным запросом
            - я учитываю ваши исходные данные и индивидуальные физические и психические особенности
            - все время тренировки моё внимание принадлежит только вам
            - я планирую для вас персональный цикл тренировок на определенный срок времени исходя из вашего запроса и индивидуальных особенностей
            - мы выбираем удобное время, место, продолжительность и регулярность занятий
            - в персональной работе мы можем добиться максимальных результатов за минимальное время

            Для кого?

            Для тех, кто ценит свое время, комфорт, индивидуальный подход и прогнозируемый результат... и готов регулярно работать.

            Запросы, с которыми можно ко мне обратиться:

            - общее оздоровление и ОФП (увеличение силы, выносливости и мобильности опорно-двигательного аппарата, профилактика гиподинамии, сердечно-сосудистых заболеваний, заболеваний ОДА и других)
            - работа над определёнными направлениями подвижности, физическими качествами (гибкость, координация, выносливость, сила и т.д.) или темами (шпагаты, прогибы, наклоны, балансы и т.д.)
            - двигательное переобучение (обучение новым двигательным навыкам)
            - работа с дыханием, концентрацией, состоянием ума, техниками сосредоточения — по умолчанию включена во все практики, но по вашему запросу этим аспектам может уделяться больше или меньше внимания

            Занятия подходят для людей любого уровня подготовки без ограничений по состоянию здоровья (если у вас есть диагнозы в ремиссии, и врач разрешает занятия физической культурой — welcome).

            Реабилитацией и лечением не занимаюсь.
        """,
        "price": 3000,
        "photo": "https://assets.yclients.com/main_service_image/basic/a/a3/a3fa859373f5c5b_20240908015458.png",
        "category": "individual",
        "type": "training"
    },
    {
        "name": "Здоровая спина",
        "duration": "1",
        "description": """
            На индивидуальных занятиях я выстраиваю  практику под человека, его особенности здоровья и состояния и, конечно, под определенный запрос, если он есть. 
            Внимательно подхожу к успехам и трудностям практикующего.
            Обучение на йогатерапевта позволяет мне грамотно подобрать техники точечно под определенное заболевание или состояние человека. 
            Практикующий учится чувствовать свое тело, владеть им и избавляется от головных болей, болей в спине, шее и пояснице. 
            Прогресс на индивидуальных занятиях всегда кратно выше.
        """,
        "price": 3000,
        "photo": "https://assets.yclients.com/main_service_image/basic/e/eb/ebc3d23b4d1c8c6_20240813212720.png",
        "category": "individual",
        "type": "training"
    },
    {
        "name": "Йога для беременных",
        "duration": "1",
        "description": """
            Татьяна Мазкина - преподаватель по женской йоге и йоге для беременных. 
            Опыт преподавания 3 года, опыт личной практики 7 лет
            Обучение: Trini yoga school, Yogamed.

            Мое призвание - помогать женщинам создавать гармоничные отношения с самими собой. Я верю, что наше тело - это священный инструмент, способный находить глубокий контакт с нашей внутренней мудростью.


            Плюсы индивидуального подхода в практике йоги для беременных:
            ✅ Персональный подход.
            Инструктор может адаптировать практику йоги под конкретные потребности каждой беременной женщины, учитывая ее физическое состояние, уровень подготовки и индивидуальный запрос.
            ✅  Безопасность и контроль.
            Индивидуальные занятия проходят в  более тесном сопровождении практикующей, что обеспечивает безопасность и создаёт комфортную и доверительную атмосферу
            ✅ Удобное время. 
            Вы можете выбрать для себя комфортное время и удобный формат (онлайн\офлайн)
            ✅ Связь с ребёнком. 
            Во время индивидуальных занятий, инструктор проводит тематические медитации, что помогает создать связь со своим малышом, снизить тревожность и взрастить в себе чувство доверия
        """,
        "price": 3000,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "training"
    },
    {
        "name": "Лечебный массаж",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 2000,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Антицеллюлитный массаж",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 2500,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Спортивный массаж",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 3500,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Массаж лица",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 2000,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Классический массаж",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 2500,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Массаж спины",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 2000,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Баночный массаж",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 2000,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Массаж головы",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 1500,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Расслабляющий массаж",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 2500,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Массаж ног",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 1500,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    },
    {
        "name": "Массаж шейно-воротниковой зоны",
        "duration": "1",
        "description": """
            Массажи проводит Елена Сагир - профессиональный массажист с опытом более 6 лет. С медицинским образованием.
            Работает с лицом,: лифтинг эффект и омоложение. 
            Есть антицеллюлитные программы + баночный массаж, быстрый результат. 
            Отличное самочувствие и счастливое настроение сразу после сеанса!
        """,
        "price": 1500,
        "photo": "https://assets.yclients.com/main_service_image/basic/c/cf/cf26b900bf1bb68_20240912172950.png",
        "category": "individual",
        "type": "massage"
    }
]

group_services_data = [
    {
        "name": "Йога критического выравнивания",
        "duration": "1.15",
        "description": """
Йога критического выравнивания (Critical Alignment Yoga) - новая голландская методика восстановления позвоночника. В Практике используется ряд опорных приспособлений:
- планка для снятия напряжения мышц вдоль позвоночника
- войлочный валик для уменьшения напряжения в пояснично-крестцовом и грудном отделе
- бэкбендер - деревянная горка для прогибов и раскрытия грудного отдела
- хэдстендер - для перевернутых поз в безопасном положении 

Результатом занятий станет:
* исчезновение дискомфорта, ощущение легкости в спине и свободы в плечах
* подвижный, гибкий позвоночник
* исправление осанки
* медитативный подход в практике дает снятие стресса и гармонизацию психологического состояния, улучшается качество сна
        """,
        "price": 900
    },
    {
        "name": "Йога-терапия позвоночника",
        "duration": "1",
        "description": """
Мягкая практика с использованием элементов ЛФК, реабилитации, йоги критического выравнивания, направленная на восстановление гибкости, подвижности и силы позвоночника. 
Практика даёт:
* мягкое вытяжение позвоночника от шейного до пояснично-крестцового отдела
* выравнивание тела, восстановление и укрепление костных соединений ног, рук, кора
* видимое улучшение осанки
* исцеление остеохондроза и других возрастных изменений в позвоночнике в результате восстановления природной регенерации тканей.
Практика подходит для тех, кто только начинает знакомиться йогой, имеет ограничения подвижности в позвоночнике и другие заболевания опорно-двигательного аппарата.
        """,
        "price": 900
    },
    {
        "name": "Йога для беременных",
        "duration": "1",
        "description": """
Йога для беременных –это специально разработанный комплекс упражнений и практик, которые приносят пользу как физическом плане, так и эмоциональном в период беременности. В физическом аспекте, занятия йогой помогают укрепить мышцы тела, особенно в области спины, таза и ног, что может помочь в подготовке к родам и уменьшить нагрузку на опорно-двигательный аппарат. 
Йога в период беременности способствует улучшению гибкости и выносливости, улучшает кровообращение и помогает справиться со специфическими физическими проблемами, такими как токсикоз, отеки и боли в спине. 
В психологическом аспекте, йога для беременных помогает снизить уровень стресса и тревоги, улучшить психоэмоциональное состояние и почувствовать связь с малышом. Правильное дыхание и медитации помогают успокоить ум, улучшить сон и развить положительный настрой, что особенно важно в период беременности. Заниматься можно начинать с первого триместра и продолжать до самых родов.

Очень важно проконсультироваться с врачом, чтобы убедиться в безопасности и получить индивидуальные рекомендации. 
Плюсы йоги для беременных:
1. Укрепление мышц тела и подготовка к родам.
2. Улучшение гибкости и общего физического состояния. 
3. Снижение уровня стресса и тревожности.
4. Повышение качества сна и общего благополучия. 
5. Создание гармоничной связи с ребенком. 
6. Улучшение кровообращения и общего здоровья.
        """,
        "price": 900
    },
    {
        "name": "Детская аэро-йога",
        "duration": "1",
        "description": """
Аэро-йога для детей?‍♂
Воздушная йога в гамаках для детей сочетает в себе черты классической йоги на коврике, акробатики и аэробики,  позволяющая заниматься в движении  и полете. 

Гамак даёт большую свободу движений.После разминки и дыхательных упражнений дети выполняют классические асаны, специально адаптированные под юный возраст — силовые, перевёрнутые и другие. 

Они совершают прогибы, раскачивания, наклоны, кувырки, медленные покачивания и другие движения. 

?Все упражнения подбираются с учётом возраста детей, их физиологических особенностей и уровня их физического развития.

?Занятия позволяют детям расслабиться, избавиться от избытка энергии и чрезмерной напряжённости в теле, балансируют тело.
        """,
        "price": 700
    },
    {
        "name": "Хатха-йога для детей",
        "duration": "50",
        "description": """
Это хатха-йога, адаптированная под особенности детской психики и физиологии.

На занятиях преподаватель большое внимание уделяет правильному выполнению асан, дыханию и сконцентрированности детей. 

Они учатся контролировать свое тело, следить за тем, чтобы не задерживать дыхание и чувствовать себя комфортно.

Все это помогает детям:

* развить выносливость и силу воли
* сформировать ровную осанку
* укрепить мышечный корсет, 
* развить гибкость
* сформировать понимание своих потребностей
* воспитать самодисциплину и саморегулировку
* стать более спокойными и последовательными.

Практика подходит для детей и подростков от 7 до 16 лет.
        """,
        "price": 700
    },
    {
        "name": "Хатха-йога для начинающих",
        "duration": "1",
        "description": """
Хатха-йога - это классика и база всей йоги, разновидность практик, которые объединяют асаны, дыхательные упражнения и концентрацию внимания. «Ха» и «тха» — «солнце» и «луна». Практика хатха-йоги направлена на то, чтобы соединить и сбалансировать эти две энергии для здоровья ума и тела.
Статичные позы отлично прорабатывают все группы мышц и развивают силу, выносливость тела. Балансы - помогают создать эмоциональную стабильность, концентрацию внимания. Асаны на вытяжение помогают сделать тело мягким и эластичным. Пранаямы очищают сознание и дыхание, создают ясность ума. Шавасана в конце занятия сгармонизирует состояние, наполнит тело расслаблением. а ум тишиной.
Регулярные занятия:
* укрепят костную и мышечную системы организма,  восстановят здоровье позвоночника и суставов
* повысят эластичность мышц
* восстановят нервную систему, помогая справляться с переживаниями и стрессом.
        """,
        "price": 900
    },
    {
        "name": "Утренняя хатха для начинающих",
        "duration": "1.15",
        "description": """
Хатха-йога - это классика и база всей йоги, разновидность практик, которые объединяют асаны, дыхательные упражнения и концентрацию внимания. «Ха» и «тха» — «солнце» и «луна». Практика хатха-йоги направлена на то, чтобы соединить и сбалансировать эти две энергии для здоровья ума и тела.
Статичные позы отлично прорабатывают все группы мышц и развивают силу, выносливость тела. Балансы - помогают создать эмоциональную стабильность, концентрацию внимания. Асаны на вытяжение помогают сделать тело мягким и эластичным. Пранаямы очищают сознание и дыхание, создают ясность ума. Шавасана в конце занятия сгармонизирует состояние, наполнит тело расслаблением. а ум тишиной.
Регулярные занятия:
* укрепят костную и мышечную системы организма,  восстановят здоровье позвоночника и суставов
* повысят эластичность мышц
* восстановят нервную систему, помогая справляться с переживаниями и стрессом.
        """,
        "price": 900
    },
    {
        "name": "FLY Йога в гамаках",
        "duration": "1",
        "description": """
Fly yoga — это не просто йога в гамаке, она совмещает в себе йогу, стрейтчинг и элементы воздушной гимнастики.
Воздушная йога считается самой безопасной формой оздоровительных тренировок.

Это эффективный метод декомпрессии позвоночника, избавление от сутулости, расслабления мышц и связок.

Приятный бонус — тренировки на гамаке помогают справиться с тревожностью и «перезагрузить» головной мозг, улучшить работу вестибулярного аппарата.
        """,
        "price": 899
    },
    {
        "name": "Медитация с поющими чашами. Открытый урок.",
        "duration": "1",
        "description": """
Медитация с поющими Тибетскими чашами.
Гармония, покой, умиротворение. 
Эти измерения бытия доступны нам постоянно. А в настоящее время мы находимся в городском потоке и порой забывается наша истинная природа. 

? Соприкоснуться, услышать и соединиться с собой возможно благодаря вибрациям древнего инструмента - тибетской поющей чаши.

?В процессе практики проводник создаст общее поле и позволяет каждому участнику ощутить акустические вибрации по телу. 

✨? Вибрации чаши балансируют наше тело и психику. В результате воздействия чаши на человека достигается состояние внутреннего спокойствия и умиротворения . Звучание поющих чаш 
помогает:
?успокоить мозг и расслабиться
?освободиться от негативных эмоций и мыслей
?улучшить сон
?снизить уровень стресса и тревожности
?избавиться от головных болей, тошноты, спазмов и зажимов, которые провоцируются напряжением
?восполнить энергию
?установить внутреннюю гармонию
?стимулировать тело на самоисцеление 

?✨После практики почувствуете перезагрузку всей вашей системы , улучшение физического и психического здоровья, освободитесь от эмоциональных блоков, услышите свой внутренний голос, уйдете домой с новыми прекрасными мыслями ?
        """
    },
    {
        "name": "Аэро-йога",
        "duration": "1",
        "description": """
Во время занятий гамак частично или полностью позволяет практикующему переносить вес тела в гамак, используя его как дополнительную опору или как средство для углубления практики. Новичкам он становится надежным помощником в выполнении простых асан, а для опытных практиков инструментом для достижения прогресса в сложных асанах.
Что дает практика в гамаках:
- улучшение подвижности тазобедренных суставов, усиление циркуляция крови в органах малого таза, что препятствует застойным явлениям в этой области.
- перевернутые позы способствуют омоложению организма на клеточном уровне и нормализации гормонального фона.
- выполнение прогибов с опорой на гамак позволяет укрепить позвоночный столб и сделать его пластичным и гибким (здоровье и молодость позвоночника являются фундаментом долголетия).
- улучшение растяжки, осанки и координации движений.
- снятие мышечных спазмов, напряжения с позвоночника.
- улучшение работы сердечно-сосудистой и дыхательных систем.
        """,
        "price": 900
    }
]

trainers_data = [
    {
        "name": "Мастер-тренер",
        "specialization": "Преподаватель йоги",
        "photo": "https://assets.yclients.com/masters/origin/a/ad/ad65931d879a1e5_20240825210707.png"
    },
    {
        "name": "Алёна Атаманенко",
        "specialization": "Преподаватель йоги",
        "photo": "https://example.com/photo2.jpg"
    },
    {
        "name": "Ольга Павленко",
        "specialization": "Преподаватель йоги",
        "photo": None
    },
    {
        "name": "Вероника Быкова",
        "specialization": "Преподаватель йоги, массажист",
        "photo": "https://assets.yclients.com/masters/origin/a/ad/ad65931d879a1e5_20240825210707.png"
    },
    {
        "name": "Степуренко Валерия",
        "specialization": "Преподаватель йоги",
        "photo": "https://assets.yclients.com/masters/origin/a/ad/ad65931d879a1e5_20240825210707.png"
    },
    {
        "name": "Анастасия Шевченко",
        "description": """
Образование и опыт работы: 

21 октября 2023 - 21 января 2024 гг. ООО «Центр дополнительного образования «ЭКСПЕРТ». (Лицензия на образовательную деятельность № 08972 от 29.03.2019 г.).
Программа: «Тренер психорегулирующих фитнес-программ» в объеме 320 академических часов.
Получен Диплом о профессиональной переподготовке
Присвоена квалификация «тренер по фитнесу»

Курсы и тренинги:
Сертифицированный фитнес-тренер по программам:
 • Хатха-йога
 • Стретчинг 
 • Пилатес

На своих занятиях обращаю внимание на правильную технику выполнения асан. Начиная от кончиков пальцев рук и ног, концентрируя всё своё внимание на каждых линиях и изгибах тела. Завершая направлением взгляда, чистотой мыслей и техникой дыхания.
        """,
        "specialization": "Преподаватель йоги",
        "photo": "https://assets.yclients.com/masters/origin/a/ad/ad65931d879a1e5_20240825210707.png"
    },
    {
        "name": "Елена Грызунова",
        "description": """
Я начала свою практику в 2007 году с направления Хатха йоги. Йога для меня стала прекрасной возможностью достичь гармонии в духовном и физическом аспектах одновременно. Практика помогала мне лучше осознавать свое тело, мышцы, связки, стать более гибкой, познать себя и увидеть окружающий мир по-новому.

В 2018 году открыла для себя направление йоги в гамаках, с тех пор я влюблена в этот вид йоги. Прошла обучение у Строгоновой Елены в Федерации профессионалов фитнеса Краснодарского края (базовый и продвинутый уровень) сертифицированный инструктор Unnata Aerial Yoga. Преподавание с 2018 года. В 2019 году пройдено обучение по освоению практики в низком гамаке в аэройга. рф. 
        """,
        "specialization": "Преподаватель йоги",
        "photo": "https://assets.yclients.com/masters/origin/a/ad/ad65931d879a1e5_20240825210707.png"
    },
    {
        "name": "Юлия Андроник",
        "description": """
https://t.me/zdorovayaspina_julyandronik

Йога-тичер, ведущая индивидуальных, групповых и онлайн практик по направлениям: Йога- терапия позвоночника, Здоровая спина, голландская методика  восстановления позвоночника и всего опрно- двигательного аппарата Йога точного выравнивания (Critical Alignment yoga) на уникальном оборудовании.

Дипломы и курсы: 
- Диплом о среднем медицинском образовании по направлению "реабилитация"
- Сертификат "Инструктор йоги" 
- Диплом о профессиональной переподготовке  "Инструктор йоги"  
- Сертификат "инструктор по миофасциальной у релизу"                               - Сертификат о прохождении модуля "Диагностика в йтога-терапии точного выравнивания" Москва, Critical Alignment Therapy & Yoga Institute.   - Стажировка в Critical Alignment Therapy & Yoga Institut, Москва, 2024 год.
        """,
        "specialization": "Преподаватель йоги",
        "photo": "https://assets.yclients.com/masters/origin/a/ad/ad65931d879a1e5_20240825210707.png"
    }
]

branch_data = [
    {
        "name": "Йога Хом",
        "address": "улица Северная, 528а",
        "phone": "+7 929 827-40-24",
        "workingHours": "пн.-вс.: 9:00-21:00",
        "description": """
Студия йоги в центре Краснодара - Йога Хом

Попробуйте захватывающие занятия йогой в гамаках, улучшите гибкость и силу с Аштанга йогой, насладитесь мягкими практиками Soft йоги или восстановите здоровье спины с помощью Йогатерапии позвоночника. Присоединяйтесь к нам и найдите свой путь к внутреннему равновесию и благополучию

Возраст и уровень подготовки не важен, мы ждём всех, до встречи на ковриках!
        """,
        "photos": ["https://assets.yclients.com/general/1/1f/1f2cc8ec4a5827f_20240514033840.png", "https://assets.yclients.com/general/f/f7/f7095ee9343ea35_20240517002851.png", "https://assets.yclients.com/general/b/ba/ba57cda5a3abd3b_20240517002933.png", "https://assets.yclients.com/general/5/51/516bd1f88a1a3a1_20240517003010.png"]

    }
]

time_slots = [time(hour, minute) for hour in range(16, 17) for minute in (0, 30)]
start_date = datetime(2024, 12, 6)
end_date = datetime(2024, 12, 15)

def insert_data():
    with next(db.get_session()) as session:

        # for group in group_services_data:
        #         group_entry = GroupClass(**group)
        #         session.add(group_entry)

        # session.commit()
        
        # services = session.exec(select(Service)).all()
        # groups = session.exec(select(GroupClass)).all()
        # trainer_service_pairs = session.exec(select(TrainerService)).all()
        trainer_group_pairs = session.exec(select(TrainerGroup)).all()

        # for service in services:
        #     if service.type.lower() == "massage":
        #         trainer_service_entry = TrainerService(trainer_id=1, service_id=service.id)
        #         session.add(trainer_service_entry)
        #     else:
        #         random_trainer = random.randint(2, 8)
        #         trainer_service_entry = TrainerService(trainer_id=random_trainer, service_id=service.id)
        #         session.add(trainer_service_entry)
        
        # session.commit()

        # for group in groups:
        #         random_trainer = random.randint(2, 8)
        #         trainer_group_entry = TrainerGroup(trainer_id=random_trainer, group_class_id=group.id)
        #         session.add(trainer_group_entry)

        # session.commit()

        # for pair in trainer_service_pairs:
        #     trainer_id = pair.trainer_id
        #     service_id = pair.service_id

        #     current_date = start_date
        #     while current_date <= end_date:
        #         for slot_time in time_slots:
        #             full_datetime = datetime.combine(current_date.date(), slot_time)

        #             time_slot = TimeSlot(
        #                 trainer_id=trainer_id,
        #                 service_id=service_id,
        #                 dates=current_date.date(),
        #                 times=full_datetime.time(),
        #                 available=True,
        #                 created_at=datetime.utcnow()
        #             )
        #             session.add(time_slot)

        #         current_date += timedelta(days=1)

        #     session.commit()

        for pair in trainer_group_pairs:
            trainer_id = pair.trainer_id
            group_id = pair.group_class_id
        
            current_date = start_date
            while current_date <= end_date:
                for slot_time in time_slots:
                    full_datetime = datetime.combine(current_date.date(), slot_time)

                    time_slot = TimeSlot(
                        trainer_id=trainer_id,
                        group_class_id=group_id,
                        dates=current_date.date(),
                        times=full_datetime.time(),
                        available=True,
                        available_spots=random.randint(1, 10),
                        created_at=datetime.utcnow()
                    )

                    session.add(time_slot)

                current_date += timedelta(days=1)

            session.commit()

if __name__ == "__main__":
    insert_data()