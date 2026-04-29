/**
 * National Land Litigation Management Portal
 * Node.js & Express REST API Server
 */
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public'))); // Serve the frontend from the public directory

// --- MongoDB Connection ---
mongoose.connect('mongodb://127.0.0.1:27017/landlitigation', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('✅ Connected to MongoDB Instance'))
  .catch(err => console.error('❌ MongoDB Connection Error:', err));

// --- Schemas & Models ---
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

const UserSchema = new mongoose.Schema({
    adminId: { type: String, required: true, unique: true },
    password: { type: String, required: true }
});
const User = mongoose.model('User', UserSchema);

// --- API Routes ---

/**
 * @route GET /api/records
 * @desc Get records filtered by State, District, Village, and Sector
 */
app.get('/api/records', async (req, res) => {
    try {
        const { state, district, villageName, sectorNumber, caseId } = req.query;
        let p = {};
        if (state) p.state = state;
        if (district) p.district = district;
        if (villageName) p.villageName = new RegExp(`^${villageName}$`, 'i');
        if (sectorNumber) p.sectorNumber = sectorNumber;
        if (caseId) p.caseNumber = new RegExp(`^${caseId}$`, 'i');

        const records = await Record.find(p);
        res.json({ success: true, count: records.length, data: records });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: 'Server Error Fetching Records' });
    }
});

/**
 * @route PUT /api/records/:id
 * @desc Update litigation status, hearing date and officer
 */
app.put('/api/records/:id', async (req, res) => {
    try {
        const caseNumber = req.params.id;
        const { status, nextHearing, officer, remarks } = req.body;
        
        let updateData = {};
        if (status) updateData.litigationStatus = status;
        if (nextHearing) updateData.nextHearing = nextHearing;
        // Optionally update officer/remarks if added to schema

        const record = await Record.findOneAndUpdate(
            { caseNumber: caseNumber },
            { $set: updateData },
            { new: true }
        );

        if (!record) {
            return res.status(404).json({ success: false, message: 'Case not found' });
        }
        res.json({ success: true, message: 'Updated successfully', data: record });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: 'Server Error on Update' });
    }
});

/**
 * @route POST /api/auth/login
 * @desc Secure Official Login (Mock Implementation for Demo)
 */
app.post('/api/auth/login', async (req, res) => {
    try {
        const { adminId, password } = req.body;
        // Check static mock admin for now to ensure the demo works without seeding users
        if (adminId === 'GOV-EMP-2026' && password === 'admin123') {
            res.json({ success: true, token: 'fake-jwt-token-738910', message: 'Auth Success' });
        } else {
            res.status(401).json({ success: false, message: 'Invalid Admin Credentials' });
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: 'Server Error on Auth' });
    }
});

// Start Server
app.listen(PORT, () => {
    console.log(`=======================================================`);
    console.log(` National Land Litigation Management Portal backend`);
    console.log(` Running on http://localhost:${PORT}`);
    console.log(`=======================================================`);
});
