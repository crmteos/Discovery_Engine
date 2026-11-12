### Комплект системної документації: Впровадження системних покращень Discovery Engine (Вузли 01 та 06\)

#### 1\. Системний огляд та архітектурне бачення

У рамках еволюції автономної детермінованої системи Discovery Engine постає завдання формального розширення та оптимізації її фундаментальних обчислювальних і модельних компонентів — Вузла 01 (Formal Core & Scientific Engines) та Вузла 06 (Formalized Target Model & Viewpoints).  
Система функціонує в умовах суворого інженерного обмеження BUDGET\_LIMIT \= \$0.00, спираючись на локальне апаратне забезпечення та гібридний механізм інференсу Dual-Provider Inference Engine (локальний сервер Ollama REST API з обчисленнями на CPU та безкоштовні хмарні квоти Google AI Studio / Vertex AI Enterprise Switcher). Двовертикальний стандарт управління Dual-Vertical 2-File Standard забезпечує чітке розділення системного контексту на Control Plane (файл PROJECT\_STATE.md) та Data Plane (файл PROJECT\_CONTEXT.md).  
Даний комплект системної документації регламентує формальні специфікації, математичні методи, архітектурні оператори та інженерні стандарти для чотирьох ключових напрямків покращення:

* Впровадження концептуальної метамоделі ISO/IEC/IEEE 42010:2022 та оператора проєкцій AXIOMATIC\_TRANSFORMER у Вузлі 06\.  
* Оптимізація ядра Топологічного аналізу даних (TDA) та формалізація модуля аксіоматичної трансформації базисів у Вузлі 01\.  
* Побудова строго типізованого мосту між неструктурованими LLM та Pure Python ядром через Firebase Genkit Python SDK, Dotprompt та Pydantic AI.  
* Забезпечення наскрізного контролю цілісності та аудиту знань на основі W3C SHACL 1.2 Profiling та W3C PROV-O.

#### 2\. Специфікація Вузла 06: Метамодель ISO/IEC/IEEE 42010:2022 та AXIOMATIC\_TRANSFORMER

##### 2.1 Концептуальна метамодель ISO/IEC/IEEE 42010:2022

Поточна реалізація Вузла 06 використовувала фіксовану трьохракурсну схему (Концептуальний, Контекстний та Логічний ракурси). Відповідно до другого видання міжнародного стандарту ISO/IEC/IEEE 42010:2022 (Systems and software engineering — Architecture description), суб'єкт архітектурного опису узагальнюється від "System of Interest" до "Entity of Interest", а структура ракурсів модернізується шляхом введення трьох фундаментальних концептів:

1. Stakeholder Perspectives: Системні перспективи стейкхолдерів, які групують занепокоєння (Concerns) та організують архітектурні точки зору (Architecture Viewpoints).  
2. View Components: Модульні компоненти ракурсів (які замінюють застарілі поняття Architecture Models), що забезпечують перевикористання графічних та онтологічних фрагментів між різними ракурсами.  
3. Architecture Aspects: Критичні характеристики та зрізи сутності (безпека, продуктивність, математична детермінованість, вартість), що проходять наскрізь через усі Architecture Views та забезпечують простежуваність (traceability) між Concerns та Views.

Стандарт ISO/IEC/IEEE 42010 визначає співвідношення між архітектурними елементами через зв'язки відповідностей (Correspondences) та правила відповідності (Correspondence Rules), що виключають внутрішні суперечності при формуванні підсумкового архітектурного опису.

##### 2.2 Архітектура та математика оператора AXIOMATIC\_TRANSFORMER

Оператор проєкцій AXIOMATIC\_TRANSFORMER є Pure Python модулем, що розміщується за шляхом 06\_Formalized\_Model/src/axiomatic\_transformer.py. Його призначення — приймати канонічний граф валідованих RDF-триплетів з каналу 05\_Knowledge\_Aggregator/Processed\_Gate/normalized\_triples/ і генерувати цільові специфіковані когнітивні проєкції без викривлення чи втрати первинних фактів.  
Формально оператор визначений як семантична функція фільтрації та реструктуризації:  
\$\$\\mathcal{T}*{\\theta}: \\mathcal{G}*{raw} \\times \\mathcal{VP}*{k} \\longrightarrow \\mathcal{V}*{k}\$\$  
де  \$\\mathcal{VP}*{k}\$  — специфікований Viewpoint (включаючи Concerns, Aspect Rules та View Components), а  \$\\mathcal{V}*{k}\$  — підсумковий Architecture View у вигляді JSON-LD / JSON 3-view конфігурації.

