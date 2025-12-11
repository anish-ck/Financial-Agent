from app.models.database import engine, Report
from sqlalchemy.orm import Session
import json

session = Session(engine)
report = session.query(Report).order_by(Report.id.desc()).first()

if report:
    print(f"Latest Report ID: {report.id}")
    print(f"Ticker: {report.ticker}")
    print(f"Status: {report.status}")
    print(f"Has result_json: {bool(report.result_json)}")
    print(f"Has pdf_url: {bool(report.pdf_url)}")
    
    if report.result_json:
        data = json.loads(report.result_json)
        print("\n=== Report Data Structure ===")
        print(f"Top-level keys: {list(data.keys())}")
        
        if 'data_sources' in data:
            print(f"Data sources keys: {list(data.get('data_sources', {}).keys())}")
            
            if 'market_research' in data['data_sources']:
                mr = data['data_sources']['market_research']
                print(f"\nMarket Research: {mr}")
            
            if 'financial_analysis' in data['data_sources']:
                fa = data['data_sources']['financial_analysis']
                print(f"\nFinancial Analysis: {fa}")
        
        if 'report' in data:
            print(f"\nReport keys: {list(data.get('report', {}).keys())}")
            print(f"Has full_text: {'full_text' in data.get('report', {})}")
        
        if 'error' in data:
            print(f"\n=== ERROR FOUND ===")
            print(f"Error: {data['error']}")
else:
    print("No reports found in database")

session.close()
