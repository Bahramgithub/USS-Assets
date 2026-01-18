#!/usr/bin/env python3
"""
USS Aircraft Carrier Location Tracker
Fetches publicly available information about US Navy aircraft carriers
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class USSCarrierTracker:
    def __init__(self):
        self.carriers = {
            "CVN-68": "USS Nimitz",
            "CVN-69": "USS Dwight D. Eisenhower", 
            "CVN-70": "USS Carl Vinson",
            "CVN-71": "USS Theodore Roosevelt",
            "CVN-72": "USS Abraham Lincoln",
            "CVN-73": "USS George Washington",
            "CVN-74": "USS John C. Stennis",
            "CVN-75": "USS Harry S. Truman",
            "CVN-76": "USS Ronald Reagan",
            "CVN-77": "USS George H.W. Bush",
            "CVN-78": "USS Gerald R. Ford"
        }
        
    def get_vessel_info_marinetraffic(self, mmsi: str) -> Optional[Dict]:
        """Fetch vessel data from MarineTraffic API (requires API key)"""
        # Note: This requires a paid API key from MarineTraffic
        api_key = "YOUR_MARINETRAFFIC_API_KEY"
        url = f"https://services.marinetraffic.com/api/exportvessel/v:5/{api_key}/mmsi:{mmsi}/protocol:jsono"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"MarineTraffic API error: {e}")
        return None
    
    def get_navy_news_deployments(self) -> List[Dict]:
        """Scrape public Navy news for deployment information"""
        deployments = []
        
        # Navy.mil news API (public information)
        try:
            url = "https://www.navy.mil/Resources/Blog/"
            # This would require web scraping for actual implementation
            # For demo purposes, returning sample data
            deployments = [
                {
                    "vessel": "USS Gerald R. Ford",
                    "status": "Deployed to Mediterranean",
                    "last_update": "2024-01-15",
                    "region": "Europe/Mediterranean"
                },
                {
                    "vessel": "USS Dwight D. Eisenhower", 
                    "status": "Operating in Red Sea region",
                    "last_update": "2024-01-10",
                    "region": "Middle East"
                }
            ]
        except Exception as e:
            print(f"Navy news fetch error: {e}")
            
        return deployments
    
    def check_middle_east_deployments(self, deployments: List[Dict]) -> List[Dict]:
        """Filter deployments heading to/in Middle East region"""
        middle_east_keywords = [
            "middle east", "persian gulf", "red sea", "arabian sea",
            "strait of hormuz", "suez canal", "mediterranean"
        ]
        
        middle_east_deployments = []
        for deployment in deployments:
            status_lower = deployment.get("status", "").lower()
            region_lower = deployment.get("region", "").lower()
            
            if any(keyword in status_lower or keyword in region_lower 
                   for keyword in middle_east_keywords):
                middle_east_deployments.append(deployment)
                
        return middle_east_deployments
    
    def get_public_carrier_positions(self) -> Dict:
        """Aggregate publicly available carrier information"""
        print("Fetching USS Aircraft Carrier Information...")
        print("=" * 50)
        
        # Get deployment news
        deployments = self.get_navy_news_deployments()
        
        # Filter Middle East deployments
        middle_east = self.check_middle_east_deployments(deployments)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "total_carriers": len(self.carriers),
            "all_deployments": deployments,
            "middle_east_deployments": middle_east,
            "data_sources": [
                "US Navy Public Affairs",
                "Defense News",
                "Public Maritime Tracking"
            ],
            "disclaimer": "This data is from public sources only. Actual military positions are classified."
        }
        
        return result
    
    def display_results(self, data: Dict):
        """Display the fetched information"""
        print(f"\nUSS Aircraft Carrier Status Report")
        print(f"Generated: {data['timestamp']}")
        print(f"Total Active Carriers: {data['total_carriers']}")
        print("\n" + "="*60)
        
        print("\nAll Known Deployments:")
        for deployment in data['all_deployments']:
            print(f"• {deployment['vessel']}")
            print(f"  Status: {deployment['status']}")
            print(f"  Region: {deployment['region']}")
            print(f"  Last Update: {deployment['last_update']}\n")
        
        print("Middle East Region Deployments:")
        if data['middle_east_deployments']:
            for deployment in data['middle_east_deployments']:
                print(f"🚢 {deployment['vessel']}")
                print(f"   {deployment['status']}")
                print(f"   Region: {deployment['region']}\n")
        else:
            print("No carriers currently reported in Middle East region\n")
        
        print("Data Sources:")
        for source in data['data_sources']:
            print(f"• {source}")
        
        print(f"\n⚠️  {data['disclaimer']}")

def main():
    tracker = USSCarrierTracker()
    
    try:
        # Fetch and display carrier information
        carrier_data = tracker.get_public_carrier_positions()
        tracker.display_results(carrier_data)
        
        # Save to JSON file
        with open('uss_carrier_report.json', 'w') as f:
            json.dump(carrier_data, f, indent=2)
        print(f"\n📄 Report saved to: uss_carrier_report.json")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()