##### 2.3 Специфікація JSON-контракту та інтерфейсу

Для забезпечення сумісності з шиною повідомлень Bridge/bus\_manager.py оновлений формат вихідної когнітивної моделі регламентується JSON-схемою 06\_Formalized\_Model/schemas/iso42010\_viewpoint\_schema.json.  
{  
  "title": "ISO42010\_Architecture\_Description\_Schema",  
  "type": "object",  
  "required": \["entity\_of\_interest", "stakeholder\_perspectives", "architecture\_views", "correspondence\_rules"\],  
  "properties": {  
    "entity\_of\_interest": {  
      "type": "string",  
      "example": "Discovery Engine Architecture v5.4.0"  
    },  
    "stakeholder\_perspectives": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "required": \["perspective\_id", "framed\_concerns"\],  
        "properties": {  
          "perspective\_id": { "type": "string" },  
          "framed\_concerns": { "type": "array", "items": { "type": "string" } }  
        }  
      }  
    },  
    "architecture\_views": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "required": \["view\_id", "governing\_viewpoint", "view\_components", "reflected\_aspects"\],  
        "properties": {  
          "view\_id": { "type": "string" },  
          "governing\_viewpoint": { "type": "string" },  
          "view\_components": {  
            "type": "array",  
            "items": {  
              "type": "object",  
              "required": \["component\_id", "triples\_subset"\],  
              "properties": {  
                "component\_id": { "type": "string" },  
                "triples\_subset": { "type": "array", "items": { "type": "object" } }  
              }  
            }  
          },  
          "reflected\_aspects": { "type": "array", "items": { "type": "string" } }  
        }  
      }  
    },  
    "correspondence\_rules": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "required": \["rule\_id", "source\_element", "target\_element", "relation\_type"\],  
        "properties": {  
          "rule\_id": { "type": "string" },  
          "source\_element": { "type": "string" },  
          "target\_element": { "type": "string" },  
          "relation\_type": { "type": "string", "enum": \["refinement", "consistency", "traceability", "dependency"\] }  
        }  
      }  
    }  
  }  
}

#### 3\. Специфікація Вузла 01: Математичне ядро, Оптимізація TDA та Аксіоматична Трансформація Базисів

##### 3.1 Оптимізація ядра топологічного аналізу даних (TDA)

Топологічний аналіз даних у Вузлі 01 відповідає за виявлення глобальних геометричних інваріантів у багатовимірних хмарах точок. У поточному Pure Python модулі pure\_tda\_engine.py обчислення персистентних гомологій базується на побудові комплексу В'єторіса-Ріпса (Vietoris-Rips Complex).  
Для будь-якої хмари точок  \$\\mathcal{X}\$  та параметра фільтрації  \$\\epsilon \> 0\$  симпліціальний комплекс В'єторіса-Ріпса  \$\\mathcal{VR}(\\mathcal{X}, \\epsilon)\$  визначається як:  
\$\$\\mathcal{VR}(\\mathcal{X}, \\epsilon) \= \\left\\{ \\sigma \\subseteq \\mathcal{X} \\;\\mid\\; \\forall x\_i, x\_j \\in \\sigma, \\; \\\|x\_i \- x\_j\\\|\_2 \\le \\epsilon \\right\\}\$\$  
Обчислювальна складність комплексу В'єторіса-Ріпса зростає комбінаторно як  \$\\mathcal{O}(2^{\|\\mathcal{X}\|})\$ , що спричиняє суттєве затримання обчислень на CPU при збільшенні кількості точок. Для подолання цього обмеження в систему впроваджуються дві оптимізації:

1. Alpha-комплекси (Alpha Complexes): Використання діаграм Вороного та тріангуляції Делоне для підпростору  \$\\mathbb{R}^d\$ . Сімпликс  \$\\sigma\$  належить Alpha-комплексу  \$\\mathcal{A}\_{\\alpha}(\\mathcal{X})\$ , якщо перетин куль радіуса  \$\\alpha\$  з центрами у вершинах  \$\\sigma\$  та відповідних осередків Вороного  \$V\_x\$  є непорожнім:

