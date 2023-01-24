

### Инструкция по запуску
1. Скачать проект
2. Установить зависимости
3. Перейти в папку crapNB, в которой расположен файл start.py
4. Запустить на исполнение
```
python3 start.py
```
### Веса для параметров 
cpu_hhz_weigth = 1/5000 #вес для частоты процессора  
ram_gb_weigth = 1/32 #вес для объема ОЗУ  
ssd_gb_weigth = 1/3000 #вес для объема SSD  
price_rub_weigth = 1/200000 #вес для цены

### топ 5 записей из получившейся  таблицы
| id   | url                                                                                                             | name                                                       | cpu  | ram | ssd  | price  | rank               |
|------|-----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|------|-----|------|--------|--------------------|
| 1291 | https://www.citilink.ru/product/noutbuk-asus-rog-strix-scar-17-se-g733cx-ll091w-i9-12950hx-16gb-ssd1tb-1887116/ | ASUS ROG Strix Scar 17 SE G733CX-LL091W                    | 2300 | 32  | 1000 | 379990 | 3.6932833333333335 |
| 1289 | https://www.citilink.ru/product/noutbuk-asus-zenbook-pro-duo-ux582hs-h2002x-i9-11900h-32gb-ssd1tb-rtx3-1887221/ | ASUS ZenBook Pro Duo 15 OLED UX582HS-H2002X                | 2500 | 32  | 1000 | 354990 | 3.6082833333333335 |
| 1152 | https://www.citilink.ru/product/noutbuk-msi-raider-ge76-12ugs-439ru-i7-12800hx-32gb-ssd2tb-rtx3080ti-1-1833340/ | MSI Raider GE77HX 12UHS-232RU                              | 2000 | 32  | 2000 | 289990 | 3.5166166666666667 |
| 1151 | https://www.citilink.ru/product/noutbuk-msi-raider-ge66-12ugs-466ru-i9-12900hk-32gb-ssd1tb-rtx3070ti-8-1709436/ | MSI Raider GE66 12UGS-466RU                                | 3800 | 32  | 1000 | 202990 | 3.1082833333333335 |
| 831  | https://novosibirsk.holodilnik.ru/digital_tech/notebook/msi/9s7_16v512_212/                                     | Ноутбук  MSI Stealth GS66 12UGS-212RU black 9S7-16V512-212 | 2300 | 32  | 1024 | 209990 | 2.8512833333333334 |

### Нюансы
- В проекте используется sqlite.
- Для запуска scrapy в файле start.py используется команда с указанием имени интерпретатора питона "python3". 
- Программа выполняется около 10 минут. В файле settings.py задано время задержки между запросами.
- При запуске программы удаляется не содержимое базы данных и вновь собранные данные добавляются.


