import requests
from bs4 import BeautifulSoup
import json
import time
import random

book_list = [
    ["GEN", 50, "1Móz", "1 Mózes"], 
    ["EXO", 40, "2Móz", "2 Mózes"], 
    ["LEV", 27, "3Móz", "3 Mózes"], 
    ["NUM", 36, "4Móz", "4 Mózes"], 
    ["DEU", 34, "5Móz", "5 Mózes"], 
    ["JOS", 24, "Józs", "Józsué"], 
    ["JDG", 21, "Bír", "Bírák"], 
    ["RUT", 4, "Ruth", "Ruth"], 
    ["1SA", 31, "1Sám", "1 Sámuel"], 
    ["2SA", 24, "2Sám", "2 Sámuel"], 
    ["1KI", 22, "1Kir", "1 Királyok"], 
    ["2KI", 25, "2Kir", "2 Királyok"], 
    ["1CH", 29, "1Krón", "1 Krónika"], 
    ["2CH", 36, "2Krón", "2 Krónika"], 
    ["EZR", 10, "Ezsd", "Ezsdrás"], 
    ["NEH", 13, "Neh", "Nehémiás"], 
    ["EST", 10, "Eszt", "Eszter"], 
    ["JOB", 42, "Jób", "Jób"], 
    ["PSA", 150, "Zsolt", "Zsoltárok"], 
    ["PRO", 31, "Péld", "Példabeszédek"], 
    ["ECC", 12, "Préd", "Prédikátor"], 
    ["SNG", 8, "Énekek", "Énekek Éneke"], 
    ["ISA", 66, "Ésa", "Ésaiás"], 
    ["JER", 52, "Jer", "Jeremiás"], 
    ["LAM", 5, "JSir", "Jeremiás Siralmai"], 
    ["EZK", 48, "Ez", "Ezékiel"], 
    ["DAN", 12, "Dán", "Dániel"], 
    ["HOS", 14, "Hós", "Hóseás"], 
    ["JOL", 3, "Jóel", "Jóel"], 
    ["AMO", 9, "Ám", "Ámós"], 
    ["OBA", 1, "Abd", "Abdiás"], 
    ["JON", 4, "Jón", "Jónás"], 
    ["MIC", 7, "Mik", "Mikeás"], 
    ["NAM", 3, "Náh", "Náhum"], 
    ["HAB", 3, "Hab", "Habakuk"], 
    ["ZEP", 3, "Sof", "Sofóniás"], 
    ["HAG", 2, "Agg", "Aggeus"], 
    ["ZEC", 14, "Zak", "Zakariás"], 
    ["MAL", 4, "Mal", "Malakiás"], 
    ["MAT", 28, "Mt", "Máté"], 
    ["MRK", 16, "Mk", "Márk"], 
    ["LUK", 24, "Lk", "Lukács"], 
    ["JHN", 21, "Jn", "János"], 
    ["ACT", 28, "ApCsel", "ApCsel"], 
    ["ROM", 16, "Róm", "Róma"], 
    ["1CO", 16, "1Kor", "1 Korinthus"], 
    ["2CO", 13, "2Kor", "2 Korinthus"], 
    ["GAL", 6, "Gal", "Galácia"], 
    ["EPH", 6, "Ef", "Efézus"], 
    ["PHP", 4, "Fil", "Filippi"], 
    ["COL", 4, "Kol", "Kolossé"], 
    ["1TH", 5, "1Thessz", "1 Thessalonika"], 
    ["2TH", 3, "2Thessz", "2 Thessalonika"], 
    ["1TI", 6, "1Tim", "1 Timótheus"], 
    ["2TI", 4, "2Tim", "2 Timótheus"], 
    ["TIT", 3, "Tit", "Titus"], 
    ["PHM", 1, "Filem", "Filemon"], 
    ["HEB", 13, "Zsid", "Zsidó"], 
    ["JAS", 5, "Jak", "Jakab"], 
    ["1PE", 5, "1Pt", "1 Péter"], 
    ["2PE", 3, "2Pt", "2 Péter"], 
    ["1JN", 5, "1Jn", "1 János"], 
    ["2JN", 1, "2Jn", "2 János"], 
    ["3JN", 1, "3Jn", "3 János"], 
    ["JUD", 1, "Júd", "Júdás"], 
    ["REV", 22, "Jel", "Jelenések"]]

book_list_test = [
    ["RUT", 4, "Ruth", "Ruth"], 
    ["JAS", 5, "Jak", "Jakab"], 
]


def chapters_content(book, chapter):
    
    short_book_list = []
    for element in book_list:
        short_book_list.append(element[2])
        
    
    # To prevent page from crash
    sleep_time = random.randrange(3, 8)   
    print(f"    Sleeping time - {sleep_time}s")     
    time.sleep(sleep_time)
    
    verse_list = []

    response = requests.get(f'https://abibliamindenkie.hu/karoli/{book}/{chapter}')
    soup = BeautifulSoup(response.content, 'html.parser')

    chapter_body = soup.find("div", class_="chapter__body")

    # Chapter title
    chapter_title = chapter_body.find("h2").text
    verse_list.append({"num": "Title", "text_hu": chapter_title})

    # Chapter verses list of elements
    chapter_verses = chapter_body.find_all("p")


    for verse in chapter_verses:      
        
        verse_ref = []

        # Verse number
        verse_number = verse.find("a").text
        
        # If verse number is empty then it's a subtitle
        if verse_number == '':
            verse_number = "Subtitle"

        # Verse references
        verse_references = verse.find_all("span")

        previous_ref_book = ''
        if len(verse_references) > 0:   
            for ref in verse_references: 
                if ref.find("a") != None:
                    
                    ref_book = ref.find("a").text.split()[0]                    
                    
                    if ref_book in short_book_list:
                        previous_ref_book = ref_book
                        verse_ref.append(ref.find("a").text)
                    else: 
                        verse_ref.append(f'{previous_ref_book} {ref.find("a").text}')          

        # Verse text
        verse_text = verse.contents[2].strip()
        
        if len(verse_ref) > 0:
            verse_list.append({ "num": verse_number, "text_hu": verse_text, "ref": verse_ref })
        else: 
            verse_list.append({ "num": verse_number, "text_hu": verse_text })

    
    print(f'*** {book} chapter {chapter} is done! ***')
    return verse_list

################################ Execute ########################

for element in book_list:
    print(element)    

    current_book = element[0]
    current_book_title = element[3]
    total_chapters = element[1]
    current_chapter = 1
    
    current_array = {}

    while current_chapter <= total_chapters:
        a_whole_chapter = chapters_content(current_book, current_chapter)
        current_array[current_chapter] = a_whole_chapter
        current_chapter += 1

    with open(f"scraped_chapters_hu/{current_book}.json", "w", encoding='utf-8') as write_file:
        json.dump(current_array, write_file, ensure_ascii=False)

    print(f"*** {current_book_title} is done ***")
    
    