\$\$\\mathcal{A}*{\\alpha}(\\mathcal{X}) \= \\left\\{ \\sigma \\subseteq \\mathcal{X} \\;\\mid\\; \\bigcap*{x \\in \\sigma} \\left( B(x, \\alpha) \\cap V\_x \\right) \\neq \\emptyset \\right\\}\$\$  
Це зменшує кількість симплексів до порядку  \$\\mathcal{O}(\|\\mathcal{X}\|^{\\lceil d/2 \\rceil})\$ , що робить обчислення на Pure Python життєздатними для  \$d \\le 3\$ .

1. Фільтрації за відстанню до міри (Distance-to-Measure, DTM): Забезпечення робастності до топологічного шуму та викидів. Для ймовірнісного розподілу  \$P\$  та параметра  \$m \\in (0, 1)\$  функція DTM  \$d\_{P, m}(x)\$  визначається як:

\$\$d\_{P, m}(x) \= \\left( \\frac{1}{m} \\int\_0^m \\delta\_{P, r}^2(x) \\, dr \\right)^{1/2}\$\$  
де  \$\\delta\_{P, r}(x) \= \\inf \\{t \> 0 \\mid P(B(x, t)) \\ge r\\}\$ . Для дискретної хмари точок  \$\\mathcal{X}\$  функція спрощується до середнього квадратичного відстанно від  \$x\$  до її  \$k \= \\lceil m \|\\mathcal{X}\| \\rceil\$  найближчих сусідів:  
\$\$d\_{\\mathcal{X}, m}(x) \= \\sqrt{\\frac{1}{k} \\sum\_{i=1}^k \\\|x \- x\_{(i)}(x)\\\|^2}\$\$

1. Time-Delay Embedding: Для обробки часових рядів  \$X(t)\$  застосовується теорема Тейкенса про вкладення із часовою затримкою  \$\\tau\$  та розмірністю вкладення  \$d\_e\$ :

