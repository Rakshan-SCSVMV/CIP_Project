import json
import random
import os
from datetime import datetime, timedelta

# Master Geography Configuration (National Coverage)
GEO_HIERARCHY = {
    "Andhra Pradesh": {
        "Visakhapatnam": ["Gajuwaka", "Madhurawada", "Seethammadhara", "Anakapalle"],
        "Vijayawada": ["Benz Circle", "Patamata", "Gunadala", "Gollapudi"],
        "Tirupati": ["Renigunta", "Chittoor Road", "Alipiri"]
    },
    "Arunachal Pradesh": {
        "Itanagar": ["Ganga Market", "Naharlagun", "Nirjuli"],
        "Tawang": ["Tawang Town", "Lumla", "Jang"]
    },
    "Assam": {
        "Guwahati": ["Dispur", "Paltan Bazaar", "Six Mile", "Maligaon"],
        "Dibrugarh": ["Chowkidingee", "Milan Nagar", "Barbaruah"]
    },
    "Bihar": {
        "Patna": ["Kankarbagh", "Patliputra Colony", "Boring Road", "Danapur"],
        "Gaya": ["Bodh Gaya", "Magadh University", "Civil Lines"],
        "Muzaffarpur": ["Mithanpura", "Bairia", "Ahiyapur"]
    },
    "Chhattisgarh": {
        "Raipur": ["Naya Raipur", "Tatibandh", "Shankar Nagar"],
        "Bilaspur": ["Tifra", "Koni", "Sarkanda"]
    },
    "Goa": {
        "North Goa": ["Panaji", "Mapusa", "Calangute", "Ponda"],
        "South Goa": ["Margao", "Vasco da Gama", "Canacona"]
    },
    "Gujarat": {
        "Ahmedabad": ["Satellite", "Vastrapur", "Prahlad Nagar", "Bopal", "Naroda"],
        "Surat": ["Adajan", "Vesu", "Varachha", "Katargam"],
        "Vadodara": ["Alkapuri", "Sayajigunj", "Gotri", "Manjalpur"]
    },
    "Haryana": {
        "Gurugram": ["DLF Phase 1", "Sushant Lok", "Sector 56", "Cyber City"],
        "Faridabad": ["Nit", "Ballabgarh", "Greater Faridabad"],
        "Panipat": ["Model Town", "Samalkha"]
    },
    "Himachal Pradesh": {
        "Shimla": ["Mall Road", "Kasumpti", "Chhota Shimla"],
        "Dharamshala": ["McLeod Ganj", "Sidhabari", "Yol"]
    },
    "Jharkhand": {
        "Ranchi": ["Hinoo", "Kanke", "Bariatu", "Dhurwa"],
        "Jamshedpur": ["Bistupur", "Sakchi", "Telco Colony"]
    },
    "Karnataka": {
        "Bangalore Urban": ["Whitefield", "Koramangala", "Indiranagar", "Jayanagar", "HSR Layout", "Electronic City"],
        "Mysuru": ["Gokulam", "Saraswathipuram", "Vijayanagar", "Hebbal"],
        "Mangaluru": ["Kadri", "Bejai", "Surathkal", "Ullal"]
    },
    "Kerala": {
        "Thiruvananthapuram": ["Vazhuthacaud", "Pattom", "Kazhakkoottam"],
        "Kochi": ["Edappally", "Kakkanad", "Fort Kochi", "Panampilly Nagar"],
        "Kozhikode": ["Medical College", "West Hill", "Nallalam"]
    },
    "Madhya Pradesh": {
        "Indore": ["Vijay Nagar", "Rajwada", "Palasia", "Bhawarkua"],
        "Bhopal": ["Arera Colony", "BHEL", "Kolar Road", "MP Nagar"],
        "Gwalior": ["Lashkar", "Morar", "City Centre"]
    },
    "Maharashtra": {
        "Mumbai Suburban": ["Andheri", "Bandra", "Borivali", "Goregaon", "Juhu", "Powai"],
        "Pune": ["Kothrud", "Hinjewadi", "Viman Nagar", "Baner", "Kharadi", "Hadapsar"],
        "Nagpur": ["Sitabuldi", "Dharampeth", "Sadar", "Manish Nagar"],
        "Thane": ["Ghodbunder Road", "Majiwada", "Vartak Nagar"]
    },
    "Manipur": {
        "Imphal West": ["Lamphelpat", "Uripok", "Sagolband"],
        "Imphal East": ["Porompat", "Khurai"]
    },
    "Meghalaya": {
        "East Khasi Hills": ["Shillong", "Laitumkhrah", "Police Bazar"],
        "West Garo Hills": ["Tura", "Phulbari"]
    },
    "Mizoram": {
        "Aizawl": ["Zarkawt", "Mission Veng", "Bawngkawn"],
        "Lunglei": ["Chanmari", "Venglai"]
    },
    "Nagaland": {
        "Kohima": ["High School", "P.R. Hill", "BOC"],
        "Dimapur": ["Purana Bazar", "Chumukedima"]
    },
    "Odisha": {
        "Khordha": ["Bhubaneswar", "Jatni", "Khurda Town"],
        "Cuttack": ["Link Road", "Chandi Chhaka", "CDA Colony"]
    },
    "Punjab": {
        "Ludhiana": ["Model Town", "Sarabha Nagar", "Civil Lines"],
        "Amritsar": ["Golden Temple Area", "Ranjit Avenue", "Putlighar"],
        "Chandigarh": ["Sector 17", "Sector 35", "Sector 22"]
    },
    "Rajasthan": {
        "Jaipur": ["Malviya Nagar", "Vaishali Nagar", "Mansarovar", "C-Scheme"],
        "Jodhpur": ["Shastri Nagar", "Sardarpura", "Ratanada"],
        "Udaipur": ["Hiran Magri", "Fatehsagar", "Panchwati"]
    },
    "Sikkim": {
        "East Sikkim": ["Gangtok", "Ranipool", "Pakyong"],
        "South Sikkim": ["Namchi", "Ravangla"]
    },
    "Tamil Nadu": {
        "Chennai": ["Kovur", "Tambaram", "Guindy", "Velachery", "Adyar", "Mylapore", "Anna Nagar", "T-Nagar"],
        "Coimbatore": ["Peelamedu", "Singanallur", "RS Puram", "Sulur", "Anaimalai", "Gandhipuram"],
        "Madurai": ["Anna Nagar", "Tallakulam", "Avaniyapuram", "Melur", "Usilampatti", "Koodal Nagar"]
    },
    "Telangana": {
        "Hyderabad": ["Gachibowli", "Banjara Hills", "Jubilee Hills", "Kukatpally", "Madhapur", "Uppal"],
        "Warangal": ["Hanamkonda", "Kazipet", "Subedari"]
    },
    "Tripura": {
        "West Tripura": ["Agartala", "Banamalipur", "Ramnagar"],
        "Dhalai": ["Ambassa", "Kamalpur"]
    },
    "Uttar Pradesh": {
        "Lucknow": ["Gomti Nagar", "Hazratganj", "Aliganj", "Indira Nagar"],
        "Kanpur": ["Civil Lines", "Swaroop Nagar", "Kidwai Nagar"],
        "Varanasi": ["Lanka", "Sigra", "Cantt Area"],
        "Gautam Buddha Nagar": ["Noida Sector 62", "Greater Noida", "Noida Sector 18"]
    },
    "Uttarakhand": {
        "Dehradun": ["Rajpur Road", "Mussoorie", "Clement Town"],
        "Haridwar": ["Kankhal", "Jwalapur", "Har ki Pauri"]
    },
    "West Bengal": {
        "Kolkata": ["Salt Lake", "New Town", "Ballygunge", "Alipore", "Dum Dum"],
        "North 24 Parganas": ["Bidhannagar", "Barasat", "Barrackpore"],
        "Darjeeling": ["Siliguri", "Kurseong", "Kalimpong"]
    },
    "Delhi": {
        "New Delhi": ["Connaught Place", "Chanakyapuri", "Hauz Khas", "RK Puram"],
        "South Delhi": ["Saket", "Vasant Kunj", "Greater Kailash", "Lajpat Nagar", "Malviya Nagar"],
        "North Delhi": ["Civil Lines", "Rohini", "Model Town", "Pitampura"]
    },
    "Jammu & Kashmir": {
        "Srinagar": ["Lal Chowk", "Dal Lake", "Sonwar"],
        "Jammu": ["Gandhi Nagar", "Trikuta Nagar", "Bari Brahmana"]
    },
    "Ladakh": {
        "Leh": ["Main Bazar", "Chanspa", "Sankar"],
        "Kargil": ["Main Market", "Baroo"]
    },
    "Puducherry": {
        "Puducherry": ["White Town", "Heritage Town", "Oulgaret"],
        "Karaikal": ["Karaikal Town", "Neravy"]
    }
}

