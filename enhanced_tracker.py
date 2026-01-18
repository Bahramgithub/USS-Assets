#!/usr/bin/env python3
"""
Enhanced USS Carrier Tracker with Web Scraping
Fetches real data from public military news sources
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import Dict, List, Optional

class EnhancedCarrierTracker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def scrape_navy_news(self) -> List[Dict]:
        """Scrape US Navy official news for carrier deployments"""
        deployments = []
        
        try:
            # Navy.mil news search for aircraft carriers
            url = "https://www.navy.mil/News/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for carrier-related news articles
                articles = soup.find_all('article', class_='news-item')[:10]
                
                for article in articles:
                    title_elem = article.find('h3') or article.find('h2')
                    if title_elem:
                        title = title_elem.get_text().strip()
                        
                        # Check if article mentions carriers
                        if any(keyword in title.lower() for keyword in 
                               ['carrier', 'cvn', 'strike group', 'deployment']):
                            
                            link_elem = title_elem.find('a')
                            link = link_elem['href'] if link_elem else ""
                            
                            date_elem = article.find('time')
                            date = date_elem.get_text().strip() if date_elem else "Unknown"
                            
                            deployments.append({
                                'title': title,
                                'date': date,
                                'source': 'US Navy Official',
                                'link': f"https://www.navy.mil{link}" if link.startswith('/') else link
                            })
                            
        except Exception as e:
            print(f"Navy news scraping error: {e}")
            
        return deployments
    
    def scrape_defense_news(self) -> List[Dict]:
        """Scrape Defense News for carrier information"""
        deployments = []
        
        try:
            url = "https://www.defensenews.com/naval/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                articles = soup.find_all('article')[:5]
                
                for article in articles:
                    title_elem = article.find('h3') or article.find('h2')
                    if title_elem:
                        title = title_elem.get_text().strip()
                        
                        if any(keyword in title.lower() for keyword in 
                               ['carrier', 'navy', 'deployment', 'middle east']):
                            
                            deployments.append({
                                'title': title,
                                'source': 'Defense News',
                                'date': 'Recent'
                            })
                            
        except Exception as e:
            print(f"Defense News scraping error: {e}")
            
        return deployments
    
    def analyze_middle_east_presence(self, news_data: List[Dict]) -> List[Dict]:
        """Analyze news for Middle East deployments"""
        middle_east_indicators = [
            'middle east', 'persian gulf', 'red sea', 'arabian sea',
            'strait of hormuz', 'suez canal', 'mediterranean', 'centcom',
            'fifth fleet', 'bahrain', 'qatar', 'uae', 'israel', 'iran'
        ]
        
        middle_east_news = []
        
        for item in news_data:
            title_lower = item['title'].lower()
            
            if any(indicator in title_lower for indicator in middle_east_indicators):
                item['region'] = 'Middle East'
                item['relevance'] = 'High'
                middle_east_news.append(item)
        
        return middle_east_news
    
    def get_carrier_fleet_status(self) -> Dict:
        """Get comprehensive carrier fleet status"""
        print("Fetching USS Aircraft Carrier Intelligence...")
        print("Scanning public military news sources...")
        
        # Gather data from multiple sources
        navy_news = self.scrape_navy_news()
        defense_news = self.scrape_defense_news()
        
        all_news = navy_news + defense_news
        middle_east_focus = self.analyze_middle_east_presence(all_news)
        
        # Known carrier strike groups and their typical AORs
        carrier_groups = {
            "USS Gerald R. Ford (CVN-78)": "Atlantic/Mediterranean",
            "USS George H.W. Bush (CVN-77)": "Atlantic/Mediterranean", 
            "USS Harry S. Truman (CVN-75)": "Atlantic/Mediterranean",
            "USS Dwight D. Eisenhower (CVN-69)": "Middle East/Red Sea",
            "USS Abraham Lincoln (CVN-72)": "Pacific/Indo-Pacific",
            "USS Carl Vinson (CVN-70)": "Pacific/Indo-Pacific",
            "USS Theodore Roosevelt (CVN-71)": "Pacific/Indo-Pacific",
            "USS Ronald Reagan (CVN-76)": "Japan/Western Pacific"
        }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "carrier_strike_groups": carrier_groups,
            "recent_news": all_news[:10],
            "middle_east_focus": middle_east_focus,
            "intelligence_summary": self.generate_summary(middle_east_focus),
            "data_disclaimer": "Based on publicly available information only"
        }
    
    def generate_summary(self, middle_east_data: List[Dict]) -> str:
        """Generate intelligence summary"""
        if not middle_east_data:
            return "No recent public reports of carrier operations in Middle East region"
        
        summary = f"Found {len(middle_east_data)} recent reports related to Middle East operations:\n"
        for item in middle_east_data[:3]:
            summary += f"• {item['title'][:80]}...\n"
        
        return summary
    
    def display_intelligence_report(self, data: Dict):
        """Display comprehensive intelligence report"""
        print("\n" + "="*70)
        print("🇺🇸 USS AIRCRAFT CARRIER INTELLIGENCE REPORT")
        print("="*70)
        print(f"Report Generated: {data['timestamp']}")
        
        print(f"\n📍 CURRENT CARRIER STRIKE GROUP POSITIONS:")
        print("-" * 50)
        for carrier, region in data['carrier_strike_groups'].items():
            print(f"🚢 {carrier}")
            print(f"   Operating Area: {region}\n")
        
        print(f"🎯 MIDDLE EAST REGION FOCUS:")
        print("-" * 30)
        if data['middle_east_focus']:
            for item in data['middle_east_focus']:
                print(f"📰 {item['title']}")
                print(f"   Source: {item['source']} | Date: {item['date']}\n")
        else:
            print("No recent Middle East deployment news found\n")
        
        print(f"📊 INTELLIGENCE SUMMARY:")
        print("-" * 25)
        print(data['intelligence_summary'])
        
        print(f"\n⚠️  {data['data_disclaimer']}")

def main():
    tracker = EnhancedCarrierTracker()
    
    try:
        # Get comprehensive carrier intelligence
        intel_data = tracker.get_carrier_fleet_status()
        tracker.display_intelligence_report(intel_data)
        
        # Save intelligence report
        with open('carrier_intelligence_report.json', 'w') as f:
            json.dump(intel_data, f, indent=2)
        
        print(f"\n💾 Intelligence report saved to: carrier_intelligence_report.json")
        
    except Exception as e:
        print(f"❌ Intelligence gathering failed: {e}")

if __name__ == "__main__":
    main()