import allure
from playwright.sync_api import Page, expect


@allure.feature('Тестовые сценарии для GitHub и Skillbox')
class TestCases:
    @allure.story('Поиск задач на GitHub')
    @allure.description('''
    Шаги:
    1. Перейти на страницу задач VSCode на GitHub
    2. Выполнить поиск задач, содержащих "bug" в заголовке
    3. Проверить, что все найденные задачи содержат "bug" в заголовке
    ''')
    @allure.severity(allure.severity_level.NORMAL)
    def test_case_1(self, set_up_browser, page):
        page = set_up_browser
        with allure.step("Переход на страницу задач VSCode"):
            page.goto("https://github.com/microsoft/vscode/issues")

        with allure.step("Поиск задач с 'bug' в заголовке"):
            page.wait_for_selector('//input[@id="repository-input"]').click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Control+X")
            search_input = page.locator('input[name="repository-inputname"]')
            search_input.press("Enter")
            search_input.fill("in:title bug")
            search_input.press("Enter")

        with allure.step("Проверка результатов поиска"):
            page.wait_for_load_state("networkidle")
            page.wait_for_selector('//h3/a/span')
            issue_titles = page.locator('//h3/a/span')

            title_texts = [issue_titles.nth(i).inner_text().lower() for i in range(issue_titles.count())]
            assert any('bug' in title for title in title_texts), "Ни один заголовок не содержит 'bug'"

            allure.attach(page.screenshot(), name="результаты_поиска", attachment_type=allure.attachment_type.PNG)

    @allure.story('Фильтрация задач по автору на GitHub')
    @allure.description('''
    Шаги:
    1. Перейти на страницу задач VSCode на GitHub
    2. Отфильтровать задачи по автору "bpasero"
    3. Проверить, что все отфильтрованные задачи принадлежат автору "bpasero"
    ''')
    @allure.severity(allure.severity_level.NORMAL)
    def test_case_2(self, set_up_browser, page):
        page = set_up_browser
        with allure.step("Переход на страницу задач VSCode"):
            page.goto("https://github.com/microsoft/vscode/issues")

        with allure.step("Фильтрация задач по автору 'bpasero'"):
            page.wait_for_selector('//span[contains(text(), "Author")]').click()
            el = page.locator('//*[@id="__primerPortalRoot__"]/div/div/div/div[2]/div[1]/span/input')
            author_name = 'bpasero'
            for char in author_name:
                el.type(char, delay=400)  # Задержка в 400 мс между символами
            el.press('Enter')
            page.wait_for_load_state('networkidle')

        with allure.step("Проверка отфильтрованных задач"):
            page.wait_for_load_state('networkidle')
            page.wait_for_selector("//li/div/div/div/div/div/a")
            issues = page.locator("//li/div/div/div/div/div/a")

            for i in range(issues.count()):
                author = issues.nth(i).inner_text()
                assert author == "bpasero", f"Автор задачи '{author}' не соответствует ожидаемому 'bpasero'"

        allure.attach(page.screenshot(), name="отфильтрованные_задачи", attachment_type=allure.attachment_type.PNG)

    @allure.story('Расширенный поиск на GitHub')
    @allure.description('''
    Шаги:
    1. Перейти на страницу расширенного поиска GitHub
    2. Установить критерии поиска: Python репозитории с >20000 звезд и файлом environment.yml
    3. Проверить, что все найденные репозитории соответствуют критериям поиска
    ''')
    @allure.severity(allure.severity_level.NORMAL)
    def test_case_3(self, set_up_browser, page):
        page = set_up_browser
        with allure.step("Переход на страницу расширенного поиска GitHub"):
            page.goto("https://github.com/search/advanced")
            page.wait_for_load_state("networkidle")
            assert page.url == "https://github.com/search/advanced", "Неверный URL страницы расширенного поиска"

        with allure.step("Установка критериев поиска"):
            page.wait_for_selector("#search_language")
            page.click("#search_language")

            page.select_option("#search_language", label="Python")
            selected_option = page.evaluate("() => document.querySelector('#search_language').value")
            assert selected_option == "Python", f"Python is not selected. Selected value: {selected_option}"

            page.wait_for_selector("#search_stars")
            page.fill("#search_stars", ">20000")
            assert page.input_value("#search_stars") == ">20000", "Неверное значение в поле количества звезд"

            page.wait_for_selector("#search_filename")
            page.fill("#search_filename", "environment.yml")
            assert page.input_value("#search_filename") == "environment.yml", "Неверное значение в поле имени файла"

            search_buttons = page.locator('button:has-text("Search")')
            search_buttons.nth(2).wait_for(state="visible")
            search_buttons.nth(2).click()

        with allure.step("Проверка результатов поиска"):
            page.wait_for_load_state("networkidle")
            page.wait_for_selector('//div/ul/li/a/span[contains(text(), "k")]', state="visible")
            repo_items = page.locator('//div/ul/li/a/span[contains(text(), "k")]')

            for i in range(repo_items.count()):
                stars_count = repo_items.nth(i).inner_text()
                if stars_count.endswith('k'):
                    result = int(float(stars_count[:-1]) * 1000)
                else:
                    result = int(stars_count.replace(',', ''))
                assert result > 20000, f"Репозиторий имеет {stars_count} звезд, вместо ожидаемых >20000"

        page.wait_for_load_state("networkidle")
        allure.attach(page.screenshot(), name="результаты_поиска", attachment_type=allure.attachment_type.PNG)

    @allure.story('Выбор курса на Skillbox')
    @allure.description('''
    Шаги:
    1. Перейти на страницу курсов Skillbox
    2. Применить фильтры: профессия, длительность курса, специализация 1С
    3. Проверить, что все отфильтрованные курсы соответствуют заданным критериям
    ''')
    @allure.severity(allure.severity_level.NORMAL)
    def test_case_4(self, set_up_browser, page):
        page = set_up_browser
        with allure.step("Переход на страницу курсов Skillbox"):
            page.goto("https://skillbox.ru/code/")
            page.wait_for_load_state('networkidle')
            page.set_viewport_size({"width": 1500, "height": 800})

        with allure.step("Применение фильтров"):
            page.locator('label[value="profession"]').click()

            range_1 = page.locator('(//div/button[@class="ui-range__dot"])[1]')
            range_1.hover()
            page.mouse.down()
            page.mouse.move(50, 0)
            page.mouse.up()
            page.wait_for_timeout(400)

            range_2 = page.locator('(//div/button[@class="ui-range__dot"])[2]')
            range_2.hover()
            page.mouse.down()
            page.mouse.move(-50, 0)
            page.mouse.up()
            page.wait_for_timeout(400)

            page.locator('//label//span/span[contains(text(), "1С")]').click()
            page.wait_for_timeout(5000)

        with allure.step("Проверка отфильтрованных результатов"):
            page.wait_for_load_state('networkidle')
            page.wait_for_selector(".ui-product-card-main__label")

            issues = page.locator(".ui-product-card-main__label").all()
            for issue in issues:
                unit = issue.text_content()
                page.wait_for_timeout(400)
                assert unit == "Профессия", f"Раздел курса '{unit}' не соответствует ожидаемому '      Профессия'"

            card_titles = page.locator(".ui-product-card-main__title").all()
            for title in card_titles:
                title_text = title.text_content()
                page.wait_for_timeout(400)
                assert "1С" in title_text, f"Название профессии '{title_text}' не содержит '1С'"

            issues = page.locator('//section/div/article/span/b')
            count = int(issues.text_content())
            assert 6 < count < 12, f"Длительность курса {count} должна быть от 6 до 12 месяцев"

        allure.attach(page.screenshot(), name="отфильтрованные_курсы",
                      attachment_type=allure.attachment_type.PNG)

    @allure.story('Проверка активности коммитов на GitHub')
    @allure.description('''
    Шаги:
    1. Перейти на страницу активности коммитов VSCode на GitHub
    2. Взаимодействовать с графиком активности коммитов
    3. Проверить всплывающую подсказку с информацией о коммитах
    ''')
    @allure.severity(allure.severity_level.NORMAL)
    def test_case_5(self, set_up_browser, page):
        page = set_up_browser
        with allure.step("Переход на страницу активности коммитов VSCode"):
            page.goto("https://github.com/microsoft/vscode/graphs/commit-activity")
            page.wait_for_load_state("networkidle")
            page.set_viewport_size({"width": 1600, "height": 920})

        with allure.step("Взаимодействие с графиком активности коммитов"):
            element = page.locator("section#commit-activity-master>svg")
            element.hover(position={"x": 200, "y": 50})
            page.mouse.click(200, 50)

        with allure.step("Проверка всплывающей подсказки активности коммитов"):
            tooltip = page.locator("//div[@class='svg-tip n']")
            expect(tooltip).to_be_visible()
            expect(tooltip).to_have_text("277 commits the week of Mar 31")

        allure.attach(page.screenshot(), name="активность_коммитов", attachment_type=allure.attachment_type.PNG)