PEOPLE = [
    "Arjun Subramaniam", "Meenakshi Rajan", "Ramesh Pillai", "Kavitha Nair", "Venkatesh Iyer", 
    "Priya Chandran", "Selvakumar Pandian", "Sneha Desai", "Muthu Kumar", "Rahul Venkat", 
    "Anil Kumar", "Sunita Reddy", "Anita Dev", "Rajesh Sharma", "Sanjay Gupta", 
    "Amitabh Bachan Singh", "Vikram Rathore", "Siddharth Malhotra", "Deepika Padukone Iyer",
    "Suresh Prabhu", "Manohar Lal", "Harpreet Singh", "Gurpreet Kaur", "Jasbir Dhillon",
    "Pranab Mukherjee", "Mamata Banerjee", "Sourav Ganguly", "Subhash Chandra",
    "Narayana Murthy", "Sudha Murthy", "Azim Premji", "Kiran Mazumdar",
    "Ratan Tata", "Mukesh Ambani", "Gautam Adani", "Nita Ambani",
    "Abhishek Chatterjee", "Debashree Roy", "Siddharth Roy Kapur",
    "Yashwant Sinha", "Sushma Swaraj", "Arun Jaitley", "Piyush Goyal",
    "Smriti Irani", "Nirmala Sitharaman", "S. Jaishankar", "Yogi Adityanath",
    "Akhilesh Yadav", "Mayawati", "Mulayam Singh", "Lalu Prasad Yadav",
    "Nitish Kumar", "Sharad Pawar", "Uddhav Thackeray", "Raj Thackeray",
    "Eknath Shinde", "Devendra Fadnavis", "Ajit Pawar", "Prakash Ambedkar"
]
ENTITIES = [
    "Vijay Constructions", "Varun Estates", "Sri Balaji Housing", "Local Panchayat", 
    "Municipal Corporation", "State Highway Board", "Nexus Builders", "DLF Group", 
    "Godrej Properties", "Tata Housing", "Lodha Group", "Sobha Limited", "Prestige Group",
    "Reliance Industries", "Adani Enterprises", "L&T Construction", "NHAI", 
    "Rail Land Development Authority", "Forest Department", "Waqf Board", 
    "Temple Trust Committee", "Housing Board", "DDA Delhi", "HUDA Haryana"
]
DISPUTE_TYPES = [
    "Boundary Dispute", "Encroachment", "Title Dispute", "Illegal Possession", 
    "Succession", "Government Acquisition Dispute", "Gift Deed Challenge", 
    "Will Validity", "Lease Agreement Violation", "Mortgage Dispute"
]
OFFICERS = [
    "Shri K. Ramachandran, DLO", "Smt. P. Vijayalakshmi, Sub-Collector", 
    "Shri T. Balasubramanian, DLO", "Smt. R. Meenakshisundaram, DLO", 
    "Shri V. Annamalai, Sub-Collector", "Shri M. Durai, DLO",
    "Shri Rajesh Kumar, District Magistrate", "Smt. Shanti Devi, Tehsildar",
    "Shri Vikram Singh, SDM", "Smt. Neha Sharma, Land Records Officer",
    "Shri Anil Deshmukh, Deputy Commissioner", "Smt. Sunita Rao, Revenue Divisional Officer"
]