\$\$\\mathbf{Y}(t) \= \\left( X(t), X(t \- \\tau), X(t \- 2\\tau), \\dots, X(t \- (d\_e \- 1)\\tau) \\right) \\in \\mathbb{R}^{d\_e}\$\$  
Отриманий фолдінг перетворює 1D часовий ряд у багатовимірну хмару точок, на якій через обчислення персистентної гомології (чисел Бетті  \$H\_0\$  — зв'язні компоненти,  \$H\_1\$  — одновимірні цикли/зацикленості) виявляються періодичні фазові атрактори та топологічні порожнини.  
\# Pure Python DTM & Time-Delay Embedding Spec (pure\_tda\_engine.py)  
import math  
import numpy as np

def time\_delay\_embedding(time\_series: list\[float\], embedding\_dim: int, delay: int) \-\> np.ndarray:  
    """Трансформує часовий ряд у багатовимірну хмару точок за теоремою Тейкенса."""  
    n \= len(time\_series)  
    max\_idx \= n \- (embedding\_dim \- 1\) \* delay  
    if max\_idx \<= 0:  
        raise ValueError("Занадто короткий часовий ряд для вказаних embedding\_dim та delay")  
      
    point\_cloud \= \[\]  
    for i in range(max\_idx):  
        point \= \[time\_series\[i \+ j \* delay\] for j in range(embedding\_dim)\]  
        point\_cloud.append(point)  
    return np.array(point\_cloud)

def compute\_dtm\_weights(point\_cloud: np.ndarray, k: int) \-\> np.ndarray:  
    """Обчислює вагові коефіцієнти DTM для кожної точки хмари."""  
    n \= len(point\_cloud)  
    dtm\_values \= np.zeros(n)  
    for i in range(n):  
        dists \= np.linalg.norm(point\_cloud \- point\_cloud\[i\], axis=1)  
        dists.sort()  
        k\_dists \= dists\[:k\]  
        dtm\_values\[i\] \= math.sqrt(np.mean(k\_dists \*\* 2))  
    return dtm\_values

##### 3.2 Символьний ШІ та доведення інваріантів (SymPy CAS)

У модулі 01\_Formal\_Core/Symbolic\_AI/sympy\_cas\_prover.py функціонує Pure Python середовище аналізу AST-дерев та символьної комп'ютерної алгебри. Воно реалізує три основні операції:

* canonical\_simplify(expr\_str): Перетворення символьного виразу у канонічну спрощену форму за допомогою AST-дерева SymPy та процедури sympy.simplify().  
* check\_satisfiability(proposition\_str): Перевірка здійснюваності та несуперечливості фактів через розв'язання символьних рівнянь  \$\\text{Solve}(P(x) \= 0)\$ .  
* verify\_invariant(system\_state, invariant\_expr): Автоматичне доведення збереження системного інваріанта  \$\\mathcal{I}(S) \\equiv \\text{True}\$  при переході станів  \$S\_t \\to S\_{t+1}\$ .

##### 3.3 Специфікація модуля basis\_transformer.py

Для виконання аксіоматичних перетворень та переходу між математичними базисами у Вузол 01 додається модуль 01\_Formal\_Core/src/basis\_transformer.py. Модуль розв'язує дві фундаментальні задачі:

###### *1\. Логарифмічна трансформація знань ( \$\\log\_{10} \\to \\log\_2\$ )*

Антропоморфна 10-кова система знань переводиться на інформаційно-природну двійкову основу (біт/нат). Для будь-якої кількісної метрики або ентропійного значення  \$K\_{10}\$  перехід здійснюється за формулою:  
\$\$K\_2 \= \\log\_2(10) \\cdot K\_{10} \= \\frac{\\ln(10)}{\\ln(2)} \\cdot K\_{10} \\approx 3.321928 \\cdot K\_{10}\$\$  
Для теорії інформації Шеннона перетворення гарантує точне вимірювання ентропії  \$H(X)\$  у двійкових одиницях (бітах):  
\$\$H\_2(X) \= \- \\sum\_{i=1}^n P(x\_i) \\log\_2 P(x\_i)\$\$

###### *2\. Заміна часового параметра суперпозицією частотних процесів (DFT/FFT)*

Антропоморфний параметр часу  \$t \\in \\mathbb{R}^+\$  замінюється на частотний спектр  \$\\omega \\in \\Omega\$  за допомогою дискретного перетворення Фур'є (Discrete Fourier Transform, DFT). Для дискретного сигналу фактів  \$fn, n \= 0, \\dots, N-1\$ :  
\$\$Fk \= \\sum\_{n=0}^{N-1} fn \\cdot e^{-i 2\\pi \\frac{k n}{N}} \= \\sum\_{n=0}^{N-1} fn \\left( \\cos\\left(\\frac{2\\pi k n}{N}\\right) \- i \\sin\\left(\\frac{2\\pi k n}{N}\\right) \\right)\$\$  
Зворотне перетворення відтворює часовий процес як суперпозицію гармонічних осциляторів:  
\$\$fn \= \\frac{1}{N} \\sum\_{k=0}^{N-1} Fk \\cdot e^{i 2\\pi \\frac{k n}{N}}\$\$  
Модуль спектра  \$\|Fk\| \= \\sqrt{\\text{Re}(Fk)^2 \+ \\text{Im}(Fk)^2}\$  фіксує амплітуду частотного процесу, а фаза  \$\\phik \= \\text{atan2}(\\text{Im}(Fk), \\text{Re}(Fk))\$  визначає його часову часову симетрію.  
\# Basis Transformer Specification (01\_Formal\_Core/src/basis\_transformer.py)  
import math  
import numpy as np

class BasisTransformer:  
    """Модуль аксіоматичної трансформації базисів знань та частотних процесів."""  
      
    @staticmethod  
    def convert\_log10\_to\_log2(val\_log10: float) \-\> float:  
        """Переводить логарифмічне значення з основи 10 в основу 2 (інформаційний базис)."""  
        return val\_log10 \* math.log2(10)

    @staticmethod  
    def time\_to\_frequency\_domain(signal: list\[float\]) \-\> dict\[str, list\[float\]\]:  
        """Трансформує часовий процес у частотний спектр через DFT (FFT)."""  
        x \= np.array(signal, dtype=float)  
        N \= len(x)  
        fft\_vals \= np.fft.fft(x)  
        freqs \= np.fft.fftfreq(N)  
          
        amplitudes \= np.abs(fft\_vals) / N  
        phases \= np.angle(fft\_vals)  
          
        return {  
            "frequencies": freqs.tolist(),  
            "amplitudes": amplitudes.tolist(),  
            "phases": phases.tolist()  
        }

#### 4\. Специфікація типізованого мосту: Google AI Ecosystem (Firebase Genkit, Dotprompt, Pydantic AI)

##### 4.1 Архітектура типізованого мосту

Застосування генеративних мовних моделей для вилучення знань у RDF-триплети створює ризик відхилень від схем та помилок. Для усунення цього бар'єра розробляється строго типізований міст між неструктурованим виводом LLM та Pure Python обчислювальним ядром.  
Стек технологій мосту включає:

* Firebase Genkit Python SDK: Інфраструктура для створення детермінованих асинхронних потоків обробки знань через декоратори асинхронних потоків та реєстрації інструментів.  
* Dotprompt Templates: Файли prompt-шаблонів (.prompt) із YAML-frontmatter.  
* Pydantic AI / Pydantic v2: Сувора декларативна валідація типів даних під час виконання.

##### 4.2 Специфікація Dotprompt-шаблону (rdf\_extraction.prompt)

Шаблон розміщується за шляхом 05\_Knowledge\_Aggregator/prompts/rdf\_extraction.prompt.  
\---  
model: googleai/gemini-2.5-flash  
config:  
  temperature: 0.0  
  maxOutputTokens: 2048  
input:  
  schema:  
    raw\_text: string  
output:  
  format: json  
  schema:  
    subject: string  
    predicate: string  
    object: string  
    graph\_context: string  
\---

Проаналізуй наданий текст та вилучи канонічні RDF-триплети знань.   
Використовуй тільки факти, явні в тексті. Не додавай зовнішніх припущень.

Текст для аналізу:  
{{raw\_text}}

##### 4.3 Python-реалізація типізованого Genkit-потоку

Реалізація розміщується у файлі 05\_Knowledge\_Aggregator/src/genkit\_typed\_bridge.py.  
from pydantic import BaseModel, Field

class RDFTripleModel(BaseModel):  
    subject: str \= Field(description="Канонічний ідентифікатор суб'єкта")  
    predicate: str \= Field(description="Префіксований онтологічний предикат")  
    object: str \= Field(description="Літеральне значення або URI об'єкта")  
    graph\_context: str \= Field(default="main\_graph")

class ExtractionResponse(BaseModel):  
    triples: list\[RDFTripleModel\] \= Field(description="Список валідованих RDF-триплетів")

#### 5\. Специфікація цілісності знань та аудиту: SHACL 1.2 Profiling та W3C PROV-O

##### 5.1 Декларативна валідація через W3C SHACL 1.2 Profiling

Для забезпечення суворої валідації онтологічних графових моделей у Вузлі 01 та Вузлі 06 використовується специфікація W3C SHACL 1.2 Profiling. Вона дає змогу групувати SHACL-форми та перевіряти відповідність RDF-графів.  
Специфікація вводить два ключові класи та правила відповідності:

* sh:ShapesGraph: Граф онтологічних форм, який імпортує інші графи через owl:imports та вказує визначені елементи через rdfs:isDefinedBy.  
* sh:DataGraph: Граф фактичних даних, для якого формується твердження про відповідність shpr:conformsTo за результатами валідації.  
* sh:ValidationReport: Граф звіту валідації, що містить булевий результат sh:conforms true/false.

##### 5.2 Повне відстеження походження фактів (W3C PROV-O Lineage)

Для забезпечення нульової галюцинативності та аудиту кожного факту в системі запроваджується наскрізне відстеження походження за онтологією W3C PROV-O (The PROV Ontology).  
Кожна одиниця знання гарантує наявність тріади PROV-O:

1. prov:Entity: Нормалізований RDF-триплет або складена когнітивна модель у Вузлі 06\.  
2. prov:Activity: Процес обробки фактів (наприклад, OSINT-пошук search\_duckduckgo, LLM-вилучення intake\_processor, TDA-аналіз pure\_tda\_engine, або аксіоматична проєкція axiomatic\_transformer).  
3. prov:Agent: Суб'єкт або модуль, що ініціював та виконав дію (наприклад, aggregator.osint\_analyst, core.tda\_engineer, model.builder або system.master\_architect).

#### 6\. План впровадження, ADR-стандарти та дорожня карта

##### 6.1 Architectural Decision Records (ADRs)

До загального реєстру архітектурних рішень системи (docs/adr/) додаються три нові стандарти:

###### *ADR-0009: ISO/IEC/IEEE 42010:2022 Architecture Transformer Standard*

* Статус: Прийнято.  
* Контекст: Необхідність генерації багаторакурсних системних моделей без втрати цілісності фактів та сумісності з 2-им виданням стандарту ISO 42010\.  
* Рішення: Реалізувати Pure Python модуль 06\_Formalized\_Model/src/axiomatic\_transformer.py на основі концептів Stakeholder Perspectives, View Components та Architecture Aspects.  
* Наслідки: Забезпечено автоматичне формування Концептуального, Контекстного та Логічного ракурсів з єдиного графа валідованих триплетів.

###### *ADR-0010: Logarithmic & Fourier Frequency Basis Shift*

* Статус: Прийнято.  
* Контекст: Відмова від антропоморфних вимірів (10-кова основа, лінійний час) на користь інформаційно-природних базисів у Вузлі 01\.  
* Рішення: Розробити модуль 01\_Formal\_Core/src/basis\_transformer.py з функціями переходу log10 \-\> log2 та заміни часового параметра частотним спектром через Discrete Fourier Transform (DFT/FFT).  
* Наслідки: Забезпечено точне обчислення ентропії в бітах та частотний аналіз фазових атракторів знань.

###### *ADR-0011: Firebase Genkit & Dotprompt Typed Bridge Protocol*

* Статус: Прийнято.  
* Контекст: Необхідність усунення відхилень від схем при вилученні знань за допомогою LLM.  
* Рішення: Впровадити Firebase Genkit Python SDK, Dotprompt executable-шаблони та Pydantic v2 моделі для суворої типізації input/output контекстів.  
* Наслідки: Гарантовано 100% відповідність вилучених триплетів JSON-контрактам до передачі в детерміноване Pure Python ядро.

##### 6.2 Дорожня карта впровадження (Roadmap)

Впровадження розбивається на 4 послідовні ітеративні фази:  
Фаза,Назва та зміст робіт,Відповідальний,Критерії готовності (DoD)  
Phase 46,"Побудова типізованого Genkit-мосту (Вузол 05 / 00): Створення rdf\_extraction.prompt, реалізація genkit\_typed\_bridge.py з Pydantic-моделями",aggregator.architect,"py\_compile OK, Інтеграційний тест test\_genkit\_typed\_bridge.py PASSED (exit\_code: 0)"  
Phase 47,"Оптимізація TDA та Basis Transformer (Вузол 01): Розширення pure\_tda\_engine.py (Alpha Complexes, DTM, Time-Delay), реалізація basis\_transformer.py (log10 \-\> log2, DFT/FFT)",core.tda\_engineer,"py\_compile OK, Тести test\_pure\_tda\_engine.py та test\_basis\_transformer.py PASSED"  
Phase 48,"Реалізація AXIOMATIC\_TRANSFORMER (Вузол 06): Розробка axiomatic\_transformer.py за ISO 42010:2022, створення JSON-схеми iso42010\_viewpoint\_schema.json",model.builder,"Валідація json.load() OK, Тест test\_axiomatic\_transformer.py PASSED"  
Phase 49,"Інтеграція SHACL 1.2 Profiling, PROV-O та E2E Benchmark: Оновлення shacl\_validator.py, запуск сквозного тесту test\_pure\_e2e\_pipeline.py",system.master\_architect,"4/4 етапи E2E тесту PASSED, Синхронізація тріади пам'яті (PROJECT\_SPEC, CONTEXT, STATE)"

#### 7\. Висновки

Сформований комплект системної документації забезпечує чітку інженерну та математичну основу для розширення Вузлів 01 та 06 Discovery Engine. Дотримання викладених специфікацій гарантує збереження суворого обмеження BUDGET\_LIMIT \= \$0.00, повну автономність Pure Python обчислювального ядра, математичну доведеність інваріантів та високу якість структуризації знань відповідно до міжнародних стандартів ISO/IEC/IEEE 42010:2022, W3C SHACL 1.2 та W3C PROV-O.  
