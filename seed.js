const mongoose = require('mongoose');

mongoose.connect('mongodb://127.0.0.1:27017/landlitigation', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('Connected to MongoDB for Seeding'))
  .catch(err => {
      console.error('Connection error:', err);
      process.exit(1);
  });

const RecordSchema = new mongoose.Schema({
    state: String,
    district: String,
    villageName: String,
    sectorNumber: String,
    plotNumber: String,
    ownerName: String,
    landArea: String,
    landType: String,
    litigationStatus: String,
    caseNumber: String,
    courtName: String,
    surveyYear: Number,
    propertyValuation: String,
    previousHearing: String,
    nextHearing: String,
    caseSummary: String
});
const Record = mongoose.model('Record', RecordSchema);

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
    // Truncated for seed simplicity; normally matches full data.js hierarchy
};

const dynamicNames = ['Rahul Venkat', 'Priya Sharma', 'Anil Kumar', 'Muthu Kumar', 'Anita Dev', 'Vijay Constructions', 'Ramesh Iyer', 'Sunita Reddy', 'Varun Estates', 'Sri Balaji Housing', 'Rajesh Patel', 'Sneha Desai', 'Karan Singh', 'Alok Nath', 'Deepak Gupta', 'Govt. Poramboke', 'Local Panchayat', 'Municipal Corporation'];
const dynamicTypes = ['Agricultural', 'Commercial', 'Residential', 'Public Infrastructure'];
const dynamicStatuses = ['Clear', 'Clear', 'Clear', 'Clear', 'Disputed', 'Under Court Stay']; 
const dynamicCourts = ['District Civil Court', 'High Court Bench', 'Supreme Court', 'Sub-Magistrate Court', 'Revenue Divisional Officer'];
const legalJargon = ['Encroachment dispute by neighbor', 'Title deed overlapping verification', 'Pending inheritance settlement', 'Illegal commercial zoning', 'Awaiting environmental clearance'];

const masterDatabase = [];

function randomDate(startObj, endObj) {
    let date = new Date(startObj.getTime() + Math.random() * (endObj.getTime() - startObj.getTime()));
    return date.toISOString().split('T')[0];
}

for (const state in geoHierarchy) {
    for (const district in geoHierarchy[state]) {
        for (const village of geoHierarchy[state][district]) {
            const numSectors = 2; // Reduced for seed speed
            for (let s = 1; s <= numSectors; s++) {
                const numPlots = Math.floor(Math.random() * 3) + 1;
                for(let p = 1; p <= numPlots; p++) {
                    const status = dynamicStatuses[Math.floor(Math.random() * dynamicStatuses.length)];
                    const hasCase = (status !== 'Clear');
                    const acreage = (Math.random() * 4.5 + 0.5).toFixed(2);
                    const surveyYear = 2000 + Math.floor(Math.random() * 26);
                    const valuation = Math.floor(parseFloat(acreage) * (Math.random() * 5000000 + 1000000));
                    
                    let prevHearing = 'N/A';
                    let nextHearing = 'N/A';
                    let legalContext = 'N/A';
                    
                    if (hasCase) {
                        prevHearing = randomDate(new Date(2023, 0, 1), new Date());
                        nextHearing = randomDate(new Date(), new Date(2027, 0, 1));
                        legalContext = legalJargon[Math.floor(Math.random() * legalJargon.length)];
                    }
                    
                    masterDatabase.push({
                        state: state,
                        district: district,
                        villageName: village,
                        sectorNumber: s.toString(),
                        plotNumber: numPlots > 1 ? `${s}/${String.fromCharCode(64 + p)}` : `${s}`,
                        ownerName: dynamicNames[Math.floor(Math.random() * dynamicNames.length)],
                        landArea: `${acreage} Acres`,
                        landType: dynamicTypes[Math.floor(Math.random() * dynamicTypes.length)],
                        litigationStatus: status,
                        caseNumber: hasCase ? `OS-${new Date().getFullYear() - Math.floor(Math.random()*5)}-${Math.floor(Math.random()*9000)+1000}` : 'N/A',
                        courtName: hasCase ? dynamicCourts[Math.floor(Math.random() * dynamicCourts.length)] : 'N/A',
                        surveyYear: surveyYear,
                        propertyValuation: '₹' + valuation.toLocaleString('en-IN') + '.00',
                        previousHearing: prevHearing,
                        nextHearing: nextHearing,
                        caseSummary: legalContext
                    });
                }
            }
        }
    }
}

// Add fixed Kovur records so searches always yield good test results
masterDatabase.push(
    { state: 'Tamil Nadu', district: 'Chennai', villageName: 'Kovur', sectorNumber: '12', plotNumber: '12/A1', ownerName: 'Rahul Venkat', landArea: '0.45 Acres', landType: 'Agricultural', litigationStatus: 'Clear', caseNumber: 'N/A', courtName: 'N/A', surveyYear: 2018, propertyValuation: '₹14,50,000.00', previousHearing: 'N/A', nextHearing: 'N/A', caseSummary: 'N/A' },
    { state: 'Tamil Nadu', district: 'Chennai', villageName: 'Kovur', sectorNumber: '12', plotNumber: '12/A2', ownerName: 'Priya Sharma', landArea: '1.2 Acres', landType: 'Commercial', litigationStatus: 'Disputed', caseNumber: 'OS-2023-1045', courtName: 'District Civil Court, Chennai', surveyYear: 2021, propertyValuation: '₹8,550,000.00', previousHearing: '2023-11-14', nextHearing: '2024-05-22', caseSummary: 'Title deed overlapping verification' },
    { state: 'Tamil Nadu', district: 'Chennai', villageName: 'Kovur', sectorNumber: '12', plotNumber: '12/A4', ownerName: 'Anil Kumar', landArea: '0.8 Acres', landType: 'Agricultural', litigationStatus: 'Under Court Stay', caseNumber: 'WP-2025-101', courtName: 'High Court Bench', surveyYear: 2020, propertyValuation: '₹2,300,000.00', previousHearing: '2024-02-12', nextHearing: '2024-08-11', caseSummary: 'Encroachment dispute by neighbor' }
);

async function seedData() {
    await Record.deleteMany({});
    console.log('Cleared existing records');
    await Record.insertMany(masterDatabase);
    console.log(`Successfully seeded ${masterDatabase.length} records!`);
    mongoose.connection.close();
}

seedData();