ACTS_AND_SECTIONS = [
    "Tamil Nadu Land Encroachment Act, 1905",
    "Section 145 CrPC (Boundary Dispute)",
    "Right to Fair Compensation (LARR) Act, 2013",
    "Transfer of Property Act, 1882",
    "Tamil Nadu Patta Pass Book Act, 1983",
    "Land Acquisition Act, 1894"
]
ADVOCATES = [
    "Adv. S. Ramaswamy", "Adv. K. Meenakshi", "Adv. R. Krishnan", "Adv. J. Deepa",
    "Adv. P. Venkatesh", "Adv. M. Anitha", "Adv. B. Senthil", "Adv. G. Kavitha",
    "Adv. T. Rajesh", "Adv. L. Vidya", "Adv. N. Chandran", "Adv. S. Preethi"
]
COURTS = [
    "District Revenue Court", "Sub-Divisional Magistrate Court",
    "Special Tahsildar (Land Reform) Court", "Land Administration Commissioner",
    "High Court - Civil Bench", "Taluk Land Board", "Principal Civil Court"
]

def generate_timeline(filed_date):
    events = [
        "Initial verification by Tahsildar",
        "Assigned to specialized Land Officer",
        "Legal notice issued to respondent",
        "Respondent filed counter-affidavit",
        "Physical site survey conducted",
        "Revenue department review completed"
    ]
    timeline = [{"d": filed_date.strftime('%d %b %Y'), "e": "Case filed online via DLLMS Portal"}]
    
    num_events = random.randint(1, len(events))
    curr_date = filed_date
    for i in range(num_events):
        curr_date += timedelta(days=random.randint(5, 25))
        if curr_date > datetime.now(): break
        timeline.append({"d": curr_date.strftime('%d %b %Y'), "e": events[i]})
    
    return timeline, curr_date

