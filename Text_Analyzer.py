import argparse
from Claude_Client import ClaudeClient

def main():
    # Testovací text
    sample_text = """
    Dnes odborné články píšou nejen lidé s akademickým titulem, ale také studenti na středních a vysokých školách. Věda se neustále rozvíjí a v dnešní době se jí snáží věnovat dokonce žáci na základních školách: pracují s výchozími zdroji,zpracovávají vlastní nové návrhy a sepisují složité práce. Při vytváření odbornéhotextu je třeba dodržovat určitý plán a používat vysvětlivky. Je třeba určit osobité rysy článku, které ho upřednostní před texty jiných vědců nebo spoluautorů ve stejném oboru. Měl by být informativní, zakládat se na originálním nápadu a zahrnovat výsledky a poznámky autora. Struktura textu by měla být přesná a systém odkazů by měly podporovat reálné teoretické zdroje. Takový článek nejen zaujme vědce z různých oborů, ale bude užitečný i pro širší čtenářskou obec.
    
    Co potřebujete pro napsání vynikajícíhoodborného článku? Několik doporučení
    
    Aby se Váš tvůrčí proces nezhroutil do trapné dříny, je dobrési pamatovat na základní pravidla pro vytvoření článku:
    
    Správně napsaný článek musí být pro čtenářeužitečný, proto ho věnujte určité vědecké oblasti. Pokud je obsah článku určen pro úzce zaměřené odborníky, nezapomeňte to poznamenat v úvodu.
    Pamatujte si na obsah: text článku se netvoří z odstavců něčích teoretických tvrzení a Vašich výsledků ve tvaru závěru. Článek musí vyjadřovatpouze Váš názor na problém založený na zpracovaných teoretických zdrojích.
    Nesnažte se napodobit publicistický styl nebo žánr eseje. Vědecká práce se vždy zakládá na již zjištěnýchpoznatcích rozvíjených pomocí určitých skutečností dle Vašeho výběru. Je třeba podložit svou práci s texty jiných badatelů ve tvaru odkazů. Pokud ve svém textuvyjadříte pouzevlastní myšlenky a názory, aniž byste je podložili nějakými důvěryhodnými zdroji, nevytvoříte tím odborný text.
    Vždy si hlídejte styl, kterým píšete svou práci. Nezkušení vědci velmi často chtějí dát najevo své znalosti a proto se schylují k používaní velkého množství odborných a úředních pojmů. Ve výsledku jsou jejichpráce těžko čitelné i pro zkušené kolegy, o vědcích z jiných oborů nemluvě: nemusejí zvládnouttolik složitých definicí a dočíst si text do konce. Používejte úzce specializované výrazy a pojmy pouze tehdy, pokud je to skutečně třeba. Vždy používejte vysvětlivky.
    Zahrňte do kontextu článku malý historický vhled přibližující čtenáři Vaše téma. Pokud je téma Vaší práce inovační, vždy můžete vyhledat teoretický základ v příbuzných vědách.
    Text musí být vždy logický. Článek musí být zřetelně kompozičně strukturován. Všude je třeba zachovávat vyváženost: forma by měla být podřízena obsahu.
    Vždy si hlídejte rozsah předpokládaného textu. Nesnažte se zahrnout do krátkého článku publikaci o několika dílech. Dobrým východiskem je pojednat pouze o jedné stránce problému, což do jisté míry omezí téma práce. Tíám informujete čtenáře o všech detailech popisovaného problému,poukážete na jemná kontextuální spojení, vysvětlíte veškeré diskutabilní otázky a nenecháte žádné nepřesnosti.
    Formát, obsahgrafická úprava Vaší prácea ilustrace v textu by měly odpovídat zaměření tiskoviny, ve které bude práce opublikována. Pokud práce bude zaslána na soutěž nebo jako příspěvek na konferenci, je třeba věnovat pozornost požadavkům na zpracování práce: rozsah, grafická úprava, konkrétní tematické zaměření. Pokud si autor předem vybere časopis, ve kterém bude publikována jeho práce, redakční rada vznese jasné požadavky na rozsah a odborné zaměření práce. Je lepší si vybrat několik tiskovin a oslovit každou z nich trochu pozměněným textem. Zvětší to šance na publikaci.
    Nejlépe vypadá strukturovaný text rozdělený na odstavce nebo oddíly.
    Snažte se držet hlavního problému své práce a nerozptylovat se ve svých úvahách. Na konci práce si ověřte, že názvy oddílů odpovídají jejich obsahu.
    Snažte se, aby počáteční úvahy měly logické zakončené závěry. Právě závěr je nejdůležitější a nejvýznamnější části vědecké práce. Myšlenky vyjádřené v závěru jsou podpořeny ilustracemi a odkazy v textu článku.
    Vytváříme vědecký text. Postup
    
    Pokud budete přesně dodržovat postup při psání článku, dokážete vytvořit logickou, zajímavou a věcnou odbornou práci se správnou grafickou úpravou.
    
    Určete aktuální stránky problému, o kterých budete pojednávat ve své práci.
    Pokud jste s daným tématem již obeznámeni a máte několik konceptů článku, určitě je zkontrolujte a opravte, tím se vyhnete drobným chybám a nepřesnostem v názorech.
    Zkuste se zamyslet, jaké inovační nápady byste mohli vyslovit ohledně zvoleného tématu a jak byste je mohli strukturovaně odrazit v textu článku.
    Vždy se obracejte na odborné originální zdroje. Kontaktujte knihovny, věnujte pozornost novým trendůma výzkumným projektům v rámci Vašeho tématu, odrazte je ve svém článku ve tvaru odkazů na použité zdroje. Nezapomínejte na periodické tiskoviny, v nich se často shrnují výsledky různých vědeckých konferencí.
    Můžete se odkazovat na vlastní články publikované dříve.
    Pokud jste předtím nikdy nepsali vědecké práce, doporučujeme se seznámit s původními zdroji ve Vaší oblasti pro hlubší pochopení tématu. Určete si okruh otázek, které Vás zajímají, poté se omezte na ty nejaktuálnější. Podpořte svůj výběrvlastními alternativními řešenímizvolených otázek.
    Poté začněte promýšlet plán své práce, měl by být logický a strukturovaný a zahrnovat následující:
    úvod;
    hlavní část (skládá se z menších oddílů);
    závěr;
    odkazy;
    seznam použitých tištěných a elektronických zdrojů.
    V pravidlech pro publikace je zpravidla uvedeno, zda je nutná anotace. Ta se skládá z max. 10 vět a klíčových slov a výrazů.
    
    Věnujte pozornost metodologii výzkumné práce. Měla by být moderní a zabývat se pouze Vašim problémem.
    Zachovejte si koncept článku. V konceptu můžete zjednodušeně popsat téma a formát budoucí práce, vyjmenovat své argumenty a nastínit teoretické pozadí. Umožní Vám to udělat vlastní závěry.
    Po ukončení hlavní části článku se zaměřte na úvod a závěr. Úvod se skládá z:
    krátkých informujících vět;
    Vašeho hodnocení jiných prací v dané oblasti;
    důvodů pro napsaní této práce;
    podstaty Vašich předpokladů;
    aktuálnosti práce;
    záměru práce.
    Ještě jednou si přečtěte úvod a hlavní část práce a zkontrolujte si zdroje. V závěru umístěte všechny výsledky Vašeho výzkumu. Nebudou pro čtenáře novinkou, protože jsou logickým závěrem všech Vašich úvah z hlavní části. Závěr neobsahuje nové informace, ale krátce shrnuje již zjištěné.
    Proveďte závěrečnou kontrolu textu. Udělejte důraz na logický a důsledný výklad materiálu. Výsledky musí být v souladu s původním cílem práce. Poté se zaměřte na grafickou úpravu práce, neignorujte požadavky a normy organizátorů konference nebo časopisu. Vědecká práce musí být promýšlená a správně upravená.
    Pokud budete dodržovat naše doporučení a popsaný postup vytvoření publikace, bude Váš článek skutečně odbornou prací. Základem úspěchu je správný poměr mezi materiálem z původních zdrojů a Vašimi osobními názory.  
    """
    client = ClaudeClient()
    result = client.analyze_text(sample_text)
    # Výpis výsledků
    print("SOUHRN:")
    print(result["summary"])
    print("\nKLÍČOVÉ BODY:")
    for i, point in enumerate(result["key_points"], 1):
        print(f"{i}. {point}")
    print("\nZÁVĚRY:")
    print(result["conclusions"])

if __name__ == "__main__":
    main()