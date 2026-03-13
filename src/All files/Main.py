
from stage1_crawler import run_stage1_crawler
from stage2_crawler import run_stage2_crawler
from stage3_analyser import run_stage3_analyser


def select_product(stage1_results):
    if not stage1_results:
        print("Nothing found to select from")
        return None

    companies = []
    for result in stage1_results:
        for kw in result['matched_keywords']:
            if kw not in companies:
                companies.append(kw)
    
    if not companies:
        print("No products identified")
        return None
    print("\n" + "="*70)
    print("SELECT PRODUCT TO INVESTIGATE")
    print("="*70)
    for i in range(len(companies)):
        print(f"  {i + 1}. {companies[i]}")
        
    while True:
        try:
            choice = int(input("\nEnter number: "))
            if choice >= 1 and choice <= len(companies):
                picked = companies[choice - 1]
                print(f"\nSelected: {picked}")
                return picked
            else:
                print("thats not a valid option, try again")
        except ValueError:
            print("enter a number")


def pick_sector():#User has to do own research(BAD)
    sector_options = [
        'Technology',
        'Finance',
        'Healthcare',
        'Energy',
        'Retail',
        'Legal',
        'General'
    ]
    print("\n" + "="*70)
    print("WHAT SECTOR IS THIS IN")
    print("="*70)
    for i in range(len(sector_options)):
        print(f"  {i + 1}. {sector_options[i]}")
    while True:
        try:
            choice = int(input("\nEnter number: "))
            if choice >= 1 and choice <= len(sector_options):
                picked = sector_options[choice - 1]
                print(f"\nSector: {picked}")
                return picked
            else:
                print("not a valid option")
        except ValueError:
            print("enter a number")


def show_report(report):#Final report    
    print("\n" + "="*70)
    print("INVESTMENT ANALYSIS REPORT")
    print("="*70)
    
    print(f"\nProduct: {report['product']}")
    print(f"Sector: {report['sector']}")
    print(f"Time: {report['timestamp']}")
    print(f"Articles analysed: {report['articles_analysed']}")
    if report['articles_failed'] > 0:
        print(f"Articles failed: {report['articles_failed']}")
    
    summary = report['analysis_summary']#summery
    print(f"\n--- Summary ---")
    print(f"  Sentiment:  {summary['overall_sentiment']}")
    print(f"  Risk:       {summary['primary_risk']}")
    print(f"  Confidence: {summary['volatility_level']}")
    print(f"  Trend:      {summary['trend_direction']}")
    print(f"  Attention:  {summary['attention_level']}")

    roi = report['roi_recommendation']# roi recommendation
    print(f"\n--- Recommendation ---")
    if roi is not None:
        # show the indicator first thats the main thing
        if 'indicator' in roi:
            print(f"  Indicator: {roi['indicator']}")
        if 'net_score' in roi:
            print(f"  Net Score: {roi['net_score']}")
        if 'confidence_score' in roi:
            print(f"  Confidence: {roi['confidence_score']}%")

        if 'user_recommendation' in roi:# user friendly recommendation
            print(f"\n  {roi['user_recommendation']}")
        if 'technical_recommendation' in roi:# technical version
            print(f"\n  Technical: {roi['technical_recommendation']}")
    
    
    articles = report['article_breakdown']#Break down what each one is 
    if articles:
        print(f"\n--- Per Article Breakdown ---")
        for i in range(len(articles)):
            a = articles[i]
            s = a['sentiment']['sentiment']
            r = a['risks']['overall_risk_score']
            print(f"  {i+1}. [{a['category']}] Sentiment: {s} | Risk score: {r}")
            print(f"     {a['url']}")
    print("\n" + "="*70)


def main():

    
    print("\n" + "="*70)
    print("FINANCIAL NEWS ANALYSIS SYSTEM")
    print("="*70)
    print("Analyses financial news to give investment recommendations")
    print("based on risk, trend and ROI.\n")
    
    # STAGE 1 
    try:
        stage1_results = run_stage1_crawler()
    except Exception as e:
        print(f"\nStage 1 crashed: {e}")
        return
    
    if not stage1_results:
        print("\nNothing found in the news. Try again later")
        return
    
    # let user pick what to research
    product = select_product(stage1_results)
    if product is None:
        print("\nNo product selected, exiting")
        return
    
    sector = pick_sector()
    
    # STAGE 2
    try:
        article_urls = run_stage2_crawler(product)
    except Exception as e:
        print(f"\nStage 2 crashed: {e}")
        return
    
    if not article_urls:
        print("\nNo articles found for this product, nothing to analyse")
        return
    
    print(f"\nGot {len(article_urls)} articles to work with")
    
    # STAGE 3
    try:
        report = run_stage3_analyser(article_urls, product, sector)
    except Exception as e:
        print(f"\nStage 3 crashed: {e}")
        return
    
    show_report(report)
    
    print("\nDone\n")


if __name__ == "__main__":
    main()