def generate_case(idx):
    state = random.choice(list(GEO_HIERARCHY.keys()))
    dist = random.choice(list(GEO_HIERARCHY[state].keys()))
    vill = random.choice(GEO_HIERARCHY[state][dist])
    
    filed_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 400))
    timeline, last_date = generate_timeline(filed_date)
    
    status = random.choice(["Pending", "Active", "Resolved", "Closed"])
    next_hearing = "\u2014"
    if status in ["Active", "Pending"]:
        h_date = datetime.now() + timedelta(days=random.randint(7, 60))
        next_hearing = h_date.strftime('%d %b %Y')
        timeline.append({"d": next_hearing, "e": "Next hearing scheduled", "u": True})
    elif status == "Resolved":
        timeline.append({"d": last_date.strftime('%d %b %Y'), "e": "Final order issued — RESOLVED"})

    # New official details
    cnr = f"{state[:2].upper()}{dist[:3].upper()}2026{random.randint(100000, 999999)}"
    pet_adv = random.choice(ADVOCATES)
    res_adv = random.choice(ADVOCATES)
    court = random.choice(COURTS)
    dtype = random.choice(DISPUTE_TYPES)
    act = random.choice(ACTS_AND_SECTIONS)

    return {
        "id": f"LL2026{str(idx+1).zfill(3)}",
        "cnr": cnr,
        "applicant": random.choice(PEOPLE),
        "respondent": random.choice(ENTITIES + PEOPLE),
        "petitionerAdvocate": pet_adv,
        "respondentAdvocate": res_adv,
        "court": court,
        "act": act,
        "state": state,
        "district": dist,
        "village": vill,
        "taluka": f"Taluk-{random.randint(1,5)}",
        "survey": f"{random.randint(1,150)}/{random.randint(1,5)}",
        "patta": f"PATTA-{random.randint(10000, 99999)}",
        "area": f"{round(random.uniform(0.5, 8.0), 2)} Acres",
        "type": dtype,
        "status": status,
        "filed": filed_date.strftime('%d %b %Y'),
        "officer": random.choice(OFFICERS) + f" ({dist})",
        "nextHearing": next_hearing,
        "prayer": f"Application for {dtype.lower()} resolution regarding Survey No. {random.randint(1, 150)} for a relief of {random.choice(['Title restoration', 'Compensation', 'Removal of encroachment', 'Partition'])}.",
        "timeline": timeline
    }

def main():
    print("Senior Seeder: Generating high-quality mockup data...")
    
    # 1. Generate db.json (Land Master Records)
    all_records = []
    for state, dists in GEO_HIERARCHY.items():
        for dist, vills in dists.items():
            for vill in vills:
                for s in range(12, 15): # Focus on specific sectors for searchable demo
                    for p in range(1, 4):
                        all_records.append({
                            "state": state, "district": dist, "villageName": vill,
                            "sectorNumber": str(s), "plotNumber": f"{s}/{p}",
                            "ownerName": random.choice(PEOPLE), "landArea": f"{round(random.uniform(1, 5), 2)} Acres",
                            "landType": random.choice(["Agricultural", "Commercial", "Residential"]),
                            "litigationStatus": random.choice(["Clear", "Clear", "Disputed", "Under Court Stay"]),
                            "caseNumber": f"OS-2025-{random.randint(1000,9999)}",
                            "courtName": "District Civil Court", "surveyYear": random.randint(2018, 2024),
                            "propertyValuation": f"₹{random.randint(10, 90)},00,000",
                            "previousHearing": "2025-10-12", "nextHearing": "2026-04-15",
                            "caseSummary": "Overlapping boundary verification pending survey."
                        })
    
    # 2. Generate cases.json (Litigation Cases) - Increase to 1500 for better search hits
    litigation = [generate_case(i) for i in range(1500)]
    
    os.makedirs('data', exist_ok=True)
    with open('data/db.json', 'w', encoding='utf-8') as f:
        json.dump(all_records, f, indent=4)
    with open('data/cases.json', 'w', encoding='utf-8') as f:
        json.dump(litigation, f, indent=2)
    
    print(f"SUCCESS: Seeded {len(all_records)} land records and {len(litigation)} litigation cases.")

if __name__ == "__main__":
    main()
