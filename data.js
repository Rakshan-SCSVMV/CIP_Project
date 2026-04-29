const geoHierarchy = {
    "Tamil Nadu": {
        "Chennai": ["Kovur", "Tambaram", "Guindy", "Velachery", "Adyar", "Mylapore"],
        "Coimbatore": ["Peelamedu", "Singanallur", "RS Puram", "Sulur"],
        "Madurai": ["Anna Nagar", "Tallakulam", "Avaniyapuram"]
    },
    "Maharashtra": {
        "Mumbai Suburban": ["Andheri", "Bandra", "Borivali", "Goregaon"],
        "Pune": ["Kothrud", "Hinjewadi", "Viman Nagar", "Baner", "Kharadi"],
        "Nagpur": ["Sitabuldi", "Dharampeth", "Sadar"]
    },
    "Karnataka": {
        "Bangalore Urban": ["Whitefield", "Koramangala", "Indiranagar", "Jayanagar", "HSR Layout"],
        "Mysuru": ["Gokulam", "Saraswathipuram", "Vijayanagar"],
        "Mangaluru": ["Kadri", "Bejai", "Surathkal"]
    },
    "Delhi": {
        "New Delhi": ["Connaught Place", "Chanakyapuri", "Hauz Khas"],
        "South Delhi": ["Saket", "Vasant Kunj", "Greater Kailash", "Lajpat Nagar"],
        "North Delhi": ["Civil Lines", "Rohini", "Model Town"]
    },
    "Uttar Pradesh": {
        "Lucknow": ["Gomti Nagar", "Aliganj", "Hazratganj", "Indira Nagar"],
        "Noida (GB Nagar)": ["Sector 15", "Sector 62", "Greater Noida", "Noida Extension"],
        "Varanasi": ["Lanka", "Sigra", "Cantt"]
    }
};

// Expose only hierarchy for cascading dropdowns. Records are fetched via REST API.
window.landData = {
    hierarchy: geoHierarchy
};
